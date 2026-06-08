// CGB Target Extractor - popup controller

const $ = (id) => document.getElementById(id);

const send = (msg) =>
  new Promise((resolve) => {
    chrome.runtime.sendMessage(msg, (resp) => resolve(resp));
  });

const setStatus = (text) => {
  $("status").textContent = text || "Idle.";
};

const CONN_ORDER = ["1st", "Pending", "2nd", "3rd+", "Following", "Other", "Unknown", ""];

const renderStats = (stats) => {
  if (!stats || stats.total === 0) {
    $("stats").innerHTML = `<div class="hint">No leads yet.</div>`;
    return;
  }
  const counts = stats.counts || {};
  const groups = Object.keys(counts).sort((a, b) => counts[b] - counts[a]);
  const rows = groups
    .map(
      (g) =>
        `<div class="group-row"><span class="name">${g}</span><span class="count">${counts[g]}</span></div>`
    )
    .join("");
  const cc = stats.connectionCounts || {};
  const connKeys = CONN_ORDER.filter((k) => cc[k]).concat(
    Object.keys(cc).filter((k) => !CONN_ORDER.includes(k))
  );
  const connRows = connKeys
    .map(
      (k) =>
        `<div class="group-row"><span class="name">${k || "Unknown"}</span><span class="count">${cc[k]}</span></div>`
    )
    .join("");
  const connBlock = connRows
    ? `<div class="subhead">Connection</div>${connRows}`
    : "";
  const queueLine = stats.queue.size
    ? `<div class="hint">Queue: ${stats.queue.cursor}/${stats.queue.size}${stats.queue.active ? " (running)" : ""}</div>`
    : "";
  $("stats").innerHTML = `${rows}${connBlock}<div class="total"><span>Total unique</span><span>${stats.total}</span></div>${queueLine}`;
};

const refresh = async () => {
  const stats = await send({ type: "popup:stats" });
  if (stats?.status) setStatus(stats.status);
  renderStats(stats);
};

$("run-here").addEventListener("click", async () => {
  await send({ type: "popup:run-here" });
  setStatus("Scraping current page…");
});

$("stop").addEventListener("click", async () => {
  await send({ type: "popup:stop-queue" });
  setStatus("Stop signal sent.");
});

$("save-queue").addEventListener("click", async () => {
  const urls = $("queue-input").value
    .split(/\r?\n/)
    .map((s) => s.trim())
    .filter((s) => s.startsWith("http"));
  const resp = await send({ type: "popup:set-queue", payload: urls });
  setStatus(`Saved ${resp?.count || 0} URLs to queue.`);
  refresh();
});

$("start-queue").addEventListener("click", async () => {
  await send({ type: "popup:start-queue" });
  setStatus("Queue started.");
});

$("stop-queue").addEventListener("click", async () => {
  await send({ type: "popup:stop-queue" });
  setStatus("Queue stopped.");
});

$("export-master").addEventListener("click", async () => {
  await send({ type: "popup:export-master" });
});

$("export-by-group").addEventListener("click", async () => {
  await send({ type: "popup:export-by-group" });
});

$("clear").addEventListener("click", async () => {
  if (!confirm("Clear ALL captured leads? This cannot be undone.")) return;
  await send({ type: "popup:clear" });
  refresh();
});

chrome.runtime.onMessage.addListener((msg) => {
  if (msg?.type === "status-tick") setStatus(msg.text);
  refresh();
});

refresh();
setInterval(refresh, 2500);
