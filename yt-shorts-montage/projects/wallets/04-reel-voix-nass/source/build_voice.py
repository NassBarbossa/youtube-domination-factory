"""Monte la voix du reel à partir des vrais passages de Nass (Video 3 de la formation), coupés au mot près.
Entrée : source/fr_words.json (faster-whisper medium, fr). Sortie : assets/voice.wav + assets/words.json"""
import json, subprocess, os, wave
import numpy as np
FF = os.path.expandvars(r"$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe")
W = json.load(open('source/fr_words.json', encoding='utf-8'))
idx = lambda t: min(range(len(W)), key=lambda i: abs(W[i]['t'] - t))
# chaque phrase = liste de plages [premier mot, dernier mot] (index dans W) mises bout à bout
PHRASES = [
    [(57, 77)],                                   # la façon la plus facile ... c'est d'acheter avant les autres.
    [(230, 236), (245, 255)],                     # Quand tu vas acheter tes premières cryptos, | tu vas les acheter sur ce qu'on appelle un CEX.
    [(332, 343)],                   # sur leur plateforme, c'est eux qui décident ce qu'ils mettent.
    [(423, 433)],                   # Mais moi, ma méthode, elle s'effectue dans le monde décentralisé.
    [(454, 462)],                   # Et là, tout le monde peut créer sa crypto.
    [(478, 484)],                   # Donc, forcément, c'est le Far West.
    [(525, 536)],                                 # C'est pour ça qu'il faut venir équipé d'une méthode.
    [(1164, 1180)],                   # on peut se positionner grâce à la méthode IOC avant que tout le monde soit au courant.
]
FIX = {"sexe.": "CEX.", "équiper": "équipé", "la": "la"}
SR = 48000
raw = subprocess.run([FF, "-v", "quiet", "-i", r"C:/Users/User/Videos/NassRiviera/Video 3.mp4", "-vn", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
A = np.frombuffer(raw, np.float32)
def cut(s0, s1):
    c = A[int(s0 * SR):int(s1 * SR)].copy(); f = int(0.01 * SR); c[:f] *= np.linspace(0, 1, f); c[-f:] *= np.linspace(1, 0, f); return c
t = 0.25; GAP = 0.14; pieces = []; words = []; starts = []
for ph in PHRASES:
    starts.append(round(t, 3))
    for k, (i0, i1) in enumerate(ph):
        s0 = W[i0]['t'] - (0.05 if k == 0 else 0.02); s1 = W[i1]['e'] + (0.12 if k == len(ph) - 1 else 0.03)
        c = cut(s0, s1); pieces.append((t, c))
        for w in W[i0:i1 + 1]:
            words.append({"t": round(t + w['t'] - s0, 3), "e": round(t + w['e'] - s0, 3), "w": FIX.get(w['w'], w['w'])})
        t += len(c) / SR
    t += GAP
end = t
buf = np.zeros(int((end + 3.6) * SR), np.float32)
for st, c in pieces: i = int(st * SR); buf[i:i + len(c)] += c
for ph_t in starts:
    for w in words:
        if abs(w['t'] - ph_t - 0.05) < 0.2: w['w'] = w['w'][:1].upper() + w['w'][1:]; break
with wave.open('assets/voice.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(buf, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump({"words": words, "phrases": starts, "voiceEnd": round(end, 3)}, open('assets/words.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('voix', round(end, 2), 's ; phrases à', starts)
print(' '.join(w['w'] for w in words))
