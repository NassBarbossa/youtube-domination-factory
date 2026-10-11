"""Convergence — bande-son de l'intro (15 s, 128 BPM) : musique synthé maison + quelques SFX.
Musique 100 % générée (libre de droits). SFX : bibliothèque media-use (voir CREDITS.md).
"""
import os, subprocess, wave
import numpy as np
import sys
PERC = "--perc" in sys.argv          # version percussions + FX uniquement

FF = os.path.expandvars(r"$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe")
SFXDIR = os.path.expanduser("~/.agents/skills/media-use/audio/assets/sfx/")
HERE = os.path.dirname(os.path.abspath(__file__))
SR, DUR = 48000, 15.0
BPM = 128; B = 60 / BPM
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(7)

music = np.zeros(N); sfx = np.zeros((N, 2))

def place(buf, sig, t, g=1.0):
    i = int(t * SR); e = min(N, i + len(sig))
    if i < N: buf[i:e] += sig[:e - i] * g

def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s; y[i] = s
    return y

def kick(g=1.0):
    n = int(0.42 * SR); t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t / 0.045)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.16) * g + 0.15 * rng.standard_normal(n) * np.exp(-t / 0.004)

def hat(g=0.3, d=0.035):
    n = int(0.12 * SR); x = rng.standard_normal(n)
    x = x - lowpass(x, 7000)
    return x * env(n, 0.001, d) * g

def clap(g=0.5):
    n = int(0.25 * SR); x = rng.standard_normal(n); x = x - lowpass(x, 1200)
    e = np.zeros(n)
    for o in (0, 0.011, 0.022):
        i = int(o * SR); e[i:] += env(n - i, 0.001, 0.05 if o < 0.02 else 0.12)
    return x * e * g

def note(freq, dur, g=0.3, shape="saw", fc=1800, a=0.004, d=None):
    if PERC: return np.zeros(int(dur * SR))
    n = int(dur * SR); t = np.arange(n) / SR
    if shape == "saw":
        x = sum(np.sin(2 * np.pi * freq * k * t) / k for k in range(1, 14) if freq * k < 9000)
    else:
        x = np.sign(np.sin(2 * np.pi * freq * t)) * 0.6
    x = lowpass(x, fc)
    e = np.minimum(1, t / a) * (np.exp(-t / d) if d else np.minimum(1, (dur - t) / 0.03).clip(0, 1))
    return x * e * g

mid = lambda m: 440 * 2 ** ((m - 69) / 12)

# --- 0 → 0,94 : boot (nappe filtrée) ---
pad = sum(note(mid(m), 1.2, 0.05, fc=600, a=0.3) for m in (57, 64, 69))
place(music, pad, 0.0)

# --- grille rythmique ---
T1, T2, T3, T4, T6 = 2 * B, 8 * B, 16 * B, 24 * B, 28 * B
bassline = [45, 45, 57, 45, 48, 48, 60, 48, 43, 43, 55, 43, 40, 40, 52, 47]   # La mineur, en croches
k = 0
t = T1
while t < T3 - 1e-6:                      # couplet : kick 4 temps, hats, basse en croches
    place(music, kick(0.9), t)
    place(music, hat(0.18), t + B / 2)
    if t >= T2:                           # à partir des mots : clap sur 2 et 4
        beat = round((t - T1) / B)
        if beat % 2 == 1: place(music, clap(0.35), t)
    for h in (0, 1):
        m = bassline[k % len(bassline)]; k += 1
        place(music, note(mid(m), B / 2 * 0.9, 0.22, fc=900, d=0.18), t + h * B / 2)
    t += B

# --- 7,5 → 11,25 : montée (roulement qui accélère + riser + basse qui monte) ---
t = T3
while t < T4 - 1e-6:
    p = (t - T3) / (T4 - T3)
    if p < 0.5: place(music, kick(0.75), t)
    step = B / 2 if p < 0.4 else (B / 4 if p < 0.75 else B / 8)
    s = t
    while s < min(t + B, T4) - 1e-6:
        place(music, clap(0.12 + 0.3 * ((s - T3) / (T4 - T3)) ** 2), s); s += step
    t += B
n = int((T4 - T3) * SR); tt = np.arange(n) / SR
noise = rng.standard_normal(n); riser = (noise - lowpass(noise, 300)) * (tt / tt[-1]) ** 2.2 * 0.12
place(music, riser, T3)
sweep_f = 110 * 2 ** (tt / (T4 - T3) * 2)          # deux octaves
if not PERC: place(music, np.sin(2 * np.pi * np.cumsum(sweep_f) / SR) * (tt / tt[-1]) ** 1.5 * 0.12, T3)
place(music, np.zeros(1), 0)

# --- 11,25 : DROP ---
n = int(1.6 * SR); tt = np.arange(n) / SR
sub = np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-tt / 0.08)) / SR) * np.exp(-tt / 0.6) * 0.9
crash = rng.standard_normal(n); crash = (crash - lowpass(crash, 3000)) * np.exp(-tt / 0.5) * 0.18
place(music, sub + crash, T4)
for m in (57, 64, 69, 72):                         # accord tenu (La mineur add9)
    place(music, note(mid(m), T6 - T4 + 0.2, 0.06, fc=2400, a=0.01), T4)
t = T4 + B
while t < 14.2:
    place(music, kick(0.8), t); place(music, hat(0.16), t + B / 2)
    place(music, note(mid(45), B * 0.45, 0.2, fc=800, d=0.15), t)
    t += B
for m in (57, 64, 69, 76):                         # accord final au tampon
    place(music, note(mid(m), 1.9, 0.07, fc=2600, a=0.005, d=0.9), T6)


# --- percussions supplémentaires (version --perc) ---
def tom(f0, g=0.5, d=0.22):
    n = int(0.5 * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.6 * np.exp(-t / 0.03))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / d) + 0.2 * rng.standard_normal(n) * np.exp(-t / 0.01)) * g

def rim(g=0.25):
    n = int(0.08 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 1700 * t) * np.exp(-t / 0.012) + 0.5 * (rng.standard_normal(n) * np.exp(-t / 0.004))
    return x * g

def shaker(g=0.08):
    n = int(0.09 * SR); x = rng.standard_normal(n); x = x - lowpass(x, 5000)
    t = np.arange(n) / SR
    return x * np.minimum(1, t / 0.02) * np.exp(-t / 0.03) * g

if PERC:
    # boot : pulsation de rimshots qui accélère
    for i, tt0 in enumerate([0.0, 0.3, 0.52, 0.68, 0.8, 0.88]): place(music, rim(0.18 + 0.03 * i), tt0)
    # couplet : shaker en doubles croches + rim sur les contretemps
    t = T1
    while t < T3 - 1e-6:
        for q in range(4): place(music, shaker(0.06 if q % 2 else 0.09), t + q * B / 4)
        if t >= T2: place(music, rim(0.2), t + B * 0.75)
        t += B
    # roulements de toms à chaque changement de partie
    for t0 in (T2 - B, T3 - B):
        for j, f0 in enumerate([180, 150, 120, 95]): place(music, tom(f0, 0.45), t0 + j * B / 4)
    # montée : shaker qui s'emballe
    t = T3
    while t < T4 - 1e-6:
        p = (t - T3) / (T4 - T3)
        place(music, shaker(0.05 + 0.1 * p), t); t += B / 4 if p < 0.6 else B / 8
    # après le drop : groove toms + rim
    t = T4 + B
    while t < 14.2:
        place(music, tom(90, 0.35), t + B / 2); place(music, rim(0.16), t + B * 0.75); t += B
    # tampon : gros tom + queue de bruit
    n = int(1.8 * SR); tt = np.arange(n) / SR
    tail = rng.standard_normal(n); tail = (tail - lowpass(tail, 2500)) * np.exp(-tt / 0.7) * 0.1
    place(music, tom(70, 0.8, 0.5) , T6); place(music, tail, T6)

# --- SFX : rares, normalisés au pic puis dosés ---
def load(name, maxlen):
    raw = subprocess.run([FF, "-v", "quiet", "-i", SFXDIR + name + ".mp3", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)[: int(maxlen * SR)].copy()
    f = int(0.03 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    return x / (np.abs(x).max() + 1e-9)

def placeS(name, t, db, maxlen=0.6):
    x = load(name, maxlen) * 10 ** (db / 20); i = int(t * SR); e = min(N, i + len(x)); sfx[i:e] += x[: e - i]

for i in range(3): placeS("key-press", 0.06 + i * 0.27, -24, 0.15)     # boot
placeS("whoosh-short", T1 - 0.12, -16, 0.5)                             # bandeaux
placeS("whoosh-short", T3 + 2 * B - 0.14, -19, 0.45)                      # course : saut du vert vers l'or
placeS("whoosh-cinematic", T4 - 0.7, -17, 0.9)                          # juste avant le contact
placeS("impact-bass-1", T4, -12, 1.0)                                   # contact → V
placeS("impact-bass-2", T6, -18, 0.6)                                   # tampon LIVE
if PERC:
    placeS("glitch-1", T2 - 0.05, -20, 0.3)                             # entrée des mots
    placeS("riser", T4 - 2.4, -19, 2.4)                                  # montée
    placeS("whoosh", T4 + 0.55, -19, 0.6)                                # le V rejoint le logo

# --- mixage ---
music = music / (np.sqrt(np.mean(music ** 2)) + 1e-9) * 10 ** (-17 / 20)
mix = np.stack([music, music], 1) + sfx
fi = int(0.01 * SR); mix[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(0.9 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
pcm = (mix * 32767).astype(np.int16)
with wave.open(os.path.join(HERE, "track-perc.wav" if PERC else "track.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok — pic", round(float(pk), 3), "RMS musique -17 dB")
