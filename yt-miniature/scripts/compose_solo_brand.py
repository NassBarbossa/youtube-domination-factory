#!/usr/bin/env python3
"""Miniature solo Convergence « ultra travaillée » : portrait chroma de Nass à droite, étoiles d'or dans les yeux,
reflet doré sur le visage, lingots en bas à gauche, texte à gauche (dernière ligne en bloc or), pastille logo + ÉP.

Usage :
  python3 yt-miniature/scripts/compose_solo_brand.py nass.jpg lingots.jpg out.jpg "ALL IN|GOLD ?" \
      --theme dark|cream --ep 04 --face 0.42 --x 0.70 --pupils 565,352 725,350 --iris 26
--pupils : coordonnées des deux pupilles dans le portrait source (px), --iris : rayon de l'iris (px) dans la source.
"""
import argparse, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from compose_podcast import chroma, FONTS, REPO_ROOT
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H, S = 1280, 720, 2
PAPER, INK, GRID, GRID_D = (242, 239, 232), (11, 14, 17), (230, 225, 214), (29, 34, 40)
GOLD, GOLD_D, GREY = (201, 138, 11), (226, 169, 59), (154, 163, 173)
LOGO = REPO_ROOT / "shows" / "emission-live" / "assets" / "logo" / "convergence-logo-sombre.png"

ap = argparse.ArgumentParser()
ap.add_argument("nass"); ap.add_argument("bars"); ap.add_argument("out"); ap.add_argument("lines")
ap.add_argument("--theme", choices=["dark", "cream"], default="dark")
ap.add_argument("--ep", default="04")
ap.add_argument("--face", type=float, default=0.42, help="hauteur du visage en fraction du cadre")
ap.add_argument("--x", type=float, default=0.70)
ap.add_argument("--pupils", nargs=2, default=["565,352", "725,350"])
ap.add_argument("--iris", type=float, default=26)
ap.add_argument("--eye-y", type=float, default=0.40, help="hauteur des yeux dans le cadre (fraction)")
ap.add_argument("--bars-w", type=float, default=0.34)
ap.add_argument("--size", type=int, default=150)
a = ap.parse_args()
dark = a.theme == "dark"
acc = GOLD_D if dark else GOLD

canvas = Image.new("RGBA", (W * S, H * S), (*(INK if dark else PAPER), 255))
d = ImageDraw.Draw(canvas)
for x in range(0, W * S, 52 * S): d.line([(x, 0), (x, H * S)], fill=GRID_D if dark else GRID, width=S)
for y in range(0, H * S, 52 * S): d.line([(0, y), (W * S, y)], fill=GRID_D if dark else GRID, width=S)
# lueur or : large derrière Nass, et montée dorée depuis le bas (reflet des lingots)
glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
cx_n = int(a.x * W * S)
gd.ellipse([cx_n - 520 * S, 40 * S, cx_n + 520 * S, 1000 * S], fill=(*GOLD, 105 if dark else 60))
gd.ellipse([-200 * S, 520 * S, 760 * S, 1000 * S], fill=(*GOLD_D, 150 if dark else 70))
canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120 * S)))

# portrait
p = chroma(Image.open(a.nass)); bb = p.getbbox(); p = p.crop(bb)
scale = (H * S * a.face / 0.26) / p.height  # sur cette ancre le visage fait ≈ 26 % de la hauteur du portrait
p = p.resize((int(p.width * scale), int(p.height * scale)), Image.LANCZOS)
eye_src = sum(float(v.split(',')[1]) for v in a.pupils) / 2
px0 = int(cx_n - p.width / 2); py0 = int(a.eye_y * H * S - (eye_src - bb[1]) * scale)  # les yeux à la hauteur voulue, le corps sort par le bas
# reflet doré sur le bas du visage et le torse (lumière des lingots, venant d'en bas à gauche)
tint = Image.new("RGBA", p.size, (0, 0, 0, 0)); td = ImageDraw.Draw(tint)
for i in range(p.height):
    t = i / p.height
    td.line([(0, i), (p.width, i)], fill=(*GOLD_D, int(55 * max(0.0, t - 0.3) / 0.7)))
tint.putalpha(Image.fromarray((__import__("numpy").asarray(tint.split()[3]).astype(int) * __import__("numpy").asarray(p.split()[3]).astype(int) // 255).astype("uint8")))
rgb = ImageEnhance.Contrast(p.convert('RGB')).enhance(1.08); rgb.putalpha(p.split()[3]); p = rgb
p.alpha_composite(tint)
sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 200 if dark else 120), (px0 - 10 * S, py0 + 10 * S), p.split()[3])
canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(40 * S)))
canvas.alpha_composite(p, (px0, py0))

# étoiles d'or dans les yeux
def star(draw, cx, cy, r, col, ratio=0.28, rot=0.0):
    pts = []
    for k in range(8):
        ang = math.radians(rot + k * 45); rr = r if k % 2 == 0 else r * ratio
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=col)
stars = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(stars)
halo = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); hd = ImageDraw.Draw(halo)
for pxy in a.pupils:
    sx, sy = (float(v) for v in pxy.split(","))
    cx = px0 + (sx - bb[0]) * scale; cy = py0 + (sy - bb[1]) * scale; r = a.iris * scale
    hd.ellipse([cx - 1.7 * r, cy - 1.7 * r, cx + 1.7 * r, cy + 1.7 * r], fill=(255, 205, 80, 190))
    star(sd, cx, cy, 1.95 * r, (255, 214, 96), ratio=0.2, rot=-90)
    star(sd, cx, cy, 1.15 * r, (255, 250, 225), ratio=0.3, rot=-90)
    star(sd, cx + 1.4 * r, cy - 1.3 * r, 0.55 * r, (255, 240, 180), ratio=0.3, rot=-90)
canvas.alpha_composite(halo.filter(ImageFilter.GaussianBlur(12 * S)))
canvas.alpha_composite(stars.filter(ImageFilter.GaussianBlur(0.6 * S)))

# lingots en bas à gauche
b = chroma(Image.open(a.bars)); b = b.crop(b.getbbox())
bw = int(a.bars_w * W * S); b = b.resize((bw, int(b.height * bw / b.width)), Image.LANCZOS)
bx = int(0.02 * W * S); by = H * S - b.height + int(0.06 * H * S)
bsh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); bsh.paste((0, 0, 0, 210), (bx, by + 16 * S), b.split()[3])
canvas.alpha_composite(bsh.filter(ImageFilter.GaussianBlur(30 * S)))
bgl = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); bgl.paste((*GOLD_D, 160), (bx, by), b.split()[3])
canvas.alpha_composite(bgl.filter(ImageFilter.GaussianBlur(60 * S)))
canvas.alpha_composite(b, (bx, by))

# texte à gauche
d = ImageDraw.Draw(canvas)
def font(size):
    f = ImageFont.truetype(str(FONTS / "InterTight-var.ttf"), size * S); f.set_variation_by_axes([900]); return f
lines = a.lines.split("|"); f_big = font(a.size); lh = int(a.size * 1.08) * S
tx = int(0.31 * W * S); y = int(0.17 * H * S)
txt, stroke = (PAPER, INK) if dark else (INK, PAPER)
for i, ln in enumerate(lines):
    last = i == len(lines) - 1; tw = d.textlength(ln, font=f_big)
    if last:
        pad = 24 * S; box = [tx - tw / 2 - pad, y + 4 * S, tx + tw / 2 + pad, y + lh - 4 * S]
        d.rounded_rectangle([box[0] + 8 * S, box[1] + 10 * S, box[2] + 8 * S, box[3] + 10 * S], radius=10 * S, fill=(0, 0, 0, 110))
        d.rounded_rectangle(box, radius=10 * S, fill=acc)
        d.text((tx, y + lh / 2), ln, font=f_big, fill=INK, anchor="mm")
    else:
        d.text((tx + 5 * S, y + lh / 2 + 6 * S), ln, font=f_big, fill=(0, 0, 0, 110), anchor="mm")
        d.text((tx, y + lh / 2), ln, font=f_big, fill=txt, anchor="mm", stroke_width=6 * S, stroke_fill=stroke)
    y += lh

# pastille logo + épisode, en haut à gauche
f_mono = ImageFont.truetype(str(FONTS / "IBMPlexMono-SemiBold.ttf"), 18 * S)
logo = Image.open(LOGO).convert("RGBA"); logo = logo.crop(logo.getbbox())
lh_px = 24 * S; logo = logo.resize((int(logo.width * lh_px / logo.height), lh_px), Image.LANCZOS)
ep = f"É P .  {a.ep}"; ew = d.textlength(ep, font=f_mono)
pw = logo.width + 18 * S + ew + 44 * S; ph = 52 * S; pxp = int(tx - pw / 2); pyp = 30 * S
d.rounded_rectangle([pxp, pyp, pxp + pw, pyp + ph], radius=6 * S, fill=INK)
canvas.alpha_composite(logo, (pxp + 22 * S, int(pyp + (ph - lh_px) / 2)))
d.text((pxp + 22 * S + logo.width + 18 * S, pyp + ph / 2), ep, font=f_mono, fill=GREY, anchor="lm")

final = canvas.convert("RGB").resize((W, H), Image.LANCZOS)
final = ImageEnhance.Contrast(final).enhance(1.04)
final.save(a.out, quality=94); final.resize((256, 144), Image.LANCZOS).save(a.out.replace(".jpg", "-preview256.jpg"), quality=85)
print(a.out)
