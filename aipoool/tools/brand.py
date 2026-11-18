from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math, random

W = H = 1080
F = "/usr/share/fonts/opentype/inter/"
GOLD = (247, 160, 10)
LOGO = Image.open("" + __import__("os").path.join(__import__("os").path.dirname(__file__), "logo_crop.png") + "").convert("RGB")
GOLD_DIM = (120, 92, 10)
INK = (8, 8, 10)
CARD = (22, 22, 26)
TXT = (232, 232, 236)
MUTED = (150, 150, 160)

def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)

def logo(img, x, y, w=300):
    """Paste the official AIPOOOL logo (black background screened away)."""
    lg = LOGO.resize((w, int(LOGO.height * w / LOGO.width)), Image.LANCZOS)
    region = img.crop((x, y, x + lg.width, y + lg.height))
    img.paste(ImageChops.lighter(region, lg), (x, y))

def background(seed=1):
    img = Image.new("RGB", (W, H), INK)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((600, -300, 1400, 500), fill=GOLD_DIM)
    glow = glow.filter(ImageFilter.GaussianBlur(200))
    img = Image.blend(img, glow, 0.55)
    d = ImageDraw.Draw(img)
    for gx in range(0, W, 60):
        d.line([(gx, 0), (gx, H)], fill=(18, 18, 20), width=1)
    for gy in range(0, H, 60):
        d.line([(0, gy), (W, gy)], fill=(18, 18, 20), width=1)
    random.seed(seed)
    pts = [(random.randint(640, 1060), random.randint(40, 380)) for _ in range(15)]
    for i, p in enumerate(pts):
        for q in pts[i + 1:]:
            if math.dist(p, q) < 150:
                d.line([p, q], fill=(90, 70, 10), width=2)
    for p in pts:
        d.ellipse((p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4), fill=GOLD)
    return img

def header(img, d, tag, title, title_y=250):
    logo(img, 66, 54, 300)
    tf = font("Bold", 24)
    tw = d.textlength(tag, font=tf)
    d.rounded_rectangle((72, 168, 72 + tw + 44, 214), radius=23, fill=GOLD)
    d.text((94, 175), tag, font=tf, fill=INK)
    d.multiline_text((72, title_y), title, font=font("ExtraBold", 66), fill=(255, 255, 255), spacing=14)

def card(d, i, big, small, alpha=1.0, dy=0):
    cw, ch, gap = 450, 250, 36
    x = 72 + (i % 2) * (cw + gap)
    y = 470 + (i // 2) * (ch + gap) + dy
    def mix(c):  # fade towards background
        return tuple(int(INK[k] + (c[k] - INK[k]) * alpha) for k in range(3))
    d.rounded_rectangle((x, y, x + cw, y + ch), radius=26, fill=mix(CARD), outline=mix((60, 54, 30)), width=2)
    d.rectangle((x, y + 30, x + 6, y + 100), fill=mix(GOLD))
    d.text((x + 36, y + 30), big, font=font("Black", 60), fill=mix(GOLD))
    d.multiline_text((x + 36, y + 120), small, font=font("Medium", 27), fill=mix(TXT), spacing=10)

def footer(d):
    d.text((72, 1036), "Empowering AI Innovators  ·  Follow AIPOOOL", font=font("Medium", 22), fill=MUTED, anchor="ls")
