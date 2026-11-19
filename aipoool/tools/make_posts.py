"""Build AIPOOOL LinkedIn media + captions.

Usage: python3 make_posts.py <posts_module.py> <out_dir>
The posts module defines POSTS (list of dicts, see posts_example.py) and caption(p).
kind "image" -> <id>.jpg ; kind "video" -> <id>.mp4 ; plus <id>.txt caption and <id>_frame.jpg preview.
"""
import sys, os, subprocess, shutil, importlib.util, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import ImageDraw
import brand as B


def load(path):
    spec = importlib.util.spec_from_file_location("posts_mod", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def seed_of(p):
    return sum(ord(c) for c in p["id"])


def still(p, path):
    img = B.background(seed_of(p))
    d = ImageDraw.Draw(img)
    B.header(img, d, p["tag"], p["title"])
    for i, (big, small) in enumerate(p["points"]):
        B.card(d, i, big, small)
    B.footer(d)
    img.save(path, "JPEG", quality=84, optimize=True)


def add_music(src, dst, volume=0.35):
    """Mux the soft music bed under a silent video, faded out at the end."""
    music = os.path.join(HERE, "music_bed.m4a")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                               capture_output=True, text=True, check=True).stdout.strip())
    fade_st = max(0, dur - 2.0)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-stream_loop", "-1", "-i", music,
                    "-filter_complex", f"[1:a]volume={volume},afade=t=in:d=1,afade=t=out:st={fade_st:.2f}:d=2[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-t", f"{dur:.2f}", "-movflags", "+faststart", dst], check=True)


def video(p, path, fps=30):
    tmp = tempfile.mkdtemp()
    base = B.background(seed_of(p))
    starts = [2.2 + i * 3.0 for i in range(4)]
    end_cards = starts[-1] + 4.0
    total = end_cards + 3.0
    title = p["title"]
    for f in range(int(total * fps)):
        t = f / fps
        img = base.copy(); d = ImageDraw.Draw(img)
        if t < end_cards:
            shown = title[: max(1, int(len(title) * min(1, t / 1.6)))]
            B.header(img, d, p["tag"], shown)
            for i, (big, small) in enumerate(p["points"]):
                a = (t - starts[i]) / 0.5
                if a > 0:
                    a = min(1, a)
                    B.card(d, i, big, small, alpha=a, dy=int((1 - a) * 40))
            d.rectangle((0, B.H - 8, int(B.W * t / total), B.H), fill=B.GOLD)
            B.footer(d)
        else:
            a = min(1, (t - end_cards) / 0.6)
            B.logo(img, 240, 330, 600)
            d.text((B.W / 2, 560), "Stay ahead in the race of Tech & AI", font=B.font("Bold", 40),
                   fill=tuple(int(c * a) for c in (255, 255, 255)), anchor="mm")
            d.text((B.W / 2, 630), "Follow AIPOOOL for daily AI & robotics news", font=B.font("Medium", 30),
                   fill=tuple(int(c * a) for c in B.GOLD), anchor="mm")
        img.save(f"{tmp}/{f:05d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", f"{tmp}/%05d.png",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "30", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", f"{tmp}/silent.mp4"], check=True)
    add_music(f"{tmp}/silent.mp4", path)
    shutil.rmtree(tmp)


if __name__ == "__main__":
    mod = load(sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for p in mod.POSTS:
        if p["kind"] == "video":
            video(p, f"{out}/{p['id']}.mp4")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "12", "-i", f"{out}/{p['id']}.mp4",
                            "-frames:v", "1", f"{out}/{p['id']}_frame.jpg"], check=True)
        else:
            still(p, f"{out}/{p['id']}.jpg")
        open(f"{out}/{p['id']}.txt", "w").write(mod.caption(p))
    print(sorted(os.listdir(out)))
