"""Short wallets/02 — bande-son : voix off (edge-tts Henri) + sound effects calés sur les animations. PAS DE MUSIQUE.
Sortie : sfx/track.wav (22,5 s). Voix ≈ -16 dBFS RMS, SFX environ 18-22 dB sous la voix."""
import os, subprocess, wave
import numpy as np
FF = os.path.expandvars(r"$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe")
SFXDIR = os.path.expanduser("~/.agents/skills/media-use/audio/assets/sfx/")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SR, DUR = 48000, 22.5; N = int(SR * DUR)
def dec(path, maxlen=None):
    raw = subprocess.run([FF, "-v", "quiet", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
    return x[: int(maxlen * SR)] if maxlen else x
voice = dec(os.path.join(ROOT, "assets", "voice.mp3"))[:N]
voice = voice / (np.sqrt(np.mean(voice ** 2)) + 1e-9) * 10 ** (-16 / 20)
out = np.zeros((N, 2)); out[: len(voice)] += voice
def at(t, name, db, ml=0.5):
    x = dec(SFXDIR + name + ".mp3", ml); f = min(len(x) // 4, int(0.03 * SR)); x[-f:] *= np.linspace(1, 0, f)[:, None]
    x = x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20); i = int(t * SR); e = min(N, i + len(x)); out[i:e] += x[: e - i]
EVENTS = [
    (0.08, "whoosh-short", -24, 0.3), (0.62, "impact-bass-2", -18, 0.5), (0.87, "whoosh-short", -24, 0.3), (1.13, "click", -22, 0.2),
    (2.22, "whoosh", -21, 0.45), (2.42, "pop", -24, 0.2), (2.54, "pop", -24, 0.2), (2.66, "pop", -24, 0.2), (2.78, "pop", -24, 0.2), (2.95, "click-soft", -20, 0.2),
    (4.12, "whoosh", -21, 0.45), (5.5, "sparkle", -23, 0.6), (5.96, "pop", -22, 0.25),
    (6.2, "whoosh-cinematic", -24, 0.6), (6.8, "ping", -24, 0.4),
    (7.7, "whoosh-short", -22, 0.3), (8.25, "glitch-1", -24, 0.25), (8.87, "impact-bass-1", -17, 0.7),
    (10.02, "pop", -22, 0.2), (10.27, "whoosh-short", -22, 0.3), (10.62, "whoosh", -22, 0.4), (10.98, "sparkle", -20, 0.7),
    (12.18, "whoosh", -21, 0.45), (12.45, "pop", -22, 0.25), (12.7, "click", -22, 0.2),
    (14.3, "whoosh-short", -22, 0.35), (15.0, "impact-bass-2", -18, 0.5), (15.57, "error", -26, 0.3),
    (16.8, "whoosh-short", -22, 0.3), (17.66, "impact-bass-1", -16, 0.7),
    (18.95, "whoosh-cinematic", -22, 0.6), (19.69, "pop", -22, 0.25), (20.37, "chime", -20, 1.4),
]
for e in EVENTS: at(*e)
fo = int(0.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
pk = np.abs(out).max(); out *= min(1, 0.89 / pk)
with wave.open(os.path.join(HERE, "track.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok —", len(EVENTS), "SFX, pic", round(float(pk), 3))
