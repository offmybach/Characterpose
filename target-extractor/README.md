# CGB Target Extractor

A Chrome extension that auto-scrapes LinkedIn Sales Navigator lead lists,
dedups across lists, categorizes every lead into one of your CGB target
groups, and exports a single grouped master CSV (or one CSV per group).

Built so you can walk away. Open Sales Nav, paste a queue of list URLs,
hit Start, go make coffee.

## Install

1. In Chrome, open `chrome://extensions`.
2. Turn on **Developer mode** (top right).
3. Click **Load unpacked** and choose this `target-extractor/` folder.
4. Pin the extension in the toolbar so you can reach the popup.

## Use it — two flows

### Flow A — one list at a time

1. In Chrome, sign into LinkedIn and open a Sales Nav list:
   `https://www.linkedin.com/sales/lists/people/...`
2. Click the extension icon. Hit **Scrape this page**.
3. The extension auto-scrolls the lead container until every card has
   loaded, then clicks **Next** until the list is exhausted.
4. Open the next list. Repeat. Leads accumulate; dups are merged.

### Flow B — queue (the "walk away" flow)

1. Go to `https://www.linkedin.com/sales/lists` so all your lists are
   visible.
2. Open the extension popup, click **Scrape this page**. It harvests every
   list URL into the queue.
3. Paste extra URLs into the textarea if you want, then click **Save queue**.
4. Click **Start queue**. The extension will, in your current tab,
   navigate to each list URL, scrape it, then move to the next.
5. When the queue is done, click **Master CSV (grouped)**.

### Export

- **Master CSV (grouped):** every lead in one file, sorted by
  `primary_group` then connection rank (1st → Pending → 2nd → 3rd+ →
  Following → Unknown), with `secondary_groups` if a lead matched
  multiple rules. The file you'll actually use for mail-merge
  segmentation.
- **One CSV per group:** dumps one file per `primary_group` into your
  default download folder, also sorted by connection rank.

### The `connection` column

Captured for every lead, one of:

| Value | Meaning |
|---|---|
| `1st` | You're connected. Can message directly. |
| `Pending` | You've already sent an invite — don't double-tap. |
| `2nd` | One mutual. Best candidates for a connect request. |
| `3rd+` | No path. Cold outreach territory. |
| `Following` | You follow them but aren't connected. |
| `Unknown` / empty | Sales Nav didn't render a badge for this row. |

Dedup keeps the most informative status: if you captured someone as
`2nd` last week and as `Pending` today (because you sent an invite),
the merged record shows `Pending`.

## Groups

The taxonomy mirrors `LinkedIn_connections_grouped_by_category.xlsx` so
new captures drop straight into your existing master spreadsheet without
re-categorizing. Each rule lives in `categorizer.js`; tweak regexes there.

Priority order (highest wins for `primary_group`; other matches go to
`secondary_groups`):

| Group | Default Relevance | Wins when… |
|---|---|---|
| Youth Financial Literacy | High | kids/youth/family **and** money/finance |
| Authors / Illustrators / KidLit | High | author, illustrator, kidlit, picture book |
| Librarians / Libraries | High | librarian, media specialist, public library |
| EdTech / Curriculum / Program Design | High | edtech, curriculum designer, instructional designer |
| Financial Literacy Educators / Advocates | High | financial literacy, NEFE, NGPF, Jump$tart, CFEI |
| Teachers / School Educators | High | teacher, principal, CTE, ISD, elementary, K-5 |
| Academic / Researchers / Professors | Medium | professor, PhD, university, research institute |
| Financial Advisors / Planners / Insurance | Medium | CFP, CFA, financial advisor, RIA, wealth |
| Financial Coaches / Wellness / Therapy | Medium | financial coach, AFC, financial therapist, wellness |
| Bankers / Financial Institutions | Medium | bank, credit union, bancorp, community banking |
| Nonprofit / Government / Policy | Medium | foundation, nonprofit, CFPB, FDIC, treasurer, .gov |
| Publishing / Book Pros / Printers | Medium | publisher, book designer, literary agent, printer |
| Media / Content / Speakers | Medium | journalist, podcaster, columnist, NPR, magazine |
| Marketing / Sales / Partnerships | Low | marketing, business development, sponsorship, BD |
| Peripheral / Not Clarence-specific | Low | FAFSA, healthcare, ESPN, fundraising — explicit non-fit |
| Needs Review / Miscellaneous | Medium | catch-all when nothing else matched |

`clarence_relevance` defaults per group above; you can override per lead in
the master CSV. `tags` are merged from every matched group, pipe-separated
(e.g. `kids/youth|financial literacy|teacher/school`).

A "Youth Financial Literacy" match requires **both** a kids signal and a
money signal — that's what separates a finlit professional whose work is
kid-focused from a generic finlit advocate. The latter goes to "Financial
Literacy Educators / Advocates."

## Files

- `manifest.json` — MV3 manifest, host permissions for linkedin.com/sales.
- `content.js` — DOM scraper with fallback selectors and auto-paginator.
- `background.js` — queue runner, dedup, CSV exporter (service worker).
- `categorizer.js` — group rules (shared between background and popup).
- `popup.html / popup.css / popup.js` — toolbar UI.

## When selectors break

LinkedIn updates Sales Nav DOM regularly. If counts go to zero on a known-
good list:

1. Open DevTools on the list page.
2. Inspect one lead card. Note the new selector for the row container,
   name, title, company.
3. Edit the `SEL` object at the top of `content.js`. Each field is an
   array — add the new selector at the **front**; old ones remain as
   fallbacks for backward compatibility.

## Heads up — LinkedIn ToS

Automated scraping of LinkedIn is against their User Agreement. LinkedIn
has been known to lock accounts that scrape aggressively. This tool runs
slowly on purpose (~700ms between scrolls, 1.5s between list nav events)
and only reads what's already rendered in your logged-in browser — but
the risk is real. Use a secondary account if you can, and don't run it
24/7. If you start seeing CAPTCHAs, stop for a day.

This is your tool, not a hosted service. Anthropic / Claude doesn't
operate it. You are the one signed in, you are the one scraping.
