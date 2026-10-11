"""Convergence — bande-son « voix » de l'intro (15 s, 128 BPM) : chœur, chops vocaux, basse vocale et beatbox.
Tout est synthétisé (synthèse par formants, libre de droits). Mêmes temps forts que build.py (drop à 11,25 s).
Sortie : track-voix.wav
"""
import os, subprocess, wave
import numpy as np
from scipy.signal import lfilter

FF = os.path.expandvars(r"$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe")
SFXDIR = os.path.expanduser("~/.agents/skills/media-use/audio/assets/sfx/")
HERE = os.path.dirname(os.path.abspath(__file__))
SR, DUR = 48000, 15.0
BPM = 128; B = 60 / BPM
N = int(SR * DUR)
rng = np.random.default_rng(11)
T1, T2, T3, T4, T6 = 2 * B, 8 * B, 16 * B, 24 * B, 28 * B

mix = np.zeros((N, 2)); sfx = np.zeros((N, 2))
mid = lambda m: 440 * 2 ** ((m - 69) / 12)

def place(sig, t, g=1.0, pan=0.0):
    """pan : -1 gauche, +1 droite"""
    i = int(t * SR); e = min(N, i + len(sig))
    if i >= N: return
    l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
    mix[i:e, 0] += sig[:e - i] * g * l * 1.414
    mix[i:e, 1] += sig[:e - i] * g * r * 1.414

# ---------- synthèse par formants ----------
VOW = {  # (fréquence, largeur de bande, gain) des 4 premiers formants
    'a': [(800, 80, 1.0), (1150, 90, 0.5), (2900, 120, 0.25), (3900, 130, 0.1)],
    'o': [(450, 70, 1.0), (800, 80, 0.4), (2830, 100, 0.12), (3800, 120, 0.05)],
    'u': [(325, 50, 1.0), (700, 60, 0.2), (2530, 170, 0.05), (3500, 180, 0.03)],
    'e': [(400, 60, 1.0), (1700, 90, 0.4), (2600, 100, 0.25), (3600, 120, 0.1)],
    'i': [(270, 60, 1.0), (2290, 90, 0.25), (3010, 100, 0.2), (3900, 120, 0.1)],
}

def bandpass(x, f, bw):
    w = 2 * np.pi * f / SR; q = f / bw; al = np.sin(w) / (2 * q)
    b = [al, 0, -al]; a = [1 + al, -2 * np.cos(w), 1 - al]
    return lfilter(b, a, x)

def formants(src, vowel):
    return sum(bandpass(src, f, bw) * g for f, bw, g in VOW[vowel])

def glottal(f0, n, vib=5.5, vdepth=0.012, jit=0.003):
    t = np.arange(n) / SR
    ph0 = rng.uniform(0, 6.28)
    f = f0 * (1 + vdepth * np.sin(2 * np.pi * vib * t + ph0) * np.minimum(1, t / 0.25)) * (1 + jit * rng.standard_normal(n).cumsum() / np.sqrt(np.arange(1, n + 1)))
    ph = 2 * np.pi * np.cumsum(f) / SR
    kmax = int(min(60, 5500 / f0))
    return sum(np.sin(k * ph) / k ** 1.1 for k in range(1, kmax + 1))

def voice(f0, dur, vowel='a', a=0.03, r=0.08, breath=0.04, vdepth=0.012, glide=None):
    n = int(dur * SR); t = np.arange(n) / SR
    if glide:  # glissando : f0 → glide
        f = f0 * (glide / f0) ** (t / dur)
        ph = 2 * np.pi * np.cumsum(f * (1 + vdepth * np.sin(2 * np.pi * 5.5 * t))) / SR
        kmax = int(min(60, 5500 / max(f0, glide)))
        src = sum(np.sin(k * ph) / k ** 1.1 for k in range(1, kmax + 1))
    else:
        src = glottal(f0, n, vdepth=vdepth)
    src = src + breath * rng.standard_normal(n)
    y = formants(src, vowel)
    env = np.minimum(1, t / a) * np.clip((dur - t) / r, 0, 1)
    y = y * env
    return y / (np.abs(y).max() + 1e-9)

def choir(midis, dur, vowel='a', g=0.2, a=0.25, r=0.4, spread=0.8):
    """accord chanté : 3 voix légèrement désaccordées par note, réparties en stéréo"""
    for j, m in enumerate(midis):
        for v in range(3):
            det = (v - 1) * 0.006
            pan = ((j / max(1, len(midis) - 1)) * 2 - 1) * spread * 0.7 + (v - 1) * 0.25
            yield voice(mid(m) * (1 + det), dur, vowel, a=a, r=r, breath=0.06), g / np.sqrt(len(midis) * 3), float(np.clip(pan, -1, 1))

def place_choir(midis, t, dur, **kw):
    for sig, g, pan in choir(midis, dur, **kw): place(sig, t, g, pan)

# ---------- beatbox ----------
def noise(n): return rng.standard_normal(n)

def bb_kick(g=1.0):          # « b » : lèvres + grave
    n = int(0.3 * SR); t = np.arange(n) / SR
    f = 52 + 95 * np.exp(-t / 0.035)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.11)
    lip = bandpass(noise(n), 180, 120) * np.exp(-t / 0.008) * 0.6
    return (body + lip) * g

def bb_hat(g=0.3, d=0.03):   # « ts »
    n = int(0.1 * SR); t = np.arange(n) / SR
    x = bandpass(noise(n), 7200, 2600) + 0.5 * bandpass(noise(n), 4800, 1500)
    return x / 3 * np.minimum(1, t / 0.003) * np.exp(-t / d) * g

def bb_snare(g=0.5):         # « pff / k » : explosion + souffle
    n = int(0.22 * SR); t = np.arange(n) / SR
    x = bandpass(noise(n), 1900, 1200) + 0.7 * bandpass(noise(n), 4200, 2000)
    tone = np.sin(2 * np.pi * 210 * t) * np.exp(-t / 0.03) * 0.5
    return (x / 3 * np.exp(-t / 0.07) + tone) * np.minimum(1, t / 0.002) * g

def bb_ka(g=0.3):            # « ka » court pour les roulements
    n = int(0.12 * SR); t = np.arange(n) / SR
    x = bandpass(noise(n), 1500, 700) * np.exp(-t / 0.012)
    v = voice(240, 0.12, 'a', a=0.005, r=0.06, breath=0.1) * np.exp(-t / 0.04) * 0.4
    return (x / 2 + v[:n]) * g

def chop(m, dur, vowel, g=0.25):   # chop vocal : consonne + voyelle très courte
    n = int(dur * SR); t = np.arange(n) / SR
    y = voice(mid(m), dur, vowel, a=0.006, r=dur * 0.5, breath=0.05, vdepth=0.004)
    y[:int(0.01 * SR)] += bandpass(noise(int(0.01 * SR)), 3000, 2000) * 0.3
    return y * g

# ---------- 0 → 0,94 : boot — fredonnement « mmm » qui monte ----------
for sig, g, pan in choir([57, 64, 69], 1.05, 'u', g=0.22, a=0.5, r=0.15):
    place(sig, 0.0, g, pan)

# ---------- 0,94 → 7,5 : beatbox + basse vocale « doum » + chops ----------
bassline = [45, 45, 57, 45, 48, 48, 60, 48, 43, 43, 55, 43, 40, 40, 52, 47]
CHOPS = [(69, 'a'), (72, 'e'), (76, 'o'), (72, 'a'), (69, 'e'), (67, 'o'), (64, 'a'), (67, 'e')]
k = 0; t = T1; beat = 0
while t < T3 - 1e-6:
    place(bb_kick(0.9), t)
    place(bb_hat(0.22), t + B / 2, pan=0.3)
    if t >= T2 and beat % 2 == 1: place(bb_snare(0.45), t)
    for h in (0, 1):
        m = bassline[k % len(bassline)]; k += 1
        place(voice(mid(m), B / 2 * 0.85, 'u', a=0.01, r=0.06, breath=0.02, vdepth=0.003), t + h * B / 2, 0.32)
    if t >= T2:  # chops sur les contretemps quand les mots arrivent
        m, v = CHOPS[beat % len(CHOPS)]
        place(chop(m, 0.16, v), t + B * 0.75, pan=0.4 if beat % 2 else -0.4)
    t += B; beat += 1

# ---------- 7,5 → 11,25 : montée — chœur qui grimpe + roulement de « ka » qui accélère + glissando ----------
t = T3
while t < T4 - 1e-6:
    p = (t - T3) / (T4 - T3)
    if p < 0.5: place(bb_kick(0.75), t)
    step = B / 2 if p < 0.4 else (B / 4 if p < 0.75 else B / 8)
    s = t
    while s < min(t + B, T4) - 1e-6:
        place(bb_ka(0.18 + 0.5 * ((s - T3) / (T4 - T3)) ** 2), s, pan=0.25 * np.sin(s * 9)); s += step
    t += B
# chœur « ah » par paliers (un accord toutes les 2 mesures), de plus en plus fort
for j, (chord, vw) in enumerate([([57, 64, 69], 'o'), ([60, 64, 69], 'a'), ([62, 65, 69], 'a'), ([64, 68, 71], 'a')]):
    place_choir(chord, T3 + j * 2 * B * 1.0 if j < 2 else T3 + 4 * B + (j - 2) * 2 * B, 2 * B + 0.05, vowel=vw, g=0.3 + 0.14 * j, a=0.06, r=0.05)
# voix soliste en glissando « aaah » sur deux octaves
gl = voice(mid(57), T4 - T3, 'a', a=0.8, r=0.02, breath=0.08, glide=mid(81))
place(gl * np.linspace(0.2, 1, len(gl)) ** 2, T3, 0.38)
# souffle « hhh » qui monte (formants qui s'ouvrent)
n = int((T4 - T3) * SR); tt = np.arange(n) / SR
br = bandpass(noise(n), 1200, 900) + bandpass(noise(n), 3200, 1800)
place(br * (tt / tt[-1]) ** 2.5 * 0.09, T3)

# ---------- 11,25 : DROP — grand chœur « AH » + grosse caisse beatbox ----------
place(bb_kick(1.3), T4)
n = int(1.4 * SR); tt = np.arange(n) / SR
place(np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-tt / 0.08)) / SR) * np.exp(-tt / 0.5) * 0.8, T4)
place_choir([45, 57, 64, 69, 72, 76], T4, T6 - T4 + 0.15, vowel='a', g=0.55, a=0.015, r=0.25)
# groove après le drop
t = T4 + B; beat = 0
while t < 14.2:
    place(bb_kick(0.8), t); place(bb_hat(0.2), t + B / 2, pan=-0.3)
    if beat % 2 == 1: place(bb_snare(0.4), t)
    place(voice(mid(45), B * 0.42, 'u', a=0.01, r=0.06, breath=0.02, vdepth=0.003), t, 0.3)
    cm, cv = CHOPS[(beat * 3) % len(CHOPS)]
    place(chop(cm, 0.14, cv), t + B * 0.75, pan=0.4 if beat % 2 else -0.4)
    t += B; beat += 1
# tampon : accord final « oh », long
place_choir([57, 64, 69, 76], T6, 1.85, vowel='o', g=0.4, a=0.01, r=0.9)

# ---------- SFX (mêmes repères que les autres versions, plus discrets) ----------
def load(name, maxlen):
    raw = subprocess.run([FF, "-v", "quiet", "-i", SFXDIR + name + ".mp3", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)[: int(maxlen * SR)].copy()
    f = int(0.03 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    return x / (np.abs(x).max() + 1e-9)

def placeS(name, t, db, maxlen=0.6):
    x = load(name, maxlen) * 10 ** (db / 20); i = int(t * SR); e = min(N, i + len(x)); sfx[i:e] += x[: e - i]

for i in range(3): placeS("key-press", 0.06 + i * 0.27, -24, 0.15)
placeS("whoosh-short", T1 - 0.12, -18, 0.5)
placeS("whoosh-short", T3 + 2 * B - 0.14, -20, 0.45)
placeS("whoosh-cinematic", T4 - 0.7, -19, 0.9)
placeS("impact-bass-1", T4, -14, 1.0)
placeS("impact-bass-2", T6, -20, 0.6)

# ---------- mixage ----------
mono_rms = np.sqrt(np.mean(mix ** 2))
out = mix / (mono_rms + 1e-9) * 10 ** (-17 / 20) + sfx
fi = int(0.01 * SR); out[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(0.9 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
pk = np.abs(out).max(); out *= min(1, 0.89 / pk)
pcm = (out * 32767).astype(np.int16)
with wave.open(os.path.join(HERE, "track-voix.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok — pic", round(float(pk), 3))
