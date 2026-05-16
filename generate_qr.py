"""Generate the Clarence Gets a Bargain QR code.

Produces images/clarence-qr.png: purple-to-teal gradient, rounded modules,
center modules intact (no knockout box), a faded-purple radial halo behind
the piggy bank, and the bank scaled 50% larger than the previous version.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent
PIGGY_SRC = ROOT / "images" / "piggy-bank.png"
OUT_PATH = ROOT / "images" / "clarence-qr.png"
URL = "https://www.clarencegetsabargain.com"

# Gradient endpoints sampled from the reference QR
TOP_LEFT = (108, 28, 200)     # vivid purple
TOP_RIGHT = (60, 60, 188)     # purple-blue
BOTTOM_LEFT = (60, 96, 180)   # blue
BOTTOM_RIGHT = (28, 168, 130) # teal/green

MODULE_PX = 28           # px per QR module in the working canvas
QUIET_MODULES = 2        # quiet zone (modules)
FINDER_SIZE = 7          # standard finder module size
DOT_RATIO = 0.78         # fill ratio for rounded data dots

PURPLE_HALO = (138, 78, 220)  # faded purple behind bank


def gradient_color(x: float, y: float, w: float, h: float) -> tuple[int, int, int]:
    """Bilinear blend across the four corner colors."""
    fx = max(0.0, min(1.0, x / max(w - 1, 1)))
    fy = max(0.0, min(1.0, y / max(h - 1, 1)))
    top = tuple(TOP_LEFT[i] * (1 - fx) + TOP_RIGHT[i] * fx for i in range(3))
    bot = tuple(BOTTOM_LEFT[i] * (1 - fx) + BOTTOM_RIGHT[i] * fx for i in range(3))
    out = tuple(top[i] * (1 - fy) + bot[i] * fy for i in range(3))
    return tuple(int(round(c)) for c in out)


def build_matrix(url: str):
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=1,
        border=0,
    )
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    return matrix  # list[list[bool]]


def is_finder(r: int, c: int, n: int) -> bool:
    """Inside one of the three 7x7 finder patterns?"""
    return (
        (r < FINDER_SIZE and c < FINDER_SIZE)
        or (r < FINDER_SIZE and c >= n - FINDER_SIZE)
        or (r >= n - FINDER_SIZE and c < FINDER_SIZE)
    )


def _perspective_coeffs(target_quad, source_quad):
    """Find 8-coeff perspective mapping output target_quad -> input source_quad.

    Returns coefficients suitable for PIL Image.transform(size, PERSPECTIVE, ...).
    """
    A = []
    for (xt, yt), (xs, ys) in zip(target_quad, source_quad):
        A.append([xt, yt, 1, 0, 0, 0, -xt * xs, -yt * xs])
        A.append([0, 0, 0, xt, yt, 1, -xt * ys, -yt * ys])
    A = np.array(A, dtype=np.float64)
    B = np.array([c for pt in source_quad for c in pt], dtype=np.float64)
    return np.linalg.solve(A, B)


def draw_finder(canvas: Image.Image, top_left_px: tuple[int, int],
                color: tuple[int, int, int], corner: str):
    """Draw a 3D-perspective finder pattern.

    Renders the standard rounded outer-ring + solid-core on its own layer,
    then perspective-transforms it so the outer-facing corner is pushed
    outward — producing the stacked-trapezoid / leaning-cube look.

    corner: 'tl', 'tr', or 'bl' — which corner of the QR this finder is in.
    """
    x0, y0 = top_left_px
    s = FINDER_SIZE * MODULE_PX

    # Work on a padded canvas so the perspective transform has room.
    pad = MODULE_PX * 2
    canvas_size = s + 2 * pad
    layer = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    outer_radius = int(MODULE_PX * 1.6)
    inner_radius = int(MODULE_PX * 1.1)
    core_radius = int(MODULE_PX * 0.9)

    # outer rounded square
    d.rounded_rectangle(
        [pad, pad, pad + s - 1, pad + s - 1],
        radius=outer_radius,
        fill=color + (255,),
    )
    # knock out interior (1 module thick ring)
    d.rounded_rectangle(
        [pad + MODULE_PX, pad + MODULE_PX,
         pad + s - MODULE_PX - 1, pad + s - MODULE_PX - 1],
        radius=inner_radius,
        fill=(0, 0, 0, 0),
    )
    # solid 3x3 core
    core_pad = 2 * MODULE_PX
    d.rounded_rectangle(
        [pad + core_pad, pad + core_pad,
         pad + s - core_pad - 1, pad + s - core_pad - 1],
        radius=core_radius,
        fill=color + (255,),
    )

    # Build target quad: push the outer-facing corner outward, pull the
    # inner-facing corner slightly toward QR center. Creates the leaning,
    # stacked-trapezoid look from the reference.
    push = MODULE_PX * 1.0  # outward extension
    pull = MODULE_PX * 0.45  # inward compression of the opposite corner

    # default corners (rectangle anchored at pad..pad+s)
    tl = [pad, pad]
    tr = [pad + s, pad]
    br = [pad + s, pad + s]
    bl = [pad, pad + s]

    if corner == "tl":   # outer corner = tl, inner-facing = br
        tl = [pad - push, pad - push]
        br = [pad + s - pull, pad + s - pull]
    elif corner == "tr": # outer corner = tr, inner-facing = bl
        tr = [pad + s + push, pad - push]
        bl = [pad + pull, pad + s - pull]
    elif corner == "bl": # outer corner = bl, inner-facing = tr
        bl = [pad - push, pad + s + push]
        tr = [pad + s - pull, pad + pull]
    else:
        raise ValueError(corner)

    target_quad = [tl, tr, br, bl]
    source_quad = [[pad, pad], [pad + s, pad], [pad + s, pad + s], [pad, pad + s]]
    coeffs = _perspective_coeffs(target_quad, source_quad)

    warped = layer.transform(
        (canvas_size, canvas_size),
        Image.PERSPECTIVE,
        coeffs,
        resample=Image.BICUBIC,
    )

    canvas.alpha_composite(warped, dest=(x0 - pad, y0 - pad))


def render_qr(matrix) -> Image.Image:
    n = len(matrix)
    total_modules = n + 2 * QUIET_MODULES
    size_px = total_modules * MODULE_PX
    canvas = Image.new("RGBA", (size_px, size_px), (255, 255, 255, 0))

    offset = QUIET_MODULES * MODULE_PX
    qr_pixel_size = n * MODULE_PX
    dot_size = int(MODULE_PX * DOT_RATIO)
    dot_pad = (MODULE_PX - dot_size) // 2

    draw = ImageDraw.Draw(canvas, "RGBA")

    # Data modules as rounded dots
    for r in range(n):
        for c in range(n):
            if not matrix[r][c]:
                continue
            if is_finder(r, c, n):
                continue
            cx_local = c * MODULE_PX + MODULE_PX // 2
            cy_local = r * MODULE_PX + MODULE_PX // 2
            color = gradient_color(cx_local, cy_local, qr_pixel_size, qr_pixel_size)
            x0 = offset + c * MODULE_PX + dot_pad
            y0 = offset + r * MODULE_PX + dot_pad
            x1 = x0 + dot_size - 1
            y1 = y0 + dot_size - 1
            draw.rounded_rectangle(
                [x0, y0, x1, y1],
                radius=dot_size // 2,
                fill=color + (255,),
            )

    # Finder patterns (with 3D perspective lean)
    finder_positions = [
        (0, 0, "tl"),
        (0, n - FINDER_SIZE, "tr"),
        (n - FINDER_SIZE, 0, "bl"),
    ]
    for (rm, cm, which) in finder_positions:
        cx_local = (cm + FINDER_SIZE / 2) * MODULE_PX
        cy_local = (rm + FINDER_SIZE / 2) * MODULE_PX
        color = gradient_color(cx_local, cy_local, qr_pixel_size, qr_pixel_size)
        draw_finder(
            canvas,
            (offset + cm * MODULE_PX, offset + rm * MODULE_PX),
            color,
            which,
        )

    return canvas


def add_halo_and_bank(canvas: Image.Image, bank_path: Path) -> Image.Image:
    """Add a faded purple radial halo behind a 50%-larger piggy bank.

    Halo layers OVER the QR modules at low opacity (so the gradient dots are
    still visible through it) and UNDER the bank, so the bank reads as sitting
    on a soft purple wash that's clearly distinct from the code itself.
    """
    w, h = canvas.size
    cx, cy = w // 2, h // 2

    bank_target_w = int(w * 0.45)  # +50% bumped to roughly the safe upper limit
    halo_radius = int(bank_target_w * 1.0)

    # Soft radial halo built by stacking ellipses, then blurred.
    halo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    halo_draw = ImageDraw.Draw(halo)
    steps = 80
    for i in range(steps, 0, -1):
        t = i / steps
        radius = int(halo_radius * t)
        # stronger toward the center, fading to zero at the rim
        alpha = int(150 * (1 - t) ** 1.6)
        halo_draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            fill=PURPLE_HALO + (alpha,),
        )
    halo = halo.filter(ImageFilter.GaussianBlur(radius=int(bank_target_w * 0.11)))

    base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    base.alpha_composite(canvas)   # QR first
    base.alpha_composite(halo)     # then the soft purple wash on top of it

    # Piggy bank on top, 50% larger than the prior reference (~22% → 33%).
    bank = Image.open(bank_path).convert("RGBA")
    bw, bh = bank.size
    scale = bank_target_w / bw
    new_size = (int(bw * scale), int(bh * scale))
    bank = bank.resize(new_size, Image.LANCZOS)
    bx = cx - new_size[0] // 2
    by = cy - new_size[1] // 2
    base.alpha_composite(bank, dest=(bx, by))

    return base


def flatten_on_white(img: Image.Image) -> Image.Image:
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bg.paste(img, mask=img.split()[-1])
    return bg


def main():
    matrix = build_matrix(URL)
    qr_img = render_qr(matrix)
    composed = add_halo_and_bank(qr_img, PIGGY_SRC)
    # Downscale slightly for a clean, web-ready size while preserving detail.
    target = 1800
    if composed.width > target:
        ratio = target / composed.width
        composed = composed.resize(
            (target, int(composed.height * ratio)),
            Image.LANCZOS,
        )
    final = flatten_on_white(composed)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    final.save(OUT_PATH, "PNG", optimize=True)
    print(f"Wrote {OUT_PATH} ({final.size[0]}x{final.size[1]})")


if __name__ == "__main__":
    main()
