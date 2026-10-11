"""Convergence — annonce du lancement (18 s, 100 BPM) : musique 100 % synthétisée + 4 SFX discrets.
Récit sonore : piano chaud (old money) → arpège synthé (new money) → les deux ensemble + rythme →
montée douce vers le V → accord plein au logo → tampon « PREMIER LIVE ». Sortie : track.wav
"""
import os, subprocess, wave
import numpy as np
from scipy.signal import lfilter

FF = os.path.expandvars(r"$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe")
SFXDIR = os.path.expanduser("~/.agents/skills/media-use/audio/assets/sfx/")
HERE = os.path.dirname(os.path.abspath(__file__))
SR, DUR, B = 48000, 18.0, 0.6
N = int(SR * DUR)
rng = np.random.default_rng(5)
mix = np.zeros((N, 2)); sfx = np.zeros((N, 2))
mid = lambda m: 440 * 2 ** ((m - 69) / 12)

def place(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); e = min(N, i + len(sig))
    if i >= N: return
    mix[i:e, 0] += sig[:e - i] * g * np.sqrt((1 - pan) / 2) * 1.414
    mix[i:e, 1] += sig[:e - i] * g * np.sqrt((1 + pan) / 2) * 1.414

def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); return lfilter([1 - a], [1, -a], x)

def piano(m, dur=1.6, g=0.3):
    """piano électrique doux : partiels inharmoniques légers + décroissance"""
    n = int(dur * SR); t = np.arange(n) / SR; f = mid(m)
    x = sum(np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.6 + k * 1.1)) / k ** 1.3 for k in range(1, 9))
    x += 0.3 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 9)        # attaque « tine »
    return x * np.minimum(1, t / 0.004) * np.clip((dur - t) / 0.05, 0, 1) * g

def saw(m, dur, g=0.2, fc=1800, a=0.005, d=0.18):
    n = int(dur * SR); t = np.arange(n) / SR; f = mid(m)
    x = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 16) if f * k < 9000)
    return lp(x, fc) * np.minimum(1, t / a) * np.exp(-t / d) * g

def pad(ms, dur, g=0.06, a=0.6, fc=1400):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for m in ms:
        for det in (-0.004, 0, 0.004):
            f = mid(m) * (1 + det)
            x += sum(np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6)) / k for k in range(1, 8))
    x = lp(x, fc) / len(ms)
    return x * np.minimum(1, t / a) * np.clip((dur - t) / 0.4, 0, 1) * g

def kick(g=0.8):
    n = int(0.4 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(48 + 80 * np.exp(-t / 0.04)) / SR) * np.exp(-t / 0.18) * g

def hat(g=0.12):
    n = int(0.08 * SR); x = rng.standard_normal(n); x = x - lp(x, 7000)
    t = np.arange(n) / SR; return x * np.exp(-t / 0.025) * g

def snap(g=0.25):
    n = int(0.2 * SR); x = rng.standard_normal(n); x = x - lp(x, 1500)
    t = np.arange(n) / SR; return x * np.exp(-t / 0.06) * g

# progression (1 accord = 4 temps) : Am – F – C – G
CH = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
ROOT = [45, 41, 48, 43]

# 0 → 2,4 : piano seul (old money) — accords arpégés lents
for bar in range(1):
    for j, m in enumerate(CH[0] + [CH[0][1] + 12]):
        place(piano(m + 12, 1.8, 0.34), j * B, pan=-0.2)
place(pad(CH[0], 2.6, 0.07), 0)

# 2,4 → 4,8 : arpège synthé (new money) en croches, + piano sur F
arp = [69, 72, 76, 72, 77, 72, 76, 72]
for k in range(8):
    place(saw(arp[k % 8], B / 2 * 0.9, 0.12, fc=2600, d=0.12), 4 * B + k * B / 2, pan=0.3)
for j, m in enumerate(CH[1]): place(piano(m + 12, 1.6, 0.18), 4 * B + j * B, pan=-0.2)

# 4,8 → 9,6 : les deux ensemble + rythme doux (kick 1 & 3, hats, claquement 2 & 4)
for i in range(8):
    t = 8 * B + i * B; c = (2 + i // 4) % 4
    if i % 2 == 0: place(kick(0.75), t)
    else: place(snap(0.2), t)
    place(hat(0.1), t + B / 2, pan=0.25)
    place(saw(ROOT[c] - 12 + 12, B * 0.9, 0.2, fc=500, d=0.3), t)
    for h in range(2):
        place(saw(arp[(i * 2 + h) % 8] - (0 if c else 0), B / 2 * 0.9, 0.09, fc=2400, d=0.1), t + h * B / 2, pan=0.3)
    if i % 4 == 0:
        for j, m in enumerate(CH[c]): place(piano(m + 12, 2.2, 0.16), t + j * 0.08, pan=-0.2)
        place(pad(CH[c], 4 * B + 0.3, 0.04), t)

# 9,6 → 12,0 : le V se dessine — rythme coupé, nappe qui monte + souffle, les deux voix montent ensemble
T6 = 16 * B
place(pad([57, 60, 64, 67], 4 * B + 0.4, 0.16, a=1.2, fc=2400), T6)
n = int(4 * B * SR); tt = np.arange(n) / SR
noise = rng.standard_normal(n); place((noise - lp(noise, 600)) * (tt / tt[-1]) ** 2.4 * 0.09, T6)
for k in range(8):   # piano et arpège qui montent en se répondant
    place(piano(64 + k * 2, 0.9, 0.22), T6 + k * B / 2, pan=-0.3)
    place(saw(64 + k * 2 + 7, 0.25, 0.1, fc=2800, d=0.1), T6 + k * B / 2 + B / 4, pan=0.3)

# 12,0 : logo — accord plein (piano + nappe + basse), groove qui revient
T7 = 20 * B
place(kick(0.9), T7)
for m in (45, 57, 60, 64, 69, 72): place(piano(m + 12 if m < 60 else m, 3.0, 0.16), T7)
place(pad([57, 60, 64, 69], 6 * B, 0.07), T7)
for i in range(1, 9):
    t = T7 + i * B
    if t > 17.2: break
    if i % 2 == 0: place(kick(0.7), t)
    else: place(snap(0.18), t)
    place(hat(0.09), t + B / 2, pan=0.25)
    place(saw(45, B * 0.9, 0.18, fc=500, d=0.3), t)
# 15,0 : tampon — accord final suspendu
for m in (57, 64, 69, 71, 76): place(piano(m, 3.0, 0.14), 25 * B)

# ---------- SFX : 4 accents, normalisés puis dosés ----------
def load(name, maxlen):
    raw = subprocess.run([FF, "-v", "quiet", "-i", SFXDIR + name + ".mp3", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)[: int(maxlen * SR)].copy()
    f = int(0.03 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    return x / (np.abs(x).max() + 1e-9)

def placeS(name, t, db, maxlen=0.6):
    x = load(name, maxlen) * 10 ** (db / 20); i = int(t * SR); e = min(N, i + len(x)); sfx[i:e] += x[: e - i]

placeS("pop", 8 * B, -24, 0.3)                       # prénoms
placeS("whoosh-short", 14 * B + 0.45, -20, 0.5)      # les moitiés glissent l'une vers l'autre
placeS("chime", 16 * B + 1.6, -21, 1.2)              # les deux traits se rejoignent
placeS("impact-bass-2", 25 * B, -19, 0.6)            # tampon PREMIER LIVE

# ---------- mixage ----------
out = mix / (np.sqrt(np.mean(mix ** 2)) + 1e-9) * 10 ** (-18 / 20) + sfx
fi = int(0.01 * SR); out[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(1.2 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
pk = np.abs(out).max(); out *= min(1, 0.89 / pk)
with wave.open(os.path.join(HERE, "track.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok — pic", round(float(pk), 3))
