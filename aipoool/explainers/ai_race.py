"""Animated explainer: Who is winning the AI race (AIPOOOL, 1080x1080, 30 fps)."""
import sys, json, math, random, subprocess
sys.path.insert(0, "/home/claude/success-code-media/aipoool/tools")
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import brand as B
import make_posts as M

W = H = 1080
FPS = 30
cues = json.load(open("/home/claude/race/cues.json"))
S = [M.VO_START + s for s in cues["starts"]]   # scene starts
END = M.VO_START + cues["dur"] + 1.4
S.append(END)

INK = (4, 4, 7)
TEAL = (163, 230, 53)
ORANGE = (236, 72, 153)
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
    g.ellipse((-300, -300, 500, 500), fill=(8, 14, 4))
    g.ellipse((640, 640, 1400, 1400), fill=(16, 4, 12))
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
LIME = (163, 230, 53)
CYAN = (34, 211, 238)
PINK = (236, 72, 153)
VIOLET = (167, 139, 250)


def streaks(d, u, a, c=LIME):
    random.seed(11)
    for k in range(14):
        y = random.uniform(150, 950)
        L = random.uniform(80, 260)
        x = (random.uniform(0, W) + u * random.uniform(500, 900)) % (W + 400) - 200
        d.line((x, y, x + L, y), fill=fade(c, a * random.uniform(.15, .45)), width=random.choice([2, 3]))


def s0(img, d, u, a):
    streaks(d, u, a)
    ctext(d, W // 2, 300 + (1 - pr(u, 0, .6)) * 40, "Who is winning", F("b", 88), fade(WHITE, a * pr(u, 0, .6)))
    ctext(d, W // 2, 410 + (1 - pr(u, .3, .9)) * 40, "the AI race?", F("b", 88), fade(LIME, a * pr(u, .3, .9)))
    # podium with question marks
    k = pr(u, 1.4, 2.2)
    for i, (h, lab) in enumerate([(150, "2"), (210, "1"), (110, "3")]):
        x0 = 330 + i * 140
        hh = h * k
        rr(d, (x0, 800 - hh, x0 + 130, 800), 10, fill=fade(mix(INK, LIME if lab == "1" else CYAN, .55), a),
           outline=fade(LIME if lab == "1" else CYAN, a * k), width=3)
        if k > .5:
            ctext(d, x0 + 65, 800 - hh + 40, lab, F("b", 44), fade(WHITE, a * pr(u, 1.9, 2.3)))
            ctext(d, x0 + 65, 800 - hh - 45, "?", F("b", 54), fade(LIME if lab == "1" else MUTED, a * pr(u, 2.2, 2.7)))
    caption(d, "It depends on how you measure it", a * pr(u, 3.0, 3.6), y=890, color=MUTED)


TESTS = ["Reasoning", "Coding", "Knowledge", "Maths", "Agents", "Science"]


def s1(img, d, u, a):
    label(d, "HOW MODELS ARE SCORED", a, LIME)
    ctext(d, W // 2, 190, "Same tough tests", F("b", 56), fade(WHITE, a * pr(u, 0, .5)))
    ctext(d, W // 2, 255, "for every model", F("b", 56), fade(LIME, a * pr(u, .2, .7)))
    cx, cy = W // 2, 760
    for i, t_ in enumerate(TESTS):
        ki = pr(u, 0.5 + i * 0.3, 0.9 + i * 0.3)
        col, row = i % 3, i // 3
        x0, y0 = 200 + col * 340, 380 + row * 100
        m = pr(u, 3.6 + i * 0.12, 4.4 + i * 0.12)  # fly into score
        x = x0 + (cx - x0) * m
        y = y0 + (cy - y0) * m
        al = a * ki * (1 - m)
        f = F("b", 30)
        tw = d.textlength(t_, font=f)
        rr(d, (x - tw / 2 - 26, y - 34, x + tw / 2 + 26, y + 34), 34, fill=fade(mix(CARD, CYAN, .2), al),
           outline=fade(CYAN, al), width=2)
        ctext(d, x, y, t_, f, fade(WHITE, al))
    ks = pr(u, 4.2, 4.9)
    r = 95 * ks
    for g in range(4, 0, -1):
        d.ellipse((cx - r - g * 12, cy - r - g * 12, cx + r + g * 12, cy + r + g * 12), outline=fade(LIME, a * ks * .1 * g), width=3)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fade(mix(CARD, LIME, .25), a * ks), outline=fade(LIME, a * ks), width=4)
    ctext(d, cx, cy - 8, "ONE", F("b", 40), fade(WHITE, a * ks))
    ctext(d, cx, cy + 32, "score", F("m", 26), fade(WHITE, a * ks))
    ctext(d, W // 2, 960, "Artificial Analysis Intelligence Index", F("m", 30), fade(MUTED, a * pr(u, 4.8, 5.4)))


RACE = [("Claude Fable 5.2", "Anthropic", 64.6, LIME), ("GPT-6.2 Astra", "OpenAI", 62.1, CYAN),
        ("Gemini 4 Carbon", "Google", 60.0, PINK)]


def race(img, d, u, a, second):
    """u measured from start of first race scene; second = time when 2nd sentence begins."""
    label(d, "INTELLIGENCE INDEX", a, LIME)
    ctext(d, W // 2, 175, "The leaderboard", F("b", 56), fade(WHITE, a))
    x0, x1 = 120, 900
    lo, hi = 40.0, 66.0
    grow = pr(u, 0.3, 3.2)
    for i, (name, lab, sc, c) in enumerate(RACE):
        y = 360 + i * 180
        hl = (i == 0 and u < second) or (i in (1, 2) and u >= second + (0 if i == 1 else 4.8))
        dim = 1.0 if (hl or u < second) else 0.85
        cur = lo + (sc - lo) * grow * (1 - 0.02 * math.sin(u * 6 + i) * (1 - grow))
        xe = x0 + (x1 - x0) * (cur - lo) / (hi - lo)
        rr(d, (x0, y, max(x0 + 30, xe), y + 70), 14, fill=fade(mix(INK, c, dim), a))
        if hl:
            for g in range(3, 0, -1):
                rr(d, (x0 - g * 6, y - g * 6, xe + g * 6, y + 70 + g * 6), 18, outline=fade(c, a * .18 * g), width=3)
        d.text((x0 + 20, y + 35), name, font=F("b", 32), fill=fade(INK, a), anchor="lm")
        d.text((x0, y - 22), f"{i + 1}  ·  {lab}", font=F("m", 24), fill=fade(mix(MUTED, c, .6 * dim), a), anchor="lm")
        d.text((xe + 16, y + 35), f"{cur:.1f}", font=F("b", 38), fill=fade(mix(MUTED, WHITE, dim), a), anchor="lm")
        if i == 0 and grow >= 1:
            # crown
            kx = xe - 40
            ky = y - 40 + math.sin(u * 4) * 3
            d.polygon([(kx - 26, ky + 22), (kx - 26, ky - 6), (kx - 13, ky + 8), (kx, ky - 14), (kx + 13, ky + 8),
                       (kx + 26, ky - 6), (kx + 26, ky + 22)], fill=fade(LIME, a * pr(u, 3.2, 3.6)))
    ctext(d, W // 2, 965, "Artificial Analysis Intelligence Index  ·  17-19 Nov 2026", F("m", 26), fade(MUTED, a))


def s2(img, d, u, a):
    race(img, d, u, a, S[3] - S[2])


def s3(img, d, u, a):
    race(img, d, u + (S[3] - S[2]), a, S[3] - S[2])


def s4(img, d, u, a):
    label(d, "ARENA · PEOPLE VOTE", a, PINK)
    ctext(d, W // 2, 180, "People vote on", F("b", 54), fade(WHITE, a * pr(u, 0, .5)))
    ctext(d, W // 2, 245, "blind answers", F("b", 54), fade(PINK, a * pr(u, .2, .7)))
    for i, nm in enumerate(["Model A", "Model B"]):
        x0 = 150 + i * 420
        k = pr(u, 0.4 + i * .2, 0.9 + i * .2)
        picked = i == 1 and 1.8 < u
        rr(d, (x0, 320, x0 + 360, 560), 22, fill=fade(mix(CARD, PINK, .25 if picked else 0), a * k),
           outline=fade(PINK if picked else EDGE, a * k), width=4 if picked else 2)
        ctext(d, x0 + 180, 360, nm, F("b", 32), fade(WHITE, a * k))
        for j in range(4):
            d.rounded_rectangle((x0 + 30, 410 + j * 34, x0 + 330 - (j % 2) * 70, 426 + j * 34), 8,
                                fill=fade((60, 70, 100), a * k))
        if picked:
            check(d, x0 + 300, 340, 34, fade(PINK, a * pr(u, 1.8, 2.1)), 6)
    # votes flying
    if u > 1.8:
        random.seed(5)
        for k_ in range(18):
            ph = ((u - 1.8) * 0.8 + k_ * .07) % 1
            x = 300 + random.uniform(-150, 500)
            y = 600 - ph * 260
            d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=fade(PINK, a * (1 - ph) * .7))
    kp = pr(u, 2.6, 3.4)
    for i, (rank, nm) in enumerate([("1", "Gemini 4 Carbon"), ("2", "Gemini 4 Argon")]):
        y = 650 + i * 110
        rr(d, (220, y, 860, y + 86), 43, fill=fade(mix(CARD, PINK, .3 if i == 0 else .15), a * kp),
           outline=fade(PINK, a * kp), width=3)
        ctext(d, 280, y + 43, rank, F("b", 40), fade(PINK, a * kp))
        d.text((340, y + 43), nm, font=F("b", 38), fill=fade(WHITE, a * kp), anchor="lm")
        d.text((830, y + 43), "Google", font=F("m", 26), fill=fade(MUTED, a * kp), anchor="rm")
    ctext(d, W // 2, 965, "Arena text leaderboard  ·  November 2026", F("m", 26), fade(MUTED, a))


def s5(img, d, u, a):
    streaks(d, u, a, CYAN)
    label(d, "THE PACE", a, CYAN)
    ctext(d, W // 2, 190, "The race is speeding up", F("b", 56), fade(WHITE, a * pr(u, 0, .5)))
    y = 560
    k = pr(u, 0.4, 1.4)
    d.line((140, y, 140 + 800 * k, y), fill=fade(EDGE, a), width=6)
    pts = [(300, "9 Nov", "Claude Fable 5.2", LIME, 1.2), (780, "17 Nov", "GPT-6.2 Astra", CYAN, 2.4)]
    for x, dt, nm, c, t0 in pts:
        kk = pr(u, t0, t0 + .4)
        r = 18 * kk
        d.ellipse((x - r, y - r, x + r, y + r), fill=fade(c, a))
        ctext(d, x, y - 60, dt, F("b", 36), fade(c, a * kk))
        ctext(d, x, y + 60, nm, F("m", 30), fade(WHITE, a * kk))
    kb = pr(u, 3.0, 3.8)
    if kb > 0:
        xe = 300 + 480 * kb
        d.line((300, 700, xe, 700), fill=fade(LIME, a), width=5)
        d.line((300, 685, 300, 715), fill=fade(LIME, a), width=5)
        if kb >= 1:
            d.line((780, 685, 780, 715), fill=fade(LIME, a), width=5)
        ctext(d, 540, 770, "8 days apart", F("b", 52), fade(LIME, a * pr(u, 3.6, 4.1)))


def s6(img, d, u, a):
    label(d, "OPEN MODELS", a, VIOLET)
    ctext(d, W // 2, 185, "Open models are", F("b", 56), fade(WHITE, a * pr(u, 0, .5)))
    ctext(d, W // 2, 250, "close behind", F("b", 56), fade(VIOLET, a * pr(u, .2, .7)))
    ctext(d, W // 2, 330, "Models anyone can download and run", F("m", 30), fade(MUTED, a * pr(u, .6, 1.1)))
    rows = [("Top closed model", LIME, 820, 1.4), ("Best open model", VIOLET, 740, 2.6)]
    for i, (nm, c, xe, t0) in enumerate(rows):
        y = 470 + i * 150
        k = pr(u, t0, t0 + 1.2)
        d.text((140, y - 30), nm, font=F("b", 30), fill=fade(WHITE, a * pr(u, t0, t0 + .4)), anchor="lm")
        rr(d, (140, y, 140 + (xe - 140) * k, y + 64), 16, fill=fade(mix(CARD, c, .75), a))
    kg = pr(u, 3.8, 4.4)
    if kg > 0:
        for yy in (450, 700):
            pass
        d.line((740, 620, 740, 700), fill=fade(LIME, a * kg), width=3)
        d.line((820, 470, 820, 700), fill=fade(LIME, a * kg), width=3)
        d.line((744, 690, 816, 690), fill=fade(LIME, a * kg), width=3)
        ctext(d, 780, 760, "just a few points", F("b", 40), fade(LIME, a * kg))
    ctext(d, W // 2, 965, "Artificial Analysis Intelligence Index", F("m", 26), fade(MUTED, a))


def s7(img, d, u, a):
    label(d, "RIGHT NOW", a, LIME)
    ctext(d, W // 2, 190, "So who is winning?", F("b", 60), fade(WHITE, a * pr(u, 0, .5)))
    cards = [("Anthropic", "Leads the tests", LIME, 1.0), ("Google", "Wins the vote", PINK, 2.6),
             ("OpenAI", "Closing in fast", CYAN, 4.2)]
    for i, (co, txt, c, t0) in enumerate(cards):
        k = pr(u, t0 - .3, t0 + .2)
        y = 320 + i * 190
        x = 140 + (1 - k) * 120
        rr(d, (x, y, x + 800, y + 150), 28, fill=fade(mix(CARD, c, .14), a * k), outline=fade(c, a * k), width=3)
        d.text((x + 40, y + 52), co, font=F("b", 46), fill=fade(c, a * k), anchor="lm")
        d.text((x + 40, y + 108), txt, font=F("m", 34), fill=fade(WHITE, a * k), anchor="lm")
    caption(d, "The lead can change with the next launch", a * pr(u, 5.4, 6.0), y=930, color=MUTED)


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
    a = pr(u, 0, XF) if si not in (0, 3) else (pr(u, 0, 0.3) if si == 0 else 1.0)
    if si == 2:
        pass
    elif si < len(SCENES) - 1:
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
            frame(t).save(f"/home/claude/race/p_{t:05.1f}.jpg", quality=88)
        sys.exit()
    n = int(END * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
                          "-pix_fmt", "yuv420p", "/home/claude/race/silent_tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    import os
    os.replace("/home/claude/race/silent_tmp.mp4", "/home/claude/race/silent.mp4")
    M.mix_voice("/home/claude/race/silent.mp4", "/home/claude/race/vo.mp3", "/home/claude/race/race_explainer.mp4", M.VO_START)
    print("done", END)
