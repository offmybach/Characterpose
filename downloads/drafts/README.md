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

## What's still TODO

- Pages 33–36 of the book (glossary / back-matter) aren't yet extracted into CLAUDE.md. Once they are, the discussion guide can pick up any back-matter vocabulary.
- The "Wyze Shopper Certificate" referenced in Week 4 of the lesson plans needs a printable design.
- The "Curriculum Alignment Matrix" tool referenced in the standards chart and assessment worksheet already exists at `resources/curriculum-alignment-matrix.html`. Sanity-check that it covers the same 20 concepts listed in `06-standards-chart.md`.
