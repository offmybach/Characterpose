# Competitive Audit — July 2026: Google Rankings & Social Comments

Follow-up to `competitive-audit-kids-finlit-social.md` (June 2026). That one asked
*what are competitors posting.* This one asks *why are they beating us in search,
and is the social gap real.*

Short answer: you rank fine for your own name and can't rank at all for the
category — because the category SERP doesn't serve book sites. The social gap is
mostly imaginary.

**Correction, and a hard method caveat.** The first version of this document
concluded the site was not in Google's index. That was wrong, and it was wrong
because of my tooling. The search API available to me returns results that do not
match real Google for this domain — it fails to surface clarencegetsabargain.com
even for the literal domain name, and for `clarence bach money book` it returns
David Bach's catalog and never the site. Real Google, logged in, returns
clarencegetsabargain.com as the **#1 organic result** for that same query, with
title and meta description rendering correctly.

So: **nothing in this report about where the site does or doesn't rank can be
sourced to my searches.** Anything ranking-related below is either from the
user's own screenshot or flagged as needing confirmation. Findings about *other*
sites (which pages own the category SERPs, what's on the ABA list) and the
LinkedIn engagement numbers came from directly fetching those pages and are
unaffected.

---

## Part 1 — Google

### What the SERP actually shows

From a real logged-in Google search for `clarence bach money book`:

- **clarencegetsabargain.com ranks #1.** Indexed, crawled, title and meta
  description rendering as written. Branded search works.
- **One blue link. No sitelinks.** For a #1 branded result, Google will often
  expand into sitelinks (Educator Toolkit, Book Facts, Buy). It didn't.
- **No Book rich result, no knowledge panel** — despite valid `Book` JSON-LD with
  Offer, Review, and Rating on the page.
- **"People also ask" served: *"What is the best finance book of all time?"* and
  *"What is the best book to read to become rich?"***

That last one is the tell, and it's the most useful thing in the screenshot.

Those are **adult personal-finance questions.** Google generated them from its
read of the query and the result. Nothing about "children's book," "ages 6–10,"
"read-aloud," "classroom," or "picture book." Google has the site indexed but has
not confidently classified it as *children's literature / K–5 education*. It's
filing you somewhere near the adult money-book shelf — the David Bach shelf.

That's a topical-authority problem, not an indexing problem. And it's consistent
with the one thing I could verify independently: the sites that own the category
queries are not books at all.

### Why competitors are above you on category searches

**1. The category SERP doesn't rank book sites. It ranks lists.**

This is the finding that survives intact, and it reframes everything.

For `best children's books to teach kids about money 2026` and
`children's picture book financial literacy ages 6-10 classroom`, page one is:

- **Affiliate listicles** — michaelryanmoney.com, wealthywomanfinance.com,
  mommoneymap.com, moneyparents.com, thatssomontessori.com, myfirstnestegg.com,
  moneyprodigy.com. My First Nest Egg discloses Amazon Associates commissions
  outright and says its 12 picks were vetted by "a persnickety book critic – a
  six-year-old."
- **Institutional lists** — ABA Foundation, ALA/FINRA LibGuides, WeAreTeachers,
  Brightly (Penguin Random House), gohenry, Creative Teaching Press, Hills Bank,
  Tuttle Twins.

Sam Renick, Beth Kobliner, Tom Henske, Susan Beacham — **none of their own sites
rank on these queries either.** Not one. They're not beating you with better SEO.
They're winning by being *listed inside* the pages that rank.

The ABA Foundation list carries 25 titles. Kimberly Wilson holds three slots. The
Berenstain Bears hold three. Jasmine Paul's *A Boy, a Budget, and a Dream* — the
closest peer comp from the June audit — sits on both the ABA list and the My First
Nest Egg list.

**You cannot win "best money books for kids" with your homepage.** The format is
wrong. Google has decided that query wants a comparison article, and a
single-book site will never be one. The only two ways in are to get cited inside
those lists, or to publish comparison-format content of your own.

**2. Name collisions — worse than I first thought.**

There are three, not two:

- **"Jonathan Bach"** belongs to Richard Bach's son, author of *Above the Clouds*,
  11 books on Goodreads, personal site at jonathanbach.info.
- **"David Bach"** — 10x NYT bestselling money author, 13 books, 7M+ copies, owns
  the *Automatic Millionaire* and *Finish Rich* series. **Bach + money already
  means him.** This is almost certainly why Google's "People also ask" went to
  adult finance: in Google's model, a Bach who writes about money is David.
- **"Clarence"** is a Cartoon Network series on Disney+ and Hulu, a 2023 A24 film
  (*The Book of Clarence*), and a town in Iowa.

You rank #1 when someone types all three signal words. The problem is everything
short of that resolves to somebody else.

**3. Verify whether the book has listings off-site.**

I flagged this as confirmed in the first draft. It isn't — same broken tool. But
it's worth you checking directly, because it's the input to the roundup-list play:
does the ISBN (979-8-234-07638-0) resolve on Amazon, Goodreads, Bookshop.org,
Google Books, and in Bowker/Books In Print?

Google builds book entities from those sources. If they're thin or absent, that
would explain both the missing Book rich result and the topical misclassification
— your `Book` schema asserts facts nothing else corroborates. And the affiliate
listicles are Amazon-monetized, so they structurally can't feature a title with no
Amazon link.

If the listings are already live and healthy, this drops off the list and the play
becomes purely outreach.

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
  Genuinely good schema work.

One thing worth chasing here: valid `Book` schema with `Offer`, `Review`, and
`Rating` and *still* no rich result at #1 is unusual. Run the homepage through
Google's Rich Results Test. Either the markup is being rejected for a reason the
validator will name, or Google isn't trusting the review data — three on-site
reviews with no corroborating source is a common reason for suppression.

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

**1. Pitch the roundup lists.** This is the whole ballgame for category search.
They are the page-one competition, and no amount of on-site work will replace
being on them. Start with the institutional lists — ABA Foundation, ALA/FINRA
LibGuides, WeAreTeachers, Brightly — because they carry the most authority and
don't need affiliate economics. Then work the affiliate blogs.

Your pitch angle writes itself and nobody else on those lists has it: **every
book on the ABA list teaches earning and saving. Yours is the only one that
teaches spending** — the complete transaction, through the register, including
sales tax. That's a genuine hole in every list I read.

**2. Confirm the off-site listings.** Amazon, Goodreads, Bookshop.org, Google
Books, Bowker/Books In Print. If the ISBN doesn't resolve on these, fix that
first — it feeds the Book rich result, the entity classification, and the
affiliate lists' ability to feature you at all. If they're already live, skip it.

**3. Fix the topical classification.** Google is serving adult-finance "People
also ask" on a K–5 picture book. Add `sameAs` to the Person schema pointing at
real author profiles. Make sure every off-site listing pairs "Jonathan Bach" with
"Clarence Gets a Bargain" *and* a children's/education context — you're competing
with David Bach for "Bach + money," and he has 7 million copies of head start.
Chase coverage in kidlit, teacher, and librarian venues over finance venues; the
inbound context is what teaches Google which shelf you're on.

**4. Publish comparison-format content.** You can't beat listicles with a
homepage, but you can publish pages that match the format the SERP wants. You
already have the raw material: `state-of-the-states.html`, the curriculum
alignment matrix, the standards crosswalk. A page like "K–5 money books, compared
by what they actually teach" — honest, including competitors — is a format Google
already rewards on these queries, and it's the kind of page librarians link to.

**5. Run the Rich Results Test** on the homepage. #1 with valid Book schema and no
rich result is a solvable anomaly.

**6. Split the 1 MB homepage.** Load the six resource modals by iframe `src`
instead of inlined `srcdoc`. Cuts page weight, kills the duplicate content, and
collapses 14 H1s to one. Also a candidate explanation for the missing sitelinks.

**7. On social, write the Henske post.** Not the stats post, not the FinLit Month
post. The arrogant checklist with a hole in it. Two you already own:
*"Everything a 4th grader should know before they walk into a store"* and
*"Nine things Clarence's mom did that your mom probably did too"* — the receipt
photo, the grocery-price game, Guess the Price at dinner. End on an open question
and let parents finish it.

**8. Point Maryann at teacher Facebook groups.** One classroom read-aloud story
from a 30-year veteran beats fifty author-page posts.

---

## Open questions I couldn't answer

My search tooling can't see this domain the way Google does, so these need to come
from Search Console. They're the difference between guessing and knowing:

1. **Which queries actually bring impressions and clicks?** Search Console →
   Performance → Queries. This answers "why are competitors above me" directly,
   with real numbers, in about a minute. Sort by impressions with low CTR — that's
   the list of queries where you're on the board but nobody's clicking.
2. **How many pages are indexed?** Search Console → Pages. All 17 sitemap URLs, or
   just a few? If the resource pages aren't indexed, that's a lot of dead weight.
3. **Any manual actions or Core Web Vitals failures?** Both would explain
   suppressed sitelinks and rich results.
4. **Does the ISBN resolve off-site?** (See fix #2.)

Send me a screenshot of the Performance → Queries tab and I can tell you exactly
which category terms you're close on and which are out of reach.
