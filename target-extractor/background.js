// CGB Target Extractor - background service worker.
// Owns: the lead store (chrome.storage.local), the queue of list URLs to
// process, dedup across lists, and CSV export.

try {
  importScripts("categorizer.js");
} catch (e) {
  console.warn("[CGB-Extractor] categorizer load failed; using stub", e);
  self.CGB_CATEGORIZER = { categorize: () => ({ primary: "Misc", secondary: "" }), GROUPS: [] };
}

const { categorize, GROUPS } = self.CGB_CATEGORIZER;

const STORE_KEY = "cgb_leads_v1";
const QUEUE_KEY = "cgb_queue_v1";
const STATUS_KEY = "cgb_status_v1";

const loadLeads = async () => {
  const v = await chrome.storage.local.get(STORE_KEY);
  return v[STORE_KEY] || {};
};

const saveLeads = async (leads) => chrome.storage.local.set({ [STORE_KEY]: leads });

const loadQueue = async () => {
  const v = await chrome.storage.local.get(QUEUE_KEY);
  return v[QUEUE_KEY] || { urls: [], cursor: 0, active: false };
};

const saveQueue = async (q) => chrome.storage.local.set({ [QUEUE_KEY]: q });

const setStatus = async (text) => {
  await chrome.storage.local.set({ [STATUS_KEY]: { text, at: Date.now() } });
  chrome.runtime.sendMessage({ type: "status-tick", text }).catch(() => {});
};

const mergeLeads = async (incoming) => {
  const store = await loadLeads();
  let added = 0;
  for (const rec of incoming) {
    if (!rec?.idKey) continue;
    if (!store[rec.idKey]) {
      store[rec.idKey] = rec;
      added++;
    } else {
      // Stitch together any new info; preserve earliest captured_at.
      const cur = store[rec.idKey];
      store[rec.idKey] = {
        ...cur,
        title: cur.title || rec.title,
        company: cur.company || rec.company,
        location: cur.location || rec.location,
        profileUrl: cur.profileUrl || rec.profileUrl,
        sourceList: cur.sourceList === rec.sourceList
          ? cur.sourceList
          : [cur.sourceList, rec.sourceList].filter(Boolean).join("|"),
      };
    }
  }
  await saveLeads(store);
  return { added, total: Object.keys(store).length };
};

const getActiveTab = async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
};

const sendToTab = async (tabId, msg) => {
  try {
    return await chrome.tabs.sendMessage(tabId, msg);
  } catch (e) {
    // Content script not loaded yet — retry after navigation.
    return null;
  }
};

// Wait for a tab to finish loading.
const waitForTabComplete = (tabId, timeoutMs = 45000) =>
  new Promise((resolve) => {
    const t = setTimeout(() => {
      chrome.tabs.onUpdated.removeListener(handler);
      resolve(false);
    }, timeoutMs);
    function handler(updatedId, info) {
      if (updatedId === tabId && info.status === "complete") {
        clearTimeout(t);
        chrome.tabs.onUpdated.removeListener(handler);
        resolve(true);
      }
    }
    chrome.tabs.onUpdated.addListener(handler);
  });

// Resolves when content script signals page-done for the given tab, or timeout.
const pageDonePromises = new Map(); // tabId -> resolver
const waitForPageDone = (tabId, timeoutMs = 5 * 60 * 1000) =>
  new Promise((resolve) => {
    const t = setTimeout(() => {
      pageDonePromises.delete(tabId);
      resolve(false);
    }, timeoutMs);
    pageDonePromises.set(tabId, () => {
      clearTimeout(t);
      resolve(true);
    });
  });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const runQueue = async () => {
  const q = await loadQueue();
  if (!q.urls.length) {
    await setStatus("Queue is empty.");
    q.active = false;
    await saveQueue(q);
    return;
  }
  q.active = true;
  await saveQueue(q);

  const tab = await getActiveTab();
  if (!tab) {
    await setStatus("No active tab. Open a Sales Nav tab first.");
    q.active = false;
    await saveQueue(q);
    return;
  }

  for (let i = q.cursor; i < q.urls.length; i++) {
    const url = q.urls[i];
    q.cursor = i;
    await saveQueue(q);
    await setStatus(`[${i + 1}/${q.urls.length}] Navigating: ${url}`);
    await chrome.tabs.update(tab.id, { url });
    await waitForTabComplete(tab.id);
    // Give Sales Nav a beat to hydrate.
    await sleep(2500);
    await sendToTab(tab.id, { type: "run" });
    const ok = await waitForPageDone(tab.id);
    if (!ok) {
      await setStatus(`[${i + 1}/${q.urls.length}] Timed out, moving on.`);
    }
    // Brief pause to look more human-ish between lists.
    await sleep(1500);
    const current = await loadQueue();
    if (!current.active) {
      await setStatus("Queue stopped.");
      return;
    }
  }
  const final = await loadQueue();
  final.active = false;
  final.cursor = 0;
  await saveQueue(final);
  const store = await loadLeads();
  await setStatus(`Queue complete. ${Object.keys(store).length} unique leads captured.`);
};

// ---- CSV export ----------------------------------------------------------

const csvEscape = (v) => {
  if (v == null) return "";
  const s = String(v);
  if (/[",\n\r]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
  return s;
};

const buildCsv = (rows, columns) => {
  const head = columns.join(",");
  const body = rows.map((r) => columns.map((c) => csvEscape(r[c])).join(",")).join("\n");
  return `${head}\n${body}\n`;
};

const exportGroupedCsv = async () => {
  const store = await loadLeads();
  const all = Object.values(store);
  if (!all.length) {
    await setStatus("No leads to export.");
    return;
  }
  const enriched = all.map((r) => {
    const { primary, secondary } = categorize(r);
    return {
      primary_group: primary,
      secondary_groups: secondary,
      name: r.name || "",
      title: r.title || "",
      company: r.company || "",
      description: r.description || "",
      location: r.location || "",
      profile_url: r.profileUrl || "",
      source_list: r.sourceList || "",
      captured_at: r.capturedAt || "",
    };
  });
  // Stable sort: primary_group then company then name.
  enriched.sort((a, b) => {
    if (a.primary_group !== b.primary_group) return a.primary_group.localeCompare(b.primary_group);
    if (a.company !== b.company) return a.company.localeCompare(b.company);
    return a.name.localeCompare(b.name);
  });
  const columns = [
    "primary_group",
    "secondary_groups",
    "name",
    "title",
    "company",
    "description",
    "location",
    "profile_url",
    "source_list",
    "captured_at",
  ];
  const csv = buildCsv(enriched, columns);
  const url = `data:text/csv;charset=utf-8,${encodeURIComponent(csv)}`;
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  await chrome.downloads.download({
    url,
    filename: `cgb-targets-master-${stamp}.csv`,
    saveAs: true,
  });
  await setStatus(`Exported ${enriched.length} leads.`);
};

const exportGroupCsvs = async () => {
  const store = await loadLeads();
  const all = Object.values(store);
  if (!all.length) {
    await setStatus("No leads to export.");
    return;
  }
  const buckets = {};
  for (const r of all) {
    const { primary, secondary } = categorize(r);
    const row = {
      name: r.name || "",
      title: r.title || "",
      company: r.company || "",
      description: r.description || "",
      location: r.location || "",
      profile_url: r.profileUrl || "",
      source_list: r.sourceList || "",
      secondary_groups: secondary,
      captured_at: r.capturedAt || "",
    };
    (buckets[primary] ||= []).push(row);
  }
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const columns = [
    "name", "title", "company", "description", "location",
    "profile_url", "source_list", "secondary_groups", "captured_at",
  ];
  for (const [group, rows] of Object.entries(buckets)) {
    rows.sort((a, b) => a.company.localeCompare(b.company) || a.name.localeCompare(b.name));
    const csv = buildCsv(rows, columns);
    const url = `data:text/csv;charset=utf-8,${encodeURIComponent(csv)}`;
    await chrome.downloads.download({
      url,
      filename: `cgb-targets-${group}-${stamp}.csv`,
      saveAs: false,
    });
  }
  await setStatus(`Exported one CSV per group (${Object.keys(buckets).length} files).`);
};

// ---- Message router ------------------------------------------------------

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  (async () => {
    if (msg?.type === "leads") {
      const { added, total } = await mergeLeads(msg.payload);
      sendResponse({ ok: true, added, total });
      return;
    }
    if (msg?.type === "status") {
      await setStatus(msg.payload);
      sendResponse({ ok: true });
      return;
    }
    if (msg?.type === "list-done") {
      await setStatus(`Finished: ${msg.payload.listName} (${msg.payload.captured} on page)`);
      sendResponse({ ok: true });
      return;
    }
    if (msg?.type === "list-urls") {
      // Pull harvested list URLs into the queue.
      const q = await loadQueue();
      const set = new Set(q.urls);
      for (const u of msg.payload) set.add(u);
      q.urls = Array.from(set);
      await saveQueue(q);
      await setStatus(`Queue: ${q.urls.length} list URLs ready.`);
      sendResponse({ ok: true });
      return;
    }
    if (msg?.type === "page-done") {
      const tabId = sender.tab?.id;
      const resolver = pageDonePromises.get(tabId);
      if (resolver) {
        resolver();
        pageDonePromises.delete(tabId);
      }
      sendResponse({ ok: true });
      return;
    }
    if (msg?.type === "popup:run-here") {
      const tab = await getActiveTab();
      await sendToTab(tab.id, { type: "run" });
      sendResponse({ ok: true });
      return;
    }
    if (msg?.type === "popup:set-queue") {
      const q = { urls: msg.payload || [], cursor: 0, active: false };
      await saveQueue(q);
      sendResponse({ ok: true, count: q.urls.length });
      return;
    }
    if (msg?.type === "popup:start-queue") {
      runQueue();
      sendResponse({ ok: true });
      return;
    }
    if (msg?.type === "popup:stop-queue") {
      const q = await loadQueue();
      q.active = false;
      await saveQueue(q);
      const tab = await getActiveTab();
      if (tab) await sendToTab(tab.id, { type: "stop" });
      sendResponse({ ok: true });
      return;
    }
    if (msg?.type === "popup:export-master") {
      await exportGroupedCsv();
      sendResponse({ ok: true });
      return;
    }
    if (msg?.type === "popup:export-by-group") {
      await exportGroupCsvs();
      sendResponse({ ok: true });
      return;
    }
    if (msg?.type === "popup:clear") {
      await chrome.storage.local.set({ [STORE_KEY]: {} });
      await setStatus("Lead store cleared.");
      sendResponse({ ok: true });
      return;
    }
    if (msg?.type === "popup:stats") {
      const store = await loadLeads();
      const counts = {};
      for (const r of Object.values(store)) {
        const { primary } = categorize(r);
        counts[primary] = (counts[primary] || 0) + 1;
      }
      const status = (await chrome.storage.local.get(STATUS_KEY))[STATUS_KEY] || { text: "" };
      const queue = await loadQueue();
      sendResponse({
        ok: true,
        total: Object.keys(store).length,
        counts,
        status: status.text,
        queue: { size: queue.urls.length, cursor: queue.cursor, active: queue.active },
      });
      return;
    }
    if (msg?.type === "content-ready") {
      sendResponse({ ok: true });
      return;
    }
  })();
  return true; // async
});
