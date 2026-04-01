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

## Site Sections (HTML) — with line numbers
- **Nav bar**: line 470 (`#mainNav`)
- **Hero** with animated stats: line 472 (`.hero`)
- **Coupon navigation grid**: line 494 (`#coupons`)
- **Asset sections**: lines 517–538 (Shopping Homework, Smart Discovery, Coupon Twist)
- **Magazine / Flipbook**: line 540 (`#magazine`, `id="magCanvas"`) — the interactive 3D flipbook
- **Cover uploads** (front/back): lines 547–548 (`#frontUpload`, `#backUpload`)
- **Buy section**: line 552 (`#buy`)
- **Email signup**: line 566
- **Trust block**: line 576
- **Educator trust block**: line 597 (`#educators`)
- **Authority anchor quote** (Maryann's endorsement): inside educators section (`.anchor-quote`)
- **Standards alignment grid**: line 612
- **Meta section**: line 693
- **Program in a Box** (resources/downloads): line 719 (`.resources-section`) — "A Complete 4-Week Financial Literacy Module"
- **Institutional/bulk orders**: line 764 (`.institutional-section`)
- **Closing pitch** ("The CFO's Desk"): line 799 (`.pitch-section`)

## Alex AI Update — 10 Website Prompts (Reference)
These are template prompts for website planning/design. Placeholders shown as `[brackets]`.

1. **Website Planning** — "Act as a website strategist. Help me plan a website for a [business type] in [industry/location]. My target audience is [audience] and the main goal is [sales/leads/bookings/portfolio]. Suggest the best pages, what each page should include, and a simple site structure."
2. **Homepage Layout** — "Act as a web designer. Create a homepage structure for a [business type] website including a hero section, trust section, services overview, testimonials, FAQ, and a strong call-to-action. Explain what content should go in each section. Tone: [tone]."
3. **Homepage Copy** — "Write homepage copy for a [business type] website. Include a strong headline, subheadline, CTA button text, 3 key benefits, and a short closing section. Tone: [tone]. Target audience: [audience]. Goal: [goal]. Keep the language simple and clear."
4. **Website Design Style** — "Act as a web art director. Suggest a visual style for a [business type] website including colors, fonts, button styles, spacing, and overall mood. The brand should feel [modern/luxury/minimal/playful/trustworthy]. Keep the design beginner-friendly."
5. **Landing Page Code** — "Generate a responsive landing page in HTML and CSS for a [business type]. Include a hero section, features, testimonials, and a contact CTA. Use clean beginner-friendly code, simple styling, and clear class names so it's easy to edit."
6. **Services Page** — "Write a services page for a [business type]. I offer [service 1], [service 2], and [service 3]. For each service include a title, short description, ideal customer, and key benefit. Tone: [tone]."
7. **About Page** — "Write an About page for a [business/person/brand]. Include a short brand story, mission, values, and what makes this brand different. Tone: [friendly/professional/warm/confident]. Keep it simple and human."
8. **SEO Content** — "Write SEO-friendly website content for a [page type] about [topic/keyword]. Include a clear title, headings, short paragraphs, and natural keyword use. Target audience: [audience]. Keep it readable and avoid keyword stuffing."
9. **Website UX Audit** — "Review my website idea for a [business type] and suggest improvements to user experience. Focus on layout, navigation, clarity, calls to action, readability, and mobile usability. Explain suggestions in simple language."
10. **Code Improvement** — "Review and improve this website code. Fix errors, clean up the structure, make it responsive, improve accessibility, and explain what you changed. Keep the code easy for a beginner to edit."

## Downloads
- `downloads/assessment-worksheet.pdf`
- `downloads/discussion-guide.pdf`
- `downloads/educator-preview.pdf`
- `downloads/family-activity.pdf`
- `downloads/lesson-plans.pdf`
- `downloads/standards-chart.pdf`
