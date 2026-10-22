import subprocess, math, random, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import os
D = os.path.join(os.getcwd(), "")  # outputs go to the current directory
W, H, FPS, DUR = 1080, 1920, 30, 23.0
BOLD = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
SERIF = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
PAPER = (244, 239, 230); INK = (28, 28, 30); GOLD = (212, 154, 31); GREY = (140, 136, 130)
f_cap = ImageFont.truetype(BOLD, 64); f_tag = ImageFont.truetype(BOLD, 32)
f_day = ImageFont.truetype(BOLD, 110); f_bub = ImageFont.truetype(SERIF, 44)
f_end = ImageFont.truetype(BOLD, 78); f_end2 = ImageFont.truetype(SERIF, 50)

rng = np.random.default_rng(1)
grain = (rng.normal(0, 4, (H, W))).astype(np.float32)[..., None]
paper = np.clip(np.array(PAPER, np.float32) + grain, 0, 255).astype(np.uint8)
paper_img = Image.fromarray(paper)

N, SW, SH, X0, Y0 = 12, 60, 80, 150, 1650
def stand(k):
    if k <= 0: return (X0 - 70 + k * 0, Y0)
    return (X0 + (k - 1) * SW + SW / 2, Y0 - k * SH)
def pos(kf):
    k0 = math.floor(kf); fr = kf - k0
    a, b = stand(k0), stand(min(k0 + 1, N))
    x = a[0] + (b[0] - a[0]) * fr
    y = a[1] + (b[1] - a[1]) * fr - math.sin(fr * math.pi) * 22
    return x, y, fr

def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)
def seg(t, a, b): return ease((t - a) / (b - a))

def wob(seed):
    r = random.Random(seed)
    return lambda: r.uniform(-2.2, 2.2)

def line(d, pts, col, w, jit):
    pts = [(x + jit(), y + jit()) for x, y in pts]
    d.line(pts, fill=col, width=w, joint="curve")
    for x, y in (pts[0], pts[-1]):
        d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=col)

def mix(c, a): return tuple(int(PAPER[i] + (c[i] - PAPER[i]) * a) for i in range(3))

def man(d, x, y, phase, pose, col, jit, dirn=1):
    w = 8
    hip = (x, y - 72); neck = (x + (6 * dirn if pose == "sad" else 0), y - 140)
    head = (neck[0] + (10 * dirn if pose == "sad" else 0), neck[1] - (20 if pose == "sad" else 26))
    sw_ = math.sin(phase)
    if pose in ("walk",):
        legs = [(hip[0] + 34 * sw_ * dirn, y), (hip[0] - 34 * sw_ * dirn, y)]
        knees = [(hip[0] + 22 * sw_ * dirn + 6 * dirn, y - 36), (hip[0] - 22 * sw_ * dirn + 6 * dirn, y - 36)]
        arms = [(neck[0] - 30 * sw_ * dirn, neck[1] + 58), (neck[0] + 30 * sw_ * dirn, neck[1] + 58)]
    elif pose == "cheer":
        legs = [(hip[0] + 26, y), (hip[0] - 26, y)]; knees = [(hip[0] + 14, y - 36), (hip[0] - 14, y - 36)]
        lift = 8 * math.sin(phase * 2)
        arms = [(neck[0] + 46, neck[1] - 52 - lift), (neck[0] - 46, neck[1] - 52 - lift)]
    else:  # idle / sad
        b = 2 * math.sin(phase)
        legs = [(hip[0] + 18, y), (hip[0] - 18, y)]; knees = [(hip[0] + 10, y - 36), (hip[0] - 10, y - 36)]
        arms = [(neck[0] + 22, neck[1] + 62 + b), (neck[0] - 22, neck[1] + 62 + b)]
    for k, f in zip(knees, legs): line(d, [hip, k, f], col, w, jit)
    line(d, [hip, neck], col, w, jit)
    for a in arms:
        sh = (neck[0], neck[1] + 12)
        el = ((sh[0] + a[0]) / 2 + (6 if pose != "cheer" else 0), (sh[1] + a[1]) / 2)
        line(d, [sh, el, a], col, w, jit)
    r = 24
    hx, hy = head[0] + jit(), head[1] + jit()
    d.ellipse((hx - r, hy - r, hx + r, hy + r), fill=PAPER, outline=col, width=w)

def caption(d, t, s, e, text, gold, y=250):
    if not (s <= t <= e): return
    a = min(seg(t, s, s + 0.35), 1 - seg(t, e - 0.3, e))
    words = text.split(); lines, cur = [], []
    for w_ in words:
        if d.textlength(" ".join(cur + [w_]), font=f_cap) > 920 and cur: lines.append(cur); cur = [w_]
        else: cur.append(w_)
    lines.append(cur)
    for li, ln in enumerate(lines):
        lw = d.textlength(" ".join(ln), font=f_cap); x = (W - lw) / 2
        for w_ in ln:
            c = GOLD if w_.strip(".,—") in gold else INK
            d.text((x, y + li * 80 + (1 - a) * 14), w_, font=f_cap, fill=mix(c, a))
            x += d.textlength(w_ + " ", font=f_cap)

def frame(t):
    im = paper_img.copy(); d = ImageDraw.Draw(im)
    jit = wob(int(t * FPS) // 4)  # hand-drawn "boil"

    if t < 19.0:
        # brand
        tag = "THE SUCCESS CODE"; tw = d.textlength(tag, font=f_tag)
        d.text(((W - tw) / 2, 110), tag, font=f_tag, fill=INK)
        d.line([((W - tw) / 2, 156), ((W + tw) / 2, 156)], fill=GOLD, width=3)
        # sun rays at the top when reached
        sa = seg(t, 17.0, 17.8)
        top = stand(N)
        if sa > 0:
            cx, cy = top[0] + 60, top[1] - 120
            for i in range(14):
                ang = i * (2 * math.pi / 14) + t * 0.4
                r1, r2 = 120, 120 + 90 * sa
                d.line([(cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)),
                        (cx + r2 * math.cos(ang), cy + r2 * math.sin(ang))], fill=mix(GOLD, sa), width=7)
        # stairs
        poly = [(40, Y0), (X0, Y0)]
        for k in range(N):
            poly += [(X0 + k * SW, Y0 - (k + 1) * SH), (X0 + (k + 1) * SW, Y0 - (k + 1) * SH)]
        poly += [(1040, Y0 - N * SH)]
        d.polygon(poly + [(1040, Y0 + 200), (40, Y0 + 200)], fill=(230, 222, 208))
        line(d, poly, INK, 7, jit)
        # flag
        fx, fy = 980, Y0 - N * SH
        line(d, [(fx, fy), (fx, fy - 170)], INK, 7, jit)
        d.polygon([(fx, fy - 170), (fx + 70, fy - 145), (fx, fy - 120)], fill=GOLD)

        # Day counter
        if t >= 3.5:
            if t < 9: day = 1 + int(29 * seg(t, 3.5, 8.5))
            elif t < 13: day = 30
            else: day = 30 + int(335 * seg(t, 13, 17.0))
            txt = f"DAY {day}"
            d.text((110, 520), txt, font=f_day, fill=GOLD if t > 17 else INK)

        # Man A (quits)
        phase = t * 9
        if t < 3.5: kA, poseA, dA = 0, "idle", 1
        elif t < 8.5: kA, poseA, dA = 4 * seg(t, 3.5, 8.5) * 0 + (t - 3.5) / 5 * 4, "walk", 1
        elif t < 11.5: kA, poseA, dA = 4, "sad", 1
        else: kA, poseA, dA = max(0, 4 - (t - 11.5) / 1.5 * 4), "walk", -1
        aA = 1.0 if t < 11.5 else max(0, 1 - (t - 11.5) / 1.8)
        if aA > 0:
            x, y, _ = pos(kA); x -= 26
            man(d, x, y, phase, poseA, mix(GREY, aA), jit, dA)
            if 9.3 < t < 11.8:
                ba = min(seg(t, 9.3, 9.6), 1 - seg(t, 11.5, 11.8))
                bx, by = x - 300, y - 340
                d.rounded_rectangle((bx, by, bx + 420, by + 96), 40, fill=mix((255, 255, 255), ba), outline=mix(INK, ba), width=5)
                d.polygon([(bx + 270, by + 94), (bx + 310, by + 94), (x - 4, y - 205)], fill=mix(INK, ba))
                d.text((bx + 30, by + 22), "It's not working…", font=f_bub, fill=mix(INK, ba))
        # Man B (keeps going)
        if t < 3.5: kB, poseB = 0, "idle"
        elif t < 8.5: kB, poseB = (t - 3.5) / 5 * 4, "walk"
        elif t < 13: kB, poseB = 4 + (t - 8.5) / 4.5 * 1, "walk"
        elif t < 17: kB, poseB = 5 + (t - 13) / 4 * 7, "walk"
        else: kB, poseB = N, "cheer"
        x, y, _ = pos(min(kB, N))
        man(d, x + 10, y, phase, poseB, INK, jit, 1)

        caption(d, t, 0.3, 3.4, "TWO PEOPLE STARTED ON THE SAME DAY.", {"SAME", "DAY"})
        caption(d, t, 3.6, 8.9, "DAY 1. BOTH WERE EXCITED.", {"EXCITED"})
        caption(d, t, 9.0, 12.9, "DAY 30. ONE QUIT. NO RESULTS YET.", {"QUIT"})
        caption(d, t, 13.0, 16.9, "THE OTHER KEPT CLIMBING. QUIETLY.", {"KEPT", "CLIMBING"})
        caption(d, t, 17.0, 18.9, "DAY 365.", {"365"})
    # end card
    ea = seg(t, 18.6, 19.4)
    if ea > 0:
        ov = Image.blend(im, paper_img, ea); im = ov; d = ImageDraw.Draw(im)
        if t > 19.0:
            a = seg(t, 19.2, 19.9)
            lines = [("SUCCESS ISN'T ONE", INK), ("GIANT LEAP.", INK), ("", INK),
                     ("IT'S SMALL STEPS", INK), ("NOBODY CLAPS FOR.", GOLD)]
            for i, (s_, c) in enumerate(lines):
                lw = d.textlength(s_, font=f_end)
                d.text(((W - lw) / 2, 700 + i * 96), s_, font=f_end, fill=mix(c, a))
            b = seg(t, 20.6, 21.3)
            for i, s_ in enumerate(["— The Success Code", "Follow for daily wisdom"]):
                lw = d.textlength(s_, font=f_end2)
                d.text(((W - lw) / 2, 1260 + i * 72), s_, font=f_end2, fill=mix(INK if i == 0 else GREY, b))
    return im

out = D + "stick_silent.mp4"
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                      "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "22",
                      "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
for i in range(int(DUR * FPS)): p.stdin.write(frame(i / FPS).tobytes())
p.stdin.close(); p.wait()

# ---- music: soft piano-like arpeggios, I–V–vi–IV, lift at the summit ----
SR = 44100; n = int(SR * DUR); audio = np.zeros(n, np.float32)
def note(f, start, dur, vol):
    s = int(start * SR); L = int(dur * SR)
    if s >= n: return
    L = min(L, n - s); tt = np.arange(L) / SR
    env = np.exp(-tt * 3.2) * np.minimum(1, tt / 0.005)
    wv = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) + 0.12 * np.sin(6 * np.pi * f * tt)
    audio[s:s + L] += vol * env * wv
chords = [[261.63, 329.63, 392.0], [196.0, 246.94, 293.66], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63]]
beat = 0.5; t0 = 0.0; ci = 0
while t0 < DUR - 1:
    ch = chords[ci % 4]; up = 2 if t0 > 17 else 1
    note(ch[0] / 2, t0, 2.2, 0.22)
    for j in range(4):
        note(ch[[0, 1, 2, 1][j]] * up, t0 + j * beat, 1.2, 0.13 if t0 < 13 else 0.17)
    t0 += 4 * beat; ci += 1
fade = np.minimum(1, np.arange(n) / (SR * 1.0)) * np.minimum(1, (n - np.arange(n)) / (SR * 2.0))
audio *= fade; audio /= max(1e-6, np.abs(audio).max()) / 0.6
with wave.open(D + "stick_music.wav", "wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((audio * 32767).astype(np.int16).tobytes())
print("ok")
