# Contact sync — project notes & chat record

Working notes for the LinkedIn → FinLit-contacts automation. Kept here because
the build happened across several sessions in an ephemeral container; this is the
durable record of what we decided, why, and where it stands.

Last updated: 2026-06-13.

---

## The goal

Each day (or when the PC wakes), pull Jonathan's new LinkedIn connections into
the contacts workbook, fill in the categorization columns, and route each person
to the right category tab — so the list stays current without hand-entry.

Workbook: `C:\Users\mdmen\Downloads\finlit_contacts_categorized_bespoke_groups.xlsx`
(the uploaded copy was `..._updated_20260612.xlsx` — same structure).

---

## Decisions so far

1. **Full browser automation of LinkedIn is tabled.** Logging a bot into LinkedIn
   to read profiles/posts violates LinkedIn's User Agreement (§8.2) and risks an
   automated, low-appeal account ban. Low volume lowers the odds but doesn't
   remove the tell, and a daily-forever cadence compounds a small per-run risk
   into a near-certain eventual hit. So we're not leading with it.
2. **The bespoke first-paragraph email writer is tabled** for now. Starting
   narrow with the contact list.
3. **Safe path first:** ingest is driven by LinkedIn's own data export (your
   data, handed over on purpose, zero account risk) or by pasted/handed rows. An
   OpenClaw browser "gather" front end exists as an option (`SKILL.md`) for when
   you want it, but it's not required and carries the risk above.
4. **The tool fills categorization, not judgment.** It writes category, segment,
   tab, group, the group's shared angle, fit notes, name-parse, degree, etc. It
   leaves Custom Email Priority/Score and the per-person Suggested Custom Angle /
   High Value Note blank — those are human calls (and the tabled email step).

---

## The workbook (15 sheets)

- **Master** — the deduped source of truth, one row per contact (~972). 30 columns.
- **Category tabs** — working views, one per Primary Category:
  Educators Schools, Media Journalists, Financial Literacy, Government Policy,
  Nonprofit Community, Financial Services, PTA Parent Leaders, Authors Books,
  Other Review.
- **Bespoke Email Groups** — the taxonomy legend: 10 groups, each with a fixed
  *Shared Bespoke Email Angle* and *Personalization Slot* the tool copies verbatim.
- **High Value Targets**, **LinkedIn Connections**, **New PDF Additions** —
  historical/priority snapshots (the tool does not write to these by default).
- **Summary** — counts.

### Primary Category → Outreach Segment → Tab → Fit Note

| Primary Category | Outreach Segment | Tab | Fit Note |
|---|---|---|---|
| Financial Literacy & Financial Education | Financial Literacy | Financial Literacy | direct financial literacy, money education, or consumer education fit |
| Educators & Schools | Educator | Educators Schools | school, educator, curriculum, or academic fit |
| Media & Journalists | Media | Media Journalists | media, journalist, editor, producer, or finance-news fit |
| Government, Policy & Regulators | Government / Policy | Government Policy | public-sector, policy, or regulator fit |
| Financial Services, Fintech & Corporate | Financial Services / Corporate | Financial Services | financial services, fintech, credit, banking, or corporate finance fit |
| Nonprofit & Community Programs | Nonprofit / Community | Nonprofit Community | nonprofit, philanthropy, community, or impact fit |
| PTA & Parent Leaders | PTA / Parent Leader | PTA Parent Leaders | parent, family, or PTA leadership fit |
| Authors, Books & Publishing | Books / Publishing | Authors Books | books, authorship, or publishing fit |
| Other / Review | Review | Other Review | not enough role/account signal to classify confidently |

### The 10 Bespoke Email Groups (shared angle in brief)

Classroom/school/curriculum/library practitioners · Personal-finance media &
storytellers · Financial wellness educators/coaches · Financial-literacy
coalitions & curriculum orgs · Federal Reserve & policy/institutional connectors ·
Parent/PTA/family advocates · Children's books & publishing · Public-sector
financial education / consumer protection · Community impact & nonprofit leaders ·
Individual review / one-off. (Exact angles live in the workbook's legend sheet and
are read at runtime — never hard-coded here, so they always match your wording.)

---

## What the tool does (`finlit_sync.py`)

For each new contact (from a CSV export, or JSON handed in by OpenClaw):

1. Parse the name → display, primary name, credentials (e.g. "Billy J. Hensley,
   Ph.D." → "Billy J. Hensley" + "Ph.D."; strips leading ★).
2. Classify Primary Category from title + account (heuristic keyword rules in the
   user's exact vocabulary).
3. Derive Outreach Segment, tab, and Fit Note from the category.
4. Assign a Bespoke Email Group (best guess; Financial Services and Review are
   left blank for manual grouping) and copy that group's Shared Angle +
   Personalization Slot from the legend.
5. Dedupe by normalized name against Master + a state file (no URL column exists,
   so name is the key).
6. Append the row to **Master** and to the matching **category tab**.
7. Back up the whole workbook first; mark new rows `auto-added by contact-sync` in
   Parse Notes; leave judgment columns blank.

**Tested against a copy of the real workbook:** correct classification and tab
routing, credential parsing, the ★ strip, legend-angle copy, dedupe (caught an
existing contact), backup, idempotent re-run, and all 15 sheets intact after save.

### Heuristic caveats (for review)

- Classification is keyword-based, not the original (likely LLM) pipeline. Edge
  cases will miss — e.g. a "Financial Literacy Director" at a "…Foundation"
  currently lands in Nonprofit because the org word wins. Auto-rows are flagged in
  Parse Notes so they're easy to find and fix.
- `openpyxl` may drop charts/images on save. The Summary here is text, so it's
  fine, but keep the backups and eyeball the file after the first real run.

---

## How to run

See `README.md` for full steps. Short version:

```
pip install -r requirements.txt
# preview:
python finlit_sync.py --from-csv "%USERPROFILE%\Downloads\Connections.csv" --dry-run
# write:
python finlit_sync.py --from-csv "%USERPROFILE%\Downloads\Connections.csv"
```

Schedule with `register-task.ps1` (logon + daily; add "On workstation unlock" in
Task Scheduler for the wake case). `run-sync.ps1` is what the task calls.

---

## Backlog / next steps

- **AI-assisted classification (high value).** Swap the keyword rules for a Claude
  call that classifies into the exact taxonomy (and could draft the Suggested
  Custom Angle). Much closer to the original pipeline's quality; needs an
  `ANTHROPIC_API_KEY`. Tiny per-contact cost at this volume.
- **Bespoke email writer** (the tabled piece): per-person opener + group angle +
  general body → Gmail drafts.
- **OpenClaw browser gather** front end, if/when you accept the LinkedIn risk.
- **Custom Email Priority/Score:** currently left blank. Decide whether to compute
  a heuristic tier or keep it a manual call.

## Open questions for Jonathan

1. The "finlit role at a foundation" classification call — prefer title to win
   (→ Financial Literacy) or org to win (→ Nonprofit)? Currently org wins.
2. Also append new connections to the **LinkedIn Connections** tab, or keep that
   as a frozen snapshot? Currently not touched.
3. Want Custom Email Priority auto-estimated, or left blank for you?
