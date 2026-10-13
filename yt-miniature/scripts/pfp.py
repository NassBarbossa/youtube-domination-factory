#!/usr/bin/env python3
"""Build an 800x800 YouTube profile picture from a green-screen cutout on a solid background.

Usage: python3 yt-miniature/scripts/pfp.py cutout.jpg out.png --bg "#FF6B35" --face-top 0.1 --face-bottom 0.5 --face-frac 0.62
Also writes out-circle.png (circle crop preview at 800) and out-98.png (YouTube display size).
"""
import argparse, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, str(Path(__file__).resolve().parent))
from composite import chroma_key

ap = argparse.ArgumentParser()
ap.add_argument("cutout"); ap.add_argument("out")
ap.add_argument("--bg", default="#FF6B35", help="solid color, or a path to an image (center square crop)")
ap.add_argument("--bg-brightness", type=float, default=1.0)
ap.add_argument("--glow", type=int, default=0, help="soft light halo behind the person (0-255 alpha)")
ap.add_argument("--face-top", type=float, required=True)
ap.add_argument("--face-bottom", type=float, required=True)
ap.add_argument("--face-frac", type=float, default=0.62, help="face height as fraction of 800")
ap.add_argument("--face-center", type=float, default=0.47, help="where the face centre sits vertically (fraction)")
a = ap.parse_args()

S = 800
if Path(a.bg).exists():
    from PIL import ImageEnhance
    im = Image.open(a.bg).convert("RGB"); w, h = im.size; side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2, (w - side) // 2 + side, (h - side) // 2 + side)).resize((S, S), Image.LANCZOS)
    bg = ImageEnhance.Brightness(im).enhance(a.bg_brightness).convert("RGBA")
else:
    bg = Image.new("RGBA", (S, S), a.bg)
person = chroma_key(Image.open(a.cutout))
face_h = (a.face_bottom - a.face_top) * person.height
scale = a.face_frac * S / face_h
person = person.resize((int(person.width * scale), int(person.height * scale)), Image.LANCZOS)
x = (S - person.width) // 2
y = int(a.face_center * S - (a.face_top + (a.face_bottom - a.face_top) / 2) * person.height)
if a.glow:
    halo = Image.new("RGBA", (S, S), (0, 0, 0, 0)); ImageDraw.Draw(halo).ellipse((S*0.18, S*0.08, S*0.82, S*0.9), fill=(255, 255, 255, a.glow))
    bg = Image.alpha_composite(bg, halo.filter(ImageFilter.GaussianBlur(90)))
shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0)); shadow.paste(Image.new("RGBA", person.size, (0, 0, 0, 120)), (x + 6, y + 8), person)
out = Image.alpha_composite(bg, shadow.filter(ImageFilter.GaussianBlur(14)))
layer = Image.new("RGBA", (S, S), (0, 0, 0, 0)); layer.paste(person, (x, y), person)
out = Image.alpha_composite(out, layer).convert("RGB")
o = Path(a.out); out.save(o)
mask = Image.new("L", (S, S), 0); ImageDraw.Draw(mask).ellipse((0, 0, S - 1, S - 1), fill=255)
circ = Image.new("RGB", (S, S), "white"); circ.paste(out, (0, 0), mask); circ.save(o.with_name(o.stem + "-circle.png"))
circ.resize((98, 98), Image.LANCZOS).save(o.with_name(o.stem + "-98.png"))
print(f"Saved {o} (+ circle, 98px)")
