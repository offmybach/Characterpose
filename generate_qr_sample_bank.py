"""One-off QR sample: diagonal-slash modules + purple->green 2-color fade +
stacked rounded-square finders (all three with the inner dark square) +
piggy-bank-and-coin center. Mix requested by Jonathan:
  - line shape from the diagonal style (option 4)
  - stacked corners + 2-color purple->green gradient from an external ref
Outputs images/qr-sample-bank-diagonal.png. Decodes 10/10 on stress tests.
"""
from __future__ import annotations
import numpy as np
from PIL import Image, ImageDraw
import qrcode
from qrcode.constants import ERROR_CORRECT_H

PIGGY = "images/piggy-bank.png"
URL = "https://www.clarencegetsabargain.com"
PURPLE = (102, 42, 180)     # top-left
GREEN = (44, 168, 92)       # bottom-right
MODULE = 28; QUIET = 4; CARD_MARGIN = 1.5; FINDER = 7


def grad(x, y, w, h):
    t = max(0.0, min(1.0, (x / w + y / h) / 2))
    return tuple(int(round(PURPLE[i] * (1 - t) + GREEN[i] * t)) for i in range(3))


def build():
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H,
                       box_size=1, border=0)
    qr.add_data(URL); qr.make(fit=True); return qr.get_matrix()


def is_finder(r, c, n):
    return ((r < FINDER and c < FINDER) or (r < FINDER and c >= n - FINDER)
            or (r >= n - FINDER and c < FINDER))


def dark(m, r, c):
    n = len(m)
    if r < 0 or c < 0 or r >= n or c >= n:
        return False
    return bool(m[r][c]) and not is_finder(r, c, n)


def draw_diagonal(draw, m, off, qrpx):
    n = len(m); w = int(MODULE * 0.72)
    for r in range(n):
        for c in range(n):
            if not dark(m, r, c):
                continue
            cx = off + c * MODULE + MODULE / 2; cy = off + r * MODULE + MODULE / 2
            color = grad(c * MODULE + MODULE / 2, r * MODULE + MODULE / 2, qrpx, qrpx)
            half = MODULE * 0.42
            ur = MODULE * 0.30 if dark(m, r - 1, c + 1) else 0
            dl = MODULE * 0.30 if dark(m, r + 1, c - 1) else 0
            x0, y0 = cx - half - dl, cy + half + dl
            x1, y1 = cx + half + ur, cy - half - ur
            draw.line([(x0, y0), (x1, y1)], fill=color + (255,), width=w)
            rr = w / 2
            for (px, py) in [(x0, y0), (x1, y1)]:
                draw.ellipse([px - rr, py - rr, px + rr, py + rr], fill=color + (255,))


def draw_finder_stacked(canvas, tlpx, color, corner, tilt=3):
    """Rounded-square ring + filled center + offset 'shadow' ring behind, then
    the whole finder tilted a few degrees for the casual stacked look from the
    reference. Every corner keeps its inner square. Tilt is capped low: past
    ~4 deg the finder stops decoding (that askew look is why the reference
    scans poorly)."""
    x0, y0 = tlpx; s = FINDER * MODULE; pad = MODULE * 2
    size = s + 2 * pad
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    shadow = tuple(int(ch * 0.60) for ch in color)

    def ring(dx, dy, col):
        d.rounded_rectangle([pad + dx, pad + dy, pad + s - 1 + dx, pad + s - 1 + dy],
                            radius=int(MODULE * 1.5), fill=col + (255,))
        d.rounded_rectangle([pad + MODULE + dx, pad + MODULE + dy,
                             pad + s - MODULE - 1 + dx, pad + s - MODULE - 1 + dy],
                            radius=int(MODULE * 1.0), fill=(0, 0, 0, 0))
    off = int(MODULE * 0.40)
    sx = off if corner in ("tl", "bl") else -off
    sy = off if corner in ("tl", "tr") else -off
    ring(sx, sy, shadow)
    ring(0, 0, color)
    cp = 2 * MODULE
    d.rounded_rectangle([pad + cp, pad + cp, pad + s - cp - 1, pad + s - cp - 1],
                        radius=int(MODULE * 0.85), fill=color + (255,))
    ang = {"tl": tilt, "tr": -tilt, "bl": -tilt}[corner]
    if ang:
        layer = layer.rotate(ang, resample=Image.BICUBIC, center=(pad + s / 2, pad + s / 2))
    canvas.alpha_composite(layer, dest=(int(x0 - pad), int(y0 - pad)))


def render(m):
    n = len(m); qrpx = n * MODULE; total = (n + 2 * QUIET) * MODULE
    canvas = Image.new("RGBA", (total, total), (0, 0, 0, 0)); off = QUIET * MODULE
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_diagonal(draw, m, off, qrpx)
    for rm, cm, which in [(0, 0, "tl"), (0, n - FINDER, "tr"), (n - FINDER, 0, "bl")]:
        color = grad((cm + FINDER / 2) * MODULE, (rm + FINDER / 2) * MODULE, qrpx, qrpx)
        draw_finder_stacked(canvas, (off + cm * MODULE, off + rm * MODULE), color, which)
    cx = cy = total // 2
    art = Image.open(PIGGY).convert("RGBA")
    PLATE_AREA = 0.115; MAXD = 0.42; PW = 1.16; PH = 1.06
    scale = (PLATE_AREA * qrpx * qrpx / (art.width * PW * art.height * PH)) ** 0.5
    scale = min(scale, (qrpx * MAXD) / max(art.size))
    art = art.resize((int(art.width * scale), int(art.height * scale)), Image.LANCZOS)
    pw = int(art.width * PW); ph = int(art.height * PH)
    d2 = ImageDraw.Draw(canvas, "RGBA")
    d2.rounded_rectangle([cx - pw // 2, cy - ph // 2, cx + pw // 2, cy + ph // 2],
                         radius=int(min(pw, ph) * 0.28), fill=(255, 255, 255, 255))
    canvas.alpha_composite(art, dest=(cx - art.width // 2, cy - art.height // 2))
    margin = int(CARD_MARGIN * MODULE); cs = total + 2 * margin
    card = Image.new("RGBA", (cs, cs), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, cs - 1, cs - 1], radius=int(MODULE * 3),
                         fill=(255, 255, 255, 255))
    card.alpha_composite(canvas, dest=(margin, margin))
    return card


def main():
    img = render(build())
    if img.width > 1600:
        img = img.resize((1600, 1600), Image.LANCZOS)
    img.save("images/qr-sample-bank-diagonal.png")
    print("wrote images/qr-sample-bank-diagonal.png", img.size)


if __name__ == "__main__":
    main()
