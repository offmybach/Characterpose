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
  `primary_group`, with `secondary_groups` if a lead matched multiple
  rules. The file you'll actually use for mail-merge segmentation.
- **One CSV per group:** dumps one file per `primary_group` into your
  default download folder.

## Groups

Categorization is rule-based, ordered by specificity (highest priority
wins). The full rule set lives in `categorizer.js` — tweak regexes there.

| Group | Wins when… |
|---|---|
| `FinancialAdvisors` | CFP, CFA, ChFC, financial/wealth advisor, RIA |
| `FinLitExperts` | "financial literacy", NEFE, NGPF, Jump$tart, CEE |
| `WritersPodcastersReporters` | journalist, reporter, columnist, podcast host, editor |
| `Authors` | author, illustrator, picture book author |
| `Librarians` | librarian, media specialist, public library |
| `K5Educators` | teacher, principal, curriculum, elementary, K-5, ISD |
| `GovernmentAgencies` | .gov, treasurer, CFPB, FDIC, Dept of Education |
| `InstitutionalBuyers` | credit union, bank, nonprofit, foundation, community outreach |
| `Parents` | parent, mom, dad, parenting (low priority — last) |
| `Misc` | catch-all when nothing matched |

A lead can match more than one group — the higher-priority rule wins for
`primary_group`, and the rest are stored in `secondary_groups` so you can
re-segment without re-scraping.

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
