---
name: linkedin-contact-sync
description: >
  Each morning, open LinkedIn in Edge, go to My Network, find newly added
  connections, and append them to the FinLit contacts workbook (classified and
  routed to the right tab) via finlit_sync.py. Use when asked to "sync contacts",
  "check for new connections", or "run the morning LinkedIn sync". Read-only on
  LinkedIn — never sends connection requests or messages.
user-invocable: true
metadata:
  author: CGB
  volume_cap: 25
  engine: finlit_sync.py
---

# LinkedIn → FinLit contacts sync (morning routine)

Collect only **newly added** first-degree connections and hand them to
`finlit_sync.py`, which classifies each into a Primary Category, routes them to
the top of Master and the right category tab, fills the categorization columns,
and dedupes against everyone already in the sheet. You just gather and hand off.

## Guardrails (do not skip)

- **Read-only.** Read pages only. Never send a connection request, open the
  messaging panel, or click Connect / Follow / Message.
- **Small and human-paced.** At most **25** people per run. Pause a few seconds
  between actions. If LinkedIn shows a checkpoint or CAPTCHA, **stop** and tell the
  user — never loop on it or try to solve it.
- **Browser:** use the configured Edge profile (see OPENCLAW-SETUP.md). With the
  `user` profile the user must approve the attach prompt — that's expected.

## Steps

1. Open Edge to the LinkedIn homepage: `https://www.linkedin.com/feed/`
2. Click **My Network** in the top nav (or go to
   `https://www.linkedin.com/mynetwork/`).
3. Open **Connections** (Manage my network → Connections, i.e.
   `https://www.linkedin.com/mynetwork/invite-connect/connections/`). Confirm the
   sort is **"Recently added"** so the newest are at the top.
4. `browser snapshot` and read connection cards from the top. For each, capture
   `name`, `headline` (the grey subtitle), and the `/in/...` profile URL. Collect
   down to **25**, or stop sooner once you reach people you recognize from a prior
   run — the engine dedupes, so a little overlap is fine.
5. (Optional, for richer columns) open each new profile and read current
   **company/account**, **title**, **location**, and the **connection degree**;
   then go back. Same 25-cap and pacing.
6. Write the people to `%USERPROFILE%\Downloads\_new_connections.json` as a JSON
   array. Keys (omit any you didn't capture — the engine fills the rest):

   ```json
   [
     {"name": "Maria Lopez", "title": "Financial Literacy Director",
      "account": "Sunrise Credit Union", "degree": "1st",
      "location": "Columbus, OH",
      "headline": "Financial Literacy Director at Sunrise Credit Union"}
   ]
   ```

7. Run the engine that ships in this skill's folder (it dedupes, classifies,
   routes to the right tab, copies the group angle, and backs up the workbook
   first). Adjust the path if you installed the skill elsewhere; the workbook path
   is already baked into the engine:

   ```
   python "%USERPROFILE%\.openclaw\skills\linkedin-contact-sync\finlit_sync.py" --from-json "%USERPROFILE%\Downloads\_new_connections.json"
   ```

8. Report the engine's summary (added / duplicates / per-category tally), then
   delete `_new_connections.json`.
