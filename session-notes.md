# Session Notes — running log for cross-session continuity

Read this at the start of every session, right after CLAUDE.md. Newest entry
on top. When an item ships or dies, move it to the Done/Dead list at the
bottom of its entry — don't delete history.

---

## 2026-06-10 — Competitor-research sprint + school visits page

**Branch:** `claude/review-comment-ad1a10b-V8qLp` — all pushed, working tree clean.

### What shipped this session (6 commits, 4a87962 → 9c39478)

1. **4a87962** — Urgency strip ("Money habits form by age 7." Cambridge 2013),
   age-band cards (3 cols, grade chips), proof capsules strip (36 / 16+ / 55+ / 4)
   before buy section.
2. **ff6644e** — Wally Luckeydoo fixed: compact seal in buy section (dark overlay
   on orange, verbatim excerpt, full 4-award credential line) + third testimonial
   card in #reviews. He's now visible before the buy decision.
3. **1675106** — SEO: title now ends "| Ages 6–10, Grades 1–5", meta description
   rewritten educator-facing (Jump$tart named), keywords replaced with Tier 1
   targets ("comparison shopping" = winnable keyword, zero competition).
4. **862421d** — Verbatim excerpt section "Read an Actual Page" (page 12, tilted
   card, dog-ear corner; page-13 cliffhanger is spoiler-safe), classroom roadmap
   in toolkit, "Give a Classroom Set" institutional card 04, 2 new FAQs (synced
   to JSON-LD FAQPage), coupon nav re-routed by audience (parents → #magazine,
   teachers → #toolkit, skeptics → #reviews).
5. **57a51de** — `resources/free-sample-print.html`: pages 1–5 verbatim, paper-look
   cards, cliffhanger close ("That's 5 pages down. 31 to go."), print stylesheet.
   4th coupon card for the sampler, audience self-segmentation buttons above email
   signup, teacher wedge line ("Free for teachers. Forever."), grandparent gift line.
6. **9c39478** — `school-visits.html` "The Clearance Aisle Assembly": 4 formats
   (Full Assembly = featured, PTA Reading, Classroom, Virtual), 5-step run of show,
   author bio, funding box (PTA / Title I / literacy grants / credit unions /
   classroom split / cultural arts), 6-item logistics FAQ, mailto booking CTA with
   pre-filled body template. Linked from educator-toolkit hero; in sitemap.

### Decisions made (don't re-litigate)

- **Second Wally LinkedIn quote stays OFF the site.** Reserved for social. The
  site already has the seal + testimonial card; a third placement dilutes.
- **No bundles.** Jonathan said "no bundle bullshit." Donate-a-classroom-set card
  is institutional, not a bundle.
- **Amazon listing = validation only**, not a sales channel push. Seller Central
  Individual plan, ship from own supply. Purpose: unlocks the hidden secondary
  buy button (`bn`/`indie` buttons at index.html ~878–879, currently
  `visibility:hidden`) and supports ALA/Goodreads vetting.
- **Press kit deferred** — "not ready for press this week but maybe next week."
  Simple static page when greenlit: bios, hi-res photos, cover art, award list.

### Jonathan's action items (not code)

- **Google Search Console** — verify domain, submit sitemap.xml. This is the
  whole SEO unlock; config is already correct (robots.txt, sitemap, JSON-LD).
- **Amazon Seller Central** setup (Individual plan, ISBN listing).
- **ESP swap** — email signup is Web3Forms → inbox only, no list, no drip.
  Fix: Brevo or Mailchimp API in the signup form handler.
- **School-reading registries:** Maryland Humanities + Delaware Humanities
  speakers bureaus; MD PTA (mdpta.org) / DE PTA (depta.org) state councils;
  MD + DE Credit Union Leagues (they fund K–5 finlit programming — fastest
  sponsorship path); district literacy coordinators (Montgomery, PG, Baltimore
  City, Anne Arundel / Christina, Red Clay, Capital).
- **ALA path:** ALA Public Programs + FINRA Foundation "Thinking Money for All
  Kids" via programminglibrarian.org (programsatlibraries@ala.org). Prereq:
  a School Library Journal or Kirkus review — that's the vetting signal ALA
  curators use. Secondary: finrafoundation.org direct.

### Open flags for Jonathan to veto

- New FAQ says **"signed-by-author available on request"** — confirm or kill.
- School-visits FAQ says **order forms go home two weeks before the visit** and
  fee language ("pricing based on format and travel") — confirm both match how
  he actually runs visits.
- school-visits.html booking email is **jonbachlaw@gmail.com** — switch to
  questions@clarencegetsabargain.com if preferred.
- Author bio cred chip says "4-Category Award Winner" — verify phrasing.

### Code landmarks added this sprint (not yet in CLAUDE.md code map)

- `index.html`: `.urgency-strip` (after banner ~740), `.age-band-section` (after
  cover showcase), `.proof-strip` (before #buy), `.wally-seal` (in #buy),
  excerpt section "Read an Actual Page", `.roadmap-wrap` (toolkit), anchor IDs
  `#toolkit` `#reviews` `#institutional`, audience router buttons above signup.
- New files: `resources/free-sample-print.html`, `school-visits.html`,
  `competitive-audit-kids-finlit-social.md` (research artifact, not site code).

### Next likely tasks

1. Press/media kit page (next week, on Jonathan's go).
2. Un-hide + wire secondary buy button once Amazon listing exists.
3. ESP integration if Jonathan picks Brevo/Mailchimp.
4. Possibly link school-visits.html from index.html nav/footer (currently only
   linked from educator-toolkit.html).
