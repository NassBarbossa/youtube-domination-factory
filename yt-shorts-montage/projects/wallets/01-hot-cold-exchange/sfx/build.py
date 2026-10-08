"""Short wallets/01 — bande-son : PAS DE MUSIQUE (règle Shorts de Nass), seulement des sound effects calés
sur les animations de index.html. Sons : bibliothèque media-use (voir CREDITS.md du skill), normalisés au pic puis dosés.
Sortie : sfx/track.wav (47 s)
"""
import os, subprocess, wave
import numpy as np

FF = os.path.expandvars(r"$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe")
SFXDIR = os.path.expanduser("~/.agents/skills/media-use/audio/assets/sfx/")
HERE = os.path.dirname(os.path.abspath(__file__))
SR, DUR = 48000, 47.0
N = int(SR * DUR)
out = np.zeros((N, 2))

def load(name, maxlen):
    raw = subprocess.run([FF, "-v", "quiet", "-i", SFXDIR + name + ".mp3", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)[: int(maxlen * SR)].copy()
    f = min(len(x) // 4, int(0.03 * SR)); x[-f:] *= np.linspace(1, 0, f)[:, None]
    return x / (np.abs(x).max() + 1e-9)

def at(t, name, db, maxlen=0.5):
    x = load(name, maxlen) * 10 ** (db / 20); i = int(t * SR); e = min(N, i + len(x)); out[i:e] += x[: e - i]

# (temps, son, gain dB, longueur max) — un son par animation qui compte
EVENTS = [
    # hook : chaque mot claque, punch sur « VRAIMENT », cadenas qui se ferme
    (0.08, "whoosh-short", -20, 0.35), (0.60, "whoosh-short", -20, 0.35), (1.15, "whoosh-short", -20, 0.35),
    (1.70, "impact-bass-2", -14, 0.6), (2.45, "click", -16, 0.2),
    # les 3 cartes tombent
    (3.40, "pop", -18, 0.25), (3.62, "pop", -18, 0.25), (3.84, "pop", -18, 0.25),
    # 1/3 exchange : chip + banque, la clé entre, tampon RETRAITS SUSPENDUS
    (5.95, "whoosh", -19, 0.4), (6.05, "pop", -17, 0.25), (9.85, "click-soft", -15, 0.2),
    (13.48, "impact-bass-1", -13, 0.7), (13.52, "error", -22, 0.35),
    # 2/3 hot wallet : transformation, ondes wifi, 12 mots, flèche on-chain, hameçon barré
    (16.95, "whoosh-short", -17, 0.4), (17.55, "ping", -20, 0.4), (21.2, "sparkle", -19, 0.8),
    (25.30, "whoosh", -19, 0.5), (25.65, "pop", -18, 0.25), (26.65, "click-soft", -18, 0.2),
    (29.30, "glitch-1", -21, 0.3), (29.90, "error", -19, 0.35),
    # 3/3 cold wallet : transformation, wifi barré, cadran, porte qui se verrouille
    (31.90, "whoosh-short", -17, 0.4), (32.55, "click", -17, 0.2), (36.2, "typing", -24, 1.0), (37.3, "impact-bass-2", -16, 0.5),
    # récap : 3 cartes + punk
    (40.0, "pop", -17, 0.25), (40.3, "whoosh-short", -20, 0.3), (41.0, "whoosh-short", -20, 0.3), (41.7, "whoosh-short", -20, 0.3),
    # fin
    (44.2, "whoosh", -19, 0.4), (44.8, "chime", -16, 1.4),
]
for t, name, db, ml in EVENTS: at(t, name, db, ml)

fo = int(0.6 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
pk = np.abs(out).max(); out *= 0.7 / pk          # sans voix : on remonte l'ensemble, pic à -3 dBFS
with wave.open(os.path.join(HERE, "track.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok —", len(EVENTS), "sons, pic", round(float(pk), 3))
