#!/usr/bin/env python3
"""Face à face aux couleurs Convergence : papier crème à grille (ou studio sombre), deux portraits chroma qui se regardent,
texte Inter Tight 900 en bas avec la dernière ligne en bloc or, pastille logo Convergence + numéro d'épisode.

Usage :
  python3 yt-miniature/scripts/compose_vs_brand.py gauche.jpg droite.jpg out.jpg "J'AI FAIT UNE|ERREUR DE DÉBUTANT" \
      --theme cream|dark --ep 01 --lf 0.30 --rf 0.30 --lx 0.24 --rx 0.82 --accent gold|green
Charte : shows/emission-live/brand-board-convergence-v2.html (papier #F2EFE8, encre #0B0E11, or #C98A0B, vert #0F8A5F).
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from compose_podcast import chroma, FONTS, REPO_ROOT
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, S = 1280, 720, 2
PAPER, CARD, INK, GRID, GRID_D = (242, 239, 232), (251, 250, 246), (11, 14, 17), (230, 225, 214), (29, 34, 40)
GOLD, GREEN, GOLD_D, GREEN_D, GREY = (201, 138, 11), (15, 138, 95), (226, 169, 59), (43, 179, 124), (154, 163, 173)
LOGO = REPO_ROOT / "shows" / "emission-live" / "assets" / "logo" / "convergence-logo-sombre.png"

ap = argparse.ArgumentParser()
ap.add_argument("left"); ap.add_argument("right"); ap.add_argument("out"); ap.add_argument("lines")
ap.add_argument("--theme", choices=["cream", "dark"], default="cream")
ap.add_argument("--accent", choices=["gold", "green"], default="gold")
ap.add_argument("--ep", default="01")
ap.add_argument("--lf", type=float, default=0.30); ap.add_argument("--rf", type=float, default=0.30)
ap.add_argument("--lx", type=float, default=0.24); ap.add_argument("--rx", type=float, default=0.82)
ap.add_argument("--size", type=int, default=112, help="Taille max du texte (px sur 720)")
a = ap.parse_args()
dark = a.theme == "dark"
acc = {"gold": GOLD_D if dark else GOLD, "green": GREEN_D if dark else GREEN}[a.accent]

canvas = Image.new("RGBA", (W * S, H * S), (*(INK if dark else PAPER), 255))
d = ImageDraw.Draw(canvas)
step = 52 * S
for x in range(0, W * S, step): d.line([(x, 0), (x, H * S)], fill=GRID_D if dark else GRID, width=S)
for y in range(0, H * S, step): d.line([(0, y), (W * S, y)], fill=GRID_D if dark else GRID, width=S)
# lueurs : or côté gauche (co-host), vert côté Nass, comme le gabarit officiel
glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
ga = 150 if dark else 70
gd.ellipse([int(a.lx * W * S) - 420 * S, 120 * S, int(a.lx * W * S) + 420 * S, 900 * S], fill=(*GOLD, ga))
gd.ellipse([int(a.rx * W * S) - 420 * S, 120 * S, int(a.rx * W * S) + 420 * S, 900 * S], fill=(*GREEN, ga))
canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(110 * S)))

def place(path, xc, face_frac):
    p = chroma(Image.open(path)); p = p.crop(p.getbbox())
    h = int(H * S * face_frac / 0.30)
    p = p.resize((int(p.width * h / p.height), h), Image.LANCZOS)
    x = int(xc * W * S - p.width / 2); y = H * S - h + int(0.02 * H * S)
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 190 if dark else 110), (x + 6 * S, y + 10 * S), p.split()[3])
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(34 * S)))
    canvas.alpha_composite(p, (x, y))

place(a.right, a.rx, a.rf)
place(a.left, a.lx, a.lf)

# voile en bas (vers l'encre ou vers le papier) pour la lisibilité du texte
veil = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); vd = ImageDraw.Draw(veil)
vc = INK if dark else PAPER
for i in range(260 * S):
    al = int((215 if dark else 200) * (i / (260 * S)) ** 1.5)
    vd.line([(0, H * S - 260 * S + i), (W * S, H * S - 260 * S + i)], fill=(*vc, al))
canvas.alpha_composite(veil)

d = ImageDraw.Draw(canvas)
lines = a.lines.split("|"); cx = W * S // 2; maxw = 0.90 * W * S
def font(size):
    f = ImageFont.truetype(str(FONTS / "InterTight-var.ttf"), size * S); f.set_variation_by_axes([900]); return f
size = a.size
while size > 60 and max(d.textlength(ln, font=font(size)) for ln in lines) > maxw - 60 * S: size -= 4
f_big = font(size); lh = int(size * 1.12) * S
y = H * S - 60 * S - lh * len(lines)
txt, stroke = (PAPER, INK) if dark else (INK, PAPER)
for i, ln in enumerate(lines):
    last = i == len(lines) - 1
    tw = d.textlength(ln, font=f_big)
    if last:
        pad = 22 * S; box = [cx - tw / 2 - pad, y + 2 * S, cx + tw / 2 + pad, y + lh - 2 * S]
        d.rounded_rectangle([box[0] + 6 * S, box[1] + 8 * S, box[2] + 6 * S, box[3] + 8 * S], radius=8 * S, fill=(0, 0, 0, 90))
        d.rounded_rectangle(box, radius=8 * S, fill=acc)
        d.text((cx, y + lh / 2), ln, font=f_big, fill=INK if a.accent == "gold" else PAPER, anchor="mm")
    else:
        d.text((cx + 4 * S, y + lh / 2 + 5 * S), ln, font=f_big, fill=(0, 0, 0, 90), anchor="mm")
        d.text((cx, y + lh / 2), ln, font=f_big, fill=txt, anchor="mm", stroke_width=5 * S, stroke_fill=stroke)
    y += lh

# pastille logo + épisode, en haut au centre (comme le gabarit officiel, remontée car le texte occupe le bas)
f_mono = ImageFont.truetype(str(FONTS / "IBMPlexMono-SemiBold.ttf"), 18 * S)
logo = Image.open(LOGO).convert("RGBA"); logo = logo.crop(logo.getbbox())
lh_px = 24 * S; logo = logo.resize((int(logo.width * lh_px / logo.height), lh_px), Image.LANCZOS)
ep = f"É P .  {a.ep}"; ew = d.textlength(ep, font=f_mono)
pw = logo.width + 18 * S + ew + 44 * S; ph = 52 * S; px = cx - pw / 2; py = 30 * S
d.rounded_rectangle([px, py, px + pw, py + ph], radius=6 * S, fill=INK)
canvas.alpha_composite(logo, (int(px + 22 * S), int(py + (ph - lh_px) / 2)))
d.text((px + 22 * S + logo.width + 18 * S, py + ph / 2), ep, font=f_mono, fill=GREY, anchor="lm")

final = canvas.convert("RGB").resize((W, H), Image.LANCZOS)
final.save(a.out, quality=94); final.resize((256, 144), Image.LANCZOS).save(a.out.replace(".jpg", "-preview256.jpg"), quality=85)
print(a.out)
