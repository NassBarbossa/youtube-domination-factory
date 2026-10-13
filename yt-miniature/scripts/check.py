#!/usr/bin/env python3
"""Quick QA on a thumbnail: size, mean brightness (0-255), dominant hue, and a 256x144 preview.

Usage: python3 yt-miniature/scripts/check.py image.jpg [image2.jpg ...]
Target: brightness 100-120, one dominant hue family (cyan ~180-200° or orange ~15-35°).
"""
import sys
from pathlib import Path

from PIL import Image, ImageStat


def hue_family(img: Image.Image) -> str:
    hsv = img.convert("RGB").resize((160, 90)).convert("HSV")
    buckets = {"orange": 0, "cyan": 0, "other": 0}
    raw = hsv.tobytes()
    for h, s, v in zip(raw[0::3], raw[1::3], raw[2::3]):
        if s < 60 or v < 60:
            continue
        deg = h * 360 / 255
        if 10 <= deg <= 40:
            buckets["orange"] += 1
        elif 170 <= deg <= 210:
            buckets["cyan"] += 1
        else:
            buckets["other"] += 1
    total = sum(buckets.values()) or 1
    return ", ".join(f"{k} {v*100//total}%" for k, v in buckets.items())


for arg in sys.argv[1:]:
    p = Path(arg)
    img = Image.open(p)
    gray = img.convert("L")
    mean = ImageStat.Stat(gray).mean[0]
    verdict = "OK" if 100 <= mean <= 120 else ("TROP SOMBRE" if mean < 100 else "TROP CLAIR")
    preview = p.with_name(p.stem + "-preview256" + p.suffix)
    img.convert("RGB").resize((256, 144), Image.LANCZOS).save(preview, quality=90)
    print(f"{p.name}: {img.size[0]}x{img.size[1]}  brightness={mean:.0f} ({verdict})  hues: {hue_family(img)}  preview -> {preview.name}")
