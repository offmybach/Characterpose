# HANDOFF — CGB outreach, session of 30 July – 3 August 2026

Read this before doing anything. It replaces scrolling a long chat.
`CLAUDE.md` is still the source of truth for voice and brand invariants; this file covers
**state, decisions, and open work.**

Branch: **main.** Everything is merged and pushed. 27 commits this session.

---

## 1. What this session actually was

Mostly **recovery, not creation.** Almost every strong line found was already Jonathan's,
written weeks earlier and invisible.

**The discovery that mattered:** the losses were never in edits or deletions. They were in
**work committed to branches that never merged.** A sweep of 36 remote branches against main
found **28 content files that existed nowhere else**, including six finished site pages and a
complete dated campaign.

> **The query that found it:** `git ls-tree -r --name-only <branch>` for every branch,
> diffed against `HEAD`. Re-run it periodically. `git log --diff-filter=D` only finds
> deletions and will miss this entirely.

Recovered and now live on main:
- `marketing-blitz.html` — two-front campaign, 22 dated posts, competitor recon, 5 outreach
  templates, the shirt spec with a trackable QR. **Robots-blocked, internal.**
- `vs-other-money-books.html` — the gracious comparison page other assets funnel into
- `school-visits.html` — "The Clearance Aisle Assembly", the only visit offer that exists
- `money-glossary.html`, `teaching-kids-about-money.html` — SEO landing pages
- `resources/free-sample-print.html` — first five pages, no email wall
- Six `research/` pitch letters, `disruptive-campaigns.md`, `seo-aeo-audit-and-plan.md`,
  `roundup-outreach-emails.md`

---

## 2. Current state — the numbers

| | |
|---|---|
| Letters, all files | **749** |
| Carrying the em-dash P.S. | **713** (36 held deadpan) |
| Em dashes | **1,878** — kept, by ruling |
| AI-ism hits, full 130-term + 9-pattern audit | **1**, kept on purpose |
| Workbook | `CGB_MASTER_outreach.xlsx`, **671 rows, 82 whales** |
| Review guard | `scripts/check_reviews.py` — 20/20 |

### Letter files
| File | Letters | What it is |
|---|---|---|
| `letters-1-198.md` / `199-396` / `397-516` / `517-616` | 620 | the short batch, ~730 chars median |
| `letters-whales-longform.md` | 43 | **rewritten this session**, 1,600–2,100 chars |
| `letters-top25-week1.md` | 25 | bespoke |
| `letters-delaware.md` | 18 | 3 carry the claw machine |
| `letters-grandparents-readalong.md` | 8 | incl. 3b, the GU follow-up |
| `letters-maesp-naesp.md` | 9 | Maryland elementary principals |
| `letters-new-july.md` / `-28-29` | 12 | |
| `jumpstart-clearinghouse-strategy.md` | 7 | |
| `letter-erikk-bonner.md` | 2 | **NEW — MSDE, message 1 + held message 2** |
| `letter-mia-russell.md`, `letter-edoho-eket.md`, `letters-cfpb-consumer-rights.md` | 5 | |

### Reference files that settle arguments
- **`reference/heavy-hitters.md`** — the short shelf. Six tiers of the lines that make the
  book sing. **Take from here before inventing anything.**
- `reference/phrasebank.md` — the full pantry, three harvest rounds, ~130 lines
- `reference/deal-master-facts.md` — **wins over any copy** on the shoes / cruise ship
- `reference/reviews-of-record.md`, `reference/pereira-review.md` — verbatim reviewer quotes

---

## 3. Decisions made this session — do not relitigate

**Em dashes are settled.** Jonathan: *"I support em dashes. They are a middle finger taking a
nap to me."* A pass thinned them; it was reverted. `CLAUDE.md` now carries the ruling.
**No future audit flags, counts or reduces em dashes.**

**The claw machine is $25 and $9.99.** Into the machine: $25. Prize: a basketball. Walmart
price: $9.99. A recalled "dollar a try, sixteen tries, $10 toy" version was **a guess and is
retired.** Do not blend them. No percentage — the raw pair does the work.

**The shoes and the cruise ship are two stories.** Nordstrom Rack: shoes compare-at **$293**,
shirt **$69.50**, both paid at **one cent**, both tags kept, both stickers say "99% Savings",
a penny off $293 is 99.997%. The cruise ship is a **website price match — no penny, no dollar
figure on record.** **"Negotiated" is a banned verb.**

**The shirt has not been worn in public.** Copy says "had printed." Never "have been wearing."

**The read-along is a fact, not a claim.** Lexile **AD 620L** = **Adult Directed**, the trade's
own code for read-*with*. It is in all 749 letters.

**The five pillars are in every letter:** spending-first · smuggled · glossary · read-along ·
idea-to-post-receipt. Verified per letter, not in aggregate.

**Two deliberate exceptions, recorded in the files so nobody "fixes" them:**
1. Morgenson states spending-first in her own better words, not the stock phrasing.
2. The Generations United letter stays a **donation** of two free games, not a pitch.

---

## 4. What is open — the actual to-do

### ✅ Resolved 3 Aug — the origin story
The grocery-cart draft is **retired**. The real memory is the **sleepaway-camp canteen
account**: one deposit for a four-week session, Blow Pops and Fun Dip every visit while
bunkmates bought one or two things, account empty halfway through week three, last week and
a half spent watching other kids buy candy. Full text and three registers in
`reference/heavy-hitters.md`.

⚠️ **The dollar amount is still not on record** — he wrote "x dollars." Never invent one.
The ratio carries the story without it.

### 📮 Already sent — promises now owed
All six grandparent letters went out. Checked against every invariant: **zero defects.**
Four promises were made in them:

| To | Promised | Status |
|---|---|---|
| **DeeDee Moore** (More Than Grand) | "I'll mail you a hardback this week" | **mail it** |
| **Generations United** | a free printable | ✅ **built** — send letter **3b** |
| **Ron Lieber** (NYT) | a copy if useful | wait for reply |
| **Greg** (Cool Grandpa) | a copy either way | **send it** |

**Letter 3b** is the GU follow-up. It is a *delivery*, not a nudge — the printable now exists
at `resources/grandparents-day-games-print.html`. Send 2–4 days after the first.

### 🔴 Send next
1. **Dr. Erikk D. Bonner** — Assistant State Superintendent, MSDE. He opened with a
   thank-you-for-connecting note. Message ready in `letter-erikk-bonner.md`. **The hook is
   Maryland-specific and verified:** the State Board's 2010 regulations already require
   financial-literacy instruction at **elementary**, middle and high school; HB 943 adds the
   graduation course effective 1 Jul 2026 for the class of 2030. So the state just put a
   course, a credit and a reporting line on the high school end of a requirement whose
   elementary end has sat there sixteen years. **Say "as I read it"** — he would know.
2. **The 43 rewritten whales**, by the day-order at the end of `letters-whales-longform.md`.
3. **Librarians — August is order season.** Boglarski (Boston PL), Wright (NYPL).

### 🗓 Dated
- **National Grandparents Day: Sunday 13 September 2026.**
- `marketing-blitz.html` front two ran 3 Aug – 11 Sep. **Check whether that window is still
  live before using those dated posts.**

---

## 5. Mistakes made this session — so they do not repeat

**A bulk edit is where errors hide.** A read-along variant rolled out to 658 letters opened
*"One spec that matters in a classroom"* — and "that matters" is on the May 8 sewage list. It
injected a kill-list phrase into **251 letters in one pass**, and the careful audit that
followed covered only the 74 hand-written letters. **Audit a rollout as part of the rollout.**

**Do not ship refinements to letters already sent.** Several passes polished copy that was
already in somebody's inbox. It makes finished work feel unfinished and helps nobody.

**Rebuild the zip after the last commit, not before.** A package was built at 14:42 and two
subject lines were added at 14:44 and 14:47; the user read the stale copy and reasonably
concluded the work was missing.

**Regexes that span sections lie.** A header pattern swallowed a section heading and wrongly
held five letters out of a rollout. Split on headers first, then test each block.

**Gmail rewrites.** A polish tool silently smoothed a sent letter — "hand them over" became
"share them", em dashes closed up. **Paste as plain text (Ctrl/Cmd+Shift+V) and decline every
"help me write" suggestion.**

---

## 6. The honest assessment, unchanged

The top 25, the 43 whales and the 6 grandparent letters are genuinely good: one concrete
image each, argued in the recipient's own terms.

**The 620 short letters are still 97% argument and 2% image.** They carry all five pillars,
the P.S., and clean voice — but they make the case rather than showing a scene. That is the
next real quality step if anyone wants one, and it is a rewrite, not a pass.

**Snark sits at ~76% of the whales** and is aimed at the category's blind spot, worksheets and
retail tricks — **never at the other authors**, who stay treated as good books doing a
different job. That distinction is load-bearing; `vs-other-money-books.html` depends on it.
