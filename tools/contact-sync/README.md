# CGB contact sync

Append **new** LinkedIn connections to the FinLit contacts workbook each day —
classified into your categories, routed to the right tab, with the group's shared
email angle filled in — without overwriting the categorizing you've already done.

Target workbook (default):
`C:\Users\mdmen\Downloads\finlit_contacts_categorized_bespoke_groups.xlsx`

This tool is tuned to your actual workbook (Master + category tabs + the Bespoke
Email Groups legend). For the full structure and design decisions, see
`PROJECT-NOTES.md`. The engine is `finlit_sync.py`.

## What it fills vs. leaves for you

**Fills** (deterministic): Primary Category, Outreach Segment, Bespoke Email
Group, the group's Shared Angle + Personalization Slot (copied from your legend),
Fit Notes, Fit Score, Name / Primary Name / Credentials, Title, Account, LI
Connection Degree, Geography, dates, and provenance (Parse Notes =
`auto-added by contact-sync <date>`).

**Leaves blank for you** (judgment / the tabled email step): Custom Email
Priority, Custom Email Score, High Value Note, Suggested Custom Angle.

Each new contact is written to **Master** and to its **category tab**.

---

## Two ways to feed it

**A — CSV export (safe, recommended).** Export your connections from LinkedIn
(Settings → Data Privacy → Get a copy of your data → *Connections*), save
`Connections.csv` to Downloads. Your data, handed over on purpose — zero account
risk.

**B — OpenClaw browser skill (optional).** `SKILL.md` tells OpenClaw to read the
newest connections off the page (read-only, capped) and write them to
`_new_connections.json`, which the same engine ingests. This is the
LinkedIn-automation path discussed in `PROJECT-NOTES.md` — use it knowing the
risk.

---

## One-time setup

1. Python 3.10+ (already installed).
2. `pip install -r requirements.txt`
3. Confirm the workbook path; override anywhere with `--file "C:\path.xlsx"`.

## Try it once, safely

```
python finlit_sync.py --from-csv "%USERPROFILE%\Downloads\Connections.csv" --dry-run
```

It prints how each new contact would be classified, which tab it'd go to, the
group it'd get, and who it'd skip as a duplicate. Looks right? Drop `--dry-run`.

## Schedule it

```
powershell -ExecutionPolicy Bypass -File .\register-task.ps1
```

Registers **CGB Contact Sync** (runs at logon and daily at 9 AM, calling
`run-sync.ps1`). To also fire when you unlock after waking the PC: Task Scheduler
→ CGB Contact Sync → Triggers → New → **"On workstation unlock"** (a ten-second
GUI add; that trigger has no clean PowerShell form).

Test now: `Start-ScheduledTask -TaskName "CGB Contact Sync"`. Logs land in
`sync.log`.

---

## Useful flags

- `--dry-run` — preview, write nothing.
- `--no-tabs` — write to Master only, skip the category tabs.
- `--limit N` — cap rows added per run (default 100).
- `--from-json -` — read a JSON array from stdin (the OpenClaw path).

## Safety notes

- **Close the workbook in Excel before a run.** Excel locks the file; the engine
  detects it and tells you to close it rather than failing silently.
- Every write makes a timestamped backup in `contact-sync-backups` next to the
  workbook. To undo a run, restore the latest backup.
- `openpyxl` may not preserve charts/images on save. Your Summary tab is text, so
  it's fine, but keep backups and eyeball the file after the first real run.
- `.contact-sync-state.json` (next to the workbook) remembers everyone ever
  added, so deleting a row won't make it reappear.

## Classification is heuristic

Categories are assigned by keyword rules in your exact vocabulary — close, not
perfect. Edge cases (e.g. a finlit role at a foundation) may land in a neighboring
category; auto-rows are flagged in Parse Notes so they're easy to spot and fix.
Higher-fidelity AI classification is on the backlog in `PROJECT-NOTES.md`.
