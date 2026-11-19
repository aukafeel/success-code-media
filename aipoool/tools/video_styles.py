"""AIPOOOL video styles. Same logo, colours and Inter fonts; different layouts and motion.

Every style is driven by a cue timeline, so visuals can follow a voiceover exactly:
  cues = {"points": [t1, t2, t3, t4], "outro": t_outro, "end": t_end}
  - before points[0]: the title / intro
  - point i appears at points[i]
  - from outro: the closing logo card, until end

Styles:
  grid   - title on top, the 4 stat cards pop in (2x2)
  slides - title slide, then one full-screen slide per point (best match for narration)
  list   - title on top, 4 full-width rows slide in from the left
"""
import datetime
from PIL import ImageDraw
import brand as B

FPS = 30
STYLES = ["grid", "slides", "list"]


def pick_style(p):
    if p.get("style") in STYLES:
        return p["style"]
    day = datetime.date.fromisoformat(p["when"][:10]).toordinal()
    return STYLES[day % len(STYLES)]


def default_cues(style, n=4):
    """Timeline for videos without a voiceover (fast reveals)."""
    if style == "slides":
        pts = [2.0 + i * 2.1 for i in range(n)]
        outro = pts[-1] + 2.1 + 3.2  # slides add a recap before the outro when silent
        return {"points": pts, "outro": outro, "end": outro + 2.5, "recap": pts[-1] + 2.1}
    gap = 0.6 if style == "grid" else 0.5
    pts = [1.0 + i * gap for i in range(n)]
    outro = pts[-1] + 6.0
    return {"points": pts, "outro": outro, "end": outro + 2.5}


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def mix(c, a):
    return tuple(int(B.INK[k] + (c[k] - B.INK[k]) * a) for k in range(3))


def typed(title, t, dur=0.8):
    return title[: max(1, int(len(title) * min(1, t / dur)))]


def outro(img, d, t0):
    a = ease(t0 / 0.5)
    B.logo(img, 240, 330, 600)
    d.text((B.W / 2, 560), "Stay ahead in the race of Tech & AI", font=B.font("Bold", 40),
           fill=mix((255, 255, 255), a), anchor="mm")
    d.text((B.W / 2, 630), "Follow AIPOOOL for daily AI & robotics news", font=B.font("Medium", 30),
           fill=mix(B.GOLD, a), anchor="mm")


def progress(d, t, total):
    d.rectangle((0, B.H - 8, int(B.W * t / total), B.H), fill=B.GOLD)


def frames(style, p, base, cues):
    total = cues["end"]
    for f in range(int(total * FPS)):
        t = f / FPS
        img = base.copy(); d = ImageDraw.Draw(img)
        if t >= cues["outro"]:
            outro(img, d, t - cues["outro"])
        else:
            DRAW[style](img, d, p, t, cues)
            progress(d, t, total)
        yield img


# ---------- grid ----------
def draw_grid(img, d, p, t, cues):
    B.header(img, d, p["tag"], typed(p["title"], t))
    for i, (big, small) in enumerate(p["points"]):
        a = ease((t - cues["points"][i]) / 0.35)
        if a > 0:
            B.card(d, i, big, small, alpha=a, dy=int((1 - a) * 30))
    B.footer(d)


# ---------- list ----------
def list_row(d, i, big, small, a, dx):
    y = 450 + i * 140
    x0, x1 = 72 + dx, 1008 + dx
    d.rounded_rectangle((x0, y, x1, y + 118), radius=22, fill=mix(B.CARD, a), outline=mix((60, 54, 30), a), width=2)
    d.rounded_rectangle((x0, y, x0 + 250, y + 118), radius=22, fill=mix((34, 28, 12), a))
    bf = B.font("Black", 52)
    while d.textlength(big, font=bf) > 210 and bf.size > 30:
        bf = B.font("Black", bf.size - 4)
    d.text((x0 + 125, y + 59), big, font=bf, fill=mix(B.GOLD, a), anchor="mm")
    d.multiline_text((x0 + 285, y + 59), small, font=B.font("Medium", 28), fill=mix(B.TXT, a),
                     spacing=8, anchor="lm")


def draw_list(img, d, p, t, cues):
    B.header(img, d, p["tag"], typed(p["title"], t))
    for i, (big, small) in enumerate(p["points"]):
        a = ease((t - cues["points"][i]) / 0.35)
        if a > 0:
            list_row(d, i, big, small, a, -int((1 - a) * 220))
    B.footer(d)


# ---------- slides ----------
def draw_slides(img, d, p, t, cues):
    pts = cues["points"]
    n = len(pts)
    if t < pts[0]:
        B.logo(img, 66, 54, 300)
        a = ease(t / 0.4)
        tf = B.font("Bold", 30)
        tw = d.textlength(p["tag"], font=tf)
        d.rounded_rectangle((72, 380, 72 + tw + 56, 436), radius=28, fill=mix(B.GOLD, a))
        d.text((100, 389), p["tag"], font=tf, fill=B.INK)
        d.multiline_text((72, 480 + int((1 - a) * 40)), typed(p["title"], t, 0.9),
                         font=B.font("ExtraBold", 84), fill=mix((255, 255, 255), a), spacing=18)
        return
    if cues.get("recap") and t >= cues["recap"]:
        lt = t - cues["recap"]
        B.header(img, d, p["tag"], p["title"])
        for i, (big, small) in enumerate(p["points"]):
            a = ease((lt - i * 0.12) / 0.3)
            if a > 0:
                B.card(d, i, big, small, alpha=a)
        B.footer(d)
        return
    k = max(i for i in range(n) if pts[i] <= t)
    lt = t - pts[k]
    big, small = p["points"][k]
    a = ease(lt / 0.3)
    dx = int((1 - a) * 160)
    B.logo(img, 66, 54, 220)
    d.text((B.W - 72, 92), f"{k + 1} / {n}", font=B.font("Bold", 30), fill=B.MUTED, anchor="rm")
    d.rectangle((72 + dx, 360, 84 + dx, 560), fill=mix(B.GOLD, a))
    bf = B.font("Black", 180)
    while d.textlength(big, font=bf) > 900 and bf.size > 90:
        bf = B.font("Black", bf.size - 10)
    d.text((120 + dx, 350), big, font=bf, fill=mix(B.GOLD, a))
    d.multiline_text((120 + dx, 620), small, font=B.font("SemiBold", 48), fill=mix(B.TXT, a), spacing=16)
    for j in range(n):
        x = 72 + j * 40
        d.ellipse((x, 980, x + 18, 998), fill=B.GOLD if j <= k else (60, 54, 30))
    B.footer(d)


DRAW = {"grid": draw_grid, "slides": draw_slides, "list": draw_list}
