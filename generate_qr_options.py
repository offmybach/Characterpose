"""Generate 6 styled QR code options for Clarence Gets a Bargain.

All six share the fixes that make the code easier to capture than v1:
- darker purple-to-teal gradient (more contrast against white)
- RoBimmie (the bargain itself) in the center on a clean white knockout —
  replaces the off-brand piggy bank, sized well under the ECC recovery limit
- white rounded card behind everything so the code pops on fabric
- error correction H, version 3 (29x29 — big fat modules)

What varies is the data-module style (the "funky lines"):
  1 vertical-bars    2 horizontal-bars   3 liquid (connected rounded)
  4 diagonal slashes 5 basket weave      6 wavy snake columns

Outputs images/qr-options/option-N-<style>.png plus a contact sheet.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
# Center art: a hand presenting a fan of US dollar bills, generated in
# Nano Banana Pro from the page-11 pose and keyed off its checkerboard
# (source: holdcash.png at repo root). A kid spending money smartly is
# the pitch — not the savings-brand piggy bank. Spares in repo:
# hand-bills.png (pointing pose), robimmie-cutout.png.
CENTER_SRC = ROOT / "images" / "holdcash-cut.png"
OUT_DIR = ROOT / "images" / "qr-options"
URL = "https://www.clarencegetsabargain.com"

# Darker gradient endpoints — same purple-to-teal family, ~35% darker
TOP_LEFT = (70, 14, 132)      # deep purple
TOP_RIGHT = (38, 38, 126)     # dark purple-blue
BOTTOM_LEFT = (36, 60, 122)   # dark blue
BOTTOM_RIGHT = (12, 106, 82)  # dark teal

MODULE_PX = 28
QUIET_MODULES = 4        # white quiet zone inside the card
CARD_MARGIN = 1.5        # extra white card margin beyond quiet zone (modules)
FINDER_SIZE = 7
BAR_RATIO = 0.78         # bar/dot thickness as fraction of a module

PLATE_AREA = 0.105       # white plate covers ~10.5% of the code — ECC H can
                         # recover 30%; v1's piggy bank plate was ~20%
ART_MAX_DIM = 0.40       # cap on center art's largest dimension vs code width
PLATE_PAD_W = 1.22       # white plate padding around the art
PLATE_PAD_H = 1.06

STYLES = [
    ("vertical-bars", "Vertical Bars"),
    ("horizontal-bars", "Horizontal Bars"),
    ("liquid", "Liquid / Connected"),
    ("diagonal", "Diagonal Slash"),
    ("weave", "Basket Weave"),
    ("wave", "Wavy Snake"),
]


def gradient_color(x: float, y: float, w: float, h: float) -> tuple[int, int, int]:
    fx = max(0.0, min(1.0, x / max(w - 1, 1)))
    fy = max(0.0, min(1.0, y / max(h - 1, 1)))
    top = tuple(TOP_LEFT[i] * (1 - fx) + TOP_RIGHT[i] * fx for i in range(3))
    bot = tuple(BOTTOM_LEFT[i] * (1 - fx) + BOTTOM_RIGHT[i] * fx for i in range(3))
    return tuple(int(round(top[i] * (1 - fy) + bot[i] * fy)) for i in range(3))


def build_matrix(url: str):
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H,
                       box_size=1, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    return qr.get_matrix()


def is_finder(r: int, c: int, n: int) -> bool:
    return ((r < FINDER_SIZE and c < FINDER_SIZE)
            or (r < FINDER_SIZE and c >= n - FINDER_SIZE)
            or (r >= n - FINDER_SIZE and c < FINDER_SIZE))


def dark(matrix, r: int, c: int) -> bool:
    n = len(matrix)
    if r < 0 or c < 0 or r >= n or c >= n:
        return False
    return bool(matrix[r][c]) and not is_finder(r, c, n)


def _perspective_coeffs(target_quad, source_quad):
    A, B = [], []
    for (xt, yt), (xs, ys) in zip(target_quad, source_quad):
        A.append([xt, yt, 1, 0, 0, 0, -xt * xs, -yt * xs])
        A.append([0, 0, 0, xt, yt, 1, -xt * ys, -yt * ys])
        B.extend([xs, ys])
    return np.linalg.solve(np.array(A, dtype=np.float64),
                           np.array(B, dtype=np.float64))


def draw_finder(canvas, top_left_px, color, corner, lean=1.0):
    """Leaning rounded-trapezoid finder from the v1 code.

    lean scales the perspective warp. 1.0 = the v1 look, which breaks the
    1:1:3:1:1 finder ratio scanners need — the main reason v1 was hard to
    capture. Keep it low enough that decode stress tests pass."""
    x0, y0 = top_left_px
    s = FINDER_SIZE * MODULE_PX
    pad = MODULE_PX * 2
    size = s + 2 * pad
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    d.rounded_rectangle([pad, pad, pad + s - 1, pad + s - 1],
                        radius=int(MODULE_PX * 1.6), fill=color + (255,))
    d.rounded_rectangle([pad + MODULE_PX, pad + MODULE_PX,
                         pad + s - MODULE_PX - 1, pad + s - MODULE_PX - 1],
                        radius=int(MODULE_PX * 1.1), fill=(0, 0, 0, 0))
    cp = 2 * MODULE_PX
    d.rounded_rectangle([pad + cp, pad + cp, pad + s - cp - 1, pad + s - cp - 1],
                        radius=int(MODULE_PX * 0.9), fill=color + (255,))

    push, pull = MODULE_PX * 1.0 * lean, MODULE_PX * 0.45 * lean
    tl, tr = [pad, pad], [pad + s, pad]
    br, bl = [pad + s, pad + s], [pad, pad + s]
    if corner == "tl":
        tl = [pad - push, pad - push]; br = [pad + s - pull, pad + s - pull]
    elif corner == "tr":
        tr = [pad + s + push, pad - push]; bl = [pad + pull, pad + s - pull]
    elif corner == "bl":
        bl = [pad - push, pad + s + push]; tr = [pad + s - pull, pad + pull]

    coeffs = _perspective_coeffs(
        [tl, tr, br, bl],
        [[pad, pad], [pad + s, pad], [pad + s, pad + s], [pad, pad + s]])
    warped = layer.transform((size, size), Image.PERSPECTIVE, coeffs,
                             resample=Image.BICUBIC)
    canvas.alpha_composite(warped, dest=(x0 - pad, y0 - pad))


# ---------------------------------------------------------------- styles

def draw_vertical_bars(draw, matrix, offset, qr_px):
    n = len(matrix)
    bw = int(MODULE_PX * BAR_RATIO)
    inset = (MODULE_PX - bw) // 2
    for c in range(n):
        r = 0
        while r < n:
            if not dark(matrix, r, c):
                r += 1
                continue
            r0 = r
            while r < n and dark(matrix, r, c):
                r += 1
            x0 = offset + c * MODULE_PX + inset
            y0 = offset + r0 * MODULE_PX + inset
            y1 = offset + r * MODULE_PX - inset - 1
            cx = c * MODULE_PX + MODULE_PX // 2
            cy = ((r0 + r) / 2) * MODULE_PX
            color = gradient_color(cx, cy, qr_px, qr_px)
            draw.rounded_rectangle([x0, y0, x0 + bw - 1, y1],
                                   radius=bw // 2, fill=color + (255,))


def draw_horizontal_bars(draw, matrix, offset, qr_px):
    n = len(matrix)
    bw = int(MODULE_PX * BAR_RATIO)
    inset = (MODULE_PX - bw) // 2
    for r in range(n):
        c = 0
        while c < n:
            if not dark(matrix, r, c):
                c += 1
                continue
            c0 = c
            while c < n and dark(matrix, r, c):
                c += 1
            x0 = offset + c0 * MODULE_PX + inset
            x1 = offset + c * MODULE_PX - inset - 1
            y0 = offset + r * MODULE_PX + inset
            cx = ((c0 + c) / 2) * MODULE_PX
            cy = r * MODULE_PX + MODULE_PX // 2
            color = gradient_color(cx, cy, qr_px, qr_px)
            draw.rounded_rectangle([x0, y0, x1, y0 + bw - 1],
                                   radius=bw // 2, fill=color + (255,))


def draw_liquid(draw, matrix, offset, qr_px):
    """Full-bleed modules; corners round only where no neighbor touches,
    so runs of modules fuse into smooth flowing lines."""
    n = len(matrix)
    rad = int(MODULE_PX * 0.43)  # near-half radius trips a Pillow geometry check
    for r in range(n):
        for c in range(n):
            if not dark(matrix, r, c):
                continue
            up, dn = dark(matrix, r - 1, c), dark(matrix, r + 1, c)
            lf, rt = dark(matrix, r, c - 1), dark(matrix, r, c + 1)
            corners = (not up and not lf, not up and not rt,
                       not dn and not rt, not dn and not lf)
            x0 = offset + c * MODULE_PX
            y0 = offset + r * MODULE_PX
            color = gradient_color(c * MODULE_PX + MODULE_PX / 2,
                                   r * MODULE_PX + MODULE_PX / 2, qr_px, qr_px)
            draw.rounded_rectangle([x0, y0, x0 + MODULE_PX - 1, y0 + MODULE_PX - 1],
                                   radius=rad, corners=corners,
                                   fill=color + (255,))


def draw_diagonal(draw, matrix, offset, qr_px):
    """Thick 45-degree slashes; slashes extend to meet diagonal neighbors."""
    n = len(matrix)
    w = int(MODULE_PX * 0.72)
    for r in range(n):
        for c in range(n):
            if not dark(matrix, r, c):
                continue
            cx = offset + c * MODULE_PX + MODULE_PX / 2
            cy = offset + r * MODULE_PX + MODULE_PX / 2
            color = gradient_color(c * MODULE_PX + MODULE_PX / 2,
                                   r * MODULE_PX + MODULE_PX / 2, qr_px, qr_px)
            half = MODULE_PX * 0.42
            # extend along "/" to fuse with diagonal neighbors
            ext_ur = MODULE_PX * 0.30 if dark(matrix, r - 1, c + 1) else 0
            ext_dl = MODULE_PX * 0.30 if dark(matrix, r + 1, c - 1) else 0
            x0, y0 = cx - half - ext_dl, cy + half + ext_dl
            x1, y1 = cx + half + ext_ur, cy - half - ext_ur
            draw.line([(x0, y0), (x1, y1)], fill=color + (255,), width=w)
            rr = w / 2
            draw.ellipse([x0 - rr, y0 - rr, x0 + rr, y0 + rr], fill=color + (255,))
            draw.ellipse([x1 - rr, y1 - rr, x1 + rr, y1 + rr], fill=color + (255,))


def draw_weave(draw, matrix, offset, qr_px):
    """Alternating full-length horizontal / vertical stitches by parity —
    reads like woven fabric."""
    n = len(matrix)
    bw = int(MODULE_PX * 0.74)
    inset = (MODULE_PX - bw) // 2
    for r in range(n):
        for c in range(n):
            if not dark(matrix, r, c):
                continue
            x = offset + c * MODULE_PX
            y = offset + r * MODULE_PX
            color = gradient_color(c * MODULE_PX + MODULE_PX / 2,
                                   r * MODULE_PX + MODULE_PX / 2, qr_px, qr_px)
            if (r + c) % 2 == 0:  # horizontal stitch
                draw.rounded_rectangle(
                    [x + 1, y + inset, x + MODULE_PX - 2, y + inset + bw - 1],
                    radius=bw // 2, fill=color + (255,))
            else:                 # vertical stitch
                draw.rounded_rectangle(
                    [x + inset, y + 1, x + inset + bw - 1, y + MODULE_PX - 2],
                    radius=bw // 2, fill=color + (255,))


def draw_wave(draw, matrix, offset, qr_px):
    """Vertical runs drawn as overlapping circles whose centers wiggle
    sideways on a sine — wavy snake columns."""
    n = len(matrix)
    dia = MODULE_PX * 0.82
    amp = MODULE_PX * 0.11
    for c in range(n):
        r = 0
        while r < n:
            if not dark(matrix, r, c):
                r += 1
                continue
            r0 = r
            while r < n and dark(matrix, r, c):
                r += 1
            y_start = r0 * MODULE_PX + MODULE_PX / 2
            y_end = (r - 1) * MODULE_PX + MODULE_PX / 2
            steps = max(1, int((y_end - y_start) / (MODULE_PX / 4)))
            for i in range(steps + 1):
                y = y_start + (y_end - y_start) * (i / max(steps, 1))
                wig = amp * math.sin(2 * math.pi * y / (MODULE_PX * 3)) \
                    if r - r0 > 1 else 0
                x = c * MODULE_PX + MODULE_PX / 2 + wig
                color = gradient_color(x, y, qr_px, qr_px)
                rr = dia / 2
                draw.ellipse([offset + x - rr, offset + y - rr,
                              offset + x + rr, offset + y + rr],
                             fill=color + (255,))


STYLE_FNS = {
    "vertical-bars": draw_vertical_bars,
    "horizontal-bars": draw_horizontal_bars,
    "liquid": draw_liquid,
    "diagonal": draw_diagonal,
    "weave": draw_weave,
    "wave": draw_wave,
}


# ---------------------------------------------------------------- compose

# v1 used full lean (1.0) and scored 6/10 on harsh decode tests (tilt, blur,
# glare, 150px). 0.5 keeps the leaning-trapezoid look and scores 10/10 on
# every module style. Don't raise this without re-running the stress tests.
FINDER_LEAN = 0.5


def render_option(matrix, style: str) -> Image.Image:
    n = len(matrix)
    qr_px = n * MODULE_PX
    total = (n + 2 * QUIET_MODULES) * MODULE_PX
    canvas = Image.new("RGBA", (total, total), (0, 0, 0, 0))
    offset = QUIET_MODULES * MODULE_PX
    draw = ImageDraw.Draw(canvas, "RGBA")

    STYLE_FNS[style](draw, matrix, offset, qr_px)

    for rm, cm, which in [(0, 0, "tl"), (0, n - FINDER_SIZE, "tr"),
                          (n - FINDER_SIZE, 0, "bl")]:
        color = gradient_color((cm + FINDER_SIZE / 2) * MODULE_PX,
                               (rm + FINDER_SIZE / 2) * MODULE_PX, qr_px, qr_px)
        draw_finder(canvas, (offset + cm * MODULE_PX, offset + rm * MODULE_PX),
                    color, which, lean=FINDER_LEAN)

    # White knockout plate + center art. Plate area stays around 10% of the
    # code — well inside ECC H's 30% recovery budget.
    cx = cy = total // 2
    art = Image.open(CENTER_SRC).convert("RGBA")
    target = PLATE_AREA * qr_px * qr_px
    scale = (target / (art.width * PLATE_PAD_W * art.height * PLATE_PAD_H)) ** 0.5
    scale = min(scale, (qr_px * ART_MAX_DIM) / max(art.size))
    art = art.resize((int(art.width * scale), int(art.height * scale)),
                     Image.LANCZOS)
    pw = int(art.width * PLATE_PAD_W)
    ph = int(art.height * PLATE_PAD_H)
    d2 = ImageDraw.Draw(canvas, "RGBA")
    d2.rounded_rectangle([cx - pw // 2, cy - ph // 2, cx + pw // 2, cy + ph // 2],
                         radius=int(min(pw, ph) * 0.28),
                         fill=(255, 255, 255, 255))
    canvas.alpha_composite(art, dest=(cx - art.width // 2,
                                      cy - art.height // 2))

    # White rounded card behind everything (shows on colored fabric)
    margin = int(CARD_MARGIN * MODULE_PX)
    card_size = total + 2 * margin
    card = Image.new("RGBA", (card_size, card_size), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, card_size - 1, card_size - 1],
                         radius=int(MODULE_PX * 3), fill=(255, 255, 255, 255))
    card.alpha_composite(canvas, dest=(margin, margin))
    return card


def contact_sheet(images, labels) -> Image.Image:
    """3x2 grid on a light-blue 'shirt' background for preview."""
    cell = 620
    pad = 40
    label_h = 56
    W = 3 * cell + 4 * pad
    H = 2 * (cell + label_h) + 3 * pad
    sheet = Image.new("RGB", (W, H), (168, 200, 232))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
    except OSError:
        font = ImageFont.load_default()
    for i, (img, label) in enumerate(zip(images, labels)):
        col, row = i % 3, i // 3
        x = pad + col * (cell + pad)
        y = pad + row * (cell + label_h + pad)
        thumb = img.resize((cell, cell), Image.LANCZOS)
        sheet.paste(thumb, (x, y), thumb)
        text = f"{i + 1}. {label}"
        tw = d.textlength(text, font=font)
        d.text((x + (cell - tw) / 2, y + cell + 10), text,
               fill=(20, 40, 80), font=font)
    return sheet


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    matrix = build_matrix(URL)
    print(f"QR version modules: {len(matrix)}x{len(matrix)}")
    images, labels = [], []
    for i, (style, label) in enumerate(STYLES, start=1):
        img = render_option(matrix, style)
        target = 1600
        if img.width > target:
            img = img.resize((target, target), Image.LANCZOS)
        out = OUT_DIR / f"option-{i}-{style}.png"
        img.save(out, "PNG", optimize=True)
        images.append(img)
        labels.append(label)
        print(f"Wrote {out}")
    sheet = contact_sheet(images, labels)
    sheet_path = OUT_DIR / "all-six-options.png"
    sheet.save(sheet_path, "PNG", optimize=True)
    print(f"Wrote {sheet_path}")


if __name__ == "__main__":
    main()
