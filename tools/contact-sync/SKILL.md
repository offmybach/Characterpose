---
name: linkedin-contact-sync
description: >
  Gather the newest LinkedIn connections from the logged-in browser and append
  them to the CGB contacts workbook with columns filled and a CGB audience group
  tagged. Use when asked to "sync contacts", "add new connections", or on the
  daily/on-wake schedule. Read-only on LinkedIn — never sends requests or messages.
metadata:
  author: CGB
  volume_cap: 25
  source: linkedin connections page
---

# LinkedIn → CGB contacts sync

Append only **new** first-degree connections to the contacts workbook. A
separate Python engine does the deduping, column-filling, grouping, and backup —
your job is just to collect the new connections and hand them over as JSON.

## Guardrails (do not skip)

- **Read-only.** Open and read pages only. Never send a connection request, never
  open the messaging panel, never click "Connect" or "Follow".
- **Stay small and human-paced.** Collect at most **25** connections per run.
  Pause a few seconds between page actions. If LinkedIn shows a checkpoint or
  CAPTCHA, stop and tell the user — do not try to solve it in a loop.
- **Use the person's own logged-in browser** (`profile: "user"`). The user is at
  the machine and will approve the attach prompt.

## Steps

1. Open the browser with `profile: "user"` and navigate to:
   `https://www.linkedin.com/mynetwork/invite-connect/connections/`
   This list is sorted **most-recent-first**.

2. Take a `browser snapshot` and read the connection cards from the top. For each
   card capture:
   - `name` — the person's full name
   - `headline` — the grey subtitle under the name
   - `profile_url` — the link on the name (the `/in/...` URL)

3. Collect down the list until you have **25** cards, or until the cards are
   clearly old (you recognize names from a previous run). Don't scroll deep — a
   handful of new people per day is expected.

4. (Optional, only if richer columns are wanted) For each new person, open the
   profile in the same tab, read the current **company**, **title**, and
   **location** from the intro section, then go back. Keep the same 25-cap and
   pacing. Skip this step if the headline already covers what's needed.

5. Write the collected people to `%USERPROFILE%\Downloads\_new_connections.json`
   as a JSON array. Each object uses these keys (omit any you didn't capture):

   ```json
   [
     {"name": "Maria Lopez", "headline": "Financial Literacy Director at Sunrise Credit Union",
      "company": "Sunrise Credit Union", "title": "Financial Literacy Director",
      "location": "Columbus, OH", "profile_url": "https://www.linkedin.com/in/marialopez/"}
   ]
   ```

6. Run the engine to append them (it dedupes, fills columns, tags the group, and
   backs up the workbook first):

   ```
   python "%USERPROFILE%\path\to\tools\contact-sync\sync_contacts.py" --from-json "%USERPROFILE%\Downloads\_new_connections.json"
   ```

   Run it once with `--dry-run` added if you want to preview before writing.

7. Report the engine's printed summary back to the user: how many were added,
   how many were duplicates, and the group tally. Then delete
   `_new_connections.json`.
