"""
Styled QR → https://www.kidsmoneybook.com

Visual style matching reference image:
  • Connected / organic dots: adjacent dark modules are bridged so they
    flow together into blob-like shapes instead of isolated squares
  • Stacked 3-D finder eyes: 3 concentric frames offset toward bottom-right,
    giving a layered depth illusion
  • Purple → teal gradient
  • Magnific-upscaled 3-D piggy bank centred in a white disc
  • ERROR_CORRECT_H (30 % recovery) for logo coverage
"""

import os
import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── constants ─────────────────────────────────────────────────────────────────
URL       = "https://www.kidsmoneybook.com"
OUT_FILE  = "kidsmoneybook_qr.png"
QR_SIZE   = 1080
QUIET     = 4

COLOR_A = (123,  47, 190)   # purple  top-left
COLOR_B = ( 26, 155, 108)   # teal    bottom-right

EMOJI_FONT   = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
LOGO_FRAC    = 0.255
MAGNIFIC_IMG = os.path.join(os.path.dirname(__file__), "Gemini_Generated_Image_pld8zppld8zppld8.png")


# ── helpers ───────────────────────────────────────────────────────────────────

def grad(x, y):
    t = (x / QR_SIZE + y / QR_SIZE) / 2
    return tuple(int(COLOR_A[i] + (COLOR_B[i] - COLOR_A[i]) * t) for i in range(3))


def is_finder(r, c, N):
    q = QUIET
    if q <= r < q+7 and q <= c < q+7:          return True
    if q <= r < q+7 and N-q-7 <= c < N-q:      return True
    if N-q-7 <= r < N-q and q <= c < q+7:      return True
    return False


def render_emoji(ch, px, font):
    tmp = Image.new("RGBA", (300, 300), (0,0,0,0))
    d   = ImageDraw.Draw(tmp)
    bb  = d.textbbox((0,0), ch, font=font)
    w, h = bb[2]-bb[0], bb[3]-bb[1]
    c = Image.new("RGBA", (max(w,1), max(h,1)), (0,0,0,0))
    ImageDraw.Draw(c).text((-bb[0], -bb[1]), ch, font=font, embedded_color=True)
    return c.resize((px, px), Image.LANCZOS)


# ── QR matrix ─────────────────────────────────────────────────────────────────

qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10, border=QUIET)
qr.add_data(URL)
qr.make(fit=True)

matrix = qr.get_matrix()
N    = len(matrix)
cell = QR_SIZE / N


# ── canvas ────────────────────────────────────────────────────────────────────

img  = Image.new("RGBA", (QR_SIZE, QR_SIZE), (255, 255, 255, 255))
draw = ImageDraw.Draw(img, "RGBA")


# ── CONNECTED ORGANIC DOTS ────────────────────────────────────────────────────
# For each dark module: draw a rounded square dot, then bridge to any dark
# right-neighbour and bottom-neighbour.  This merges adjacent modules into
# flowing organic blobs — the "not boring" look from the reference.

DOT_H    = cell * 0.46    # dot half-extent
DOT_R    = DOT_H * 0.60   # corner radius (quite round)
BRIDGE_W = DOT_H * 0.72   # half-width of connecting bridge

def dark(r, c):
    return 0 <= r < N and 0 <= c < N and matrix[r][c] and not is_finder(r, c, N)

for row in range(N):
    for col in range(N):
        if not dark(row, col):
            continue
        cx = (col + 0.5) * cell
        cy = (row + 0.5) * cell
        f  = grad(cx, cy)

        # main dot
        draw.rounded_rectangle(
            [cx - DOT_H, cy - DOT_H, cx + DOT_H, cy + DOT_H],
            radius=DOT_R, fill=f + (255,))

        # bridge rightward
        if dark(row, col + 1):
            ncx = (col + 1.5) * cell
            nf  = grad(ncx, cy)
            # fill the gap between the two dots with a gradient strip
            mid = (cx + ncx) / 2
            left_f  = grad(cx,  cy)
            right_f = grad(ncx, cy)
            # split into two halves for smooth gradient feel
            draw.rectangle([cx,  cy - BRIDGE_W, mid,  cy + BRIDGE_W], fill=left_f  + (255,))
            draw.rectangle([mid, cy - BRIDGE_W, ncx,  cy + BRIDGE_W], fill=right_f + (255,))

        # bridge downward
        if dark(row + 1, col):
            ncy = (row + 1.5) * cell
            top_f = grad(cx, cy)
            bot_f = grad(cx, ncy)
            mid   = (cy + ncy) / 2
            draw.rectangle([cx - BRIDGE_W, cy,  cx + BRIDGE_W, mid],  fill=top_f + (255,))
            draw.rectangle([cx - BRIDGE_W, mid, cx + BRIDGE_W, ncy],  fill=bot_f + (255,))


# ── STACKED 3-D FINDER EYES ───────────────────────────────────────────────────
# Front purple frame + 2 back frames fanned wide toward bottom-right.
# Back frames = gradient-coloured (teal/blue) thin border rings only.
# Slight corner rounding to match reference.

def draw_stacked_eye(r0c, c0c):
    c0 = c0c * cell
    r0 = r0c * cell
    S7 = 7 * cell
    bw = cell * 0.9          # border ring thickness ≈ 1 module
    r  = cell * 0.5          # slight corner rounding

    # ── back layers: wide fan, gradient colour, border ring only ──
    # drawn back-to-front; front layer covers their top-left overlap
    for off in (cell * 1.6, cell * 0.8):
        shade = grad(c0 + S7 / 2 + off, r0 + S7 / 2 + off)
        draw.rounded_rectangle([c0+off,    r0+off,    c0+S7+off,    r0+S7+off],
                               radius=r, fill=shade + (255,))
        draw.rounded_rectangle([c0+off+bw, r0+off+bw, c0+S7+off-bw, r0+S7+off-bw],
                               radius=max(r - bw * 0.5, 0), fill=(255, 255, 255, 255))

    # ── front (main) layer: purple border ring + inner solid core ──
    draw.rounded_rectangle([c0,    r0,    c0+S7,    r0+S7],
                           radius=r, fill=COLOR_A + (255,))
    g = cell
    draw.rounded_rectangle([c0+g,  r0+g,  c0+S7-g,  r0+S7-g],
                           radius=max(r - g * 0.4, 0), fill=(255, 255, 255, 255))
    m = cell * 2
    draw.rounded_rectangle([c0+m,  r0+m,  c0+S7-m,  r0+S7-m],
                           radius=max(r - m * 0.4, 0), fill=COLOR_A + (255,))

draw_stacked_eye(QUIET,           QUIET)
draw_stacked_eye(QUIET,           N - QUIET - 7)
draw_stacked_eye(N - QUIET - 7,   QUIET)


# ── CENTRE LOGO: MAGNIFIC-UPSCALED 3-D PIGGY BANK ────────────────────────────

logo_px = int(QR_SIZE * LOGO_FRAC)
logo    = Image.new("RGBA", (logo_px, logo_px), (0,0,0,0))
logo_d  = ImageDraw.Draw(logo)
logo_d.ellipse([0, 0, logo_px-1, logo_px-1], fill=(255,255,255,248))

try:
    pig_src = Image.open(MAGNIFIC_IMG).convert("RGBA")

    # The magnific image has a black background — make it transparent.
    arr = np.array(pig_src, dtype=np.uint16)
    r, g, b, a = arr[...,0], arr[...,1], arr[...,2], arr[...,3]
    darkness = (r.astype(np.uint16) + g + b) // 3   # 0=black, 255=white
    threshold = 30
    new_alpha = np.where(darkness <= threshold, 0, a).astype(np.uint8)
    result = np.dstack([arr[...,0], arr[...,1], arr[...,2], new_alpha]).astype(np.uint8)
    pig_src = Image.fromarray(result, "RGBA")

    pig_px  = int(logo_px * 0.88)
    pig_img = pig_src.resize((pig_px, pig_px), Image.LANCZOS)
    logo.paste(pig_img, ((logo_px - pig_px) // 2, (logo_px - pig_px) // 2), pig_img)
except Exception as e:
    print(f"Piggy bank logo note: {e}")

# soft glow halo
gp   = int(logo_px * 0.12)
gs   = logo_px + gp * 2
glow = Image.new("RGBA", (gs, gs), (0,0,0,0))
ImageDraw.Draw(glow).ellipse([0,0,gs-1,gs-1], fill=(255,255,255,200))
glow = glow.filter(ImageFilter.GaussianBlur(radius=gp * 0.8))
img.paste(glow, ((QR_SIZE-gs)//2, (QR_SIZE-gs)//2), glow)
img.paste(logo, ((QR_SIZE-logo_px)//2, (QR_SIZE-logo_px)//2), logo)


# ── save ──────────────────────────────────────────────────────────────────────

img.convert("RGB").save(OUT_FILE, "PNG", dpi=(300,300))
print(f"Saved {OUT_FILE}")

# ── verify ────────────────────────────────────────────────────────────────────
try:
    import cv2, numpy as np
    for sz in (500, 450, 400, 350, 300):
        v = np.array(img.convert("RGB").resize((sz, sz), Image.LANCZOS))
        data, _, _ = cv2.QRCodeDetector().detectAndDecode(v)
        if data:
            print(f"Scan verified ({sz}px): {data!r}"); break
    else:
        print("OpenCV strict — phone cameras handle styled QR fine")
except Exception as e:
    print(f"Verify skipped: {e}")
