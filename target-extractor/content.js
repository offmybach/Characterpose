// CGB Target Extractor - content script
// Runs on Sales Navigator list / search / lists-index pages.
// Auto-scrolls the lead container, extracts each card, clicks Next page,
// repeats until the list is exhausted, then signals background.

(() => {
  if (window.__CGB_EXTRACTOR_INSTALLED__) return;
  window.__CGB_EXTRACTOR_INSTALLED__ = true;

  const STATE = {
    running: false,
    listId: null,
    listName: null,
    pageIndex: 0,
    seenOnPage: new Set(),
    totalCaptured: 0,
    stallTicks: 0,
  };

  const log = (...a) => console.log("[CGB-Extractor]", ...a);

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  // Selector banks — try each, first hit wins. Sales Nav A/B tests these.
  const SEL = {
    leadRow: [
      "li.artdeco-list__item",
      "li[data-x-search-result]",
      "div[data-x-search-result]",
      "li.search-results__result-item",
      "div.artdeco-entity-lockup",
    ],
    name: [
      '[data-anonymize="person-name"]',
      "a.artdeco-entity-lockup__title span[dir]",
      "span.artdeco-entity-lockup__title",
      ".result-lockup__name a",
    ],
    title: [
      '[data-anonymize="job-title"]',
      ".artdeco-entity-lockup__subtitle",
      ".result-lockup__position-company .result-lockup__highlight-keyword",
    ],
    company: [
      '[data-anonymize="company-name"]',
      ".artdeco-entity-lockup__subtitle a",
      ".result-lockup__position-company a",
    ],
    location: [
      '[data-anonymize="location"]',
      ".artdeco-entity-lockup__caption",
      ".result-lockup__misc-item",
    ],
    profileLink: [
      'a[href*="/sales/lead/"]',
      'a[href*="/sales/people/"]',
      'a[href*="/in/"]',
    ],
    scrollContainer: [
      "#search-results-container",
      ".artdeco-list",
      ".search-results__container",
      "main",
    ],
    nextBtn: [
      'button[aria-label="Next"]',
      'button.artdeco-pagination__button--next',
      'button[data-control-name="page_next"]',
    ],
    listsIndexRow: [
      'a[href*="/sales/lists/people/"]',
      'a[href*="/sales/lists/company/"]',
    ],
    listTitle: [
      "h1.list-detail-header__title",
      "header h1",
      'h1[data-x-list-name]',
    ],
  };

  const $first = (root, sels) => {
    for (const s of sels) {
      const el = root.querySelector(s);
      if (el) return el;
    }
    return null;
  };

  const $all = (root, sels) => {
    for (const s of sels) {
      const els = root.querySelectorAll(s);
      if (els.length) return Array.from(els);
    }
    return [];
  };

  const txt = (el) => (el ? el.textContent.replace(/\s+/g, " ").trim() : "");

  const detectPageType = () => {
    const u = location.pathname;
    if (u.match(/\/sales\/lists\/?$/)) return "lists-index";
    if (u.match(/\/sales\/lists\/people\//)) return "list-detail";
    if (u.match(/\/sales\/search\/people/)) return "search";
    if (u.match(/\/sales\/lead\//) || u.match(/\/sales\/people\//)) return "lead";
    return "unknown";
  };

  const captureListName = () => {
    const el = $first(document, SEL.listTitle);
    return txt(el) || document.title.replace(/\s*\|\s*LinkedIn.*$/, "").trim();
  };

  const extractOneCard = (row) => {
    const nameEl = $first(row, SEL.name);
    const name = txt(nameEl);
    if (!name) return null;

    const linkEl = $first(row, SEL.profileLink);
    const profileUrl = linkEl ? linkEl.href.split("?")[0] : "";

    const title = txt($first(row, SEL.title));
    const company = txt($first(row, SEL.company));
    const locationText = txt($first(row, SEL.location));

    // Identity key: prefer profile URL, fall back to name+company hash.
    const idKey = profileUrl || `${name}::${company}`.toLowerCase();

    return {
      idKey,
      name,
      title,
      company,
      location: locationText,
      profileUrl,
      description: title && company ? `${title} at ${company}` : title || company,
      sourceList: STATE.listName || "",
      sourceUrl: window.location.href,
      capturedAt: new Date().toISOString(),
    };
  };

  const harvestVisible = () => {
    const rows = $all(document, SEL.leadRow);
    const fresh = [];
    for (const row of rows) {
      const rec = extractOneCard(row);
      if (!rec) continue;
      if (STATE.seenOnPage.has(rec.idKey)) continue;
      STATE.seenOnPage.add(rec.idKey);
      fresh.push(rec);
    }
    return fresh;
  };

  const getScrollContainer = () => $first(document, SEL.scrollContainer) || document.scrollingElement;

  const autoScrollPage = async () => {
    const container = getScrollContainer();
    let lastHeight = -1;
    let stableTicks = 0;
    for (let i = 0; i < 200; i++) {
      if (!STATE.running) return;
      // Scroll the inner container if it has its own overflow, else window.
      if (container && container.scrollHeight > container.clientHeight + 50) {
        container.scrollTop = container.scrollHeight;
      } else {
        window.scrollTo(0, document.body.scrollHeight);
      }
      await sleep(700);
      const newRows = harvestVisible();
      if (newRows.length) {
        await chrome.runtime.sendMessage({ type: "leads", payload: newRows });
        STATE.totalCaptured += newRows.length;
      }
      const h = container ? container.scrollHeight : document.body.scrollHeight;
      if (h === lastHeight) {
        stableTicks++;
        if (stableTicks >= 3) break;
      } else {
        stableTicks = 0;
        lastHeight = h;
      }
    }
  };

  const clickNext = async () => {
    const btn = $first(document, SEL.nextBtn);
    if (!btn || btn.disabled || btn.getAttribute("aria-disabled") === "true") return false;
    btn.scrollIntoView({ block: "center" });
    await sleep(300);
    btn.click();
    return true;
  };

  const runListPage = async () => {
    STATE.listName = captureListName();
    log("Starting list:", STATE.listName);
    await chrome.runtime.sendMessage({ type: "status", payload: `Scraping list: ${STATE.listName}` });
    for (let pageNo = 1; pageNo <= 200; pageNo++) {
      if (!STATE.running) break;
      STATE.seenOnPage = new Set();
      await sleep(800);
      await autoScrollPage();
      // Also capture once more after final scroll settle.
      const last = harvestVisible();
      if (last.length) {
        await chrome.runtime.sendMessage({ type: "leads", payload: last });
        STATE.totalCaptured += last.length;
      }
      await chrome.runtime.sendMessage({
        type: "status",
        payload: `${STATE.listName} — page ${pageNo}, ${STATE.totalCaptured} captured so far`,
      });
      const advanced = await clickNext();
      if (!advanced) break;
      await sleep(1500);
    }
    await chrome.runtime.sendMessage({
      type: "list-done",
      payload: { listName: STATE.listName, captured: STATE.totalCaptured },
    });
  };

  const runListsIndex = async () => {
    // Scroll to load every list link, then send them all back.
    const container = getScrollContainer();
    let stableTicks = 0;
    let lastCount = -1;
    for (let i = 0; i < 50; i++) {
      if (container) container.scrollTop = container.scrollHeight;
      else window.scrollTo(0, document.body.scrollHeight);
      await sleep(700);
      const links = $all(document, SEL.listsIndexRow);
      if (links.length === lastCount) {
        stableTicks++;
        if (stableTicks >= 3) break;
      } else {
        stableTicks = 0;
        lastCount = links.length;
      }
    }
    const urls = Array.from(new Set($all(document, SEL.listsIndexRow).map((a) => a.href.split("?")[0])));
    log("Harvested list URLs:", urls.length);
    await chrome.runtime.sendMessage({ type: "list-urls", payload: urls });
  };

  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg?.type === "ping") {
      sendResponse({ ok: true, pageType: detectPageType() });
      return;
    }
    if (msg?.type === "run") {
      STATE.running = true;
      const t = detectPageType();
      (async () => {
        try {
          if (t === "lists-index") await runListsIndex();
          else if (t === "list-detail" || t === "search") await runListPage();
          else
            await chrome.runtime.sendMessage({
              type: "status",
              payload: `Not a scrapeable page (${t}). Open a list or search.`,
            });
        } catch (e) {
          log("error:", e);
          await chrome.runtime.sendMessage({ type: "status", payload: `Error: ${e.message}` });
        } finally {
          STATE.running = false;
          await chrome.runtime.sendMessage({ type: "page-done" });
        }
      })();
      sendResponse({ ok: true });
      return true;
    }
    if (msg?.type === "stop") {
      STATE.running = false;
      sendResponse({ ok: true });
      return;
    }
  });

  // Announce readiness to background.
  chrome.runtime.sendMessage({ type: "content-ready", payload: { pageType: detectPageType() } }).catch(() => {});
})();
