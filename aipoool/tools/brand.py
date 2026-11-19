"""AIPOOOL drawing kit. The logo is fixed; colours, fonts and background decoration come from a theme.

Images (18:30 posts) use the default "gold" theme. Videos rotate themes via set_theme(name).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math, random, os

W = H = 1080
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = Image.open(os.path.join(HERE, "logo_crop.png")).convert("RGB")

INTER = "/usr/share/fonts/opentype/inter/"
GF = "/usr/share/fonts/truetype/google-fonts/"
DJ = "/usr/share/fonts/truetype/dejavu/"
LIB = "/usr/share/fonts/truetype/liberation/"

FONTSETS = {
    "inter": {w: INTER + f"Inter-{w}.otf" for w in ["Black", "ExtraBold", "Bold", "SemiBold", "Medium"]},
    "display": {w: INTER + f"InterDisplay-{w}.otf" for w in ["Black", "ExtraBold", "Bold", "SemiBold", "Medium"]},
    "poppins": {"Black": GF + "Poppins-Bold.ttf", "ExtraBold": GF + "Poppins-Bold.ttf", "Bold": GF + "Poppins-Bold.ttf",
                "SemiBold": GF + "Poppins-Medium.ttf", "Medium": GF + "Poppins-Regular.ttf"},
    "condensed": {"Black": DJ + "DejaVuSansCondensed-Bold.ttf", "ExtraBold": DJ + "DejaVuSansCondensed-Bold.ttf",
                  "Bold": DJ + "DejaVuSansCondensed-Bold.ttf", "SemiBold": DJ + "DejaVuSansCondensed.ttf",
                  "Medium": DJ + "DejaVuSansCondensed.ttf"},
    "terminal": {"Black": LIB + "LiberationMono-Bold.ttf", "ExtraBold": INTER + "Inter-ExtraBold.otf",
                 "Bold": LIB + "LiberationMono-Bold.ttf", "SemiBold": INTER + "Inter-SemiBold.otf",
                 "Medium": INTER + "Inter-Medium.otf"},
}

# name: ink (background), accent, glow, card, edge, panel, text, muted, fonts, deco
THEMES = {
    "gold":   dict(ink=(8, 8, 10), accent=(247, 160, 10), glow=(120, 92, 10), card=(22, 22, 26), edge=(60, 54, 30),
                   panel=(34, 28, 12), txt=(232, 232, 236), muted=(150, 150, 160), fonts="inter", deco="network"),
    "cyan":   dict(ink=(5, 11, 26), accent=(34, 211, 238), glow=(6, 70, 110), card=(13, 24, 46), edge=(30, 70, 100),
                   panel=(10, 40, 62), txt=(226, 238, 250), muted=(125, 150, 178), fonts="poppins", deco="circuit"),
    "mint":   dict(ink=(5, 15, 12), accent=(52, 211, 153), glow=(8, 80, 55), card=(13, 30, 25), edge=(30, 80, 62),
                   panel=(10, 46, 36), txt=(225, 242, 235), muted=(128, 160, 150), fonts="display", deco="rings"),
    "coral":  dict(ink=(17, 8, 11), accent=(251, 113, 133), glow=(110, 25, 45), card=(32, 17, 22), edge=(90, 40, 52),
                   panel=(58, 22, 32), txt=(245, 228, 232), muted=(172, 138, 148), fonts="condensed", deco="stripes"),
    "violet": dict(ink=(11, 8, 24), accent=(167, 139, 250), glow=(60, 35, 120), card=(24, 18, 44), edge=(70, 55, 120),
                   panel=(40, 30, 78), txt=(236, 232, 250), muted=(150, 140, 182), fonts="poppins", deco="waves"),
    "signal": dict(ink=(10, 10, 10), accent=(250, 204, 21), glow=(90, 75, 5), card=(22, 22, 20), edge=(70, 64, 20),
                   panel=(40, 36, 8), txt=(240, 240, 232), muted=(150, 150, 140), fonts="terminal", deco="scan"),
}
VIDEO_THEMES = ["cyan", "mint", "coral", "violet", "signal", "gold"]

THEME = "gold"
GOLD = INK = GOLD_DIM = CARD = EDGE = PANEL = TXT = MUTED = None
_FONTS = FONTSETS["inter"]
DECO = "network"


def set_theme(name):
    global THEME, GOLD, INK, GOLD_DIM, CARD, EDGE, PANEL, TXT, MUTED, _FONTS, DECO
    t = THEMES[name]
    THEME, GOLD, INK, GOLD_DIM, CARD = name, t["accent"], t["ink"], t["glow"], t["card"]
    EDGE, PANEL, TXT, MUTED = t["edge"], t["panel"], t["txt"], t["muted"]
    _FONTS, DECO = FONTSETS[t["fonts"]], t["deco"]


set_theme("gold")


def font(w, s):
    return ImageFont.truetype(_FONTS.get(w, _FONTS["Bold"]), s)


def logo(img, x, y, w=300):
    """Paste the official AIPOOOL logo (its black background screened away)."""
    lg = LOGO.resize((w, int(LOGO.height * w / LOGO.width)), Image.LANCZOS)
    region = img.crop((x, y, x + lg.width, y + lg.height))
    img.paste(ImageChops.lighter(region, lg), (x, y))


def _shade(c, k):
    return tuple(int(v * k) for v in c)


def background(seed=1):
    img = Image.new("RGB", (W, H), INK)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((600, -300, 1400, 500), fill=GOLD_DIM)
    g.ellipse((-400, 700, 300, 1400), fill=_shade(GOLD_DIM, 0.5))
    glow = glow.filter(ImageFilter.GaussianBlur(200))
    img = Image.blend(img, glow, 0.55)
    d = ImageDraw.Draw(img)
    line = tuple(min(255, v + 10) for v in INK)
    dim = _shade(GOLD, 0.38)
    random.seed(seed)
    if DECO == "network":
        for gx in range(0, W, 60):
            d.line([(gx, 0), (gx, H)], fill=line, width=1)
        for gy in range(0, H, 60):
            d.line([(0, gy), (W, gy)], fill=line, width=1)
        pts = [(random.randint(640, 1060), random.randint(40, 380)) for _ in range(15)]
        for i, p in enumerate(pts):
            for q in pts[i + 1:]:
                if math.dist(p, q) < 150:
                    d.line([p, q], fill=dim, width=2)
        for p in pts:
            d.ellipse((p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4), fill=GOLD)
    elif DECO == "circuit":
        for gx in range(0, W, 40):
            for gy in range(0, H, 40):
                d.point((gx, gy), fill=line)
        for _ in range(9):
            x, y = random.randrange(620, 1040, 40), random.randrange(40, 400, 40)
            x2 = x + random.choice([-120, -80, 80, 120])
            y2 = y + random.choice([40, 80, 120])
            d.line([(x, y), (x2, y), (x2, y2)], fill=dim, width=3)
            d.ellipse((x - 6, y - 6, x + 6, y + 6), outline=GOLD, width=2)
            d.ellipse((x2 - 5, y2 - 5, x2 + 5, y2 + 5), fill=GOLD)
    elif DECO == "rings":
        cx, cy = 930, 170
        for r in range(40, 360, 38):
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=dim if r % 76 else _shade(GOLD, 0.6), width=2)
        for _ in range(6):
            a = random.uniform(0, math.tau); r = random.choice(range(40, 360, 38))
            x, y = cx + r * math.cos(a), cy + r * math.sin(a)
            d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=GOLD)
    elif DECO == "stripes":
        for k in range(-H, W, 46):
            d.line([(k + 560, 0), (k + 560 + 420, 420)], fill=line, width=10)
        d.polygon([(760, 0), (1080, 0), (1080, 320)], fill=_shade(GOLD, 0.22))
        d.line([(760, 0), (1080, 320)], fill=GOLD, width=4)
    elif DECO == "waves":
        for j in range(7):
            pts = [(x, 140 + j * 34 + 40 * math.sin(x / 90 + j * 0.6)) for x in range(560, W + 10, 10)]
            d.line(pts, fill=dim if j % 2 else _shade(GOLD, 0.6), width=3)
    elif DECO == "scan":
        for gy in range(0, H, 6):
            d.line([(0, gy), (W, gy)], fill=line, width=1)
        for i in range(8):
            x = 700 + i * 44
            h = random.randint(60, 300)
            d.rectangle((x, 420 - h, x + 26, 420), fill=dim if i % 3 else GOLD)
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
    d.rounded_rectangle((x, y, x + cw, y + ch), radius=26, fill=mix(CARD), outline=mix(EDGE), width=2)
    d.rectangle((x, y + 30, x + 6, y + 100), fill=mix(GOLD))
    bf = font("Black", 60)
    while d.textlength(big, font=bf) > cw - 60 and bf.size > 34:
        bf = font("Black", bf.size - 4)
    d.text((x + 36, y + 30), big, font=bf, fill=mix(GOLD))
    d.multiline_text((x + 36, y + 120), small, font=font("Medium", 27), fill=mix(TXT), spacing=10)


def footer(d):
    d.text((72, 1036), "Empowering AI Innovators  ·  Follow AIPOOOL", font=font("Medium", 22), fill=MUTED, anchor="ls")
