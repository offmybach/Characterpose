# CGB Visibility Audit + Plan of Attack — SEO / AEO / GEO

Compiled July 2026. Companion to `competitive-audit-kids-finlit-social.md` (which covers
social). This one covers the two engines that decide whether a parent, teacher, or
librarian ever *finds* the book: **classic search (Google) and answer engines
(ChatGPT, Perplexity, Gemini, Google AI Overviews, Claude).**

The social audit answered "how do we get comments?" This one answers "how do we get
found when nobody typed our name?"

---

## The one-paragraph verdict

The site is already best-in-category on *technical* SEO/AEO — full `Book`, `FAQPage`,
and `Review` schema, an llms.txt, a book-facts page, clean OG/Twitter cards, a sitemap.
That's the moat. The problem is the bridge. Every keyword that matters
("money books for kids," "financial literacy picture book," "teach kids about money")
is owned by **roundup listicles** — "29 Money Books for Kids," the ALA LibGuide, US
News' "10 Best," Brightly, mommoneymap, "35 Financial Literacy Books." Those same lists
are what ChatGPT and Perplexity read back when a parent asks for a recommendation.
**Clarence is in none of them.** We built a beautiful store on a street with no signs
pointing to it. The whole plan below is about the signs.

---

## Part 1 — The SEO battlefield (who actually ranks)

### What owns the money keywords right now

Search any core term and the first page is not books. It's *lists of books*:

| Ranking page | For queries like | Clarence listed? |
|---|---|---|
| moneyprodigy.com "29 Money Books for Kids (by Age)" | best money books for kids | No |
| ALA `libguides.ala.org` FINRA finlit-children | library financial literacy kids | No |
| US News "10 Best Money Books for Kids" | best money books for kids | No |
| readbrightly.com "Books to Help Teach Kids About Money" | picture books teach money | No |
| mommoneymap "Best Money Books... 2026" | money books for kids 2026 | No |
| thatssomontessori "35 Financial Literacy Books" | financial literacy books kids | No |
| Amazon "Best Sellers: Children's Money Books" | (Amazon's own engine) | No |
| Programming Librarian "7 Picture Books... Money" | financial literacy month picture books | No |

**The takeaway is not "we rank badly." It's "we don't play."** Ranking your own domain
above moneyprodigy for "best money books for kids" is a five-year fight nobody wins. Getting
*added to* moneyprodigy's list is a five-email fight. Same visibility, 1% of the effort.

### The one direct keyword competitor worth contesting

**The Comparison Shopping Cow** (Charlotte Dane, "It's My Money!" series) owns the exact
long-tail we should own: *"comparison shopping for kids."* It's a thin, POD-style book.
Clarence beats it on every axis — real plot, real character, a full transaction, standards
alignment, a named veteran-educator endorsement. We are not losing that keyword on merit.
We're losing it because the Cow published a book literally titled the search query and we
never wrote the page that says "here's the story version, and here's why a story beats a
lesson." That page is a layup.

### Where Clarence can actually win on merit (the moat keywords)

Every competitor teaches **earning and saving** — piggy banks (Money Savvy Pig), lemonade
stands (Ruby/Max, Bunny Money), chores-and-matching (Rock Brock), money-as-a-seed (Meko).
**Nobody owns spending.** These queries have real intent and near-zero strong competition:

- "kids book about **spending** money" / "how to teach kids to spend wisely"
- "teach kids about **clearance** / **markdowns**"
- "teach kids about **sales tax**" (parents genuinely search this; almost no picture-book result)
- "**comparison shopping** for kids" (contest the Cow)
- "what to do at the **register** / checkout — teach kids"
- "money book that teaches the whole **purchase**, not just saving"

**Positioning line to own, verbatim, everywhere:** *the money book that teaches spending —
the complete purchase, all the way to the register.* It's already in llms.txt. It needs to
be a headline, a page title, an H1, and a blog post — not a buried sentence.

---

## Part 2 — The AEO / GEO battlefield (what the robots say)

### How the answer engines actually pick a book

From current (2026) citation research:

- **ChatGPT** pulls ~48% of citations from **Wikipedia**, plus Reddit.
- **Perplexity** pulls ~47% from **Reddit-style community threads**.
- **Gemini / Google AI Overviews** lean on the **Google index, YouTube, and Reddit**.
- **Claude** rewards **long-form editorial from named authors**.

Read that again. When a parent asks any assistant "what's a good money book for a 7-year-old,"
the answer is assembled from **Wikipedia, Reddit, YouTube, and the same roundup listicles** —
almost none of which live on our domain. On-page schema gets us *quoted accurately once we're
already named.* It does not get us named. **AEO is mostly an off-site game, and we've been
playing it entirely on-site.**

### What we already do right (keep doing)

- Front-loaded, extractable answers (the FAQ block, book-facts) — exactly what engines lift.
- `FAQPage` schema with real Q&A — quotable, structured, done.
- llms.txt with hard facts (ISBN, LCCN, Lexile, standards, price) — few competitors have this.
- Specific, checkable numbers (36 pages, 21 glossary terms, $19.99) — engines trust specifics
  over adjectives. "Comprehensive resource" gets ignored; "36 pages, 16+ concepts, $19.99" gets cited.

### The AEO gaps

1. **No Wikipedia footprint.** ChatGPT's single biggest source. Neither the book, the author,
   nor even a mention on an existing finlit page exists. (A standalone article for a new book
   likely fails notability — but a *sentence* on relevant existing pages, cited to press, is fair game.)
2. **No Reddit presence.** Perplexity's #1 source. Zero threads mention Clarence in r/Teachers,
   r/homeschool, r/personalfinance, r/predaddit, r/Money, r/ecr_eal (parents ask this constantly).
3. **No YouTube.** Gemini/Overviews lean on it. No read-aloud, no "Page 22" clip, no author 60-second explainer.
4. **Not in any roundup.** The listicles ARE the AEO training data. Not being in them is the whole problem.
5. **Comparison content missing.** Engines love "X vs Y" tables. We have no page that says
   "Clarence Gets a Bargain vs. the other money books" — the exact structure an engine extracts for a rec.

---

## Part 3 — Technical SEO fixes (do these first; they're cheap and they compound)

**P0 — the canonical/host mismatch (real defect).**
`CNAME` = `clarencegetsabargain.com` (apex), but every `<link rel=canonical>`, `og:url`, sitemap
entry, and llms.txt URL uses `www.`. GitHub Pages 301-redirects one host to the other based on
the CNAME, so **every canonical currently points at a URL that redirects.** Pick one host and make
everything agree. Simplest fix: change `CNAME` to `www.clarencegetsabargain.com` so the apex
redirects to www and all existing canonicals become correct. (One-line change, re-verify domain in
GitHub Pages settings.) Alternative: rewrite all canonicals/OG/sitemap to apex. Either works; the
mismatch does not.

**P1 — schema depth.**
- Add `AggregateRating` to the Book schema (you have three `Review`s; engines surface star ratings
  in results when an aggregate exists).
- Add `BreadcrumbList` schema to resource pages.
- Add `HowTo` schema to the receipt-builder and quiz (interactive = extractable).
- Add `Organization` / `publisher` sameAs links pointing to every social profile and Amazon.

**P2 — indexation coverage.**
- Sitemap lists 18 URLs but omits several indexable standalone pages (`the-money-talk.html`,
  `smart-shopper-challenge.html`, `sea-mart-secret-mission.html`, `zero-prep-lesson-plans.html`).
  Add them.
- Confirm the OG image (`images/clarence-og-card.jpg`) actually exists and is 1200x630. A broken
  OG card kills social/AI link previews.

**P3 — content architecture for extraction.**
- Every new content page: front-load a 2-3 sentence direct answer under the H1 before any prose.
- Use question-shaped H2s ("Is this good for reluctant readers?") — the literal phrasing parents type.

---

## Part 4 — The Plan of Attack (the "audit pack")

Framed like a skills pack: numbered plays, grouped by engine, most-leverage first.
Each is a discrete unit of work, not a vague direction.

### SEARCH — classic SEO (own the moat keywords)

1. **`/spending` money page** — build the page that owns "kids book about spending money."
   Direct-answer H1, the earning-vs-spending contrast table, the whole-transaction argument.
2. **`/comparison-shopping-for-kids` page** — contest the Comparison Shopping Cow head-on.
   Story-vs-lesson framing, Aisle Five teased (never the wordplay), CTA to buy + free quiz.
3. **`/sales-tax-for-kids` + `/clearance-and-markdowns-for-kids`** — two near-uncontested queries,
   two thin books' worth of demand, one page each, both pointing at Page 22.
4. **Amazon listing optimization** — treat Amazon as its own search engine: title keywords,
   backend search terms, A+ content, first-image with the standards badges. Amazon's bestseller
   list is a ranking factor for every other list.
5. **Blog cadence** — one extraction-shaped post/week on a real parent query
   ("how do I explain sales tax to a 7-year-old"), each ending in the book as the answer.

### ANSWER ENGINES — AEO / GEO (get named, not just quoted)

6. **The "vs the other money books" comparison page** — the single highest-leverage AEO asset.
   A real table: Clarence vs. Money Savvy Pig vs. Rock/Brock vs. Comparison Shopping Cow, across
   earning/saving/**spending**/standards/story. Engines extract comparison tables verbatim.
7. **Reddit seeding (honest, disclosed)** — answer real questions in r/Teachers, r/homeschool,
   r/personalfinance, r/Mommit where "money book recommendation" threads already exist. Perplexity's
   #1 source. Author transparency: say it's your book. One genuine answer beats ten drops.
8. **YouTube: three assets** — (a) a 60-second "Page 22. Aisle Five." author explainer,
   (b) a full read-aloud for teachers, (c) a "how to teach clearance to a kid" clip. Gemini/Overviews
   pull from YT transcripts; caption everything.
9. **Wikipedia-adjacent footprint** — don't force a book article (notability risk). Instead add a
   sourced sentence to existing pages (financial-literacy-education, list-of-financial-literacy-books
   if one exists) once press coverage exists to cite. Press first, edit second.
10. **Keep the llms.txt + book-facts current** — they're working; add the comparison data and the
    new landing pages to llms.txt so the engines have the full map.

### AUTHORITY — off-site (the actual "EI-EI-O": get into everybody's list)

11. **Roundup outreach** — the campaign that matters most. Email every listicle owner
    (moneyprodigy, mommoneymap, readbrightly, thatssomontessori, Programming Librarian, the ALA
    FINRA guide contact) with a one-paragraph pitch + free educator toolkit link + review copy offer.
    The angle they can't resist: *"every book on your list teaches saving; here's the one that
    teaches spending."* Being added to eight lists = ranking + AEO in one move.
12. **Credibility-stamp stacking** (borrowed from the social audit's Jasmine Paul note) —
    Parents Magazine best-books, ALA FINRA-Foundation diverse-reads, EIFLE (you have the Luckeydoo
    connection), Mom's Choice. Each stamp is a citation source engines and listicles trust.

---

## Part 5 — Sequencing (what to do in what order)

**Week 1 — technical, no dependencies.** Fix the CNAME/canonical mismatch. Add AggregateRating +
missing sitemap URLs. Verify the OG image. These are pure upside and unblock everything downstream.

**Weeks 2-3 — the moat pages.** Ship the `/spending`, `/comparison-shopping-for-kids`, and the
`vs-the-other-money-books` comparison page. Update llms.txt and sitemap to include them. This is the
content the roundups and engines will point at, so it has to exist before outreach.

**Weeks 3-6 — the outreach engine.** Roundup pitches (play 11) and credibility stamps (play 12) run
in parallel and take weeks to land, so start early. Reddit and YouTube seed continuously.

**Ongoing — the cadence.** One extraction-shaped blog post/week, one Reddit answer/week, one YouTube
clip/month. Compounding, not campaign.

---

## The single sentence to take away

We spent a year building a technically flawless site nobody is pointed to. The next move is not
more schema. It's twelve emails to the people who write the lists, three pages that own the word
"spending," and one comparison table the robots can copy. **Get in the lists. Own the moat. Let the
engines quote the page we already built.**
