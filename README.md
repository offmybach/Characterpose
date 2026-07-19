# The Crabby Guy's Little Book of Beach Etiquette — official site

Single-page site for the book. Read before your feet meet sand.

Live file: `index.html`. No build step, no dependencies, no framework. Open it in a browser and it works. Fonts load from Google Fonts (Staatliches, Spectral, Caveat).

## Dropping in the illustrations

Every art slot on the page is wired to a filename. When a file with that name lands in `images/`, the placeholder disappears and the art shows up on its own — no HTML edits.

| File | What goes there | Source prompt in the manuscript |
|---|---|---|
| `images/cover.png` | Hero book cover (portrait, 2:3) | Front cover art |
| `images/host.png` | Your Host section (landscape) | HOST PAGE — The Crabby Guy |
| `images/rule-01.png` | Rule 1 · Personal Space | RULE 1a — THE INVADER |
| `images/rule-02.png` | Rule 2 · The Smoke Show | RULE 2 |
| `images/rule-03.png` | Rule 3 · Audio Terrorism | RULE 3 |
| `images/rule-04.png` | Rule 4 · The Excavators | RULE 4 |
| `images/rule-05.png` | Rule 5 · Fire & Flight | RULE 5a or 5b |
| `images/rule-06.png` | Rule 6 · Shanty Towns & Projectiles | RULE 6 |
| `images/rule-07.png` | Rule 7 · Trash & Beasts | RULE 7b (the seagull crime family) |
| `images/rule-08.png` | Rule 8 · Unsupervised Chaos | RULE 8 |
| `images/rule-09.png` | Rule 9 · The Exfoliators | RULE 9 |
| `images/rule-10.png` | Rule 10 · The Nuisance Trifecta | RULE 10a or 10b |
| `images/rule-11.png` | Rule 11 · Authority | RULE 11a or 11b |
| `images/rule-12.png` | Rule 12 · The Ocean Is Not a Toilet | RULE 12a |
| `images/rule-13.png` | Rule 13 · The Squatters | RULE 13 |
| `images/rule-14.png` | Rule 14 · Rods & Boards | RULE 14 |
| `images/rule-15.png` | Rule 15 · Personal Maintenance | RULE 15 |
| `images/rule-16.png` | Rule 16 · Parenting | RULE 16 |
| `images/rule-17.png` | Rule 17 · The Golden Rule | RULE 17 |

Rule illustrations are landscape (3:2), per the style reference. PNG or JPG both work — if you use `.jpg`, update the matching `src` in `index.html`.

## Still to wire up

- Buy button currently points to the launch-notify list. Swap in the Stripe/store link when the book goes on sale.
- Google Analytics tag, if wanted.
- Custom domain: add a `CNAME` file once the domain exists.
