"""Position médiane du visage dans chaque clip caméra (coordonnées du recadrage source), pour cadrer sans trou.

Lit cut.json (caméras) et timeline.json, ouvre assets/video/<cam>_<seg>.mp4, détecte le visage le plus sûr (YuNet)
toutes les 0,4 s et écrit timeline.json["faces"][cam][seg] = [x, y] (pixels du recadrage, avant pré-agrandissement).
Usage : python face_track.py <dossier_projet>
"""
import json
import os
import statistics
import sys
from pathlib import Path

os.environ.setdefault("OPENCV_LOG_LEVEL", "ERROR")   # sans les avertissements du moteur dnn
import cv2  # noqa: E402

from common import YUNET, load_cut

proj = Path(sys.argv[1])
cams = list(load_cut(proj)["crops"])
tl = json.loads((proj / "timeline.json").read_text(encoding="utf-8"))
k = tl["prescale"]
det = None
faces = {}
for cam in cams:
    faces[cam] = {}
    for s in tl["segments"]:
        cap = cv2.VideoCapture(str(proj / f"assets/video/{cam}_{s['id']}.mp4"))
        fps = cap.get(cv2.CAP_PROP_FPS) or 60
        xs, ys = [], []
        t = tl["handle"]
        while t < tl["handle"] + s["dur"]:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
            ok, frame = cap.read()
            if not ok:
                break
            small = cv2.resize(frame, None, fx=0.5, fy=0.5)
            if det is None:
                det = cv2.FaceDetectorYN.create(str(YUNET), "", (small.shape[1], small.shape[0]), 0.6, 0.3, 50)
            det.setInputSize((small.shape[1], small.shape[0]))
            _, found = det.detect(small)
            if found is not None and len(found):
                x, y, w, h = max(found, key=lambda r: r[14])[:4]   # le plus sûr
                xs.append((x + w / 2) * 2 / k)
                ys.append((y + h / 2) * 2 / k)
            t += 0.4
        cap.release()
        if xs:
            faces[cam][s["id"]] = [round(statistics.median(xs)), round(statistics.median(ys))]
        print(f"{cam:5} {s['id']:4} visages {len(xs):2} -> {faces[cam].get(s['id'])}")
tl["faces"] = faces
(proj / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
