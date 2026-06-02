# CGB Cowork Hub

Centralized session-priming doc for "Clarence Gets a Bargain" work in this repo.
At the start of a session, tell Claude: **"read COWORK.md first."**

The goal of this file: cut down on re-exploration (which burns credits) and lock
in the facts/style rules that must never drift.

---

## 1. Repo Map (CGB-relevant)

### Main site
- `index.html` — single-file site + interactive 3D flipbook. CSS + JS inline. ~5000 lines.

### Supporting HTML pages
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

### Static
- `fonts/Hold.{woff2,woff,otf}` — brand font (NEVER fall back to Nunito as primary)
- `downloads/*.pdf` — assessment-worksheet, discussion-guide, educator-preview, family-activity, lesson-plans, standards-chart
- `images/`, `resources/`, `forsite/`, `characterposes&face/`

### Scripts (image / QR tooling, not site code)
- `image_dedupe_manager.py`, `image_prompt_search.py`, `streamlit_image_search_app.py`, `generate_qr.py`

---

## 2. Brand Invariants (Do Not Drift)

| Rule | Value |
|---|---|
| Brand font | **Hold** — everywhere |
| Headline color | `#0054a6` (blue) |
| Orange accents | `#ff6b2b`, `#F57C00` |
| Magazine cream bg | `#f5ecd7` |
| "Wants vs. Needs" | ALWAYS **bold and italic** |
| Author | Jonathan Bach |
| Maryann's credentials | **30+ years** K–5 (NOT 20+) |
| Standards | Jump$tart, Common Core Math, Common Core ELA, CEE — 4 frameworks |

---

## 3. `index.html` Quick-Jump (approx line numbers)

| Section | Line |
|---|---|
| `@font-face` Hold declaration | 35 |
| CSS styles | 34–352 |
| JSON-LD structured data | 353–465 |
| Nav bar (`#mainNav`) | 470 |
| Hero (`.hero`) | 472 |
| Stats row (Pages / Concepts / Frameworks / Laughs) | 671 |
| Coupon grid (`#coupons`) | 678 |
| Asset rows | 517–538 |
| Magazine flipbook (`#magazine`, `#magCanvas`) | 540 |
| Buy section (`#buy`) | 552 |
| Email signup | 566 |
| Trust block | 576 |
| Educators (`#educators`, `.anchor-quote`) | 597 |
| Standards grid | 612 |
| Resources / Program in a Box | 719 |
| Institutional / bulk | 764 |
| Pitch ("CFO's Desk") | 799 |
| Canvas helpers (`drawHeader`, `drawCard`, etc.) | 900–1130 |
| Magazine pages array | 1160–1500 |
| Cover texture / 3D flipbook renderer | 1500–2200 |

---

## 4. Common Tasks → Where to Touch

- **Stats row tweaks** → `index.html` ~line 671 (`.stats-row`)
- **New magazine page** → pages array starts ~line 1160; add canvas-drawn block
- **New download PDF** → drop into `downloads/`, link from Resources section (~line 719)
- **Educator endorsement text** → `#educators` (~line 597)
- **Standards alignment** → `.std-cell` grid ~line 1020
- **Site colors / fonts** → CSS block lines 34–352

---

## 5. Session-Saving Setup (one-time)

### a. Tighten permissions
Create `.claude/settings.json` to skip prompts on read-only commands:
```json
{
  "permissions": {
    "allow": [
      "Bash(grep:*)",
      "Bash(rg:*)",
      "Bash(ls:*)",
      "Bash(find:*)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git branch:*)"
    ]
  }
}
```
Or just run `/fewer-permission-prompts` after a few sessions — it scans your history and auto-suggests.

### b. Lock in CLAUDE.md
`CLAUDE.md` is auto-loaded every session — anything in it is "free context."
Keep brand invariants + file map there. Keep workflow/process here in COWORK.md.

### c. Claude Code on the web project
In the web UI, create a project pinned to `offmybach/characterpose` so every new
session inherits the same environment, env vars, and any SessionStart hook.
Docs: https://code.claude.com/docs/en/claude-code-on-the-web

### d. (Optional) SessionStart hook
If you ever add tests/linters, wire them via a SessionStart hook so they're
ready by the time Claude takes its first action. For a static HTML site this is
usually overkill — skip until you need it.

---

## 6. Phrasing That Saves Credits

Vague prompts trigger long exploration passes. Specific prompts go straight to the edit.

- 👎 "fix the stats row"
- 👍 "in index.html ~line 671, the stats row order should be Pages → Concepts → Frameworks → Laughs"

- 👎 "update Maryann"
- 👍 "in `#educators` (~line 597), make sure Maryann's bio says 30+ years"

- 👎 "add a download"
- 👍 "add `downloads/spring-activity.pdf` and link it from Resources (~line 719) next to family-activity"

---

## 7. What This Doc Is NOT

- Not a replacement for `CLAUDE.md` (which is auto-loaded). This is a session primer Claude only sees when you ask.
- Not a changelog. Use git for that.
- Not a style guide for the book itself — that lives in your editorial notes.
