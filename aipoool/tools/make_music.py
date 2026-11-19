"""Generate an original, royalty-free soft ambient music bed for AIPOOOL videos.

Usage: python3 make_music.py <out.wav> [seconds]
Warm pad chords (Cmaj7 - Am7 - Fmaj7 - G6) with a gentle bell arpeggio, soft and calm.
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def pad(freqs, dur, rng):
    t = np.arange(int(SR * dur)) / SR
    out = np.zeros_like(t)
    for f in freqs:
        for det in (-0.12, 0.0, 0.12):  # slight detune for warmth
            ph = rng.uniform(0, 2 * np.pi)
            ff = f * 2 ** (det / 12)
            out += np.sin(2 * np.pi * ff * t + ph) + 0.25 * np.sin(4 * np.pi * ff * t + ph)
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)  # slow swell in/out
    return out * env / (len(freqs) * 3)


def bell(f, dur):
    t = np.arange(int(SR * dur)) / SR
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t * 3.0)


def render(seconds):
    rng = np.random.default_rng(7)
    chords = [[48, 55, 59, 64], [45, 52, 55, 60], [41, 48, 52, 57], [43, 50, 52, 59]]  # C, Am, F, G
    arps = [[72, 76, 79, 83], [69, 72, 76, 79], [65, 69, 72, 76], [67, 71, 74, 76]]
    bar = 4.0
    n = int(SR * seconds)
    mix = np.zeros(n + SR * 6)
    i = 0
    pos = 0.0
    while pos < seconds:
        c = chords[i % 4]
        start = int(pos * SR)
        p = pad([midi(m) for m in c], bar + 1.2, rng)  # overlap for smooth transitions
        mix[start:start + len(p)] += 0.55 * p
        for k, m in enumerate(arps[i % 4]):
            b = bell(midi(m), 2.0)
            s = start + int(k * bar / 4 * SR)
            mix[s:s + len(b)] += 0.10 * b
        pos += bar
        i += 1
    mix = mix[:n]
    b, a = butter(2, 3500 / (SR / 2), "low")  # soften highs
    mix = lfilter(b, a, mix)
    fade = int(SR * 1.5)
    mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix = mix / np.max(np.abs(mix)) * 0.8
    return np.stack([mix, np.roll(mix, int(SR * 0.012))], axis=1)  # gentle stereo width


if __name__ == "__main__":
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 40
    wavfile.write(sys.argv[1], SR, (render(secs) * 32767).astype(np.int16))
    print("ok", sys.argv[1])
