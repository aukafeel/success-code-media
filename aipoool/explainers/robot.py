"""Animated explainer: How does a robot work (AIPOOOL, 1080x1080, 30 fps)."""
import sys, json, math, random, subprocess
sys.path.insert(0, "/home/claude/success-code-media/aipoool/tools")
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import brand as B
import make_posts as M

W = H = 1080
FPS = 30
cues = json.load(open("/home/claude/robot/cues.json"))
S = [M.VO_START + s for s in cues["starts"]]   # scene starts
END = M.VO_START + cues["dur"] + 1.4
S.append(END)

INK = (4, 4, 7)
TEAL = (34, 211, 238)
ORANGE = (251, 146, 60)
WHITE = (238, 240, 246)
MUTED = (140, 150, 172)
CARD = (22, 22, 34)
EDGE = (52, 52, 76)
GF = "/usr/share/fonts/truetype/google-fonts/"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
_fc = {}


def F(kind, size):
    key = (kind, size)
    if key not in _fc:
        path = {"b": GF + "Poppins-Bold.ttf", "m": GF + "Poppins-Medium.ttf", "r": GF + "Poppins-Regular.ttf",
                "mono": MONO}[kind]
        _fc[key] = ImageFont.truetype(path, size)
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
    g.ellipse((-300, -300, 500, 500), fill=(2, 12, 16))
    g.ellipse((640, 640, 1400, 1400), fill=(18, 8, 2))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img = Image.blend(img, glow, 0.0)
    img = Image.fromarray(__import__("numpy").clip(
        __import__("numpy").asarray(img, dtype="int16") + __import__("numpy").asarray(glow, dtype="int16"), 0, 255).astype("uint8"))
    d = ImageDraw.Draw(img)
    return img


BG = make_bg()
random.seed(7)
DOTS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(-12, 12), random.uniform(-18, -4),
         random.choice([TEAL, ORANGE, (120, 140, 200)]), random.uniform(1.5, 3.2)) for _ in range(55)]


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
CYANC = (34, 211, 238)
VIO = (167, 139, 250)
ORG = (251, 146, 60)
GRN = (52, 211, 153)
BODY = (44, 48, 64)
LINE = (170, 180, 205)


def robot(d, cx, cy, s, a, hl=(), larm=0.15, rarm=0.15, lbend=0.25, rbend=0.25, tilt=0.0, glow=1.0):
    pivot = (cx, cy + 280 * s)
    ct, st = math.cos(tilt), math.sin(tilt)

    def P(x, y):
        X, Y = cx + x * s, cy + y * s
        dx, dy = X - pivot[0], Y - pivot[1]
        return (pivot[0] + dx * ct - dy * st, pivot[1] + dx * st + dy * ct)

    def limb(p0, p1, w):
        d.line((p0, p1), fill=fade(BODY, a), width=int(w * s))
        d.line((p0, p1), fill=fade(LINE, a * .25), width=2)

    def joint(p, r, key):
        on = key in hl
        c = ORG if on else LINE
        if on:
            for g in range(3, 0, -1):
                rg = (r + g * 7) * s
                d.ellipse((p[0] - rg, p[1] - rg, p[0] + rg, p[1] + rg), fill=fade(ORG, a * .12 * g * glow))
        rr_ = r * s
        d.ellipse((p[0] - rr_, p[1] - rr_, p[0] + rr_, p[1] + rr_), fill=fade(mix(BODY, c, .6 if on else .2), a),
                  outline=fade(c, a), width=3)

    def poly(pts, fill, outline):
        d.polygon([P(*p) for p in pts], fill=fade(fill, a), outline=fade(outline, a))

    # legs
    for sx in (-1, 1):
        hip = P(sx * 40, 70); knee = P(sx * 44, 175); foot = P(sx * 46, 262)
        limb(hip, knee, 34); limb(knee, foot, 30)
        poly([(sx * 46 - 34, 258), (sx * 46 + 34, 258), (sx * 46 + 38, 282), (sx * 46 - 38, 282)], BODY, LINE)
        joint(knee, 16, "motors")
        joint(hip, 18, "motors")
    # torso
    poly([(-82, -112), (82, -112), (70, 62), (-70, 62)], BODY, LINE)
    core = P(0, -40)
    cc = GRN if "balance" in hl else (VIO if "brain" in hl else (90, 100, 130))
    rcore = 22 * s
    if "balance" in hl or "brain" in hl:
        for g in range(4, 0, -1):
            rg = rcore + g * 9 * s
            d.ellipse((core[0] - rg, core[1] - rg, core[0] + rg, core[1] + rg), fill=fade(cc, a * .1 * g * glow))
    d.ellipse((core[0] - rcore, core[1] - rcore, core[0] + rcore, core[1] + rcore), fill=fade(cc, a))
    # arms
    for sx, th, bend in ((-1, larm, lbend), (1, rarm, rbend)):
        sh = (sx * 98, -96)
        el = (sh[0] + sx * 100 * math.sin(th), sh[1] + 100 * math.cos(th))
        th2 = th + bend
        ha = (el[0] + sx * 92 * math.sin(th2), el[1] + 92 * math.cos(th2))
        limb(P(*sh), P(*el), 28); limb(P(*el), P(*ha), 24)
        joint(P(*el), 14, "motors")
        joint(P(*sh), 18, "motors")
        hp = P(*ha)
        on = "touch" in hl
        hr = 17 * s
        if on:
            for g in range(3, 0, -1):
                rg = hr + g * 8 * s
                d.ellipse((hp[0] - rg, hp[1] - rg, hp[0] + rg, hp[1] + rg), fill=fade(CYANC, a * .12 * g * glow))
        d.ellipse((hp[0] - hr, hp[1] - hr, hp[0] + hr, hp[1] + hr), fill=fade(CYANC if on else BODY, a), outline=fade(LINE, a), width=2)
    # neck + head
    limb(P(0, -112), P(0, -128), 26)
    poly([(-58, -222), (58, -222), (58, -128), (-58, -128)], BODY, LINE)
    poly([(-44, -200), (44, -200), (44, -160), (-44, -160)], (8, 10, 18), (60, 66, 88))
    ec = CYANC if "eyes" in hl else (120, 200, 230)
    for ex in (-20, 20):
        e = P(ex, -180)
        r = 8 * s
        d.ellipse((e[0] - r, e[1] - r, e[0] + r, e[1] + r), fill=fade(ec, a))
    if "brain" in hl:
        h = P(0, -175)
        for g in range(4, 0, -1):
            rg = (70 + g * 10) * s
            d.ellipse((h[0] - rg, h[1] - rg, h[0] + rg, h[1] + rg), outline=fade(VIO, a * .12 * g * glow), width=3)
    # ears = mics
    for sx in (-1, 1):
        e = P(sx * 64, -175)
        c = CYANC if "ears" in hl else LINE
        d.rounded_rectangle((e[0] - 7 * s, e[1] - 18 * s, e[0] + 7 * s, e[1] + 18 * s), 5, fill=fade(mix(BODY, c, .7), a))
    return P


def waves(d, x, y, u, c, a, direction=1, n=3, spread=0.5):
    for i in range(n):
        ph = (u * 1.2 + i / n) % 1
        r = 20 + ph * 90
        box = (x - r, y - r, x + r, y + r)
        st = -math.degrees(spread) if direction > 0 else 180 - math.degrees(spread)
        d.arc(box, st, st + 2 * math.degrees(spread), fill=fade(c, a * (1 - ph)), width=4)


def tag(d, x, y, txt, c, al, anchor="lm"):
    f = F("b", 30)
    tw = d.textlength(txt, font=f)
    x0 = x if anchor == "lm" else x - tw - 44
    rr(d, (x0, y - 30, x0 + tw + 44, y + 30), 30, fill=fade(mix(INK, c, .25), al), outline=fade(c, al), width=2)
    d.text((x0 + 22, y), txt, font=f, fill=fade(WHITE, al), anchor="lm")


def s0(img, d, u, a):
    ctext(d, W // 2, 190, "How does a", F("b", 76), fade(WHITE, a * pr(u, 0, .6)))
    ctext(d, W // 2, 280, "robot work?", F("b", 88), fade(CYANC, a * pr(u, .3, .9)))
    k = pr(u, 1.0, 2.0)
    robot(d, W // 2, 560 + (1 - k) * 60, 0.8, a * k, hl=("eyes",), larm=0.15 + 0.1 * math.sin(u * 2), rarm=0.15)
    for i, (txt, c, t0) in enumerate([("Sense", CYANC, 4.8), ("Think", VIO, 5.6), ("Act", ORG, 6.4)]):
        kk = pr(u, t0, t0 + .4)
        x = 200 + i * 340
        pill = F("b", 40)
        tw = d.textlength(txt, font=pill)
        rr(d, (x - tw / 2 - 30, 860, x + tw / 2 + 30, 940), 40, fill=fade(mix(INK, c, .3), a * kk), outline=fade(c, a * kk), width=3)
        ctext(d, x, 900, txt, pill, fade(WHITE, a * kk))


def s1(img, d, u, a):
    label(d, "1 · SENSE", a, CYANC)
    ctext(d, W // 2, 175, "It senses the world", F("b", 58), fade(WHITE, a * pr(u, 0, .5)))
    hl = []
    if u > 1.6: hl.append("eyes")
    if u > 2.9: hl.append("ears")
    if u > 4.1: hl.append("touch")
    if u > 5.8: hl.append("balance")
    cx, cy, s = 330, 600, 1.0
    robot(d, cx, cy, s, a, hl=hl, larm=0.2, rarm=0.3, rbend=0.4)
    if u > 1.6:
        waves(d, cx + 50, cy - 180, u, CYANC, a, 1)
        tag(d, 600, 380, "Cameras: see", CYANC, a * pr(u, 1.6, 2.0))
    if u > 2.9:
        tag(d, 600, 470, "Microphones: hear", CYANC, a * pr(u, 2.9, 3.3))
    if u > 4.1:
        tag(d, 600, 560, "Touch sensors: feel", CYANC, a * pr(u, 4.1, 4.5))
    if u > 5.8:
        tag(d, 600, 650, "Balance sensor", GRN, a * pr(u, 5.8, 6.2))
        ctext(d, 600 + 160, 720, "which way is up", F("m", 26), fade(MUTED, a * pr(u, 6.0, 6.4)))


def s2(img, d, u, a):
    label(d, "2 · THINK", a, VIO)
    ctext(d, W // 2, 175, "It thinks and plans", F("b", 58), fade(WHITE, a * pr(u, 0, .5)))
    cx, cy = 300, 620
    robot(d, cx, cy, 0.9, a, hl=("brain", "eyes"), glow=0.6 + 0.4 * math.sin(u * 4))
    # thought panel: camera view with detection box and plan
    k = pr(u, 1.2, 1.8)
    x0, y0, x1, y1 = 520, 300, 980, 760
    rr(d, (x0, y0, x1, y1), 24, fill=fade((12, 12, 22), a * k), outline=fade(VIO, a * k), width=3)
    d.text((x0 + 24, y0 + 34), "What it sees", font=F("b", 26), fill=fade(VIO, a * k), anchor="lm")
    # table + cup
    d.rectangle((x0 + 40, 600, x1 - 40, 616), fill=fade((90, 80, 70), a * k))
    cupx = 790
    d.rounded_rectangle((cupx - 32, 530, cupx + 32, 600), 8, fill=fade((220, 70, 70), a * k))
    d.arc((cupx + 20, 545, cupx + 52, 585), -90, 90, fill=fade((220, 70, 70), a * k), width=6)
    kb = pr(u, 2.4, 2.9)
    d.rectangle((cupx - 48, 512, cupx + 62, 612), outline=fade(GRN, a * kb), width=3)
    d.text((cupx - 48, 498), "cup  98%", font=F("b", 22), fill=fade(GRN, a * kb), anchor="lb")
    kp = pr(u, 3.8, 5.0)
    if kp > 0:
        pts = []
        for i in range(21):
            t_ = i / 20 * kp
            px = 580 + (cupx - 60 - 580) * t_
            py = 720 - 160 * math.sin(math.pi * t_ * 0.9)
            pts.append((px, py))
        for i in range(0, len(pts) - 1, 2):
            d.line((pts[i], pts[i + 1]), fill=fade(ORG, a), width=5)
        d.text((x0 + 24, y1 - 30), "Plan: reach and grasp", font=F("b", 26), fill=fade(ORG, a * pr(u, 4.6, 5.2)), anchor="lm")
    ctext(d, W // 2, 900, "A computer running AI models", F("m", 34), fade(WHITE, a * pr(u, 1.0, 1.6)))


def s3(img, d, u, a):
    label(d, "3 · ACT", a, ORG)
    ctext(d, W // 2, 175, "It moves", F("b", 60), fade(WHITE, a * pr(u, 0, .5)))
    lift = pr(u, 2.0, 3.6)
    wave = math.sin((u - 3.6) * 3) * 0.25 if u > 3.6 else 0
    robot(d, W // 2, 600, 1.05, a, hl=("motors",) if u > 1.8 else (), rarm=0.15 + 1.9 * lift + wave, rbend=0.3 - 0.2 * lift,
          larm=0.15 + 0.5 * lift, lbend=0.25 + 0.6 * lift)
    caption(d, "Electric motors in every joint", a * pr(u, 1.8, 2.4), y=950)


def s4(img, d, u, a):
    label(d, "THE LOOP", a, GRN)
    ctext(d, W // 2, 175, "Again and again", F("b", 60), fade(WHITE, a * pr(u, 0, .5)))
    cx, cy, R = W // 2, 570, 250
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=fade((60, 62, 80), a), width=3)
    ang = -math.pi / 2 + u * 5
    for j in range(36):
        aa = ang - j * 0.06
        x, y = cx + R * math.cos(aa), cy + R * math.sin(aa)
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=fade(GRN, a * (1 - j / 36)))
    for i, (nm, c) in enumerate([("Sense", CYANC), ("Think", VIO), ("Act", ORG)]):
        aa = -math.pi / 2 + i * 2 * math.pi / 3
        x, y = cx + R * math.cos(aa), cy + R * math.sin(aa)
        k = pr(u, .3 + i * .3, .7 + i * .3)
        f = F("b", 36)
        tw = d.textlength(nm, font=f)
        rr(d, (x - tw / 2 - 30, y - 40, x + tw / 2 + 30, y + 40), 40, fill=fade(mix(INK, c, .35), a * k), outline=fade(c, a * k), width=3)
        ctext(d, x, y, nm, f, fade(WHITE, a * k))
    ctext(d, cx, cy - 10, "many times", F("b", 40), fade(GRN, a * pr(u, 1.4, 2.0)))
    ctext(d, cx, cy + 40, "every second", F("b", 40), fade(GRN, a * pr(u, 1.6, 2.2)))
    caption(d, "Checking and correcting as it goes", a * pr(u, 3.0, 3.6), y=930)


def s5(img, d, u, a):
    label(d, "IN PRACTICE", a, CYANC)
    ctext(d, W // 2, 175, "Balance and a gentle grip", F("b", 54), fade(WHITE, a * pr(u, 0, .5)))
    # balance: tilt and recover
    tl = 0.0
    if 0.8 < u < 3.6:
        tt = u - 0.8
        tl = 0.22 * math.exp(-tt * 1.5) * math.sin(tt * 6)
    robot(d, 300, 560, 0.85, a, hl=("balance",) if u < 3.6 else ("touch",), tilt=tl, larm=0.35 + tl * 2, rarm=0.35 - tl * 2)
    tag(d, 120, 920, "Keeps its balance", GRN, a * pr(u, 1.0, 1.5))
    # cup grip
    k = pr(u, 3.4, 4.0)
    x0 = 600
    rr(d, (x0, 330, 980, 800), 24, fill=fade((14, 14, 24), a * k), outline=fade(CYANC, a * k), width=2)
    cupx, cupy = 790, 560
    d.rounded_rectangle((cupx - 50, cupy - 70, cupx + 50, cupy + 70), 12, fill=fade((220, 70, 70), a * k))
    gp = pr(u, 4.0, 4.8)
    for sx in (-1, 1):
        fx = cupx + sx * (140 - 86 * gp)
        d.rounded_rectangle((fx - 14 if sx < 0 else fx - 14, cupy - 40, fx + 14, cupy + 40), 10, fill=fade(LINE, a * k))
    # grip meter
    d.text((x0 + 30, 740), "Grip force", font=F("b", 26), fill=fade(WHITE, a * k), anchor="lm")
    d.rounded_rectangle((x0 + 190, 728, x0 + 350, 752), 10, fill=fade((40, 42, 56), a * k))
    d.rounded_rectangle((x0 + 190, 728, x0 + 190 + 160 * 0.35 * gp, 752), 10, fill=fade(GRN, a * k))
    tag(d, 980, 920, "Gentle grip", CYANC, a * pr(u, 4.6, 5.1), anchor="rm")


def s6(img, d, u, a):
    label(d, "NEWER ROBOTS", a, VIO)
    ctext(d, W // 2, 175, "One AI model:", F("b", 58), fade(WHITE, a * pr(u, 0, .5)))
    ctext(d, W // 2, 245, "see, hear, then act", F("b", 58), fade(VIO, a * pr(u, .2, .7)))
    ins = [("Camera view", CYANC), ("\"Pick up the cup\"", CYANC)]
    for i, (t_, c) in enumerate(ins):
        k = pr(u, 0.6 + i * .4, 1.0 + i * .4)
        y = 430 + i * 170
        rr(d, (90, y, 380, y + 110), 22, fill=fade(mix(INK, c, .2), a * k), outline=fade(c, a * k), width=2)
        ctext(d, 235, y + 55, t_, F("b", 28), fade(WHITE, a * k))
    km = pr(u, 1.8, 2.4)
    rr(d, (420, 420, 660, 710), 30, fill=fade(mix(INK, VIO, .35), a * km), outline=fade(VIO, a * km), width=4)
    ctext(d, 540, 540, "AI", F("b", 64), fade(WHITE, a * km))
    ctext(d, 540, 610, "model", F("m", 34), fade(WHITE, a * km))
    # flowing particles in and out
    if u > 2.4:
        for j in range(10):
            ph = ((u - 2.4) * 0.9 + j / 10) % 1
            x = 380 + ph * 330
            y = 565 + math.sin(ph * 6 + j) * 60 * (1 - ph)
            c = CYANC if x < 540 else ORG
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=fade(c, a * .9))
    ko = pr(u, 3.0, 3.6)
    rr(d, (710, 470, 990, 660), 22, fill=fade(mix(INK, ORG, .2), a * ko), outline=fade(ORG, a * ko), width=2)
    ctext(d, 850, 530, "Actions", F("b", 34), fade(WHITE, a * ko))
    ctext(d, 850, 595, "arm · hand · grip", F("m", 24), fade(WHITE, a * ko * .8))
    caption(d, "Vision-language-action models", a * pr(u, 3.8, 4.4), y=900, color=MUTED)


def s7(img, d, u, a):
    label(d, "IN SHORT", a, CYANC)
    cards = [("Sensors", "its senses", CYANC, 0.3), ("Computer", "its brain", VIO, 2.8), ("Motors", "its muscles", ORG, 5.0)]
    for i, (nm, sub, c, t0) in enumerate(cards):
        k = pr(u, t0, t0 + .5)
        y = 220 + i * 230
        x = 140 + (1 - k) * 100
        rr(d, (x, y, x + 800, y + 190), 34, fill=fade(mix(INK, c, .2), a * k), outline=fade(c, a * k), width=3)
        d.text((x + 50, y + 70), nm, font=F("b", 56), fill=fade(c, a * k), anchor="lm")
        d.text((x + 50, y + 140), "= " + sub, font=F("m", 40), fill=fade(WHITE, a * k), anchor="lm")


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
    d.rectangle((0, H - 8, int(W * t / END), H), fill=ORANGE if si in (4, 5) else TEAL)
    return img


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        for t in [float(x) for x in sys.argv[2:]]:
            frame(t).save(f"/home/claude/robot/p_{t:05.1f}.jpg", quality=88)
        sys.exit()
    n = int(END * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
                          "-pix_fmt", "yuv420p", "/home/claude/robot/silent_tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    import os
    os.replace("/home/claude/robot/silent_tmp.mp4", "/home/claude/robot/silent.mp4")
    M.mix_voice("/home/claude/robot/silent.mp4", "/home/claude/robot/vo.mp3", "/home/claude/robot/robot_explainer.mp4", M.VO_START)
    print("done", END)
