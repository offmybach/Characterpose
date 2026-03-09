# Printing Quote Collector

Automated browser-based quote collection for children's book printing from multiple U.S. vendors.

## Quick Start

```bash
cd printing-quotes
npm install
npx playwright install chromium
node main.js
```

## Configuration

Edit `config.json` to change:
- **trim size** — `book_specs.trim_size`, `trim_size_width`, `trim_size_height`
- **page count** — `book_specs.page_count`
- **binding** — `book_specs.binding`
- **interior stock** — `book_specs.interior_stock`
- **quantities** — `quantities` array
- **shipping ZIP** — `shipping.zip_code`
- **headless mode** — `browser.headless` (set `false` to watch the browser)

## Outputs

| File | Description |
|------|-------------|
| `quotes.csv` | All captured data in CSV format |
| `quotes_summary.md` | Human-readable comparison with rankings |
| `vendor_screenshots/` | Screenshots of quote pages or failure points |

## Vendor Status

| Vendor | Quote Type | Handler |
|--------|-----------|---------|
| OnPress | ASP.NET quoter | `vendor_handlers/onpress.js` |
| 48 Hour Books | Pricing calculator | `vendor_handlers/48hrbooks.js` |
| Mixam | JS configurator | `vendor_handlers/mixam.js` |
| BookBaby | Multi-step quoter | `vendor_handlers/bookbaby.js` |
| Books.by | POD platform (no bulk) | `vendor_handlers/booksby.js` |

## Adding a New Vendor

1. Create `vendor_handlers/vendorname.js`
2. Export `async function getQuote(page, config, quantity, screenshotDir)`
3. Add the vendor to `config.json` vendors array
4. Import it in `main.js` handlers map

## Status Codes

- `success` — Full quote captured
- `partial` — Some data captured, price may be missing
- `blocked` — Anti-bot, CAPTCHA, or error prevented access
- `rejected_non_gloss` — Vendor cannot do glossy hardcover interiors
- `manual_follow_up_needed` — Requires human action to complete

## Rules

- No logins, no accounts, no payments
- No CAPTCHA bypassing
- Public calculators only
- Screenshots saved for every attempt
