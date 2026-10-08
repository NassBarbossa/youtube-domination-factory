"""Short wallets/03 « Punk en mission » — voix off (edge-tts Henri) + sons 8-bit générés en code (ondes carrées / bruit).
PAS DE MUSIQUE (règle Shorts de Nass). Sortie : sfx/track.wav (22,5 s)."""
import os, subprocess, wave
import numpy as np
FF = os.path.expandvars(r"$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SR, DUR = 48000, 22.5; N = int(SR * DUR)
rng = np.random.default_rng(8)
out = np.zeros(N)

def sq(f, dur, duty=0.5, vol=1.0):
    t = np.arange(int(dur * SR)) / SR
    if callable(f): ph = np.cumsum(f(t)) / SR
    else: ph = f * t
    return np.where((ph % 1) < duty, 1.0, -1.0) * vol
def env(x, a=0.002, r=0.05):
    n = len(x); t = np.arange(n) / SR
    return x * np.minimum(1, t / a) * np.clip((n / SR - t) / r, 0, 1)
def noise(dur, vol=1.0, step=4):
    n = int(dur * SR); x = np.repeat(rng.uniform(-1, 1, n // step + 1), step)[:n]; return x * vol
def seq(notes, d, duty=0.5):   # liste de fréquences jouées à la suite
    return np.concatenate([env(sq(f, d, duty), 0.002, 0.02) for f in notes])
NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)

S = {
    'slam':   lambda: env(sq(lambda t: 220 * np.exp(-t * 10) + 60, 0.16, 0.5), 0.001, 0.08),
    'open':   lambda: seq([NOTE(m) for m in (60, 64, 67)], 0.05, 0.25),
    'blip':   lambda: env(sq(NOTE(84), 0.06, 0.25), 0.001, 0.03),
    'whip':   lambda: env(noise(0.3, 1, 2) * np.linspace(0.2, 1, int(0.3 * SR)) ** 2, 0.01, 0.12),
    'land':   lambda: env(sq(lambda t: 160 * np.exp(-t * 18) + 50, 0.09, 0.5), 0.001, 0.05),
    'coin':   lambda: np.concatenate([env(sq(NOTE(83), 0.07, 0.5), 0.001, 0.01), env(sq(NOTE(88), 0.25, 0.5), 0.001, 0.2)]),
    'power':  lambda: seq([NOTE(m) for m in (60, 64, 67, 72, 76, 79, 84)], 0.045, 0.25),
    'fanfare':lambda: np.concatenate([seq([NOTE(72), NOTE(76), NOTE(79)], 0.09, 0.5), env(sq(NOTE(84), 0.45, 0.5), 0.002, 0.35)]),
    'jump':   lambda: env(sq(lambda t: 300 + 900 * t / 0.18, 0.18, 0.25), 0.002, 0.05),
    'hurt':   lambda: env(sq(lambda t: 600 - 2200 * t, 0.22, 0.5) * 0.7 + noise(0.22, 0.3), 0.001, 0.1),
    'break':  lambda: env(noise(0.45, 1, 6) * np.exp(-np.arange(int(0.45 * SR)) / SR * 6), 0.001, 0.2),
    'lose':   lambda: seq([NOTE(m) for m in (71, 67, 64, 60, 55)], 0.08, 0.5),
    'tick':   lambda: env(sq(NOTE(96), 0.025, 0.25), 0.001, 0.01),
    'respawn':lambda: seq([NOTE(m) for m in (67, 72, 79)], 0.05, 0.125),
    'spooky': lambda: env(sq(lambda t: 140 + 40 * np.sin(2 * np.pi * 6 * t), 0.45, 0.5), 0.05, 0.2),
    'steal':  lambda: env(sq(lambda t: 1200 - 3000 * t, 0.2, 0.25), 0.001, 0.05),
    'bump':   lambda: env(sq(lambda t: 260 * np.exp(-t * 6) + 120, 0.12, 0.5), 0.001, 0.06),
    'gate':   lambda: env(noise(0.35, 1, 12) * np.exp(-np.arange(int(0.35 * SR)) / SR * 9) + sq(55, 0.35, 0.5) * np.exp(-np.arange(int(0.35 * SR)) / SR * 8), 0.001, 0.15),
    'bonk':   lambda: env(sq(lambda t: 180 * np.exp(-t * 12) + 80, 0.12, 0.5), 0.001, 0.06),
    'start':  lambda: seq([NOTE(84), 0.0001, NOTE(84)], 0.07, 0.25),
}

def at(t, name, db):
    x = S[name](); x = x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20)
    i = int(t * SR); e = min(N, i + len(x)); out[i:e] += x[: e - i]

EV = [(0.08, 'slam', -23), (0.6, 'slam', -21), (0.87, 'slam', -23), (1.13, 'open', -25), (1.4, 'blip', -26),
      (2.2, 'whip', -24), (2.42, 'land', -25), (2.51, 'land', -26), (2.6, 'land', -25), (2.69, 'land', -26), (2.78, 'land', -25), (2.95, 'coin', -22),
      (4.1, 'whip', -24), (4.45, 'open', -25), (5.5, 'power', -23), (5.8, 'jump', -24), (5.98, 'fanfare', -21),
      (6.25, 'whip', -27), (6.78, 'jump', -24), (6.98, 'coin', -25),
      (7.7, 'whip', -26), (8.25, 'hurt', -24), (8.87, 'break', -20), (8.92, 'lose', -23)]
EV += [(8.95 + 0.5 * i / 12, 'tick', -30) for i in range(12)]
EV += [(10.0, 'respawn', -24), (10.25, 'spooky', -24), (10.6, 'steal', -24), (10.95, 'coin', -24)]
EV += [(10.97 + 0.58 * i / 12, 'tick', -30) for i in range(12)]
EV += [(11.62, 'whip', -27), (12.15, 'whip', -24), (12.45, 'land', -24), (12.72, 'bump', -22),
       (14.3, 'whip', -26), (14.98, 'gate', -19), (15.57, 'bonk', -22), (15.6, 'blip', -26),
       (16.82, 'slam', -21), (17.66, 'slam', -19), (19.0, 'fanfare', -20), (20.37, 'start', -24), (20.9, 'start', -27)]
for e in EV: at(*e)

raw = subprocess.run([FF, "-v", "quiet", "-i", os.path.join(ROOT, "assets", "voice.mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
v = np.frombuffer(raw, dtype=np.float32)[:N].copy(); v = v / (np.sqrt(np.mean(v ** 2)) + 1e-9) * 10 ** (-16 / 20)
mix = out.copy(); mix[: len(v)] += v
fo = int(0.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
st = np.stack([mix, mix], 1)
with wave.open(os.path.join(HERE, "track.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok —", len(EV), "sons 8-bit, pic", round(float(pk), 3))
