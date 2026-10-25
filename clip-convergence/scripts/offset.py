"""Décalage entre deux fichiers du même son (enregistrements OBS d'une session, brut et replay monté, YouTube),
par corrélation audio.

Usage : python offset.py <référence> <cible> <t1> [<t2> ...] [--guess D] [--probe 8]
  t           instant dans <référence> (s, mm:ss ou h:mm:ss), choisi en pleine parole, loin d'une coupe
  --guess D   décalage attendu (cible − référence) : recherche limitée à ±6 s autour, rapide
  sans guess  recherche grossière sur toute la cible (2 kHz, lit tout le fichier), puis fine (16 kHz)
Affiche le temps dans la cible, le décalage (cible − référence) et le score (1 = même son ; sous 0,9, ne pas s'y fier).
Deux enregistrements OBS d'une même session : décalage constant. Brut vs replay monté ou YouTube : il change à chaque
coupe du montage, on le mesure donc pour chaque clip.
"""
import argparse

import numpy as np

from common import pcm, seconds


def best(hay, probe):
    n = len(hay) + len(probe)
    nfft = 1 << (n - 1).bit_length()
    corr = np.fft.irfft(np.fft.rfft(hay, nfft) * np.conj(np.fft.rfft(probe, nfft)), nfft)[: len(hay) - len(probe) + 1]
    # énergie glissante de la cible en O(n) (np.convolve sur des fenêtres de plusieurs secondes prend des minutes)
    c = np.concatenate(([0.0], np.cumsum(hay.astype(np.float64) ** 2)))
    e = np.sqrt(np.maximum(c[len(probe):] - c[: -len(probe)], 0.0))[: len(corr)]
    # plancher d'énergie : dans un silence, diviser par ~0 crée de faux pics
    e = np.maximum(e, 0.25 * np.median(e[e > 0])) if np.any(e > 0) else np.ones_like(e)
    score = corr / e / (np.linalg.norm(probe) + 1e-9)
    i = int(np.argmax(score))
    return i, float(score[i])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ref")
    ap.add_argument("target")
    ap.add_argument("times", nargs="+")
    ap.add_argument("--guess", type=float)
    ap.add_argument("--probe", type=float, default=8.0)
    a = ap.parse_args()
    coarse, SRC = None, 2000
    for t in map(seconds, a.times):
        if a.guess is None:
            if coarse is None:
                coarse = pcm(a.target, 0, None, sr=SRC)
            i, _ = best(coarse, pcm(a.ref, t, 15.0, sr=SRC))
            guess = i / SRC - t
        else:
            guess = a.guess
        lo = max(t + guess - 6, 0)
        j, s = best(pcm(a.target, lo, 12 + a.probe), pcm(a.ref, t, a.probe))
        tt = lo + j / 16000
        print(f"référence {t:9.3f} s -> cible {tt:9.3f} s   décalage {tt - t:+9.3f} s   score {s:.3f}", flush=True)


if __name__ == "__main__":
    main()
