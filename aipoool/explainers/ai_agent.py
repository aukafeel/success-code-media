"""Animated explainer: What is an AI agent (AIPOOOL, 1080x1080, 30 fps)."""
import sys, json, math, random, subprocess
sys.path.insert(0, "/home/claude/success-code-media/aipoool/tools")
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import brand as B
import make_posts as M

W = H = 1080
FPS = 30
cues = json.load(open("/home/claude/agent/cues.json"))
S = [M.VO_START + s for s in cues["starts"]]   # scene starts
END = M.VO_START + cues["dur"] + 1.4
S.append(END)

INK = (4, 4, 7)
TEAL = (245, 158, 11)
ORANGE = (59, 130, 246)
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
    g.ellipse((-300, -300, 500, 500), fill=(16, 10, 2))
    g.ellipse((640, 640, 1400, 1400), fill=(4, 8, 18))
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
BLUE = (59, 130, 246)
AMBER = (245, 158, 11)
MINT = (52, 211, 153)
ROSE = (244, 63, 94)


def pill(d, cx, cy, txt, c, al, size=30, fillk=.22):
    f = F("b", size)
    tw = d.textlength(txt, font=f)
    rr(d, (cx - tw / 2 - 28, cy - size - 4, cx + tw / 2 + 28, cy + size + 4), size + 4,
       fill=fade(mix(INK, c, fillk), al), outline=fade(c, al), width=3)
    ctext(d, cx, cy, txt, f, fade(WHITE, al))


def s0(img, d, u, a):
    ctext(d, W // 2, 300 + (1 - pr(u, 0, .6)) * 40, "What is an", F("b", 92), fade(WHITE, a * pr(u, 0, .6)))
    ctext(d, W // 2, 410 + (1 - pr(u, .3, .9)) * 40, "AI agent?", F("b", 104), fade(AMBER, a * pr(u, .3, .9)))
    k = pr(u, 2.6, 3.3)
    pill(d, W // 2 - 220 - (1 - k) * 250, 640, "Chatbot", BLUE, a * k, 40)
    pill(d, W // 2 + 220 + (1 - k) * 250, 640, "Agent", AMBER, a * k, 40)
    ctext(d, W // 2, 640, "vs", F("b", 40), fade(MUTED, a * pr(u, 3.0, 3.5)))


def s1(img, d, u, a):
    label(d, "A CHATBOT", a, BLUE)
    ctext(d, W // 2, 200, "Answers, then waits", F("b", 60), fade(WHITE, a * pr(u, 0, .5)))
    k1 = pr(u, 0.3, 0.7)
    rr(d, (420, 330 + (1 - k1) * 20, 920, 420 + (1 - k1) * 20), 30, fill=fade(mix(INK, BLUE, .6), a * k1))
    d.text((450, 375 + (1 - k1) * 20), "What were our sales?", font=F("m", 32), fill=fade(WHITE, a * k1), anchor="lm")
    k2 = pr(u, 1.0, 1.4)
    rr(d, (160, 460, 700, 560), 30, fill=fade((30, 32, 44), a * k2), outline=fade(BLUE, a * k2), width=2)
    d.text((190, 510), "Here is a summary ...", font=F("m", 32), fill=fade(WHITE, a * k2), anchor="lm")
    kw = pr(u, 1.9, 2.4)
    if kw > 0:
        for i in range(3):
            ph = (u * 2 - i * .3) % 1.5
            al = a * kw * (0.3 + 0.7 * (ph < .5))
            d.ellipse((470 + i * 50, 690, 496 + i * 50, 716), fill=fade(MUTED, al))
        ctext(d, W // 2, 790, "waiting for you", F("b", 40), fade(MUTED, a * kw))


def s2(img, d, u, a):
    label(d, "AN AGENT", a, AMBER)
    ctext(d, W // 2, 190, "Give it a goal", F("b", 60), fade(WHITE, a * pr(u, 0, .5)))
    # target at right
    tx, ty = 860, 560
    kt = pr(u, 0.6, 1.2)
    for r_, c in [(90, AMBER), (62, INK), (38, AMBER), (14, INK)]:
        r2 = r_ * kt
        d.ellipse((tx - r2, ty - r2, tx + r2, ty + r2), fill=fade(c, a) if c != INK else (*INK, 255))
    ctext(d, tx, ty + 140, "GOAL", F("b", 34), fade(AMBER, a * kt))
    # stepping stones lighting up
    steps = [(170, 700), (300, 620), (440, 680), (580, 590), (700, 560)]
    for i, (x, y) in enumerate(steps):
        ki = pr(u, 2.0 + i * 0.55, 2.3 + i * 0.55)
        c = mix((50, 52, 66), AMBER, ki)
        d.ellipse((x - 34, y - 20, x + 34, y + 20), fill=fade(c, a))
        if ki > .5:
            ctext(d, x, y - 48, f"step {i + 1}", F("m", 22), fade(WHITE, a * ki))
    caption(d, "It works out the steps by itself", a * pr(u, 2.0, 2.6), y=900)


PARTS = [("Tools", "take action", BLUE, 4.2), ("Memory", "keep track", MINT, 5.9), ("Loop", "keep going", ROSE, 7.6)]


def s3(img, d, u, a):
    label(d, "4 PARTS", a, AMBER)
    ctext(d, W // 2, 180, "What an agent is made of", F("b", 54), fade(WHITE, a * pr(u, 0, .5)))
    cx, cy = W // 2, 560
    km = pr(u, 2.2, 2.8)
    r = 120 * km
    for g in range(4, 0, -1):
        d.ellipse((cx - r - g * 12, cy - r - g * 12, cx + r + g * 12, cy + r + g * 12), outline=fade(AMBER, a * km * .1 * g), width=3)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fade(mix(INK, AMBER, .35), a * km), outline=fade(AMBER, a * km), width=4)
    ctext(d, cx, cy - 18, "Model", F("b", 44), fade(WHITE, a * km))
    ctext(d, cx, cy + 28, "thinks", F("m", 28), fade(WHITE, a * km))
    angs = [-150, -30, 90]
    for (nm, sub, c, t0), ang in zip(PARTS, angs):
        k = pr(u, t0 - .3, t0 + .3)
        rad = math.radians(ang)
        R = 330 + (1 - k) * 60
        x, y = cx + R * math.cos(rad), cy + R * math.sin(rad)
        d.line((cx + 130 * math.cos(rad), cy + 130 * math.sin(rad), x - 95 * math.cos(rad), y - 70 * math.sin(rad)),
               fill=fade(c, a * k * .7), width=4)
        rr(d, (x - 120, y - 62, x + 120, y + 62), 30, fill=fade(mix(INK, c, .3), a * k), outline=fade(c, a * k), width=3)
        ctext(d, x, y - 16, nm, F("b", 36), fade(WHITE, a * k))
        ctext(d, x, y + 26, sub, F("m", 24), fade(WHITE, a * k * .85))
    if u > 7.6:  # loop arrow spinning around model
        ang0 = (u - 7.6) * 3
        for j in range(18):
            aa = ang0 + j * 0.12
            x, y = cx + 165 * math.cos(aa), cy + 165 * math.sin(aa)
            d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=fade(ROSE, a * (j / 18)))


CUST = [("Acme Co", "$48,200"), ("Brightline", "$12,900"), ("Nova Foods", "$41,700"), ("Kestrel", "$9,400"),
        ("Harbor Ltd", "$37,500")]
TOP = {0, 2, 4}


def s4(img, d, u, a):
    label(d, "EXAMPLE", a, AMBER)
    kg = pr(u, 0.2, 0.7)
    rr(d, (140, 140, 940, 230), 45, fill=fade(mix(INK, AMBER, .25), a * kg), outline=fade(AMBER, a * kg), width=3)
    ctext(d, W // 2, 185, "Goal: thank our top 3 customers", F("b", 36), fade(WHITE, a * kg))
    # sales table
    kt = pr(u, 3.2, 3.8)
    x0, y0 = 120, 290
    rr(d, (x0, y0, x0 + 400, y0 + 400), 20, fill=fade((18, 20, 30), a * kt), outline=fade(BLUE, a * kt), width=2)
    d.text((x0 + 24, y0 + 36), "Sales data", font=F("b", 28), fill=fade(BLUE, a * kt), anchor="lm")
    for i, (nm, amt) in enumerate(CUST):
        y = y0 + 100 + i * 60
        hl = i in TOP and u > 5.3
        if hl:
            rr(d, (x0 + 12, y - 25, x0 + 388, y + 25), 12, fill=fade(mix(INK, MINT, .35), a * pr(u, 5.3, 5.8)))
        d.text((x0 + 28, y), nm, font=F("m", 26), fill=fade(WHITE, a * kt), anchor="lm")
        d.text((x0 + 372, y), amt, font=F("b", 26), fill=fade(MINT if hl else WHITE, a * kt), anchor="rm")
    # emails
    names = [CUST[i][0] for i in sorted(TOP)]
    for j, nm in enumerate(names):
        k = pr(u, 6.9 + j * 0.45, 7.3 + j * 0.45)
        x = 580 + (1 - k) * 80
        y = 300 + j * 135
        rr(d, (x, y, x + 380, y + 115), 18, fill=fade((24, 26, 38), a * k), outline=fade(AMBER, a * k), width=2)
        d.text((x + 24, y + 32), f"To: {nm}", font=F("b", 26), fill=fade(AMBER, a * k), anchor="lm")
        d.text((x + 24, y + 76), "Thank you for your ...", font=F("m", 24), fill=fade(WHITE, a * k), anchor="lm")
    caption(d, "Checks data  ·  finds top 3  ·  drafts emails", a * pr(u, 3.5, 4.1), y=880)
    ctext(d, W // 2, 1000, "illustrative example", F("r", 22), fade(MUTED, a * .8))


def s5(img, d, u, a):
    label(d, "THE LOOP", a, ROSE)
    ctext(d, W // 2, 190, "After every step", F("b", 60), fade(WHITE, a * pr(u, 0, .5)))
    cx, cy, R = W // 2, 580, 230
    nodes = [("Act", BLUE), ("Look at result", MINT), ("Decide next", AMBER)]
    ang = -math.pi / 2 + u * 1.6
    for j in range(40):
        aa = ang - j * 0.05
        x, y = cx + R * math.cos(aa), cy + R * math.sin(aa)
        d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=fade(ROSE, a * (1 - j / 40)))
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=fade((60, 62, 80), a), width=3)
    for i, (nm, c) in enumerate(nodes):
        k = pr(u, 0.4 + i * 0.5, 0.8 + i * 0.5)
        aa = -math.pi / 2 + i * 2 * math.pi / 3
        x, y = cx + R * math.cos(aa), cy + R * math.sin(aa)
        pill(d, x, y, nm, c, a * k, 30, .4)


def s6(img, d, u, a):
    label(d, "YOU STAY IN CONTROL", a, MINT)
    ctext(d, W // 2, 190, "It asks before", F("b", 60), fade(WHITE, a * pr(u, 0, .5)))
    ctext(d, W // 2, 260, "anything important", F("b", 60), fade(MINT, a * pr(u, .2, .7)))
    kq = pr(u, 1.0, 1.5)
    rr(d, (240, 380, 840, 680), 30, fill=fade((20, 22, 34), a * kq), outline=fade(MINT, a * kq), width=3)
    ctext(d, W // 2, 450, "Send 3 thank-you emails?", F("b", 40), fade(WHITE, a * kq))
    press = 3.0 < u < 3.6
    rr(d, (300, 540, 520, 620), 26, fill=fade(MINT if press else mix(INK, MINT, .35), a * kq), outline=fade(MINT, a * kq), width=3)
    ctext(d, 410, 580, "Approve", F("b", 32), fade(INK if press else WHITE, a * kq))
    rr(d, (560, 540, 780, 620), 26, fill=fade((30, 32, 44), a * kq), outline=fade(MUTED, a * kq), width=2)
    ctext(d, 670, 580, "Edit", F("b", 32), fade(MUTED, a * kq))
    if u > 1.8:
        k = pr(u, 1.8, 3.0)
        mx, my = 760 + (420 - 760) * k, 860 + (590 - 860) * k
        d.polygon([(mx, my), (mx, my + 40), (mx + 11, my + 30), (mx + 26, my + 30)], fill=fade(WHITE, a))
    if u > 3.6:
        check(d, 505, 730, 70, fade(MINT, a * pr(u, 3.6, 3.9)), 10)


def s7(img, d, u, a):
    label(d, "THE DIFFERENCE", a, AMBER)
    rows = [("Chatbot", "gives you answers", BLUE, 0.3), ("Agent", "gets the job done", AMBER, 2.9)]
    for i, (nm, txt, c, t0) in enumerate(rows):
        k = pr(u, t0, t0 + .5)
        y = 290 + i * 280
        x = 140 + (1 - k) * 100
        if i == 1 and k > 0:
            for g in range(3, 0, -1):
                rr(d, (x - g * 8, y - g * 8, x + 800 + g * 8, y + 220 + g * 8), 40, outline=fade(AMBER, a * k * .15 * g), width=3)
        rr(d, (x, y, x + 800, y + 220), 36, fill=fade(mix(INK, c, .22), a * k), outline=fade(c, a * k), width=3)
        d.text((x + 50, y + 75), nm, font=F("b", 58), fill=fade(c, a * k), anchor="lm")
        d.text((x + 50, y + 155), txt, font=F("m", 42), fill=fade(WHITE, a * k), anchor="lm")


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
            frame(t).save(f"/home/claude/agent/p_{t:05.1f}.jpg", quality=88)
        sys.exit()
    n = int(END * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
                          "-pix_fmt", "yuv420p", "/home/claude/agent/silent_tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    import os
    os.replace("/home/claude/agent/silent_tmp.mp4", "/home/claude/agent/silent.mp4")
    M.mix_voice("/home/claude/agent/silent.mp4", "/home/claude/agent/vo.mp3", "/home/claude/agent/agent_explainer.mp4", M.VO_START)
    print("done", END)
