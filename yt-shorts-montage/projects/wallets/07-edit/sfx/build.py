"""Reel 07 « motion design » — voix réelle de Nass + sound effects (bibliothèque media-use), PAS DE MUSIQUE."""
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
AV, DEC, FAR, IOC = wt('avant'), wt('décentralisé'), wt('far'), wt('ioc')
EV = [(wt('façon') - 0.04, 'click', -24, 0.15), (wt('plus') - 0.04, 'click', -24, 0.15), (wt('facile') - 0.04, 'impact-bass-1', -23, 0.5), (wt('facile') + 0.1, 'glitch-1', -30, 0.25),
      (wt('et') - 0.06, 'whoosh-short', -26, 0.35), (wt('puissante') - 0.04, 'impact-bass-2', -23, 0.5), (wt('pour') - 0.05, 'pop', -24, 0.25), (wt("'argent,") - 0.1, 'sparkle', -27, 0.8),
      (wt("'acheter") - 0.04, 'impact-bass-1', -22, 0.5), (AV - 0.04, 'impact-bass-2', -19, 0.6), (AV + 0.14, 'glitch-2', -29, 0.25), (wt('les', 6.2) - 0.04, 'whoosh-short', -27, 0.3), (wt('autres.'), 'pop', -26, 0.2),
      (PH[1] - 0.06, 'whoosh', -25, 0.5), (wt('acheter', 7) - 0.05, 'click-soft', -24, 0.15), (wt('premières') - 0.05, 'click-soft', -24, 0.15), (wt('cryptos,') - 0.05, 'click-soft', -24, 0.15),
      (wt('tu', 9) - 0.06, 'whoosh-short', -26, 0.35), (wt('acheter', 9.4) + 0.08, 'click', -22, 0.15), (wt('appelle') - 0.2, 'riser', -29, 0.6),
      (wt('cex') - 0.04, 'impact-bass-1', -19, 0.6), (wt('cex') + 0.2, 'glitch-3', -28, 0.3),
      (PH[2] - 0.06, 'whoosh-short', -26, 0.35), (wt('eux') - 0.08, 'impact-bass-2', -24, 0.4), (wt('décident') - 0.04, 'error', -26, 0.3), (wt('mettent') + 0.06, 'click', -20, 0.15),
      (PH[3] - 0.06, 'whoosh-cinematic', -24, 0.9), (wt('moi,'), 'pop', -24, 0.25), (wt('méthode,') - 0.02, 'click-soft', -24, 0.15),
      (DEC - 0.05, 'impact-bass-2', -19, 0.6), (DEC, 'sparkle', -27, 0.8), (DEC + 0.25, 'glitch-1', -29, 0.25),
      (PH[4] - 0.06, 'whoosh-short', -26, 0.35), (wt('tout', PH[4]) + 0.1, 'pop', -29, 0.2), (wt('tout', PH[4]) + 0.4, 'pop', -29, 0.2), (wt('créer') - 0.05, 'impact-bass-1', -24, 0.4),
      (PH[5] - 0.06, 'whoosh', -26, 0.4), (wt('forcément,') + 0.1, 'error', -29, 0.25), (FAR - 0.06, 'impact-bass-2', -19, 0.6), (wt('west.') - 0.04, 'impact-bass-1', -22, 0.5), (wt('west.') + 0.1, 'glitch-2', -29, 0.25),
      (PH[6] - 0.04, 'whoosh-short', -26, 0.35), (wt('équipé') - 0.06, 'impact-bass-1', -21, 0.5), (wt('équipé'), 'ping', -27, 0.5), (wt('méthode', PH[6]) - 0.05, 'click', -22, 0.15),
      (PH[7] - 0.06, 'whoosh', -26, 0.4), (wt('positionner') - 0.05, 'impact-bass-2', -24, 0.4), (wt('positionner') + 0.1, 'riser', -29, 0.9),
      (IOC - 0.05, 'impact-bass-1', -18, 0.7), (IOC + 0.2, 'glitch-3', -28, 0.3), (IOC + 0.3, 'sparkle', -27, 0.8),
      (wt('avant', 28.5) - 0.06, 'whoosh-short', -26, 0.35), (wt('tout', 29.5), 'pop', -27, 0.2), (wt('courant.'), 'pop', -24, 0.25),
      (VEND + 0.15, 'impact-bass-2', -21, 0.6), (VEND + 0.6, 'whoosh-short', -26, 0.35), (VEND + 1.05, 'chime', -21, 1.4)]
for e in EV: at(*e)
vw = wave.open(os.path.join(ROOT, 'assets', 'voice.wav')); v = np.frombuffer(vw.readframes(vw.getnframes()), np.int16).astype(np.float32) / 32768
v = v[:N]; v = v / (np.sqrt(np.mean(v[v != 0] ** 2)) + 1e-9) * 10 ** (-16 / 20)
mix = out.copy(); mix[:len(v)] += v
fo = int(0.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo); pk = np.abs(mix).max(); mix *= min(1, 0.89 / pk)
with wave.open(os.path.join(HERE, 'track.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
print('ok —', len(EV), 'sons, pic', round(float(pk), 3))
