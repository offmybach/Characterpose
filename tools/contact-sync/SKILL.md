---
name: linkedin-contact-sync
description: >
  Gather the newest LinkedIn connections from the logged-in browser and append
  them to the FinLit contacts workbook, classified into the right category and
  tab. Use when asked to "sync contacts", "add new connections", or on the
  daily/on-wake schedule. Read-only on LinkedIn — never sends requests or messages.
metadata:
  author: CGB
  volume_cap: 25
  engine: finlit_sync.py
---

# LinkedIn → FinLit contacts sync

Collect only **new** first-degree connections and hand them to `finlit_sync.py`,
which classifies each into a Primary Category, routes them to Master and the right
category tab, and fills the categorization columns. Your job is just to gather and
hand off.

## Guardrails (do not skip)

- **Read-only.** Read pages only. Never send a connection request, never open the
  messaging panel, never click Connect or Follow.
- **Small and human-paced.** At most **25** connections per run. Pause a few
  seconds between actions. If LinkedIn shows a checkpoint or CAPTCHA, stop and
  tell the user — do not loop on it.
- **Use the person's own logged-in browser** (`profile: "user"`). They're at the
  machine to approve the attach prompt.

## Steps

1. Open the browser with `profile: "user"` and navigate to:
   `https://www.linkedin.com/mynetwork/invite-connect/connections/`
   (sorted most-recent-first).

2. `browser snapshot` and read connection cards from the top. For each, capture
   `name`, `headline` (the grey subtitle), and the `/in/...` profile URL.

3. Collect down to **25** cards, or until you recognize names from a prior run.
   Don't scroll deep — a handful of new people per day is expected.

4. (Optional, for richer columns) open each new profile and read current
   **company**, **title**, **location**, and the **connection degree**; then go
   back. Same 25-cap and pacing.

5. Write the people to `%USERPROFILE%\Downloads\_new_connections.json` as a JSON
   array. Use these keys (omit any you didn't capture — the engine fills the rest):

   ```json
   [
     {"name": "Maria Lopez", "title": "Financial Literacy Director",
      "account": "Sunrise Credit Union", "degree": "1st",
      "location": "Columbus, OH", "headline": "Financial Literacy Director at Sunrise Credit Union"}
   ]
   ```
   (`account` = company; `title` or `headline` both work; `degree` like "1st".)

6. Run the engine to classify and append (it dedupes, routes to the right tab,
   copies the group angle, and backs up the workbook first):

   ```
   python "%USERPROFILE%\path\to\tools\contact-sync\finlit_sync.py" --from-json "%USERPROFILE%\Downloads\_new_connections.json"
   ```
   Add `--dry-run` first to preview.

7. Report the engine's summary (added / duplicates / per-category tally), then
   delete `_new_connections.json`.
