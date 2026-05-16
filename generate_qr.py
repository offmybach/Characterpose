"""Generate the Clarence Gets a Bargain QR code.

Produces images/clarence-qr.png: purple-to-teal gradient, rounded modules,
center modules intact (no knockout box), a faded-purple radial halo behind
the piggy bank, and the bank scaled 50% larger than the previous version.
"""

from __future__ import annotations

import math
from pathlib import Path

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


def draw_finder(canvas: Image.Image, top_left_px: tuple[int, int], color: tuple[int, int, int]):
    """Draw a rounded finder pattern: outer ring + solid inner square."""
    x, y = top_left_px
    size = FINDER_SIZE * MODULE_PX
    draw = ImageDraw.Draw(canvas, "RGBA")
    outer_radius = int(MODULE_PX * 1.6)
    ring_thickness = MODULE_PX  # 1 module thick
    # outer rounded square
    draw.rounded_rectangle(
        [x, y, x + size - 1, y + size - 1],
        radius=outer_radius,
        fill=color + (255,),
    )
    # knock out interior
    inner_x = x + ring_thickness
    inner_y = y + ring_thickness
    inner_size = size - 2 * ring_thickness
    inner_radius = int(MODULE_PX * 1.1)
    draw.rounded_rectangle(
        [inner_x, inner_y, inner_x + inner_size - 1, inner_y + inner_size - 1],
        radius=inner_radius,
        fill=(0, 0, 0, 0),
    )
    # solid inner 3x3
    pad = 2 * MODULE_PX
    core_x = x + pad
    core_y = y + pad
    core_size = size - 2 * pad
    core_radius = int(MODULE_PX * 0.9)
    draw.rounded_rectangle(
        [core_x, core_y, core_x + core_size - 1, core_y + core_size - 1],
        radius=core_radius,
        fill=color + (255,),
    )


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

    # Finder patterns
    finder_positions_modules = [
        (0, 0),
        (0, n - FINDER_SIZE),
        (n - FINDER_SIZE, 0),
    ]
    for (rm, cm) in finder_positions_modules:
        cx_local = (cm + FINDER_SIZE / 2) * MODULE_PX
        cy_local = (rm + FINDER_SIZE / 2) * MODULE_PX
        color = gradient_color(cx_local, cy_local, qr_pixel_size, qr_pixel_size)
        draw_finder(
            canvas,
            (offset + cm * MODULE_PX, offset + rm * MODULE_PX),
            color,
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

    bank_target_w = int(w * 0.33)  # ~50% larger than the previous ~22% center
    halo_radius = int(bank_target_w * 1.05)

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
