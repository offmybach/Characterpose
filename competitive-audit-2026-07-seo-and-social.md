# Competitive Audit — July 2026: Google Rankings & Social Comments

Follow-up to `competitive-audit-kids-finlit-social.md` (June 2026). That one asked
*what are competitors posting.* This one asks *why are they beating us in search,
and is the social gap real.*

Short answer: the search gap is real and it has a specific, fixable cause. The
social gap is mostly imaginary.

**Method caveat up front:** search results here came through a search API, not a
logged-in Google session, and LinkedIn gates post bodies behind auth. Where a
number is verified, it says so. Where it's inferred, it says that too. The one
thing that would settle the search question in 30 seconds is Google Search
Console — see "Verify this yourself" at the bottom.

---

## Part 1 — Google

### The finding: this isn't a ranking problem

Ran the obvious searches. Here's what came back.

| Query | Does clarencegetsabargain.com appear? |
|---|---|
| `best children's books to teach kids about money 2026` | No |
| `children's picture book financial literacy ages 6-10 classroom` | No |
| `"Clarence Gets a Bargain" Jonathan Bach book` | **No** |
| `clarencegetsabargain.com` | **No** |
| `"Story First. Money Smarts Sneak In."` | **No** |
| `"9798234076380"` (the ISBN) | **No** |

Read those bottom four rows again. An exact-match search for the book's title
plus the author's name returns nothing. A search for the literal domain returns
the City of Clarence, Iowa. A quoted search for a tagline that exists on exactly
one page on the internet returns nothing.

You are not ranking #40 for "money books for kids." You are not in the index in
any way these searches can reach. Competitors aren't soaring above you. They're
the only ones in the pool.

That's the good news, weirdly. Ranking gaps take a year to close. Indexing gaps
take weeks.

### Why it's happening — four causes, in order of damage

**1. The book has no presence anywhere except your own website.**

This is the big one. Searched the ISBN — nothing. Searched Amazon — nothing.
Goodreads returns a different Jonathan Bach entirely.

Google ranks *entities*, not just pages. For a book, the entity gets built from
Amazon, Bowker/Books In Print, Goodreads, WorldCat/library catalogs, Bookshop.org,
and Google Books. You have an LCCN (2026906164) and an ISBN, which means the book
is real and registered — but if the ISBN doesn't resolve anywhere Google crawls,
Google has no reason to believe the book exists. Your `Book` JSON-LD is asserting
a thing that nothing else on the web corroborates.

Every competitor on every list I pulled has an Amazon detail page. That page is
what ranks, and it's what feeds every other mention.

**2. Name collisions are eating your brand searches.**

Two of them, both brutal:

- **"Jonathan Bach"** already belongs to Richard Bach's son, author of *Above the
  Clouds*, with 11 books on Goodreads and a personal site at jonathanbach.info.
  Google has had 30 years to decide who that name means. It isn't you.
- **"Clarence"** is a Cartoon Network series on Disney+ and Hulu, a 2023 A24 film
  (*The Book of Clarence*), and a town in Iowa.

You're fighting two established entities for your own name. This is why
title-plus-author searches fail: Google resolves both halves of the query to
somebody else. The fix isn't keywords, it's disambiguation — schema `sameAs`
links, an author entity tied to *this* book, and third-party listings that pair
the two names in a context Google trusts.

**3. The pages that actually rank for your keywords aren't authors — they're
affiliate roundups and institutions.**

This reframes the whole competitive set. Who owns page one:

- **Affiliate listicles** — michaelryanmoney.com, wealthywomanfinance.com,
  mommoneymap.com, moneyparents.com, thatssomontessori.com, myfirstnestegg.com,
  moneyprodigy.com. My First Nest Egg discloses Amazon Associates commissions
  outright and says its 12 picks were vetted by "a persnickety book critic – a
  six-year-old."
- **Institutional lists** — ABA Foundation, ALA/FINRA LibGuides, WeAreTeachers,
  Brightly (Penguin Random House), gohenry, Creative Teaching Press, Hills Bank,
  Tuttle Twins.

Sam Renick, Beth Kobliner, Tom Henske, Susan Beacham — none of their own sites
showed up in these SERPs either. They're not winning search. They're winning
*placement inside the pages that win search.*

The ABA Foundation list alone carries 25 titles. Kimberly Wilson has three slots
on it. The Berenstain Bears have three. Jasmine Paul's *A Boy, a Budget, and a
Dream* — the closest peer comp, flagged in the June audit — appears on both the
ABA list and the My First Nest Egg list. That's not a social-media win. That's
list placement.

**Your entire SEO strategy should be: get on those lists.** Not outrank them.
Get on them. They're mostly affiliate sites that need Amazon links to monetize —
which loops straight back to cause #1.

**4. Technical issues — real, but the smallest of the four.**

- `index.html` is **1 MB**, mostly from six resource pages inlined as iframe
  `srcdoc` attributes. That's a Core Web Vitals drag and it duplicates content
  that also lives at `resources/*.html` as standalone pages.
- **14 `<h1>` tags** on the homepage. Most come from those inlined modals, but a
  crawler doesn't know that. One page, one H1.
- The `keywords` meta tag has been ignored by Google since 2009. Harmless, but
  it's not doing anything.
- GA4 (`G-EC7YNHV890`) is installed; no `google-site-verification` meta tag found.
  You may be verified via DNS or the GA property — worth confirming.
- `robots.txt`, `sitemap.xml` (17 URLs), `llms.txt`, canonical tag, and the
  JSON-LD (Book, FAQPage, Review, Person, AlignmentObject) are all **correct**.
  Genuinely good schema work. It's just describing a book the rest of the web has
  never heard of.

Fixing all of #4 changes nothing if #1 stays broken.

---

## Part 2 — Facebook and LinkedIn

### The premise is mostly wrong. Nobody in this category gets comments.

You asked what they're posting that pulls the most comments. Verified numbers
from this round plus the June audit:

| Account | Post | Verified engagement |
|---|---|---|
| Sam X Renick (Sammy Rabbit) | "Share the early money lessons you learned" — his own 1960s memory, dad saying *"you can have anything you want if you're willing to work for it"* | **9 reactions, 1 comment** |
| Sam X Renick | "Dad Never Spoke to Me Again" (LinkedIn Pulse, deathbed story + Cambridge age-7 study) | **21 likes, 1 comment** |
| Greenlight (45,488 followers) | Level Up stats post — 4.3M games played, 6x more savings goals | **55 reactions, 1 comment** |
| Tom Henske, CFP (~3K followers) | "Everything Your Child Should Know About Money" | **22 comments** ← the outlier |
| CEE (16,968 followers) | partnership / Survey of the States posts | single digits |

Sam Renick is the dean of this beat — 20+ years, 250,000 kids, posts nearly
daily. His best-performing emotional post in a decade got **one comment.**
Greenlight has 45,000 followers and got **one comment.**

Nobody is soaring past you on social. The category is a graveyard. What's beating
you on Facebook and LinkedIn is not a competitor's post — it's the fact that you
don't have a book listing for anyone to link to when they do want to share it.

### The one real outlier, and what it teaches

Tom Henske: **22 comments on a ~3,000-follower account.** That's a 40x better
comment-per-follower rate than Greenlight. The post: *"Everything Your Child
Should Know About Money."*

Why it worked, against a field of posts that didn't:

- **"Everything" is an arrogant promise.** It's a little bit stupid and that's the
  point. Every other post in the category hedges.
- **It's a checklist.** Parents can audit themselves against it in real time, and
  the natural comment is "we do 6 of these" or "wait, what about X?"
- **It leaves room to argue.** A stats brag leaves nothing to say. A list of what
  your kid *should* know invites every parent to add the one you missed.

Cross-reference the flatlines and the pattern is clean: **posts pull comments when
they hand the reader an unfinished sentence.** Renick's money-memory prompt has
the right shape but he buries the ask under his own story. Greenlight's post has
no ask at all. Henske's has a list you can fight with.

### Where Facebook actually matters here

Direct Facebook comment data on author pages wasn't verifiable — Meta gates it and
the roundup-site research turned up nothing. But the marketing research surfaced
the relevant 2026 shift: children's book authors are getting traction through
**micro-influencers — kidlit accounts, teacher accounts, librarian recommendation
accounts** — not through their own pages. Small, hyper-engaged audiences.

The Facebook play isn't your page. It's teacher groups. A veteran K–5 educator
(Maryann, 30+ years) posting "here's what happened when I read this to my class"
in a 40,000-member elementary teachers group will outperform anything on an author
page by an order of magnitude. That's a real asset you're not using.

---

## What to do, ranked by return

**1. Get the book listed where Google looks.** Amazon first — it's the single
highest-leverage action available and it unblocks everything below it. Then
Goodreads, Bookshop.org, Google Books, and confirm the Bowker/Books In Print
record is live so the ISBN resolves. Nothing else on this list works until the
ISBN returns something.

**2. Pitch the roundup lists.** They're the actual page-one competition and most
of them are affiliate-funded, so they want new titles with buyable links. Start
with the institutional ones (ABA Foundation, ALA/FINRA LibGuides, WeAreTeachers,
Brightly) because they carry the most authority and don't need affiliate
economics — then work the affiliate blogs. Your angle writes itself and no one
else on those lists has it: **every book on the ABA list teaches earning and
saving. Yours is the only one that teaches spending** — the whole transaction,
through the register, including sales tax.

**3. Fix the name collision.** Add `sameAs` to the Person schema pointing at your
real author profiles. Where possible, publish as a distinct byline. Make every
third-party listing pair "Jonathan Bach" with "Clarence Gets a Bargain" so Google
gets enough co-occurrence to build a separate entity.

**4. Split the 1 MB homepage.** Load the six resource modals by iframe `src`
instead of inlined `srcdoc`. Cuts page weight hard, kills the duplicate content,
and collapses 14 H1s down to one.

**5. On social, write the Henske post.** Not the stats post, not the FinLit Month
post. The arrogant checklist with a hole in it. Two you already own:
*"Everything a 4th grader should know before they walk into a store"* and
*"Nine things Clarence's mom did that your mom probably did too"* — the receipt
photo, the grocery-price game, Guess the Price at dinner. End on an open question
and let parents finish it.

**6. Point Maryann at teacher Facebook groups.** One classroom read-aloud story
from a 30-year veteran beats fifty author-page posts.

---

## Verify this yourself

The API-based searches behind this report are strong evidence but not proof.
Settle it in five minutes:

1. Google `site:clarencegetsabargain.com` while logged in. Zero results confirms
   the diagnosis outright.
2. Google Search Console → **Pages** report. It will name the exact reason
   (Discovered–not indexed, Crawled–not indexed, noindex, etc.).
3. Search Console → **URL Inspection** on the homepage → Request Indexing.
4. Search Console → **Sitemaps** — confirm `sitemap.xml` was submitted and read.

If Search Console shows the site indexed and I've read this wrong, the story
changes from "invisible" to "ranking poorly," and the fix list reorders — but
items 1 and 2 stay at the top either way.
