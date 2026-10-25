"""Extrait l'écran partagé de Nass (TradingView, deck) pour les morceaux où il le montre.

Lit cut.json["screen"] = {"crop": [x, y, w, h], "size": [W, H], "segments": ["s3a", ...]} et timeline.json.
Écrit assets/video/screen_<seg>.mp4 (mêmes poignées que build_media.py, 60 i/s, GOP 1 s).
Usage : python build_screen.py <dossier_projet>
"""
import json
import subprocess
import sys
from pathlib import Path

from common import FF, load_cut

proj = Path(sys.argv[1])
cfg = load_cut(proj)
if "screen" not in cfg:
    sys.exit('cut.json sans bloc "screen" : rien à extraire')
(x, y, w, h), (ow, oh), want = cfg["screen"]["crop"], cfg["screen"]["size"], set(cfg["screen"]["segments"])
tl = json.loads((proj / "timeline.json").read_text(encoding="utf-8"))
H = tl["handle"]
for s in (s for s in tl["segments"] if s["id"] in want):
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{s['src_a'] - H:.3f}", "-t", f"{s['dur'] + 2 * H:.3f}", "-i", cfg["source"],
                    "-vf", f"crop={w}:{h}:{x}:{y},scale={ow}:{oh}:flags=lanczos,fps=60,format=yuv420p",
                    "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-g", "60", "-keyint_min", "60",
                    "-movflags", "+faststart", str(proj / f"assets/video/screen_{s['id']}.mp4")], check=True)
    print("écran", s["id"], "ok")
