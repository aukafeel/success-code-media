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


VO_START = 0.4  # seconds of silence before the voice starts
OUTRO_LINE = "Follow A.I. Pool, to stay ahead in the race of Tech and A.I."  # spoken sign-off, always the last voiceover sentence


def voiceover(segments, out_mp3):
    """ElevenLabs TTS with word timings (voice: Daniel - Radio news host).

    segments = [intro, point1, point2, point3, point4, outro] (one sentence each).
    Returns (mp3_path, [start time in seconds of each segment]) or None without ELEVENLABS_API_KEY.
    """
    import json, base64, urllib.request
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        return None
    voice = os.environ.get("ELEVENLABS_VOICE_ID", "3WqHLnw80rOZqJzW9YRB")
    segs = [s.strip() for s in segments][:-1] + [OUTRO_LINE]
    text = " ".join(segs)
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps({"text": text, "model_id": "eleven_multilingual_v2",
                         "voice_settings": {"stability": 0.55, "similarity_boost": 0.8}}).encode(),
        headers={"xi-api-key": key, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        res = json.loads(r.read())
    open(out_mp3, "wb").write(base64.b64decode(res["audio_base64"]))
    al = res.get("alignment") or res.get("normalized_alignment")
    starts_t = al["character_start_times_seconds"]
    starts, pos = [], 0
    for s in segs:
        idx = min(pos, len(starts_t) - 1)
        starts.append(float(starts_t[idx]))
        pos += len(s) + 1
    return out_mp3, starts


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True, check=True).stdout.strip())


def mix_voice(src, vo, dst, start=0.4):
    """Video + voiceover at full level + music bed kept low underneath."""
    music = os.path.join(HERE, "music_bed.m4a")
    dur = duration(src)
    fade_st = max(0, dur - 2.0)
    ms = int(start * 1000)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", vo, "-stream_loop", "-1", "-i", music,
                    "-filter_complex",
                    f"[1:a]adelay={ms}|{ms},volume=1.0[v];"
                    f"[2:a]volume=0.12,afade=t=in:d=1,afade=t=out:st={fade_st:.2f}:d=2[m];"
                    f"[v][m]amix=inputs=2:duration=longest:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-t", f"{dur:.2f}", "-movflags", "+faststart", dst], check=True)


def video(p, path):
    import video_styles as VS
    style = VS.pick_style(p)
    theme = VS.pick_theme(p)
    B.set_theme(theme)
    tmp = tempfile.mkdtemp()
    base = B.background(seed_of(p))
    vo = voiceover(p["voiceover"], f"{tmp}/vo.mp3") if p.get("voiceover") else None
    if vo:
        mp3, st = vo
        n = len(p["points"])
        cues = {"points": [max(0.3, VO_START + st[i + 1] - 0.15) for i in range(n)],
                "outro": VO_START + st[n + 1] - 0.1,
                "end": VO_START + duration(mp3) + 1.6}
    else:
        cues = VS.default_cues(style, len(p["points"]))
    for f, img in enumerate(VS.frames(style, p, base, cues)):
        img.save(f"{tmp}/{f:05d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(VS.FPS), "-i", f"{tmp}/%05d.png",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "30", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", f"{tmp}/silent.mp4"], check=True)
    if vo:
        mix_voice(f"{tmp}/silent.mp4", vo[0], path, start=VO_START)
    else:
        add_music(f"{tmp}/silent.mp4", path)
    shutil.rmtree(tmp)
    B.set_theme("gold")
    print("video style:", style, "theme:", theme, "voiceover:", bool(vo), "cues:", {k: (round(v, 2) if isinstance(v, float) else [round(x, 2) for x in v]) for k, v in cues.items()}, path)


if __name__ == "__main__":
    mod = load(sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for p in mod.POSTS:
        if p["kind"] == "video":
            video(p, f"{out}/{p['id']}.mp4")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "8", "-i", f"{out}/{p['id']}.mp4",
                            "-frames:v", "1", f"{out}/{p['id']}_frame.jpg"], check=True)
        else:
            still(p, f"{out}/{p['id']}.jpg")
        open(f"{out}/{p['id']}.txt", "w").write(mod.caption(p))
    print(sorted(os.listdir(out)))
