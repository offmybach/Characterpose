# Outreach generator

Turns the categorized FinLit contact spreadsheet into personalized **email +
LinkedIn** drafts for every Tier-1 and Strong contact, written in the CGB voice
and grouped by the 10 bespoke email groups defined in the workbook.

## Run it

```bash
python3 outreach/generate_outreach.py /path/to/finlit_contacts.xlsx
```

Output lands in `outreach/drafts/` (git-ignored):

- `ALL-216-DRAFTS.md` — everything in one file
- `by-group/NN-<group>.md` — one file per audience
- `clarence_outreach_drafts.csv` — all rows, merge-ready
- `HOW-TO-USE.md` — sending notes

## What it does

- Pulls the **Tier-1 (71)** and **Strong (145)** contacts — 216 total.
- Picks the right voice per group: punchy pitch for media, a *referral* ask (not
  a pitch) for the Federal Reserve / policy group, practitioner-to-practitioner
  for coaches, and so on.
- Personalizes each opener from the contact's real role and org, and cleans up
  OCR junk, buzzword self-descriptions, and duplicated org names along the way.
- Rotates subjects/bodies/openers by a hash of the name so a group of 88 doesn't
  read like one email sent 88 times.

## Set once

At the top of `generate_outreach.py`:

- `SITE` — your book link (set to `www.clarencegetsabargain.com`).
- `BOOK`, `AUTHOR` — title and signature name.

## Voice guardrails (baked in)

No marketing slop, no AI tells, no finance puns, zero em-dashes. Never reveals
the Clarence/Clearance wordplay or explains the "Wyze" pun. See `CLAUDE.md` §2.

## Privacy

The contact spreadsheet holds 972 real people's names, titles, and locations.
It is **not** committed to this repo, and neither are the generated drafts
(see `.gitignore`). Keep it that way.
