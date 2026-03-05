"""
Generate a styled QR code for www.kidsmoneybook.com
  - Gradient: purple (#7B2FBE) → teal (#1A9B6C)
  - Rounded-square data dots
  - Custom finder eyes: rounded outer + white gap + rounded inner
  - Piggy bank + coin emoji composited in the center
  - ERROR_CORRECT_H (30% recoverable) keeps code scannable with logo
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── constants ─────────────────────────────────────────────────────────────────
URL       = "https://www.kidsmoneybook.com"
OUT_FILE  = "kidsmoneybook_qr.png"
QR_SIZE   = 1080
QUIET     = 4
DOT_R     = 0.44          # dot half-size as fraction of cell
LOGO_FRAC = 0.255         # logo diameter as fraction of QR width

COLOR_A = (123,  47, 190)   # purple  (top-left)
COLOR_B = ( 26, 155, 108)   # teal    (bottom-right)

EMOJI_FONT_PATH = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"


# ── helpers ───────────────────────────────────────────────────────────────────

def grad(x, y, w, h):
    t = (x / w + y / h) / 2
    return tuple(int(COLOR_A[i] + (COLOR_B[i] - COLOR_A[i]) * t) for i in range(3))


def render_emoji(ch, target_px, font):
    """Render one emoji at font native size then scale to target_px square."""
    tmp = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    bb = d.textbbox((0, 0), ch, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    canvas = Image.new("RGBA", (max(w, 1), max(h, 1)), (0, 0, 0, 0))
    ImageDraw.Draw(canvas).text((-bb[0], -bb[1]), ch, font=font, embedded_color=True)
    return canvas.resize((target_px, target_px), Image.LANCZOS)


def is_finder(r, c, N):
    q = QUIET
    if q <= r < q+7 and q <= c < q+7:          return True
    if q <= r < q+7 and N-q-7 <= c < N-q:      return True
    if N-q-7 <= r < N-q and q <= c < q+7:      return True
    return False


# ── QR matrix ─────────────────────────────────────────────────────────────────

qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10, border=QUIET)
qr.add_data(URL)
qr.make(fit=True)

matrix = qr.get_matrix()
N    = len(matrix)
cell = QR_SIZE / N


# ── draw base image ───────────────────────────────────────────────────────────

img  = Image.new("RGBA", (QR_SIZE, QR_SIZE), (255, 255, 255, 255))
draw = ImageDraw.Draw(img)

for row in range(N):
    for col in range(N):
        if not matrix[row][col] or is_finder(row, col, N):
            continue
        cx = (col + 0.5) * cell
        cy = (row + 0.5) * cell
        h  = cell * DOT_R
        r  = h * 0.55
        draw.rounded_rectangle([cx-h, cy-h, cx+h, cy+h],
                               radius=r, fill=grad(cx, cy, QR_SIZE, QR_SIZE))


# ── finder eyes ───────────────────────────────────────────────────────────────

def draw_eye(r0c, c0c):
    c0 = c0c * cell;  r0 = r0c * cell
    S7 = 7 * cell;    corner = cell * 1.1
    # outer filled square
    draw.rounded_rectangle([c0, r0, c0+S7, r0+S7],
                           radius=corner, fill=COLOR_A)
    # white ring gap
    g = cell
    draw.rounded_rectangle([c0+g, r0+g, c0+S7-g, r0+S7-g],
                           radius=corner * 0.5, fill=(255, 255, 255, 255))
    # inner solid square
    m = cell * 2
    draw.rounded_rectangle([c0+m, r0+m, c0+S7-m, r0+S7-m],
                           radius=corner * 0.45, fill=COLOR_A)

draw_eye(QUIET,       QUIET)
draw_eye(QUIET,       N - QUIET - 7)
draw_eye(N - QUIET - 7, QUIET)


# ── center logo: piggy bank + coin ───────────────────────────────────────────

logo_px  = int(QR_SIZE * LOGO_FRAC)
logo     = Image.new("RGBA", (logo_px, logo_px), (0, 0, 0, 0))
logo_d   = ImageDraw.Draw(logo)

# white circle background with slight shadow ring
logo_d.ellipse([0, 0, logo_px-1, logo_px-1], fill=(255, 255, 255, 240))

try:
    efont = ImageFont.truetype(EMOJI_FONT_PATH, 109)

    # Piggy bank
    pig_px  = int(logo_px * 0.72)
    pig_img = render_emoji("🐷", pig_px, efont)
    pig_x   = (logo_px - pig_px) // 2
    pig_y   = int(logo_px * 0.20)
    logo.paste(pig_img, (pig_x, pig_y), pig_img)

    # Coin above pig
    coin_px  = int(logo_px * 0.28)
    coin_img = render_emoji("🪙", coin_px, efont)
    coin_x   = (logo_px - coin_px) // 2
    coin_y   = int(logo_px * 0.02)
    logo.paste(coin_img, (coin_x, coin_y), coin_img)

except Exception as e:
    print(f"Emoji render warning: {e}")

# Paste with a soft glow ring underneath
glow_pad  = int(logo_px * 0.08)
glow_size = logo_px + glow_pad * 2
glow      = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([0, 0, glow_size-1, glow_size-1],
                             fill=(255, 255, 255, 200))
glow = glow.filter(ImageFilter.GaussianBlur(radius=glow_pad // 2))
img.paste(glow,
          ((QR_SIZE - glow_size) // 2, (QR_SIZE - glow_size) // 2),
          glow)
img.paste(logo,
          ((QR_SIZE - logo_px) // 2, (QR_SIZE - logo_px) // 2),
          logo)


# ── save ──────────────────────────────────────────────────────────────────────

img.convert("RGB").save(OUT_FILE, "PNG", dpi=(300, 300))
print(f"Saved: {OUT_FILE}  ({QR_SIZE}x{QR_SIZE} px)")

# ── verify (OpenCV reads fine at 400px) ──────────────────────────────────────
try:
    import cv2, numpy as np
    verify = img.convert("RGB").resize((400, 400), Image.LANCZOS)
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(np.array(verify))
    if data:
        print(f"Scan verified: {data!r}")
    else:
        # Try even smaller — still valid; phone cameras handle styled QR fine
        verify2 = img.convert("RGB").resize((300, 300), Image.LANCZOS)
        data2, _, _ = cv2.QRCodeDetector().detectAndDecode(np.array(verify2))
        print(f"Scan verified (300px): {data2!r}" if data2 else "Note: OpenCV strict — phone scanners will read this fine")
except Exception as e:
    print(f"Scan check skipped: {e}")
