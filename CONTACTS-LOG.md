# CONTACTS LOG — the high-water mark

**Read this before adding any LinkedIn contacts. Update it the moment you finish adding them.**

Claude sessions do not remember anything between conversations. The only thing that survives
is what is written down here. If you add contacts and do not update this file, the next
session will have no way to know where you stopped, and you will spend an hour searching
for a name you already processed. That has already happened once.

---

## Current master: `CGB_MASTER_merged.xlsx` — 1,576 contacts

**9 Sep 2026.** `CGB_MASTER_outreach.xlsx` was never the whole picture. A second contact
database built during August — 1,129 contacts with scoring, bespoke email groups, connection
degree and drafted letters — lived outside this repository entirely. 609 of its contacts
appeared nowhere here. It has been recovered and merged.

| | |
|---|---|
| **Master file** | **`CGB_MASTER_merged.xlsx`** (1,576 contacts, 41 columns — grown from the 1,328 of the original merge) |
| Built from | `CGB_MASTER_outreach.xlsx` (690) + `finlit_contacts_categorized_bespoke_groups.xlsx` (1,129) |
| Overlap | 491 in both · 638 uploaded-only · 199 repo-only |
| Verified | 689/689 finished letters preserved · 1,128/1,128 uploaded contacts preserved · zero losses |

Neither source was a superset, so neither could be discarded. A straight replace would have
destroyed 432 finished letters; keeping only the repo copy would have dropped 609 contacts.

### Letter coverage across the merged list

| | |
|---|---|
| Finished letter (from `CGB_MASTER_outreach.xlsx`) | 690 |
| ~~Draft only (from the August workbook)~~ → extracted 9 Sep | 196 |
| ~~No letter yet~~ *(figure from the original merge)* | ~~442~~ |

**Current counts, 14 Sep 2026:** 1,576 rows — **1,173 finished**, 391 with no letter, 12 skipped.
Nothing reads NEEDS LETTER. The live backlog is `gap-backlog.xlsx`, not the 442 figure below,
which described the workbook as it stood before the LinkedIn export.

The 442 were the backlog as of the merge. ~~`august_top100_letters.md` holds 37 finished letters, 34 of
which are for contacts this repo had never heard of.~~ **Closed 9 Sep 2026 — all 37 are covered.**

**`august_top100_letters.md` is fully absorbed. Don't re-import it.** Re-checked 9 Sep against
every letter file: 37 of 37 now have a repo letter. It was drawn from the same `Draft Letter`
column the 196 extraction came from, so its text *is* the repo text — the repo copies just also
carry the published-status clause, the sign-off and the P.S., which that file has on none of its
37. Nothing there to salvage.

**The uploaded `finlit_contacts_categorized_bespoke_groups.xlsx` is fully absorbed too.** Three
copies were sent on 9 Sep; all three are the same 1,129-row file, and all 1,121 distinct names
are already in `CGB_MASTER_merged.xlsx`. Re-uploading it adds nothing.

**The 196 drafts are done (9 Sep 2026).** They now live in real letter files, signed, with the
P.S. and the published-status clause: 175 first-degree in `letters-601-775.md`, 21 second- and
third-degree appended to `letters-inmail-required.md` as #122–142.

### The lesson, recorded so it doesn't repeat

Searching git history, row counts and all 38 branches proves what is *in the repository*. It
proves nothing about what work exists. Both are true at once: nothing had been committed
since 3 Aug, **and** hundreds of contacts had been added during August. If a file is not
committed here, no amount of searching here will find it — ask for the file.

---

## Where the contacts actually live

**Screenshot batches, newest connection date first.** This is the order that matters when you
ask "what's the most recent thing added" — not the order rows landed in the workbook.

| Screenshot batch | Connections dated | Count | Letter file |
|---|---|---|---|
| 8 screens, sent 8 Sep | **4–8 Sep** ← newest | 66 | `letters-new-sept.md` #535–600 — complete |
| 4 screens, sent 9 Sep | 23–26 Aug | 36 | `letters-776-809.md` #776–809 |
| New Aug | 30 Jul – 3 Aug | 19 | folded into `letters-517-616.md` |
| New Jul 28–29 | 28–29 Jul | 2 | folded into `letters-517-616.md` #510–511 |
| New July | 19–27 Jul | 10 | folded into `letters-517-616.md` |

### Coverage timeline — measured against the real data, 14 Sep 2026

**Screenshot capture is retired.** The LinkedIn data export settles what the screens could only
estimate. `Connections.csv` from the export of 10 Sep 2026 holds **4,244 connections** with name,
URL, company, position and exact connection date — every field the screenshots kept losing.

The gaps were real and larger than the estimate:

| Window | Actual connections | Captured by screenshot | Missed |
|---|---|---|---|
| **4 – 22 Aug** | 104 | 0 | **104** |
| 23–26 Aug | 42 | 36 | 6 |
| **27 Aug – 3 Sep** | 184 | 0 | **184** |
| 4–8 Sep | 77 | 66 | 11 |
| **since 8 Sep** | 22 | 0 | **22** |

Even the "captured" windows were short — 36 of 42, and 66 of 77. Screenshots miss rows.

Of everyone in those windows, 231 had no letter. **The entire educator block is now written** —
all 147, letters 810–956 in `letters-gap-educators.md`. **84 remain**: 30 financial literacy &
services, 7 media & journalists, 47 other. Listed with full titles in **`gap-backlog.md`** and
**`gap-backlog.xlsx`**, ready to draft with no further capture needed.

### Whales & HVTs — `whales-and-hvts.xlsx`

**The whale flagging had stopped dead after the New Aug batch (30 Jul – 3 Aug).** The 23–26 Aug
screens, the 4–8 Sep screens and the entire gap backlog were never assessed at all — so anything
added from late August onward was invisible to a whale or HVT filter. That's now fixed.

| | |
|---|---|
| Flagged in total | **114 whales · 537 HVTs** |
| Added 1 Aug onward | 138 |
| With no letter | **0** |

Both passes are in one sheet, sorted whales first, then anyone missing a letter, then the
August-forward wave. Column **Flagged by** separates the two:

- **hand-judged** — the original editorial pass. Never overwritten.
- **auto** — assessed 14 Sep from the LinkedIn export by role and employer reach. **Needs your
  eye.** A big organisation doesn't mean the person can say yes; the first pass promoted a
  school psychologist and an early-childhood instructor purely because their districts were
  large, and those were pulled back. Two still worth checking: Raquel Sheetz and Arielle Wright.

**Every flagged whale and HVT already has a letter.** The five that looked like gaps were data
artifacts — org names in the Name field, notes sitting in the Title field — and are marked
"NOT A GAP" in the workbook.

### A matching bug worth knowing about

Ten letter files don't use the `### N. Name` heading format: the MAESP/NAESP file uses `## N.`,
Delaware and the standalone `letter-*.md` files use `#`, the consider-tier file uses no headings
at all, and grandparents uses sub-lettered numbers (3b, 7a). Any script that indexes letters by
that one pattern will under-count by about 130 and invent gaps that don't exist. Index on all of
`#`, `##`, `###`, allow sub-letters, and fall back to a raw full-name match — initials like
"J.J." and "R P" collapse to a single token and vanish otherwise.

### How to add contacts from now on

**Ask for a fresh LinkedIn export, not screenshots.** Settings → Data Privacy → Get a copy of your
data → Connections. It arrives within a day and carries the title and the exact date for every
connection, which is what makes a letter personal and what makes gaps visible. One export replaces
every screenshot batch and cannot skip a row.

The old screenshot rules — capture overlap, write titles down first — only apply if the export
route is unavailable. Both failures they guarded against are solved by the export.

Everything else, by how it was assembled rather than when it connected:

| Batch | Count | Workbook rows | Letter file |
|---|---|---|---|
| 1–202 (rescored master) | 202 | 2–203 | `letters-1-198.md` |
| 199–396 | 198 | 204–401 | `letters-199-396.md` |
| 397–516 | 120 | 402–521 | `letters-397-516.md` |
| 517–616 | 100 | 522–621 | `letters-517-616.md` |
| New July (19–27 Jul) | 10 | 622–631 | folded into `letters-517-616.md` #512–516, #530–534 |
| New Jul 28–29 | 2 | 632–633 | folded into `letters-517-616.md` #510–511 |
| MAESP/NAESP | 9 | 634–642 | `letters-maesp-naesp.md` |
| Delaware | 17 | 643–659 | `letters-delaware.md` |
| Standalone / CFPB / Jump$tart | ~8 | 660–665 | `letter-*.md` files |
| New Aug (30 Jul – 3 Aug) | 19 | 666–684 | folded into `letters-517-616.md` #500–509, #517–529 |
| Grandparents | 6 | 686–691 | `letters-grandparents-readalong.md` |
| New Sept batch 1 (4–8 Sep) | 40 | added 9 Sep | `letters-new-sept.md` #535–574 |
| New Sept batch 2 (4–8 Sep) | 26 | added 9 Sep | `letters-new-sept.md` #575–600 |
| August workbook drafts, 1st-degree | 175 | merged master | `letters-601-775.md` #601–775 |
| August workbook drafts, 2nd/3rd | 21 | merged master | `letters-inmail-required.md` #122–142 |
| New Aug 23–26 (4 screens, sent 9 Sep) | 36 | added 9 Sep | `letters-776-809.md` #776–809 |

After the degree split (Sep 2026), the four main files hold **first-degree only**, numbered
as one running sequence 1–534, continued by `letters-new-sept.md` (535–574) and
`letters-601-775.md` (601–775). All 2nd/3rd-degree contacts live in
`letters-inmail-required.md`, numbered separately 1–142.

**575–600 are written** (14 Sep), so the run 535–600 is continuous and no block is reserved any
more. The gap-backlog educator letters continue the sequence from 810 in
`letters-gap-educators.md`.

### HIGH-WATER MARK — 14 Sep 2026

**Source of truth is now the LinkedIn export, not screenshots.** `Connections.csv` from the
export of 10 Sep 2026: 4,244 connections, each with title, employer, profile URL and exact
connection date. Ask for a fresh one whenever you want to know what's new.

**Newest connection on record: 9 Sep 2026.** Everyone connected on or before 8 Sep who deserves
a letter either has one or is listed in `gap-backlog.md`. The 22 who connected after 8 Sep are in
that file too.

**Highest letter number in use: 809.** Sequence 535–600 is closed — the reserved block is gone,
September batch 2 is written. Next new letter gets 810.

### The old screenshot markers, kept for reference

**Newest connection processed: James Totton, M.Ed, MBA.** Top of the 8 screens sent 8 Sep 2026,
which covered connections made 4–8 September. Nothing newer than him has been touched — anything
that connected after that capture is unprocessed. He has a letter, `letters-new-sept.md` #535.

**Scroll resumes below: Ma Charisse Joanne Labadan** (connected 24 Aug). She is the bottom of
the most recent screen batch — but **do not treat everything above her as handled.** Two windows
inside that range were never captured (4–22 Aug and roughly 27 Aug – 3 Sep). See the coverage
timeline below before deciding where to scroll.

**Highest letter number in use: 809.** The next letter written gets 810, unless it belongs to
September batch 2, which owns the reserved block 575–600.

Those first two are different questions and it's worth keeping them apart. Newest-processed
tells you whether a fresh batch has appeared since. Scroll-resumes-below tells you where to
start capturing. The order of rows in the workbook answers neither — rows get appended in
whatever order a batch was worked, so the last row added is meaningless as a marker.

LinkedIn lists My Network newest first, so the top of a screen is the most recent connection.
The 66 September names were captured in screen order, which is how James Totton is known to be
the newest of them; their individual connection dates were not recorded, only the 4–8 Sep range.

### Workbook status, 9 Sep 2026 — 1,430 rows

| Letter Status | Rows |
|---|---|
| Finished (letter written, file + number in `Notes (CGB)`) | 967 |
| blank (no letter, not yet triaged) | 430 |
| NEEDS LETTER (triaged, letter owed) | 26 |
| Skip — low fit | 7 |

Every letter in every `letters-*.md` file now has a workbook row. That was not true before
today: the four names flagged below as a known gap had letters and no rows, and **none of the
66 September contacts had ever been added at all** — their letters were written straight into
`letters-new-sept.md` and the workbook never heard about it. Both are fixed.

`Notes (CGB)` now carries the file and number for every finished letter, so you can go from a
workbook row to the letter text without grepping.

---

## Leads without names

**`targets-curriculum-directors.md`** — 19 elementary and district curriculum directors off three
LinkedIn People searches, 9 Sep 2026. Role, district, location and tenure captured; **no names**,
because LinkedIn shows out-of-network profiles as "LinkedIn Member". Not in the workbook, because
a row with no name is not a contact. The file explains the three ways to get a name; once you
have one, the letter joins the running sequence at 810.

## Known gaps — fix these when you get to them

- ~~**September batch 2 is blocked on titles.**~~ **Done, 14 Sep 2026.** The LinkedIn export
  supplied the role, employer and connection date for all 26, so they are written:
  `letters-new-sept.md` #575–600. Nothing in the workbook reads NEEDS LETTER any more.
- **`gap-backlog.md` / `gap-backlog.xlsx` — 231 connections with no letter.** The people in the
  capture windows nobody screenshotted, plus everyone who connected after 8 Sep. Titles already in
  hand from the export; they need drafting, not capturing.
  **Educators are being worked 40 at a time in `letters-gap-educators.md`.**

  | Batch | Numbers | Status |
  |---|---|---|
  | 1 | 810–849 | **done** — 14 Sep |
  | 2 | 850–889 | **done** — 14 Sep |
  | 3 | 890–929 | **done** — 14 Sep |
  | 4 | 930–956 | **done** — 14 Sep, 27 letters |

  147 educators in total: 117 from the 27 Aug – 3 Sep window, 17 who connected after 8 Sep, 13
  from 4–22 Aug. After those, 30 finance, 7 media and 47 other remain untouched.
- **Ra Chan · Tripti · Jamie Brydone-Jack.** Rows added 9 Sep 2026, so they are tracked now.
  Their letters (`letters-517-616.md` #531–534) still have generic opening lines that need
  personalising from each profile before anything is sent. Jennifer Pasteur turned out to be
  already present and needed nothing.
- **Duplicate source files.** `letters-new-aug.md`, `letters-new-july.md` and
  `letters-new-july-28-29.md` still exist alongside the folded copies in
  `letters-517-616.md`. Not deleted. Decide whether to keep them.

---

## How to update this file

When you add contacts from a LinkedIn screenshot batch:

1. **Write the name AND the job title down immediately**, before writing a single letter. The
   title is what makes the letter personal, and it lives nowhere but the screenshot. A name
   with no title is a contact you cannot write to later.
2. Add them to `CGB_MASTER_merged.xlsx` (Master sheet) — **this is the master now**, not
   `CGB_MASTER_outreach.xlsx`. Give the batch a name in `CGB Batch`.
3. Write the letters into the appropriate `letters-*.md` file, continuing the running number,
   and put the file and number in the row's `Notes (CGB)`.
4. **Come back here** and update the LAST CONTACT ADDED line, the batch table, and any gap you
   knowingly left open.

Step 2 is the one that got skipped for all 66 September contacts. The letters existed, the rows
did not, so the next session had no way to see the batch had happened.

A name in a screenshot that is not in this file is not tracked anywhere. Screenshots are not
storage.
