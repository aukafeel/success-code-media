"""Animated explainer: How Claude works vs Claude Code (AIPOOOL, 1080x1080, 30 fps)."""
import sys, json, math, random, subprocess
sys.path.insert(0, "/home/claude/success-code-media/aipoool/tools")
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import brand as B
import make_posts as M

W = H = 1080
FPS = 30
cues = json.load(open("/home/claude/explain/cues.json"))
S = [M.VO_START + s for s in cues["starts"]]   # scene starts
END = M.VO_START + cues["dur"] + 1.4
S.append(END)

INK = (7, 11, 26)
TEAL = (45, 212, 191)
ORANGE = (251, 146, 60)
WHITE = (238, 240, 246)
MUTED = (140, 150, 172)
CARD = (17, 24, 44)
EDGE = (40, 52, 84)
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
    g.ellipse((-300, -300, 500, 500), fill=(10, 60, 70))
    g.ellipse((640, 640, 1400, 1400), fill=(70, 34, 10))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img = Image.blend(img, glow, 0.0)
    img = Image.fromarray(__import__("numpy").clip(
        __import__("numpy").asarray(img, dtype="int16") + __import__("numpy").asarray(glow, dtype="int16"), 0, 255).astype("uint8"))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 54):
        d.line((x, 0, x, H), fill=(12, 18, 36))
    for y in range(0, H, 54):
        d.line((0, y, W, y), fill=(12, 18, 36))
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
def s0(img, d, u, a):
    ctext(d, W // 2, 330 + (1 - pr(u, 0, .6)) * 40, "How does", F("b", 92), fade(WHITE, a * pr(u, 0, .6)))
    ctext(d, W // 2, 440 + (1 - pr(u, .3, .9)) * 40, "Claude work?", F("b", 92), fade(TEAL, a * pr(u, .3, .9)))
    k = pr(u, 2.3, 3.0)
    for i, (txt, c, sx) in enumerate([("Claude", TEAL, -1), ("Claude Code", ORANGE, 1)]):
        cx = W // 2 + sx * 230 + sx * (1 - k) * 300
        f = F("b", 46)
        tw = d.textlength(txt, font=f)
        rr(d, (cx - tw / 2 - 34, 600, cx + tw / 2 + 34, 690), 45, fill=fade(c, .16 * k * a), outline=fade(c, k * a), width=3)
        ctext(d, cx, 645, txt, f, fade(c, k * a))
    ctext(d, W // 2, 645, "vs", F("b", 40), fade(MUTED, a * pr(u, 2.8, 3.3)))
    caption(d, "What is the difference?", a * pr(u, 3.2, 3.8), y=800, color=MUTED)


TOKENS = ["Explain", " AI", " to", " a", " busy", " CEO"]
TOKC = [TEAL, ORANGE, (167, 139, 250), (96, 165, 250), (52, 211, 153), (251, 113, 133)]


def s1(img, d, u, a):
    label(d, "STEP 1 · TOKENS", a)
    ctext(d, W // 2, 250, "Your words become tokens", F("b", 52), fade(WHITE, a * pr(u, 0, .5)))
    full = "".join(TOKENS)
    f = F("m", 50)
    split = pr(u, 3.2, 4.4)
    if u < 3.2:
        n = int(len(full) * pr(u, 0.4, 2.4) + 0.001) if u > 0.4 else 0
        tw = d.textlength(full, font=f)
        rr(d, (W / 2 - tw / 2 - 40, 430, W / 2 + tw / 2 + 40, 540), 24, fill=fade(CARD, a), outline=fade(EDGE, a))
        shown = full[:n]
        d.text((W / 2 - tw / 2, 485), shown, font=f, fill=fade(WHITE, a), anchor="lm")
        if int(u * 3) % 2 == 0:
            cx = W / 2 - tw / 2 + d.textlength(shown, font=f) + 4
            d.line((cx, 455, cx, 515), fill=fade(TEAL, a), width=3)
    else:
        widths = [d.textlength(tk.strip(), font=f) + 44 for tk in TOKENS]
        gap = 14 + 26 * split
        total = sum(widths) + gap * (len(TOKENS) - 1)
        x = W / 2 - total / 2
        for i, (tk, w) in enumerate(zip(TOKENS, widths)):
            c = TOKC[i]
            yoff = math.sin(u * 3 + i) * 6 * split
            k = split
            rr(d, (x, 440 + yoff, x + w, 530 + yoff), 18, fill=fade(mix(CARD, c, .25 * k), a),
               outline=fade(mix(EDGE, c, k), a), width=3)
            ctext(d, x + w / 2, 485 + yoff, tk.strip(), f, fade(mix(WHITE, c, .5 * k), a))
            x += w + gap
        ctext(d, W // 2, 620, "6 tokens", F("b", 40), fade(TEAL, a * pr(u, 4.4, 5.0)))
    caption(d, "Text is split into small pieces called tokens", a * pr(u, 3.6, 4.3))


LAYERS = [5, 7, 7, 5]
NX = [220, 420, 620, 820]


def node_pos():
    pos = []
    for li, n in enumerate(LAYERS):
        ys = [470 + (j - (n - 1) / 2) * 58 for j in range(n)]
        pos.append([(NX[li], y) for y in ys])
    return pos


NODES = node_pos()
OUT = ["AI", "helps", "your", "team", "decide", "faster."]


def s2(img, d, u, a):
    label(d, "STEP 2 · PREDICT", a)
    ctext(d, W // 2, 160, "A neural network predicts", F("b", 46), fade(WHITE, a * pr(u, 0, .5)))
    ctext(d, W // 2, 215, "the next token", F("b", 46), fade(TEAL, a * pr(u, .2, .7)))
    grow = pr(u, 0.3, 1.6)
    # edges
    for li in range(len(NODES) - 1):
        for p in NODES[li]:
            for q in NODES[li + 1]:
                d.line((p, q), fill=fade((36, 48, 80), a * grow), width=1)
    # pulses
    if u > 1.2:
        random.seed(3)
        for k in range(26):
            li = k % 3
            p = random.choice(NODES[li]); q = random.choice(NODES[li + 1])
            ph = ((u - 1.2) * 1.4 + k * 0.137) % 1.0
            x = p[0] + (q[0] - p[0]) * ph; y = p[1] + (q[1] - p[1]) * ph
            c = TEAL if k % 2 else ORANGE
            d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=fade(c, a))
    for li, layer in enumerate(NODES):
        for j, (x, y) in enumerate(layer):
            pulse = 0.5 + 0.5 * math.sin(u * 5 - li * 1.2 + j)
            c = mix((60, 80, 130), TEAL if li < 3 else ORANGE, pulse * (u > 1.2))
            r = 15 * grow
            d.ellipse((x - r, y - r, x + r, y + r), fill=fade(c, a), outline=fade(WHITE, a * .3))
    ctext(d, NX[0], 665, "tokens in", F("m", 24), fade(MUTED, a * grow))
    ctext(d, NX[3], 665, "next token out", F("m", 24), fade(MUTED, a * grow))
    # output sentence built token by token
    t0 = 4.2
    n = max(0, min(len(OUT), int((u - t0) / 0.75) + 1)) if u > t0 else 0
    f = F("b", 44)
    words = OUT[:n]
    line = " ".join(words)
    tw = d.textlength(" ".join(OUT), font=f)
    x0 = W / 2 - tw / 2
    rr(d, (x0 - 34, 720, x0 + tw + 34, 820), 22, fill=fade(CARD, a * pr(u, 3.6, 4.2)), outline=fade(EDGE, a * pr(u, 3.6, 4.2)))
    xx = x0
    for i, w_ in enumerate(words):
        newest = i == n - 1 and (u - t0 - i * 0.75) < 0.6
        d.text((xx, 770), w_, font=f, fill=fade(ORANGE if newest else WHITE, a), anchor="lm")
        xx += d.textlength(w_ + " ", font=f)
    if n and n < len(OUT) and int(u * 3) % 2 == 0:
        d.line((xx, 745, xx, 795), fill=fade(TEAL, a), width=3)
    caption(d, "Trained on huge amounts of text  ·  one token at a time", a * pr(u, 1.0, 1.6), y=900, color=MUTED)
    ctext(d, W // 2, 1000, "illustrative example", F("r", 22), fade(MUTED, a * .8))


def bubble(d, box, c, a, k):
    rr(d, box, 26, fill=fade(c, a * k))


def s3(img, d, u, a):
    label(d, "CLAUDE · CHAT APP", a)
    ctext(d, W // 2, 180, "In the Claude app, you chat", F("b", 50), fade(WHITE, a * pr(u, 0, .5)))
    win = (150, 260, 930, 800)
    rr(d, win, 30, fill=fade(CARD, a), outline=fade(EDGE, a))
    for i, c in enumerate([(251, 113, 133), (250, 204, 21), (52, 211, 153)]):
        d.ellipse((185 + i * 30, 288, 203 + i * 30, 306), fill=fade(c, a))
    k1 = pr(u, 0.5, 1.0)
    bubble(d, (440, 340 + (1 - k1) * 20, 890, 420 + (1 - k1) * 20), (30, 64, 120), a, k1)
    d.text((470, 380 + (1 - k1) * 20), "Write an email checker", font=F("m", 32), fill=fade(WHITE, a * k1), anchor="lm")
    # typing dots then answer
    if 1.2 < u < 2.2:
        for i in range(3):
            y = 480 + math.sin(u * 10 + i) * 6
            d.ellipse((200 + i * 30, y - 8, 216 + i * 30, y + 8), fill=fade(TEAL, a))
    k2 = pr(u, 2.2, 2.7)
    if k2 > 0:
        rr(d, (190, 450, 760, 650), 22, fill=fade((10, 16, 32), a * k2), outline=fade(TEAL, a * k2), width=2)
        code = ["def is_email(s):", "    return \"@\" in s", "        and \".\" in s"]
        for i, ln in enumerate(code):
            ki = pr(u, 2.5 + i * 0.35, 2.8 + i * 0.35)
            d.text((220, 495 + i * 46), ln, font=F("mono", 30), fill=fade(TEAL if i == 0 else WHITE, a * ki), anchor="lm")
    # copy button press
    kc = pr(u, 4.3, 4.6)
    press = 1.0 if 4.6 < u < 5.0 else 0.0
    rr(d, (190, 680, 360, 750), 20, fill=fade(mix(CARD, ORANGE, .2 + .6 * press), a * kc), outline=fade(ORANGE, a * kc))
    ctext(d, 275, 715, "Copy", F("b", 30), fade(WHITE, a * kc))
    ka = pr(u, 5.0, 5.6)
    if ka > 0:
        d.line((380, 715, 380 + 260 * ka, 715), fill=fade(ORANGE, a), width=5)
        rr(d, (660, 680, 900, 750), 20, fill=fade(CARD, a * ka), outline=fade(EDGE, a * ka))
        ctext(d, 780, 715, "Your work", F("m", 30), fade(WHITE, a * ka))
    caption(d, "You ask  ·  Claude answers  ·  you copy", a * pr(u, 1.0, 1.6), y=900)


TOOLS = ["Files", "Terminal", "Tests", "Git"]


def s4(img, d, u, a):
    label(d, "CLAUDE CODE", a, ORANGE)
    ctext(d, W // 2, 190, "Claude Code", F("b", 80), fade(ORANGE, a * pr(u, 0, .5)))
    cx, cy = W // 2, 540
    k = pr(u, 0.2, 0.9)
    r = 110 * k
    for g in range(4, 0, -1):
        rr_ = r + g * 14
        d.ellipse((cx - rr_, cy - rr_, cx + rr_, cy + rr_), outline=fade(TEAL, a * k * .12 * g), width=3)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fade(mix(CARD, TEAL, .25), a), outline=fade(TEAL, a * k), width=4)
    ctext(d, cx, cy - 18, "Same Claude", F("b", 30), fade(WHITE, a * k))
    ctext(d, cx, cy + 22, "models", F("b", 30), fade(WHITE, a * k))
    for i, tl in enumerate(TOOLS):
        ki = pr(u, 1.6 + i * 0.35, 2.0 + i * 0.35)
        ang = -math.pi / 2 + i * math.pi / 2 + u * 0.25
        R = 240 + (1 - ki) * 80
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        d.line((cx + 115 * math.cos(ang), cy + 115 * math.sin(ang), x - 60 * math.cos(ang), y - 60 * math.sin(ang)),
               fill=fade(ORANGE, a * ki * .6), width=3)
        f = F("b", 30)
        tw = d.textlength(tl, font=f)
        rr(d, (x - tw / 2 - 26, y - 34, x + tw / 2 + 26, y + 34), 34, fill=fade(mix(CARD, ORANGE, .22), a * ki),
           outline=fade(ORANGE, a * ki), width=3)
        ctext(d, x, y, tl, f, fade(WHITE, a * ki))
    caption(d, "Same brain  +  tools to act", a * pr(u, 1.4, 2.0), y=900)


LOOP = ["Read files", "Plan", "Edit code", "Run tests", "Check result"]
TERM = ["> fix the login bug", "reading auth.py ...", "plan: 2 files to change", "editing 2 files",
        "tests: 24 passed", "done"]


def s5(img, d, u, a):
    label(d, "CLAUDE CODE · AGENT LOOP", a, ORANGE)
    ctext(d, W // 2, 160, "It works in a loop", F("b", 54), fade(WHITE, a * pr(u, 0, .5)))
    cx, cy, R = W // 2, 570, 330
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=fade(EDGE, a), width=4)
    step_t = [0.3 + i * 1.55 for i in range(5)]
    active = max([i for i, s in enumerate(step_t) if u >= s] or [0])
    # moving glow dot
    ph = cl((u - 0.3) / (1.55 * 5))
    ang = -math.pi / 2 + ph * 2 * math.pi * (1 if u < 8.3 else 1) + (u > 8.05) * (u - 8.05) * 2.5
    gx, gy = cx + R * math.cos(ang), cy + R * math.sin(ang)
    for g in range(3, 0, -1):
        d.ellipse((gx - 8 * g, gy - 8 * g, gx + 8 * g, gy + 8 * g), fill=fade(ORANGE, a * 0.25 * (4 - g)))
    for i, st in enumerate(LOOP):
        ang_i = -math.pi / 2 + i * 2 * math.pi / 5
        x, y = cx + R * math.cos(ang_i), cy + R * math.sin(ang_i)
        on = i == active and u < 8.3
        ki = pr(u, 0.0 + i * 0.1, 0.5 + i * 0.1)
        f = F("b", 28)
        tw = d.textlength(st, font=f)
        c = ORANGE if on else (u >= step_t[i] and TEAL or MUTED)
        rr(d, (x - tw / 2 - 24, y - 32, x + tw / 2 + 24, y + 32), 32,
           fill=fade(mix(CARD, c, .35 if on else .1), a * ki), outline=fade(c, a * ki), width=4 if on else 2)
        ctext(d, x, y, st, f, fade(WHITE, a * ki))
    # terminal in the middle
    rr(d, (cx - 165, cy - 115, cx + 165, cy + 115), 18, fill=fade((5, 8, 18), a), outline=fade(EDGE, a))
    n = min(len(TERM), int(u / 1.45) + 1)
    for i, ln in enumerate(TERM[:n]):
        row = i - max(0, n - 5)
        if row < 0:
            continue
        col = TEAL if i == 0 else (ORANGE if ln == "done" else (210, 215, 230))
        d.text((cx - 148, cy - 84 + row * 42), ln, font=F("mono", 17), fill=fade(col, a), anchor="lm")
    caption(d, "...and repeats until the job is done", a * pr(u, 7.5, 8.1), y=995)


def s6(img, d, u, a):
    label(d, "YOU STAY IN CONTROL", a, TEAL)
    ctext(d, W // 2, 190, "You approve the changes", F("b", 54), fade(WHITE, a * pr(u, 0, .5)))
    rr(d, (170, 280, 910, 560), 22, fill=fade((5, 8, 18), a), outline=fade(EDGE, a))
    d.text((200, 315), "login.py", font=F("mono", 24), fill=fade(MUTED, a), anchor="lm")
    rows = [("-", "if user.password == pw:", (251, 113, 133)), ("+", "if check_hash(user, pw):", (52, 211, 153)),
            ("+", "    log_attempt(user)", (52, 211, 153))]
    for i, (s_, ln, c) in enumerate(rows):
        ki = pr(u, 0.4 + i * 0.3, 0.7 + i * 0.3)
        y = 375 + i * 58
        d.rectangle((172, y - 25, 908, y + 25), fill=fade(mix((5, 8, 18), c, .14), a * ki))
        d.text((200, y), s_ + " " + ln, font=F("mono", 30), fill=fade(c, a * ki), anchor="lm")
    kq = pr(u, 1.4, 1.9)
    rr(d, (270, 620, 810, 830), 26, fill=fade(CARD, a * kq), outline=fade(TEAL, a * kq), width=3)
    ctext(d, W // 2, 675, "Apply this change?", F("b", 38), fade(WHITE, a * kq))
    press = 2.6 < u < 3.1
    rr(d, (330, 725, 520, 795), 22, fill=fade(mix(CARD, TEAL, .9 if press else .35), a * kq), outline=fade(TEAL, a * kq))
    ctext(d, 425, 760, "Yes", F("b", 32), fade(INK if press else WHITE, a * kq))
    rr(d, (560, 725, 750, 795), 22, fill=fade(CARD, a * kq), outline=fade(MUTED, a * kq))
    ctext(d, 655, 760, "No", F("b", 32), fade(MUTED, a * kq))
    if u > 1.9:  # cursor moving to Yes
        k = pr(u, 1.9, 2.6)
        mx, my = 760 + (440 - 760) * k, 900 + (770 - 900) * k
        d.polygon([(mx, my), (mx, my + 40), (mx + 11, my + 30), (mx + 26, my + 30)], fill=fade(WHITE, a), outline=fade(INK, a))
    if u > 3.1:
        check(d, 830, 360, 50, fade((52, 211, 153), a * pr(u, 3.1, 3.4)), 8)


def s7(img, d, u, a):
    label(d, "THE DIFFERENCE", a)
    cols = [("Claude", TEAL, ["Thinks", "Writes"], 0.4), ("Claude Code", ORANGE, ["Thinks", "Writes", "Acts"], 2.6)]
    for ci, (name, c, items, t0) in enumerate(cols):
        x0 = 120 + ci * 440
        k = pr(u, t0 - 0.4, t0)
        rr(d, (x0, 230, x0 + 400, 800), 30, fill=fade(mix(CARD, c, .08), a * k), outline=fade(c, a * k), width=3)
        ctext(d, x0 + 200, 300, name, F("b", 46), fade(c, a * k))
        for i, it in enumerate(items):
            ki = pr(u, t0 + i * 0.55, t0 + 0.3 + i * 0.55)
            y = 420 + i * 120
            last = ci == 1 and i == 2
            if last and ki > 0:
                for g in range(3, 0, -1):
                    rr(d, (x0 + 40 - g * 8, y - 45 - g * 8, x0 + 360 + g * 8, y + 45 + g * 8), 40,
                       outline=fade(ORANGE, a * ki * .15 * g), width=3)
            rr(d, (x0 + 40, y - 45, x0 + 360, y + 45), 40, fill=fade(mix(CARD, c, .25 if last else .12), a * ki))
            check(d, x0 + 75, y - 18, 36, fade(c, a * ki), 6)
            d.text((x0 + 135, y), it, font=F("b", 40), fill=fade(WHITE, a * ki), anchor="lm")
    caption(d, "Same brain. Claude Code adds hands.", a * pr(u, 4.6, 5.2), y=900)


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
            frame(t).save(f"/home/claude/explain/p_{t:05.1f}.jpg", quality=88)
        sys.exit()
    n = int(END * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
                          "-pix_fmt", "yuv420p", "/home/claude/explain/silent_tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    import os
    os.replace("/home/claude/explain/silent_tmp.mp4", "/home/claude/explain/silent.mp4")
    M.mix_voice("/home/claude/explain/silent.mp4", "/home/claude/explain/vo.mp3", "/home/claude/explain/claude_explainer.mp4", M.VO_START)
    print("done", END)
