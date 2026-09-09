# CONTACTS LOG — the high-water mark

**Read this before adding any LinkedIn contacts. Update it the moment you finish adding them.**

Claude sessions do not remember anything between conversations. The only thing that survives
is what is written down here. If you add contacts and do not update this file, the next
session will have no way to know where you stopped, and you will spend an hour searching
for a name you already processed. That has already happened once.

---

## Current master: `CGB_MASTER_merged.xlsx` — 1,328 contacts

**9 Sep 2026.** `CGB_MASTER_outreach.xlsx` was never the whole picture. A second contact
database built during August — 1,129 contacts with scoring, bespoke email groups, connection
degree and drafted letters — lived outside this repository entirely. 609 of its contacts
appeared nowhere here. It has been recovered and merged.

| | |
|---|---|
| **Master file** | **`CGB_MASTER_merged.xlsx`** (1,328 contacts, 41 columns) |
| Built from | `CGB_MASTER_outreach.xlsx` (690) + `finlit_contacts_categorized_bespoke_groups.xlsx` (1,129) |
| Overlap | 491 in both · 638 uploaded-only · 199 repo-only |
| Verified | 689/689 finished letters preserved · 1,128/1,128 uploaded contacts preserved · zero losses |

Neither source was a superset, so neither could be discarded. A straight replace would have
destroyed 432 finished letters; keeping only the repo copy would have dropped 609 contacts.

### Letter coverage across the merged list

| | |
|---|---|
| Finished letter (from `CGB_MASTER_outreach.xlsx`) | 690 |
| Draft only (from the August workbook) | 196 |
| **No letter yet** | **442** |

The 442 are the real backlog. `august_top100_letters.md` holds 37 finished letters, 34 of
which are for contacts this repo had never heard of.

### The lesson, recorded so it doesn't repeat

Searching git history, row counts and all 38 branches proves what is *in the repository*. It
proves nothing about what work exists. Both are true at once: nothing had been committed
since 3 Aug, **and** hundreds of contacts had been added during August. If a file is not
committed here, no amount of searching here will find it — ask for the file.

---

## Where the contacts actually live

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

After the degree split (Sep 2026), the four main files hold **first-degree only**, numbered
as one running sequence 1–534. All 2nd/3rd-degree contacts live in
`letters-inmail-required.md`, numbered separately 1–121.

---

## Known gaps — fix these when you get to them

- **Ra Chan · Tripti · Jennifer Pasteur · Jamie Brydone-Jack.** Letters exist
  (`letters-new-aug.md` #20–23, folded in as `letters-517-616.md` #531–534) but these four
  were **never added to the workbook**. The New Aug batch is 19 workbook rows against 23
  people in the file. Their opening lines still need personalising from each profile before
  anything is sent.
- **Duplicate source files.** `letters-new-aug.md`, `letters-new-july.md` and
  `letters-new-july-28-29.md` still exist alongside the folded copies in
  `letters-517-616.md`. Not deleted. Decide whether to keep them.

---

## How to update this file

When you add contacts from a LinkedIn screenshot batch:

1. Add them to `CGB_MASTER_outreach.xlsx` (Master sheet), giving the batch a name in column B.
2. Write the letters into the appropriate `letters-*.md` file, continuing the running number.
3. **Come back here** and update: the Last-contact-added table, the batch table, and any gap
   you knowingly left open.

A name in a screenshot that is not in this file is not tracked anywhere. Screenshots are not
storage.
