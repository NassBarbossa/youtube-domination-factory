"""Reel 06 « motion design » — voix réelle de Nass + sound effects (bibliothèque media-use), PAS DE MUSIQUE."""
import os, subprocess, wave, json
import numpy as np
FF = os.path.expandvars(r"$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe")
SFXDIR = os.path.expanduser("~/.agents/skills/media-use/audio/assets/sfx/")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SR, DUR = 48000, 34.4; N = int(SR * DUR); out = np.zeros(N)
D = json.load(open(os.path.join(ROOT, 'assets', 'words.json'), encoding='utf-8')); WD, PH, VEND = D['words'], D['phrases'], D['voiceEnd']
norm = lambda x: x.lower().replace('.', '').replace(',', '')
wt = lambda txt, after=0: next(w['t'] for w in WD if w['t'] >= after and norm(w['w']) == norm(txt))
def load(name, ml):
    raw = subprocess.run([FF, "-v", "quiet", "-i", SFXDIR + name + ".mp3", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)[: int(ml * SR)].copy(); f = min(len(x) // 4, int(0.03 * SR)); x[-f:] *= np.linspace(1, 0, f); return x / (np.abs(x).max() + 1e-9)
def at(t, name, db, ml=0.6):
    x = load(name, ml) * 10 ** (db / 20); i = int(t * SR); e = min(N, i + len(x)); out[i:e] += x[:e - i]
AV, DEC, FAR, ME, IOC = wt('avant'), wt('décentralisé'), wt('far'), wt('méthode', PH[6]), wt('ioc')
EV = [(0.05, 'sparkle', -27, 0.8), (wt("'acheter"), 'pop', -26, 0.25), (AV, 'impact-bass-2', -20, 0.6), (wt('autres.') - 0.1, 'click-soft', -26, 0.2),
      (PH[1] + 0.2, 'whoosh-cinematic', -24, 1.0), (PH[1] + 2.45, 'impact-bass-1', -21, 0.7), (wt('cex'), 'pop', -24, 0.3),
      (wt('eux') - 0.2, 'whoosh-short', -27, 0.4), (wt('décident'), 'error', -27, 0.3), (wt('mettent'), 'click', -21, 0.2),
      (PH[3] - 0.05, 'whoosh-cinematic', -23, 1.0), (DEC, 'impact-bass-2', -20, 0.6), (DEC + 0.05, 'sparkle', -27, 0.8),
      (wt('tout', PH[4]) - 0.2, 'pop', -28, 0.2), (wt('tout', PH[4]) + 0.3, 'pop', -29, 0.2), (wt('tout', PH[4]) + 0.7, 'pop', -29, 0.2),
      (FAR - 0.3, 'glitch-1', -25, 0.4), (FAR, 'impact-bass-1', -21, 0.6),
      (wt('équipé') - 0.2, 'riser', -27, 0.9), (ME - 0.15, 'click', -21, 0.2), (ME + 0.1, 'impact-bass-2', -20, 0.6), (ME + 0.4, 'chime', -26, 1.0),
      (PH[7] + 0.05, 'whoosh-cinematic', -23, 1.0), (IOC, 'impact-bass-1', -19, 0.7), (IOC + 0.05, 'sparkle', -26, 0.8),
      (wt('soit', 29.5) - 0.05, 'whoosh', -24, 0.8), (VEND + 0.3, 'whoosh-short', -25, 0.4), (VEND + 1.25, 'chime', -21, 1.4)]
for e in EV: at(*e)
vw = wave.open(os.path.join(ROOT, 'assets', 'voice.wav')); v = np.frombuffer(vw.readframes(vw.getnframes()), np.int16).astype(np.float32) / 32768
v = v[:N]; v = v / (np.sqrt(np.mean(v[v != 0] ** 2)) + 1e-9) * 10 ** (-16 / 20)
mix = out.copy(); mix[:len(v)] += v
fo = int(0.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo); pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
with wave.open(os.path.join(HERE, 'track.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
print('ok —', len(EV), 'sons, pic', round(float(pk), 3))
