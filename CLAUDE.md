# Project: Clarence Gets a Bargain

Single-page children's book website + interactive magazine flipbook.

## Key File
- `clarence-gets-a-bargain.html` — the entire site (HTML + CSS + JS in one file, ~2200 lines)

## Font
- **Hold** is the brand font. Use it everywhere. Never use Nunito or other fallbacks as primary.
- Font files: `fonts/Hold.woff2`, `fonts/Hold.woff`, `fonts/Hold.otf`
- `@font-face` declared at line ~35

## File Structure (approximate line ranges)
- **CSS styles**: lines 34–352
- **JSON-LD structured data**: lines 353–465
- **HTML content**: lines 466–700
- **Canvas JS helpers** (`drawHeader`, `drawCard`, `drawReview`, `wrapText`, etc.): lines 900–1130
- **Magazine pages array** (10 canvas-drawn pages): lines 1160–1500
  - Page 0: Inside front cover (dedication/welcome)
  - Page 1: "Here's The Deal" (hook)
  - Page 5: "Money Skills" (6 concept cards in 2x3 grid)
  - Page 6: Reviews (3 review coupon cards)
  - Page 7: "Inside the Story" (key scenes)
  - Page 8: "What Kids Learn" (skills at a glance)
  - Page 9: FAQ
- **Cover texture / 3D flipbook renderer**: lines 1500–2200

## Design Rules
- **"Wants vs. Needs"** must ALWAYS be bold and italic — it's a core FLAC concept
- Headline color: `#0054a6` (blue) — NOT dark navy, needs contrast against `#111` body text
- Orange accent: `#ff6b2b`, `#F57C00`
- Cream background on magazine pages: `#f5ecd7`
- All magazine cards use dashed coupon-style borders

## People
- **Author**: Jonathan Bach (attorney, artist)
- **Maryann Milewski Moskal**: Veteran Elementary School Educator, **30+ years** K–5 classroom experience (not 20+)

## Site Sections (HTML)
- Hero with animated stats
- Coupon navigation grid (`#coupons`)
- Asset sections (Shopping Homework, Smart Discovery, Coupon Twist)
- Educator trust block (`#educators`)
- Authority anchor quote (Maryann's endorsement — `.anchor-quote`)
- Standards alignment grid
- Resources (downloadable PDFs in `downloads/`)
- Institutional/bulk orders
- Closing pitch ("The CFO's Desk")

## Downloads
- `downloads/assessment-worksheet.pdf`
- `downloads/discussion-guide.pdf`
- `downloads/educator-preview.pdf`
- `downloads/family-activity.pdf`
- `downloads/lesson-plans.pdf`
- `downloads/standards-chart.pdf`
