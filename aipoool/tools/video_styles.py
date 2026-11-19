"""AIPOOOL video styles. Same logo, colours and Inter fonts; different layouts and motion.

Styles:
  grid   - title, then the 4 stat cards pop in quickly (2x2 grid)
  slides - title slide, then one big full-screen slide per point, then a recap
  list   - title, then 4 full-width rows slide in from the left

pick_style(post) rotates by the post date so consecutive days look different
(override with post["style"]).
"""
import datetime
from PIL import Image, ImageDraw
import brand as B

FPS = 30
STYLES = ["grid", "slides", "list"]


def pick_style(p):
    if p.get("style") in STYLES:
        return p["style"]
    day = datetime.date.fromisoformat(p["when"][:10]).toordinal()
    return STYLES[day % len(STYLES)]


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


# ---------- grid ----------
def grid_frames(p, base):
    starts = [1.0 + i * 0.6 for i in range(4)]
    hold_end = starts[-1] + 6.0
    total = hold_end + 2.5
    for f in range(int(total * FPS)):
        t = f / FPS
        img = base.copy(); d = ImageDraw.Draw(img)
        if t < hold_end:
            B.header(img, d, p["tag"], typed(p["title"], t))
            for i, (big, small) in enumerate(p["points"]):
                a = ease((t - starts[i]) / 0.35)
                if a > 0:
                    B.card(d, i, big, small, alpha=a, dy=int((1 - a) * 30))
            progress(d, t, total); B.footer(d)
        else:
            outro(img, d, t - hold_end)
        yield img


# ---------- slides ----------
def slides_frames(p, base):
    intro, per, recap = 2.0, 2.1, 3.2
    n = len(p["points"])
    t_recap = intro + n * per
    hold_end = t_recap + recap
    total = hold_end + 2.5
    for f in range(int(total * FPS)):
        t = f / FPS
        img = base.copy(); d = ImageDraw.Draw(img)
        if t < intro:
            B.logo(img, 66, 54, 300)
            a = ease(t / 0.4)
            tf = B.font("Bold", 30)
            tw = d.textlength(p["tag"], font=tf)
            d.rounded_rectangle((72, 380, 72 + tw + 56, 436), radius=28, fill=mix(B.GOLD, a))
            d.text((100, 389), p["tag"], font=tf, fill=B.INK)
            d.multiline_text((72, 480 + int((1 - a) * 40)), typed(p["title"], t, 0.9),
                             font=B.font("ExtraBold", 84), fill=mix((255, 255, 255), a), spacing=18)
        elif t < t_recap:
            k = int((t - intro) // per)
            lt = (t - intro) - k * per
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
            d.multiline_text((120 + dx, 620), small,
                             font=B.font("SemiBold", 48), fill=mix(B.TXT, a), spacing=16)
            for j in range(n):  # progress dots
                x = 72 + j * 40
                d.ellipse((x, 980, x + 18, 998), fill=B.GOLD if j <= k else (60, 54, 30))
            B.footer(d)
        elif t < hold_end:
            lt = t - t_recap
            B.header(img, d, p["tag"], p["title"])
            for i, (big, small) in enumerate(p["points"]):
                a = ease((lt - i * 0.12) / 0.3)
                if a > 0:
                    B.card(d, i, big, small, alpha=a)
            progress(d, t, total); B.footer(d)
        else:
            outro(img, d, t - hold_end)
        yield img


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


def list_frames(p, base):
    starts = [1.0 + i * 0.5 for i in range(4)]
    hold_end = starts[-1] + 6.0
    total = hold_end + 2.5
    for f in range(int(total * FPS)):
        t = f / FPS
        img = base.copy(); d = ImageDraw.Draw(img)
        if t < hold_end:
            B.header(img, d, p["tag"], typed(p["title"], t))
            for i, (big, small) in enumerate(p["points"]):
                a = ease((t - starts[i]) / 0.35)
                if a > 0:
                    list_row(d, i, big, small, a, -int((1 - a) * 220))
            progress(d, t, total); B.footer(d)
        else:
            outro(img, d, t - hold_end)
        yield img


FRAMES = {"grid": grid_frames, "slides": slides_frames, "list": list_frames}
