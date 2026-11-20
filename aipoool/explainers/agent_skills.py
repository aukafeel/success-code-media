"""Animated explainer: What are agent skills (AIPOOOL, 1080x1080, 30 fps)."""
import sys, json, math, random, subprocess
sys.path.insert(0, "/home/claude/success-code-media/aipoool/tools")
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import brand as B
import make_posts as M

W = H = 1080
FPS = 30
cues = json.load(open("/home/claude/skills/cues.json"))
S = [M.VO_START + s for s in cues["starts"]]   # scene starts
END = M.VO_START + cues["dur"] + 1.4
S.append(END)

INK = (12, 10, 9)
TEAL = (255, 107, 74)
ORANGE = (255, 107, 74)
WHITE = (245, 235, 221)
MUTED = (160, 148, 136)
CARD = (22, 22, 34)
EDGE = (52, 52, 76)
GF = "/usr/share/fonts/truetype/google-fonts/"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
_fc = {}


def F(kind, size):
    key = (kind, size)
    if key not in _fc:
        IN = "/usr/share/fonts/opentype/inter/"
        path = {"b": IN + "InterDisplay-Black.otf", "m": IN + "Inter-Medium.otf", "r": IN + "Inter-Regular.otf",
                "i": GF + "Lora-Italic-Variable.ttf", "mono": MONO}[kind]
        f = ImageFont.truetype(path, size)
        if kind == "i":
            try:
                f.set_variation_by_axes([600])
            except Exception:
                pass
        _fc[key] = f
    return _fc[key]


def cl(x): return max(0.0, min(1.0, x))
def ease(x): x = cl(x); return x * x * (3 - 2 * x)
def pr(u, a, b): return ease((u - a) / (b - a))
def mix(c1, c2, k): return tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3))
def fade(c, a): return tuple(c[:3]) + (int(255 * cl(a)),)


# ---------- static background ----------
def make_bg():
    img = Image.new("RGB", (W, H), INK)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.polygon([(700, -100), (1250, -100), (380, 1200), (-170, 1200)], fill=(22, 16, 12))
    g.ellipse((-350, 700, 450, 1500), fill=(30, 8, 2))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    img = Image.blend(img, glow, 0.0)
    img = Image.fromarray(__import__("numpy").clip(
        __import__("numpy").asarray(img, dtype="int16") + __import__("numpy").asarray(glow, dtype="int16"), 0, 255).astype("uint8"))
    d = ImageDraw.Draw(img)
    return img


BG = make_bg()
random.seed(7)
DOTS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(-4, 4), random.uniform(-8, -2),
         (245, 225, 200), random.uniform(1.0, 2.2)) for _ in range(30)]


def dots(d, t):
    for x, y, vx, vy, c, r in DOTS:
        px = (x + vx * t) % W
        py = (y + vy * t) % H
        tw = 0.45 + 0.35 * math.sin(t * 2 + x)
        d.ellipse((px - r, py - r, px + r, py + r), fill=fade(c, tw * 0.6))


def ctext(d, cx, y, s, f, fill, anchor="mm"):
    d.text((cx, y), s, font=f, fill=fill, anchor=anchor)


def rr(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def label(d, text, a, color=TEAL):
    f = F("b", 24)
    w = d.textlength(text, font=f)
    x = W - 60 - w - 36
    rr(d, (x, 58, W - 60, 102), 22, fill=fade(color, 0.18 * a), outline=fade(color, a), width=2)
    d.text((x + 18, 80), text, font=f, fill=fade(color, a), anchor="lm")


def caption(d, text, a, y=965, color=WHITE):
    ctext(d, W // 2, y + (1 - a) * 20, text, F("m", 34), fade(color, a))


def check(d, x, y, s, c, w=6):
    d.line((x, y + s * 0.5, x + s * 0.38, y + s * 0.88, x + s, y), fill=c, width=w, joint="curve")


# ---------- scenes (u = local time, a = scene opacity) ----------
CREAM = (245, 235, 221)
CORAL = (255, 107, 74)
SAGE = (150, 214, 170)
GOLD = (240, 190, 80)
PAPER = (28, 24, 22)
LINE2 = (70, 62, 56)


def chapter(d, n, title, a, u, accent=CORAL, y=245):
    k = pr(u, 0, .5)
    d.text((90, y - 70), f"{n:02d}", font=F("i", 44), fill=fade(accent, a * k), anchor="lm")
    d.line((160, y - 70, 160 + 120 * k, y - 70), fill=fade(accent, a * k), width=2)
    d.text((90 + (1 - k) * 30, y), title, font=F("b", 64), fill=fade(CREAM, a * k), anchor="lm")


def folder(d, x, y, w, h, c, al, name=None, open_=0.0):
    tab = 0.38 * w
    d.rounded_rectangle((x, y - 22, x + tab, y + 10), 8, fill=fade(mix(INK, c, .9), al))
    d.rounded_rectangle((x, y, x + w, y + h), 14, fill=fade(mix(INK, c, .9), al))
    if open_ > 0:  # front flap tilts down
        fy = y + h * 0.18 + open_ * h * 0.25
        d.polygon([(x, fy), (x + w, fy), (x + w - 10, y + h), (x + 10, y + h)], fill=fade(mix(INK, c, .65), al))
    if name:
        d.text((x + 20, y + h - 26), name, font=F("mono", 22), fill=fade(INK, al), anchor="lm")


def doc(d, x, y, w, h, title, lines, al, accent=CORAL, highlight=-1):
    rr(d, (x, y, x + w, y + h), 16, fill=fade(PAPER, al), outline=fade(LINE2, al), width=2)
    d.text((x + 24, y + 34), title, font=F("mono", 24), fill=fade(accent, al), anchor="lm")
    d.line((x + 24, y + 60, x + w - 24, y + 60), fill=fade(LINE2, al), width=2)
    for i, (txt, t_al) in enumerate(lines):
        yy = y + 96 + i * 50
        if i == highlight:
            rr(d, (x + 14, yy - 22, x + w - 14, yy + 22), 10, fill=fade(mix(PAPER, accent, .25), al * t_al))
        d.text((x + 28, yy), txt, font=F("m", 26), fill=fade(CREAM, al * t_al), anchor="lm")


def s0(img, d, u, a):
    d.text((90, 330 + (1 - pr(u, 0, .6)) * 30), "What are", font=F("b", 96), fill=fade(CREAM, a * pr(u, 0, .6)), anchor="lm")
    d.text((90, 450 + (1 - pr(u, .3, .9)) * 30), "agent skills?", font=F("i", 110), fill=fade(CORAL, a * pr(u, .3, .9)), anchor="lm")
    k = pr(u, 2.6, 3.4)
    d.line((90, 560, 90 + 900 * k, 560), fill=fade(LINE2, a), width=2)
    d.text((90, 620), "Training manuals an AI agent", font=F("m", 40), fill=fade(CREAM, a * pr(u, 3.0, 3.6)), anchor="lm")
    d.text((90, 672), "picks up when it needs them", font=F("m", 40), fill=fade(CREAM, a * pr(u, 3.2, 3.8)), anchor="lm")
    for i, (nm, c) in enumerate([("excel-reports", SAGE), ("brand-style", CORAL), ("pdf-forms", GOLD)]):
        kk = pr(u, 4.2 + i * .35, 4.7 + i * .35)
        x = 90 + i * 310
        folder(d, x, 790 + (1 - kk) * 40, 270, 160, c, a * kk, nm)


def s1(img, d, u, a):
    chapter(d, 1, "A skill is a folder", a, u)
    kf = pr(u, 1.2, 1.8)
    folder(d, 90, 330, 330, 210, CORAL, a * kf, "my-skill/", open_=pr(u, 3.6, 4.3))
    # SKILL.md document emerging
    kd = pr(u, 4.0, 4.8)
    lines = [("name: excel-reports", pr(u, 6.4, 6.9)), ("description: makes sales", pr(u, 7.2, 7.7)),
             ("  reports in Excel", pr(u, 7.4, 7.9)), ("1. Load the data", pr(u, 9.0, 9.4)),
             ("2. Build the summary", pr(u, 9.4, 9.8)), ("3. Add the chart", pr(u, 9.8, 10.2))]
    doc(d, 470 + (1 - kd) * 60, 300, 520, 410, "SKILL.md", lines, a * kd,
        highlight=0 if 6.4 < u < 7.2 else (1 if 7.2 < u < 9.0 else -1))
    k1 = pr(u, 6.4, 6.9); k2 = pr(u, 7.2, 7.7); k3 = pr(u, 9.0, 9.5)
    for i, (t_, c, k_) in enumerate([("name", CORAL, k1), ("description", CORAL, k2), ("instructions", SAGE, k3)]):
        x = [470, 590, 805][i]
        d.text((x, 760), t_, font=F("b", 30), fill=fade(c, a * k_), anchor="lm")
    d.text((90, 880), "The only required file:", font=F("m", 34), fill=fade(MUTED, a * pr(u, 4.6, 5.2)), anchor="lm")
    d.text((470, 880), "SKILL.md", font=F("mono", 36), fill=fade(CORAL, a * pr(u, 4.6, 5.2)), anchor="lm")


def s2(img, d, u, a):
    chapter(d, 2, "Plus helpers", a, u, SAGE)
    folder(d, 90, 360, 330, 210, CORAL, a, "my-skill/", open_=1.0)
    items = [("scripts/", "code it can run", SAGE, 1.1), ("templates/", "ready-made files", GOLD, 1.9),
             ("reference/", "extra guides", CREAM, 2.7)]
    for i, (nm, sub, c, t0) in enumerate(items):
        k = pr(u, t0, t0 + .4)
        y = 330 + i * 150
        x = 480 + (1 - k) * 60
        d.line((420, 470, x, y + 50), fill=fade(LINE2, a * k), width=2)
        rr(d, (x, y, x + 470, y + 105), 18, fill=fade(PAPER, a * k), outline=fade(c, a * k), width=2)
        d.text((x + 28, y + 36), nm, font=F("mono", 30), fill=fade(c, a * k), anchor="lm")
        d.text((x + 28, y + 76), sub, font=F("m", 26), fill=fade(CREAM, a * k * .85), anchor="lm")


SHELF = [("excel-reports", "Sales reports in Excel", SAGE), ("brand-style", "Our colours and fonts", CORAL),
         ("pdf-forms", "Fill in PDF forms", GOLD), ("meeting-notes", "Clean meeting minutes", (140, 170, 255)),
         ("invoices", "Check and file invoices", (200, 160, 255)), ("slides", "Build a slide deck", (255, 180, 140))]


def shelf(d, u, a, k_all, open_idx=-1, open_k=0.0):
    for i, (nm, desc, c) in enumerate(SHELF):
        col, row = i % 2, i // 2
        x, y = 90 + col * 460, 320 + row * 170
        k = k_all(i)
        hl = i == open_idx
        al = a * k * (1 if (open_idx < 0 or hl) else 1 - 0.6 * open_k)
        rr(d, (x, y, x + 430, y + 140), 20, fill=fade(mix(PAPER, c, .18 if hl else .06), al),
           outline=fade(c if hl else LINE2, al), width=3 if hl else 2)
        d.rounded_rectangle((x + 22, y + 26, x + 64, y + 56), 6, fill=fade(c, al))
        d.text((x + 80, y + 42), nm, font=F("mono", 26), fill=fade(c, al), anchor="lm")
        d.text((x + 24, y + 100), desc, font=F("m", 26), fill=fade(CREAM, al * .9), anchor="lm")


def s3(img, d, u, a):
    chapter(d, 3, "Just the labels first", a, u, GOLD)
    shelf(d, u, a, lambda i: pr(u, 0.6 + i * .25, 1.0 + i * .25))
    kk = pr(u, 2.3, 2.9)
    d.text((90, 860), "Name + description only", font=F("b", 40), fill=fade(GOLD, a * kk), anchor="lm")
    d.text((90, 915), "so it can keep many skills ready", font=F("m", 34), fill=fade(CREAM, a * pr(u, 5.4, 6.0)), anchor="lm")


def s4(img, d, u, a):
    chapter(d, 4, "A task comes in", a, u, SAGE)
    kt = pr(u, 0.6, 1.2)
    rr(d, (90, 300, 990, 380), 40, fill=fade(mix(PAPER, SAGE, .2), a * kt), outline=fade(SAGE, a * kt), width=2)
    d.text((130, 340), "“Make a sales report in Excel”", font=F("i", 38), fill=fade(CREAM, a * kt), anchor="lm")
    if u < 4.8:
        km = pr(u, 2.8, 3.6)
        shelf_y = 0
        for i, (nm, desc, c) in enumerate(SHELF[:4]):
            x, y = 90 + (i % 2) * 460, 430 + (i // 2) * 170
            hl = i == 0 and km > 0
            al = a * (1 if (i == 0 or km == 0) else 1 - .6 * km)
            rr(d, (x, y, x + 430, y + 140), 20, fill=fade(mix(PAPER, c, .2 if hl else .06), al),
               outline=fade(c if hl else LINE2, al), width=4 if hl else 2)
            d.text((x + 30, y + 42), nm, font=F("mono", 26), fill=fade(c, al), anchor="lm")
            d.text((x + 30, y + 100), desc, font=F("m", 26), fill=fade(CREAM, al * .9), anchor="lm")
        if km > 0:
            check(d, 470, 450, 34, fade(SAGE, a * km), 6)
    else:
        ko = pr(u, 4.8, 5.6)
        lines = [("1. Load the sales data", pr(u, 6.0, 6.4)), ("2. Group by month and region", pr(u, 6.4, 6.8)),
                 ("3. Add totals and a chart", pr(u, 6.8, 7.2)), ("4. Use the company template", pr(u, 7.2, 7.6))]
        doc(d, 90, 430, 900, 330, "excel-reports/SKILL.md", lines, a * ko, SAGE)
        d.text((90, 830), "Opens it. Follows the steps.", font=F("b", 42), fill=fade(SAGE, a * pr(u, 7.0, 7.6)), anchor="lm")


def s5(img, d, u, a):
    chapter(d, 5, "Only what is needed", a, u, CORAL)
    files = [("SKILL.md", 1, SAGE), ("charts.md", 1, SAGE), ("forms.md", 0, LINE2), ("api-notes.md", 0, LINE2),
             ("template.xlsx", 1, GOLD), ("old-guide.md", 0, LINE2)]
    for i, (nm, used, c) in enumerate(files):
        k = pr(u, 0.4 + i * .12, 0.8 + i * .12)
        col, row = i % 3, i // 3
        x, y = 90 + col * 305, 330 + row * 230
        on = used and u > 1.6
        rr(d, (x, y, x + 280, y + 190), 18, fill=fade(mix(PAPER, c, .2 if on else 0), a * k),
           outline=fade(c if on else LINE2, a * k * (1 if on or not used else .6)), width=3 if on else 2)
        d.text((x + 24, y + 40), nm, font=F("mono", 24), fill=fade(CREAM if on else MUTED, a * k), anchor="lm")
        d.text((x + 24, y + 140), "opened" if on else "not needed", font=F("m", 24),
               fill=fade(c if on else (90, 82, 76), a * k * pr(u, 1.6, 2.0)), anchor="lm")
    d.text((90, 860), "Extra files stay closed until needed", font=F("m", 34), fill=fade(CREAM, a * pr(u, 2.0, 2.6)), anchor="lm")


def s6(img, d, u, a):
    chapter(d, 6, "Write your own", a, u, GOLD)
    d.text((90, 330), "Your company's way of working,", font=F("m", 38), fill=fade(CREAM, a * pr(u, 1.2, 1.8)), anchor="lm")
    d.text((90, 385), "packaged once, reused every time", font=F("i", 40), fill=fade(GOLD, a * pr(u, 1.6, 2.2)), anchor="lm")
    cards = [("brand-style", ["Logo always top left", "Colours: navy + gold", "No emojis in posts"], CORAL, 4.7),
             ("monthly-report", ["Pull last month's sales", "Compare to target", "Email to managers"], SAGE, 6.2)]
    for i, (nm, lines, c, t0) in enumerate(cards):
        k = pr(u, t0, t0 + .5)
        x = 90 + i * 460
        y = 470 + (1 - k) * 50
        rr(d, (x, y, x + 430, y + 380), 22, fill=fade(PAPER, a * k), outline=fade(c, a * k), width=3)
        d.text((x + 28, y + 44), nm + "/", font=F("mono", 28), fill=fade(c, a * k), anchor="lm")
        d.line((x + 28, y + 76, x + 402, y + 76), fill=fade(LINE2, a * k), width=2)
        for j, ln in enumerate(lines):
            d.text((x + 28, y + 130 + j * 70), ln, font=F("m", 28), fill=fade(CREAM, a * k), anchor="lm")
    ctext(d, W // 2, 1000, "illustrative examples", F("r", 22), fade(MUTED, a * .8))


def s7(img, d, u, a):
    k1 = pr(u, 0.4, 1.0)
    d.text((90, 330), "The model is", font=F("m", 50), fill=fade(CREAM, a * k1), anchor="lm")
    d.text((90, 420), "the brain.", font=F("b", 100), fill=fade(CREAM, a * k1), anchor="lm")
    k2 = pr(u, 2.8, 3.4)
    d.line((90, 520, 90 + 900 * k2, 520), fill=fade(LINE2, a), width=2)
    d.text((90, 610), "Skills are", font=F("m", 50), fill=fade(CREAM, a * k2), anchor="lm")
    d.text((90, 710), "the know-how.", font=F("i", 110), fill=fade(CORAL, a * pr(u, 3.0, 3.6)), anchor="lm")
    d.text((90, 830), "picked up for each job", font=F("m", 38), fill=fade(MUTED, a * pr(u, 3.8, 4.4)), anchor="lm")


def s8(img, d, u, a):
    k = pr(u, 0, .6)
    lw = 600
    lg_h = int(B.LOGO.height * lw / B.LOGO.width)
    x, y = (W - lw) // 2, 340
    rr(d, (x - 30, y - 25, x + lw + 30, y + lg_h + 25), 30, fill=INK)
    if k > 0:
        B.logo(img, x, y, w=lw)
        if k < 1:
            ov = Image.new("RGB", (lw + 60, lg_h + 50), INK)
            region = img.crop((x - 30, y - 25, x + lw + 30, y + lg_h + 25))
            img.paste(Image.blend(ov, region, k), (x - 30, y - 25))
    ctext(d, W // 2, y + lg_h + 110, "Follow AIPOOOL", F("b", 52), fade(WHITE, a * pr(u, .3, .9)))
    ctext(d, W // 2, y + lg_h + 180, "to stay ahead in the race of Tech & AI", F("m", 34), fade(TEAL, a * pr(u, .6, 1.2)))


SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8]
XF = 0.35


def frame(t):
    img = BG.copy()
    d = ImageDraw.Draw(img, "RGBA")
    orig = d.text

    def atext(xy, s_, font=None, fill=None, anchor=None, **kw):
        if fill is None or len(fill) < 4 or fill[3] >= 255:
            return orig(xy, s_, font=font, fill=fill[:3] if fill else fill, anchor=anchor, **kw)
        if fill[3] <= 2:
            return
        bb = d.textbbox(xy, s_, font=font, anchor=anchor)
        mw, mh = int(bb[2] - bb[0]) + 6, int(bb[3] - bb[1]) + 6
        mask = Image.new("L", (mw, mh), 0)
        ImageDraw.Draw(mask).text((xy[0] - bb[0] + 3, xy[1] - bb[1] + 3), s_, font=font, fill=fill[3], anchor=anchor)
        img.paste(Image.new("RGB", (mw, mh), fill[:3]), (int(bb[0]) - 3, int(bb[1]) - 3), mask)
    d.text = atext
    dots(d, t)
    si = max(i for i in range(len(SCENES)) if t >= S[i] - (0 if i == 0 else 0)) if t >= S[0] else 0
    si = min(si, len(SCENES) - 1)
    u = t - S[si]
    a = pr(u, 0, XF) if si else pr(u, 0, 0.3)
    if si < len(SCENES) - 1:
        a = min(a, 1 - pr(t, S[si + 1] - XF, S[si + 1]))
    else:
        a = min(a, 1 - pr(t, END - 0.8, END))
    if si != 8:
        B.logo(img, 60, 52, w=220)
    SCENES[si](img, d, u, a)
    # progress bar
    px = int(90 + (W - 180) * t / END)
    d.line((90, H - 40, W - 90, H - 40), fill=(48, 42, 38), width=2)
    d.line((90, H - 40, px, H - 40), fill=(255, 107, 74), width=3)
    d.ellipse((px - 6, H - 46, px + 6, H - 34), fill=(255, 107, 74))
    return img


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        for t in [float(x) for x in sys.argv[2:]]:
            frame(t).save(f"/home/claude/skills/p_{t:05.1f}.jpg", quality=88)
        sys.exit()
    n = int(END * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
                          "-pix_fmt", "yuv420p", "/home/claude/skills/silent_tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    import os
    os.replace("/home/claude/skills/silent_tmp.mp4", "/home/claude/skills/silent.mp4")
    M.mix_voice("/home/claude/skills/silent.mp4", "/home/claude/skills/vo.mp3", "/home/claude/skills/skills_explainer.mp4", M.VO_START)
    print("done", END)
