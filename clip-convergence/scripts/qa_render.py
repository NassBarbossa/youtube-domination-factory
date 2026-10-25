"""Contrôle final d'un rendu : format, durée, sonie.

Usage : python qa_render.py <rendu.mp4> [--duration D]
OK si : 1080×1920, 60 i/s, H.264 + AAC, durée = D à ±0,05 s (data-duration de la racine), sonie intégrée entre
-16 et -13 LUFS, crête vraie ≤ -1 dBTP. Le contrôle mesure, il n'écoute pas : regarder et écouter le fichier ensuite.
"""
import argparse
import json
import re
import subprocess

from common import FF, FFPROBE

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--duration", type=float)
a = ap.parse_args()
info = json.loads(subprocess.run([FFPROBE, "-v", "error", "-show_streams", "-show_format", "-of", "json", a.video],
                                 capture_output=True, text=True, check=True).stdout)
v = next(s for s in info["streams"] if s["codec_type"] == "video")
au = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
dur = float(info["format"]["duration"])
num, den = map(int, v["r_frame_rate"].split("/"))
log = subprocess.run([FF, "-hide_banner", "-nostats", "-i", a.video, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])
tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)[-1])
checks = [
    ("taille", f"{v['width']}×{v['height']}", (v["width"], v["height"]) == (1080, 1920)),
    ("cadence", f"{num / den:g} i/s", abs(num / den - 60) < 0.01),
    ("codecs", f"{v['codec_name']} + {au['codec_name'] if au else 'pas de son'}", v["codec_name"] == "h264" and au is not None and au["codec_name"] == "aac"),
    ("durée", f"{dur:.2f} s", a.duration is None or abs(dur - a.duration) <= 0.05),
    ("sonie", f"{lufs:.1f} LUFS", -16 <= lufs <= -13),
    ("crête vraie", f"{tp:.1f} dBTP", tp <= -1.0),
]
for name, val, ok in checks:
    print(f"{'ok ' if ok else 'NON'}  {name:12} {val}")
print(f"{int(info['format']['size']) / 1e6:.1f} Mo — {'tout est bon' if all(c[2] for c in checks) else 'à corriger avant de livrer'}")
