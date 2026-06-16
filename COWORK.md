# CGB Cowork Hub

Session-priming + process doc for "Clarence Gets a Bargain" work in this repo.
Start a session with: **"read COWORK.md first."**

`CLAUDE.md` holds the brand facts, voice rules, and site map (auto-loaded every
session). **COWORK.md holds the workflows** — the step-by-step plays we run often,
so they don't get re-figured-out from scratch each time.

---

## 1. FinLit Contacts → Outreach Workflow (the main play)

Turning new LinkedIn connections into grouped, drafted outreach. Run this whenever
a fresh batch of connections comes in.

### What lives where

| Piece | Path | Branch (today) |
|---|---|---|
| Contacts DB (source of truth = `Master` sheet) | `data/finlit_contacts_categorized_bespoke_groups.xlsx` | `claude/zen-curie-8igow`, `claude/intelligent-planck-112zss` |
| Contact sync (classify + group + dedupe) | `tools/contact-sync/finlit_sync.py` | `claude/tender-pascal-e27bzj` |
| Outreach generator (writes the letters) | `outreach/generate_outreach.py` | `claude/zealous-thompson-s67uwn` |

> **TODO:** these three live on three different branches. Consolidate onto one
> branch (or `main`) so a session doesn't have to hunt across branches.

### The workbook, briefly

14 sheets. The ones that matter:
- **Master** — one row per contact, the source of truth. Newest at the top (row 2).
- **Bespoke Email Groups** — the legend: 10 groups, each with a Shared Angle + a
  Personalization Slot. This drives the letter voice.
- **High Value Targets** — the curated Tier-1 + Strong subset the generator reads.
- **Category tabs** (Educators Schools, Media Journalists, etc.) — filtered views.

### Step 1 — Export from LinkedIn
My Network → Connections → **Sort by: Recently added**. Save the page (docx, CSV,
or screenshots). Newest connection is at the top; every LinkedIn connection is
1st-degree by definition.

### Step 2 — Find what's new
Compare the top of the export to the **sync watermark in `CLAUDE.md` §11**.
Everything above that name is new since the last run.

### Step 3 — Merge into the DB
Use `finlit_sync.py` (or its logic). For each new contact it:
- classifies a **Primary Category**, assigns the matching **Bespoke Email Group**,
  and copies that group's Shared Angle + Personalization Slot from the legend;
- sets degree (`1st`) and the connected date; inserts at the **top** of Master and
  the category tab.

Then mark + tidy:
- **`Letter Status` column on Master**: `NEEDS DRAFT` for new rows, `Drafted` for
  ones already worked. Also a soft-yellow row highlight and a `Parse Notes` tag.
- Financial Services + Other/Review get **no auto group** by design; flag them for
  manual grouping (the generator's neutral one-off voice covers them meanwhile).
- After inserting rows, **extend every Excel table's `ref`** (openpyxl will not do
  this for you) and add a TableColumn if you added a column. Bump `Summary` counts.
- **Update the watermark in `CLAUDE.md` §11** to the new newest contact.

### Step 4 — Draft the letters
Run `outreach/generate_outreach.py <workbook>`. Same voice + templates every time,
email + LinkedIn per contact, rotated by a name hash so 88 people don't get one
identical email.

Catch: the generator reads **High Value Targets** and only drafts rows with a
Custom Email Priority. New rows sit in Master with no priority, so either (a) give
them a priority and add them to High Value Targets, or (b) call `build()` directly
on the `NEEDS DRAFT` rows and route the ungrouped ones through the
`Individual review / one-off custom` voice. Output is by-group `.md` + a merge CSV.

### Step 5 — Review + send
Retune the ungrouped/neutral drafts once you slot them into a real group. Tighten
any opener that fell back to a generic role (the generator refuses to parrot a
long or buzzwordy headline). Send, then flip `Letter Status` `NEEDS DRAFT` →
`Drafted` as you go.

### The 10 bespoke groups
Classroom/library practitioners · Personal-finance media · Financial-wellness
coaches · Finlit coalitions & curriculum orgs · Federal Reserve / policy
connectors · Parent/PTA/family · Children's books & publishing · Public-sector
financial education · Individual one-off · Community/nonprofit programs.

---

## 2. Gotchas learned the hard way

- **Dedupe across all name columns** (`Name`, `LinkedIn Display Name`,
  `Primary Name / Org`). The shipped `finlit_sync.py` checks only one, so it will
  duplicate someone who was already in as 2nd-degree and has since upgraded to 1st.
- **openpyxl + Excel tables**: it preserves tables but does NOT grow `table.ref`
  when you insert rows. Set the ref by hand; verify by reopening the file and
  parsing the XML before you commit.
- **Two date formats** live in `Saved/Recent Date` (e.g. `June 9, 2026` and
  `6/7/2026; June 9, 2026`). Parse the latest, don't assume one format.

---

## 3. Privacy (do not skip)

The contacts workbook and the generated drafts hold **real people's names, titles,
and locations**. `offmybach/Characterpose` is a **public** repo. `outreach/README.md`
and `.gitignore` say to keep both **out of git** for this reason.

- Generated drafts: deliver as files, never commit.
- The workbook: gitignored and kept local; pass its path to the tools on the CLI.
  Do **not** take the repo private; it serves the public Pages site
  (`clarencegetsabargain.com`). Keep the repo public, keep the data out of it.
- Still-open cleanup: the workbook remains in git history and on branch
  `claude/zen-curie-8igow`. Removing it from a branch tip does not purge history;
  a full scrub means rewriting history on all branches and force-pushing, and you
  should assume anything already public may have been copied.

---

## 4. Sync watermark
Single source of truth is **`CLAUDE.md` §11**. The newest 1st-degree connection
was added 2026-06-16 (name in the local workbook, not in this public repo); 989
unique contacts after that merge.

---

## 5. What this doc is NOT
- Not a replacement for `CLAUDE.md` (auto-loaded; brand + site facts live there).
- Not a changelog. Git does that.
- A living playbook: when a workflow changes, update the steps here.
