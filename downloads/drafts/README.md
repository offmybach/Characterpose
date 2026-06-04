# Toolkit Refresh — Drafts

Six rewritten educator PDFs, scaffolded against the real book.

## What's in here

| File | Replaces | Status |
|---|---|---|
| `01-educator-preview.md` | `downloads/educator-preview.pdf` | Draft |
| `02-lesson-plans.md` | `downloads/lesson-plans.pdf` | Draft |
| `03-discussion-guide.md` | `downloads/discussion-guide.pdf` | Draft |
| `04-assessment-worksheet.md` | `downloads/assessment-worksheet.pdf` | Draft |
| `05-family-activity.md` | `downloads/family-activity.pdf` | Draft |
| `06-standards-chart.md` | `downloads/standards-chart.pdf` | Draft |

## Why this exists

The original PDFs (still sitting in `downloads/`) were generated against an imagined version of the book — Turbo-Zoom Racer 3000 at "Barginville," three vendors, $4.75 piggy bank, lemonade vendor at the end. None of that is in the published book. A teacher who actually reads Clarence Gets a Bargain and then opens those PDFs catches the mismatch inside five minutes.

These drafts are anchored to the real book: Clarence Wyze, RoBimmie, Sea-Mart, the Clearance/Clarence joke, the 10%-off coupon at checkout, Mom's bills speech, the 529, the family games at the end.

## Review checklist

Before any of these get converted to PDF, confirm:

- [ ] Page-number references match your printed edition exactly
- [ ] Voice passes the AI smell test (see CLAUDE.md §2)
- [ ] No invented dialogue (mom/dad/Clarence quoted verbatim or paraphrased — never put new words in their mouths)
- [ ] Standards codes match the latest Jump$tart / CEE / CCSS frameworks you're targeting
- [ ] Grade band says **1–5**, not K–5
- [ ] Author bio + ordering info match the live site (price $19.99 + $5.99 shipping, direct order at clarencegetsabargain.com)

## Converting to PDF

When the drafts are approved, options:

1. **Markdown → PDF via Pandoc** — preserves styling, fast, scriptable:
   ```
   pandoc 01-educator-preview.md -o ../educator-preview.pdf --pdf-engine=weasyprint -c cgb-style.css
   ```
2. **Markdown → HTML → Print to PDF** — paste into a styled HTML shell, print via browser. Most control over Hold-font headers and orange/blue brand colors.
3. **Hand-layout in Canva or InDesign** — best for the marketing-grade educator preview, slowest.

A custom `cgb-style.css` (Hold font headers, #0054a6 blue, #ff6b2b orange, cream backgrounds for callouts) would make all six match the brand. Worth building once, reusing forever.

## Revision history

**v2 — Critical + important fixes applied across all 6 drafts:**
- Folded in the **official 21-term back-matter glossary** (verbatim from `images/CGB_Glossary_Page1.png` + `Page2.png`), now also in CLAUDE.md
- Added the **Receipt habit** (Mom photographs every receipt, page 22) as a real-world money skill
- Added the **Wyze wordplay** callout — explicit on page 21 and in the glossary
- Replaced fabricated standards codes with valid Jump$tart 2021 / CEE / CCSS / FDIC citations + source URLs
- Killed the "Whether you're X or Y" AI-tell pattern
- Rebalanced lesson plan time budgets (the 12-min read-aloud for 3 pages was wrong)
- Added accessibility/ELL/IEP/trauma-informed framing throughout the lesson plans
- Added accommodations page to assessment worksheet (read-aloud, picture-supported, oral, extended time, Spanish)
- Fixed Pre-Q4 juice question (specified "same juice"), Pre-Q9 ("winter coat" → "glass of water"), Post-Q5 distractor
- Expanded class data tracking table from 12 rows to 25 + "duplicate as needed"
- Softened grant claims to "supports common documentation requirements" with note to verify per-foundation
- Family activity: shrunk Activity 4 from 1 week to 1 grocery run; added ⏱ time + 🛒 materials per activity; bilingual pointer
- Discussion guide: added whole-book themes closing section, Clarence/Clearance teaching-moment callout, Wyze pun callout, trauma-informed facilitation note for the bills question
- Standards chart: full rewrite — CEE has 6 standards (not 12/13); Jump$tart strands renamed correctly; concept-by-concept crosswalk moved to top; framework source URLs added; 21-term glossary count integrated; 23 enumerated teaching concepts

## What's still TODO

- The **Wyze Shopper Certificate** referenced in Week 4 of the lesson plans needs a printable design.
- The **Curriculum Alignment Matrix** tool already exists at `resources/curriculum-alignment-matrix.html`. Sanity-check that its concept list matches the 23 concepts in `06-standards-chart.md`.
- **Printables marked [P]** in the lesson plans (sort cards, clearance stickers, comparison worksheets, coupon templates) — either ship as a "Curriculum Companion Pack" or remove the [P] markers and rely on teachers to make their own.
- Polish-tier suggestions from the review weren't addressed (these are nice-to-have, not credibility risks). See chat transcript or rerun the review for the punch list.
