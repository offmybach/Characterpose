# Project: Clarence Gets a Bargain (CGB)

Single-page children's book website + interactive 3D magazine flipbook for a
financial-literacy picture book aimed at ages 6–10, grades 1–5.

This file is auto-loaded every session. It is the single source of truth for
mission, voice, invariants, and code map. Keep it tight; don't bloat it.

---

## 1. Mission

> **We snuck a financial education inside a story about a kid and a robot.**

CGB is a 36-page narrative picture book that teaches 16+ financial concepts
without ever feeling like a textbook. Clarence earns a robot reward for good
grades and chores, then learns budgeting, comparison shopping, markdowns, and
coupons on a trip to Sea-Mart. Story first. Money smarts sneak in.

**What success looks like:** kids read it for the story and *absorb* the
concepts because the plot demands it — not because a worksheet told them to.

**Positioning lines we own:**
- "A money book kids actually read."
- "Story first. Money smarts sneak in."
- "Edutainment at its finest."
- "Kid lit is a hit! Kid fin is a win!"

---

## 2. Voice & Tone

The CGB voice is **Jonathan Bach's voice** — attorney + artist + dad. It is:

- **Punchy and declarative.** Short sentences. Periods are weapons.
  - "Clarence Did It. Your Kids Can Too."
  - "Page 22. Aisle Five."
- **Self-aware and winking.** Headlines flirt with the reader.
  - "Shopping Homework? Yes, Really."
  - "They Didn't Expect to Love a Money Book."
- **Retail/coupon metaphors everywhere.** It's the book's whole conceit.
  - "BOGO: Buy the Story, Get the Lessons FREE!"
  - "100% OFF Boring Textbooks!"
  - "5-STAR VALUE!"
- **Anti-textbook, pro-narrative.** Frame everything against worksheets.
  - "Built alongside the book, not bolted on after."
  - "Every concept is woven into the plot."
- **Confident, no fluff.** Triplets and parallel structure.
  - "All six tools. All free. All yours."
  - "36 pages of adventure. 16+ concepts. One very determined kid with a robot obsession."
- **Direct-address parental.** Speaks to the buying adult about the kid.
  - "Your kids will too."

**When writing new copy, ask: would Jonathan say it this way?** If it sounds
like AI marketing slop ("unlock", "empower", "leverage", "in today's world"),
rewrite it.

<!-- TODO: paste Jonathan's "never-say" list here (phrases/tones to reject) -->

---

## 3. Audience

| Audience | What they want |
|---|---|
| **Parents (ages 6–10)** | A book their kid will actually finish that teaches money skills |
| **K–5 Educators** | Standards-aligned narrative tool with zero-prep lesson plans |
| **Librarians** | Classroom-ready picture book with credible endorsements |
| **Institutional buyers** (districts, credit unions, financial-literacy programs) | PO-friendly, Title I pricing, grant-report-ready data |

---

## 4. Brand Invariants — DO NOT DRIFT

### People
- **Author**: Jonathan Bach — attorney, mixed-media artist, children's book author
- **Maryann Milewski Moskal**: Veteran Elementary School Educator, **30+ years** K–5 classroom experience (NOT 20+)

### Typography
- **Hold** is the brand font. Use it everywhere. NEVER fall back to Nunito as primary.
- Font files: `fonts/Hold.woff2`, `fonts/Hold.woff`, `fonts/Hold.otf`
- `@font-face` declared at `index.html` line ~35

### Color
- Headline blue: `#0054a6` (NOT dark navy — needs contrast against `#111` body)
- Orange accents: `#ff6b2b`, `#F57C00`
- Cream magazine bg: `#f5ecd7`
- All magazine cards use dashed coupon-style borders

### Copy invariants
- **"Wants vs. Needs"** must ALWAYS be **bold and italic** — core FLAC concept
- Standards: **Jump$tart, Common Core Math, Common Core ELA, CEE** (4 frameworks)
- Page count: **36 pages**
- Concepts taught: **16+**
- Ages: **6–10**, Grades **1–5**

---

## 5. Story Beats (for marketing copy alignment)

1. Clarence earns a robot reward for good grades and chores
2. He gets "shopping homework" — learns to compare prices, read ads, find real value
3. Trip to Sea-Mart: Aisle Five, Page 22 is the pivotal moment
4. He finds a marked-down RoBimmie, compares it with newer models
5. Two small differences (smaller screen, antenna). One much smarter choice.
6. Payoff: newer doesn't always mean better

**The Big Six concepts** (plus more):
1. ***Wants vs. Needs*** (bold + italic, always)
2. Budgeting & Goal Setting
3. Comparison Shopping
4. Coupons & Markdowns
5. College Savings (529)
6. Consumer Awareness

<!-- TODO: paste full 36-page book text here so Claude can quote/reference it accurately -->

---

## 6. Code Map — `index.html` (the main site, ~5000 lines, all inline)

| Section | Line |
|---|---|
| `@font-face` Hold declaration | ~35 |
| CSS styles | 34–352 |
| JSON-LD structured data | 353–465 |
| Nav bar (`#mainNav`) | 644 |
| Hero (`.hero`) + masthead | 648–656 |
| Banner ticker | 669 |
| Stats row (Pages / Concepts / Frameworks / Laughs) | 671 |
| Coupon nav grid (`#coupons`) | 678 |
| Asset rows (Shopping Homework, Smart Discovery, Coupon Twist) | 700–720 |
| Front & Back Cover | 737 |
| Magazine flipbook (`#magazine`, `#magCanvas`) | 752 |
| Moment headline ("Page 22. Aisle Five.") | 768 |
| Buy section (`#buy`) | 785 |
| Reviews ("They Didn't Expect to Love a Money Book") | 826 |
| User review submission | 851 |
| Email signup | 890 |
| Educators block (`#educators`, `.anchor-quote`) | 906 |
| Concepts section ("The Big Six. Plus Many More.") | 928 |
| Standards alignment grid | 1015 |
| Book specs / cataloging | 1095 |
| Resources / "Program in a Box" | 1122 |
| Institutional / bulk ordering | 1167 |
| Pitch section ("CFO's Desk") | ~799 / `.pitch-section` |
| Canvas helpers (`drawHeader`, `drawCard`, `drawReview`, `wrapText`) | 900–1130 |
| Magazine pages array (10 canvas-drawn pages) | 1160–1500 |
| 3D flipbook renderer / cover texture | 1500–2200 |

### Magazine page index (canvas-drawn, not story text)
- Page 0 — Inside front cover (dedication/welcome)
- Page 1 — "Here's The Deal" (hook)
- Page 5 — "Money Skills" (6 concept cards, 2x3 grid)
- Page 6 — Reviews (3 review coupon cards)
- Page 7 — "Inside the Story" (key scenes)
- Page 8 — "What Kids Learn" (skills at a glance)
- Page 9 — FAQ

---

## 7. Supporting HTML Pages

- `educator-toolkit.html` — teacher resources hub
- `quiz.html` — interactive concept quiz
- `wants-vs-needs.html` — FLAC module
- `review-cards.html` — printable review/testimonial cards
- `badge-generator.html` — endorsement badges
- `post-writer.html` — content drafting helper
- `social-assets.html` — social graphic kit
- `linkedin-carousel.html` — LinkedIn carousel posts
- `linkedin-profile-assets.html` — LinkedIn profile assets
- `instagram-stories.html` — Instagram stories
- `social-media-campaigns-april.html` — April campaign

## Downloads
- `downloads/assessment-worksheet.pdf`
- `downloads/discussion-guide.pdf`
- `downloads/educator-preview.pdf`
- `downloads/family-activity.pdf`
- `downloads/lesson-plans.pdf`
- `downloads/standards-chart.pdf`

## Python utilities (not site code)
- `image_dedupe_manager.py`, `image_prompt_search.py`, `streamlit_image_search_app.py`, `generate_qr.py`

---

## 8. Common Tasks → Where to Touch

- **Stats row tweaks** → `index.html` ~line 671 (`.stats-row`)
- **New magazine page** → pages array ~line 1160; add canvas-drawn block
- **New download PDF** → drop in `downloads/`, link from Resources (~line 1122)
- **Maryann's credentials** → `#educators` (~line 906) — 30+ years, not 20+
- **Standards alignment** → `.std-cell` grid ~line 1020
- **Site colors / fonts** → CSS block lines 34–352
- **Voice/copy edits** → defer to §2 above; mirror Jonathan's punchy/coupon tone

---

## 9. Phrasing That Saves Credits

Specific prompts skip exploration. Vague prompts burn tokens.

| 👎 Vague | 👍 Specific |
|---|---|
| "fix the stats row" | "in index.html ~line 671, reorder stats to Pages → Concepts → Frameworks → Laughs" |
| "update Maryann" | "in `#educators` ~line 906, make sure Maryann's bio says 30+ years" |
| "add a download" | "add `downloads/spring-activity.pdf` and link from Resources ~line 1122 next to family-activity" |
| "write some copy" | "write a 2-line hook for the Buy section that mirrors the 'Page 22. Aisle Five.' cadence" |

---

## 10. Alex AI Update — 10 Website Prompts (Reference)

Template prompts for website planning/design. Placeholders shown as `[brackets]`.

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
