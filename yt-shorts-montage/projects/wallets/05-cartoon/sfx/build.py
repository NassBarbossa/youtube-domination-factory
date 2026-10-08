"""Reel wallets/04 — VRAIE voix de Nass (Video 3 de la formation) + sons 8-bit générés en code (ondes carrées / bruit).
PAS DE MUSIQUE (règle Shorts de Nass). Sortie : sfx/track.wav (22,5 s)."""
import os, subprocess, wave
import numpy as np
FF = os.path.expandvars(r"$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SR, DUR = 48000, 34.4; N = int(SR * DUR)
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


S['go'] = lambda: seq([NOTE(72), 0.0001, NOTE(72), 0.0001, NOTE(84)], 0.07, 0.25)
S['pop'] = lambda: env(sq(lambda t: 500 + 1400 * t / 0.08, 0.08, 0.25), 0.001, 0.03)
S['wind'] = lambda: env(noise(1.6, 1, 24) * (0.5 + 0.5 * np.sin(np.linspace(0, 9, int(1.6 * SR)))), 0.3, 0.6)
import json
D = json.load(open(os.path.join(ROOT, 'assets', 'words.json'), encoding='utf-8'))
WD, PH = D['words'], D['phrases']
norm = lambda x: x.lower().replace('.', '').replace(',', '')
wt = lambda txt, after=0: next(w['t'] for w in WD if w['t'] >= after and norm(w['w']) == norm(txt))
AV, GO = wt('avant'), wt("'acheter") - 0.25
EV = [(GO, 'go', -24), (GO + 0.1, 'whip', -26), (AV - 0.08, 'jump', -24), (AV, 'fanfare', -21), (AV + 0.02, 'coin', -24),
      (PH[1] - 0.1, 'whip', -24), (wt('cex'), 'slam', -21), (wt('plateforme') + 0.15, 'blip', -27), (wt('plateforme') + 0.25, 'blip', -27), (wt('plateforme') + 0.35, 'blip', -27),
      (wt('eux') - 0.05, 'spooky', -25), (wt('décident'), 'hurt', -25), (wt('mettent'), 'gate', -19),
      (PH[3] - 0.1, 'whip', -23), (wt('décentralisé'), 'slam', -23), (PH[5] - 0.1, 'wind', -27), (wt('far') - 0.05, 'bump', -21), (wt('far') + 0.08, 'gate', -22),
      (wt('équipé') - 0.1, 'land', -22), (wt('méthode', PH[6]), 'power', -22), (wt('méthode', PH[6]) + 0.25, 'fanfare', -23),
      (PH[7] - 0.15, 'whip', -24), (PH[7] + 0.35, 'jump', -25), (PH[7] + 0.77, 'jump', -25), (PH[7] + 1.19, 'jump', -25),
      (wt('ioc'), 'fanfare', -20), (wt('ioc') + 0.05, 'coin', -24), (wt('courant'), 'blip', -24), (D['voiceEnd'], 'fanfare', -21), (D['voiceEnd'] + 1.2, 'start', -25)]
EV += [(wt('tout', PH[4]) + i * 0.08, 'pop', -28) for i in range(12)]
for e in EV: at(*e)
import wave as _w
vw = _w.open(os.path.join(ROOT, 'assets', 'voice.wav'))
v = np.frombuffer(vw.readframes(vw.getnframes()), np.int16).astype(np.float32) / 32768
v = v[:N]; v = v / (np.sqrt(np.mean(v[v != 0] ** 2)) + 1e-9) * 10 ** (-16 / 20)
mix = out.copy(); mix[:len(v)] += v
fo = int(0.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
st = np.stack([mix, mix], 1)
with wave.open(os.path.join(HERE, 'track.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print('ok —', len(EV), 'sons, pic', round(float(pk), 3))
