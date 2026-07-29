# The deal-master stories — facts of record

**This file wins.** If site copy disagrees with what is here, the copy is wrong.

These are the anecdotes Jonathan leads with, including interview question one in the press
kit. They had already drifted badly once — see the correction log — so they get the same
treatment as a reviewer's quote: one canonical version, and nothing invented.

Standing rule from CLAUDE.md applies with full force: **dollar amounts are never rounded,
estimated, or editorialised.** $293 is $293. Not "$300," not "nearly $300."

---

## Story 1 — the cruise-ship price match

**What actually happened:** He got a merchant on a cruise ship to match the sale price on the
company's own website.

That's the whole story. The skill in it is comparison shopping: he knew the company was
selling the same item cheaper on its own site than in its shipboard shop, and he asked.

**Do not write:**
- that he "negotiated," "talked down," or "haggled" anyone to a penny — this story has no
  penny in it
- any dollar figure — **none is on record.** If a figure is wanted, ask Jonathan; do not
  supply one.

**Why it's on-brand:** this is page 5 of the book. Comparison shopping, one seller against
another price for the same thing. It is the cleanest real-life proof of the book's core
concept that he owns.

---

## Story 2 — the one-cent shoes

Nordstrom Rack. Photographed tag on file.

| Field | Value |
|---|---|
| Item | Mephisto Sano |
| Size | 10.5 |
| Compare at | **$293** |
| Rack price | **$199.97** |
| **Paid** | **$.01** |
| Sticker reads | "99% Savings" |
| Barcode / store | 8826S8314065 · **077** |

## Story 3 — the one-cent shirt

Nordstrom Rack, **same store — 077**. Photographed tag on file.

| Field | Value |
|---|---|
| Item | "RB" hangtag · colour **PINE** |
| Size | X-LARGE |
| Original | **$69.50** |
| **Paid** | **$.01** |
| Sticker reads | "99% Savings" |
| Barcode / store | 692562230096 · **077** |

### The two penny finds are one story, and it is better than a single one

Both tags are from store **077**. Same Nordstrom Rack. That makes it a documented habit
rather than a fluke, which is what "deal master" is supposed to mean and what the book is
actually about — Clarence learns the clearance aisle is where the real deals hide, and the
author has two red clearance stickers from the same aisle.

**These were found, not negotiated.** The skill is working the clearance rack relentlessly,
not haggling. Use verbs like *found, paid, walked out having paid.* Never *negotiated.*

### The joke is on the sticker, not in the copy

Both stickers say **"99% Savings."**

- $.01 off $293 is **99.997%**
- $.01 off $69.50 is **99.986%**

Nordstrom Rack understated both markdowns. The retailer is being modest on his behalf. That
line is free and it is funnier than anything written about it, so let their label deliver it.

---

## Approved copy

**Long bio / press kit:**
> He once got a merchant on a cruise ship to match the sale price on the company's own
> website. Separately, and with the tags to prove it, he has walked out of the same Nordstrom
> Rack having paid one cent — once for a $293 pair of Mephistos, once for a $69.50 shirt.
> Both stickers say "99% Savings," which undersells it.

**Short / one line:**
> An attorney who has paid one cent for a $293 pair of shoes. He kept the tag.

**Never again:**
- ❌ "negotiated $300 shoes down to one cent"
- ❌ "price-matched $300 shoes down to $0.01 on a cruise ship"
- ❌ "$0" or "$0.01" in place of one cent — the penny is the punchline and $0 is also false

---

## Correction log

- **Before 29 Jul 2026** — Copy in 15 places across 6 files merged Story 1 and Story 2 into a
  single claim that he *negotiated* a $300 pair of shoes down to a penny on a cruise ship.
  That event never happened: the cruise-ship win was a website price match with no penny, and
  the penny was a Nordstrom Rack clearance sticker he found. Two instances additionally said
  "$0" instead of one cent.
- **29 Jul 2026** — All 15 corrected against the photographed tags. Story 3 (the shirt) added.
  Cruise-ship story kept, stripped of the invented penny and the invented dollar figure.

## Still open — the tag photos

The photographed tags are **not in the repo**. Only `images/sticker.png` is here, and that is
the orange brand graphic, not a receipt. Pasting a photo into chat lets it be read but does
not create a file, and dragging one into a local folder does not reach this container.

**To get them in:** commit them from the local machine and push to the working branch.

```
git add images/tag-mephisto-one-cent.jpg images/tag-shirt-one-cent.jpg
git commit -m "Add one-cent clearance tag photos"
git push origin claude/competitor-seo-social-analysis-n6caiy
```

Filenames do not matter; whatever lands in `images/` will be found.

### Decision on record — barcodes get obscured (Jonathan, 29 Jul 2026)

Both tags carry scannable barcodes and identify store **077**. Before publishing, **crop or
blur the barcode strips.** Keep everything the story needs and nothing it does not:

| Keep | Remove |
|---|---|
| Brand and item (Mephisto Sano · RB) | Barcode strips, both the printed number and the bars |
| Size, colour | Store number 077 |
| Compare at $293 · $199.97 · $69.50 | |
| **$.01** and **"99% Savings"** | |

Pillow 12.3.0 is available and verified for crop, Gaussian blur, and JPEG save. Blur is
preferable to a hard crop where the barcode sits inside the sticker, so the red clearance
label stays visibly intact — the label is the point.

### Then, in one pass

1. **`press-kit.html`** — a "Proof" card beside the art downloads, both tags, captioned with
   Nordstrom Rack's own "99% Savings" and the real percentages underneath. Turns interview
   question one from an anecdote into a document.
2. **`index.html` ~1633** — the deal-master line currently asserts the penny with nothing
   behind it. The tags belong there.
3. **Alt text, stated as fact:** "Nordstrom Rack clearance tag: Mephisto Sano, compare at
   $293, marked $199.97, final price $.01, sticker reads 99% Savings."
4. **A social post** — two tags, the two percentages their sticker rounded down, one line
   about the clearance aisle.
