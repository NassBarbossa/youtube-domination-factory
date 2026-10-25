"""Les deux fauteuils sont-ils occupés ? Par caméra, part des images avec un visage et part d'images figées.

Usage : python presence.py <source> <début> <fin> <zones.json> [--offset -1.76] [--step 1]
  début / fin   temps de la source (s, mm:ss ou h:mm:ss) ; avec --offset, temps de la transcription
                (--offset = raw_to_source du cut.json : source = transcription + offset)
  zones.json    un JSON avec "crops": {"nass": [x, y, w, h], "sadek": [...]} : le cut.json du clip, ou
                projects/<ep>/zones-<mise en page>.json (les zones changent avec la mise en page OBS)
Sous 80 % de visages ou au-dessus de 20 % d'images figées : fauteuil vide, caméra coupée ou flux gelé
(Sadek arrive par le réseau). Choisir un autre passage, ou montrer l'écran / le deck à la place.
"""
import argparse
import json
import os
import subprocess

os.environ.setdefault("OPENCV_LOG_LEVEL", "ERROR")   # sans les avertissements du moteur dnn
import cv2  # noqa: E402
import numpy as np

from common import FF, YUNET, seconds

ap = argparse.ArgumentParser()
ap.add_argument("source")
ap.add_argument("start")
ap.add_argument("end")
ap.add_argument("zones")
ap.add_argument("--offset", type=float, default=0.0)
ap.add_argument("--step", type=float, default=1.0)
a = ap.parse_args()
t0, t1 = seconds(a.start) + a.offset, seconds(a.end) + a.offset
crops = json.load(open(a.zones, encoding="utf-8"))["crops"]
for cam, (x, y, w, h) in crops.items():
    w2, h2 = w // 4 * 2, h // 4 * 2   # demi-taille, dimensions paires
    out = subprocess.run([FF, "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", a.source,
                          "-vf", f"fps=1/{a.step},crop={w}:{h}:{x}:{y},scale={w2}:{h2}", "-f", "rawvideo",
                          "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    frames = np.frombuffer(out, np.uint8).reshape(-1, h2, w2, 3)
    det = cv2.FaceDetectorYN.create(str(YUNET), "", (w2, h2), 0.6, 0.3, 50)
    seen = sum(1 for f in frames if (r := det.detect(f)[1]) is not None and len(r))
    grey = frames.mean(axis=3)
    frozen = int((np.abs(np.diff(grey, axis=0)).mean(axis=(1, 2)) < 0.5).sum()) if len(frames) > 1 else 0
    n = max(len(frames), 1)
    ok = seen / n >= 0.8 and frozen / n <= 0.2
    print(f"{cam:6} visages {seen:3}/{len(frames):3} ({seen / n:4.0%})   figées {frozen:3} ({frozen / n:4.0%})   "
          f"{'ok' if ok else 'À VÉRIFIER'}")
