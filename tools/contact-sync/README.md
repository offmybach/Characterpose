# CGB contact sync

Append **new** LinkedIn connections to your contacts workbook each day, with the
columns filled in and a CGB audience group tagged — without ever overwriting the
categorizing you've already done.

Target workbook (default):
`C:\Users\mdmen\Downloads\finlit_contacts_categorized_bespoke_groups.xlsx`

The engine reads your sheet's **own header row** and fills whatever columns it
finds. It never invents columns and never edits existing rows. Before every
write it drops a timestamped copy in a `contact-sync-backups` folder next to the
workbook.

---

## Two ways to feed it

**A — CSV export (safe, recommended).** Export your connections from LinkedIn
(Settings → Data Privacy → Get a copy of your data → *Connections*), save the
`Connections.csv` to your Downloads folder. The scheduled task picks it up,
appends anyone new, and moves the export aside. This is your data, handed over by
LinkedIn on purpose — zero account risk.

**B — OpenClaw browser skill (optional).** `SKILL.md` tells OpenClaw to read the
newest connections straight off the connections page (capped at 25, read-only)
and write them to `_new_connections.json`, which the same engine then ingests.
This skips the manual export but is the LinkedIn-automation path we talked about —
use it knowing that.

Either way the engine does the identical work; only the source differs.

---

## One-time setup

1. Install Python 3.10+ (you already have it).
2. Install the one dependency:
   ```
   pip install -r requirements.txt
   ```
3. Confirm the workbook path. If it ever moves, pass `--file "C:\new\path.xlsx"`.

## Try it once, safely

Drop a `Connections.csv` in Downloads, then preview without writing:

```
python sync_contacts.py --from-csv "%USERPROFILE%\Downloads\Connections.csv" --dry-run
```

It prints which columns it recognized, who it would add, who it'd skip as a
duplicate, and how it tagged each group. Happy with it? Drop the `--dry-run`.

## Schedule it

```
powershell -ExecutionPolicy Bypass -File .\register-task.ps1
```

That registers a task named **CGB Contact Sync** that runs at logon and daily at
9 AM, calling `run-sync.ps1`. To also fire the instant you unlock after waking
the PC: open **Task Scheduler → CGB Contact Sync → Triggers → New → "On
workstation unlock"**. (That trigger has no clean PowerShell form, so it's a
ten-second GUI add.)

Test the task immediately:
```
Start-ScheduledTask -TaskName "CGB Contact Sync"
```

Logs land in `sync.log` next to the script.

---

## How the columns get filled

| Your column (matched loosely) | Filled with |
|---|---|
| First / Last / Full Name | the connection's name |
| Company / Organization | current company |
| Title / Position / Headline | current role |
| URL / Profile / LinkedIn | profile link (also the dedupe key) |
| Email | email (only present in CSV exports) |
| Location | city/region (only if captured) |
| Connected On | LinkedIn connection date |
| Date Added / Imported | today's date |
| Group / Category / Bespoke / Audience | the CGB group (below) |
| Notes / Why / Opener | left blank — that's the tabled bespoke-email step |

**Grouping.** Each new contact is tagged from title + company into one of:
Librarian, Educator (K-5), Institutional / Bulk, or Parent / General. If your
sheet already uses its own labels (e.g. "Educators", "Parents"), the engine
reuses *your* wording instead of imposing new labels. The rules live in
`SEGMENT_RULES` near the top of `sync_contacts.py` — easy to adjust.

## Safety notes

- **Close the workbook in Excel before a run.** Excel locks the file; the engine
  detects that and tells you to close it rather than failing silently.
- Every write makes a backup first. To undo a run, restore the latest file from
  `contact-sync-backups`.
- `.contact-sync-state.json` (next to the workbook) remembers everyone ever
  added, so deleting a row won't cause it to come back.

## Tested

The engine was run against a synthetic sheet: column detection, duplicate
skipping (by profile URL), group tagging, reuse of existing labels, the backup,
and a no-op re-run all verified. The only thing tuned to *your* file at runtime
is the header mapping — send me your actual header row and I'll tighten the
column matches and the group labels to match exactly.
