#!/usr/bin/env python3
"""Vérification de ressemblance à taille réelle : la sortie générée à côté de la photo de référence.

Usage :
  python3 yt-miniature/scripts/compare_ref.py sortie.jpg reference.jpg [--out planche.jpg] [--top 0.55]
  python3 yt-miniature/scripts/compare_ref.py sortie.jpg ref1.jpg ref2.jpg   # plusieurs références

Produit une planche où chaque image est recadrée sur sa partie haute (--top, fraction de la hauteur,
là où se trouve le visage sur un portrait 3:4) et redimensionnée à la même hauteur (900 px), sans
réduction du visage. À ouvrir avant de montrer quoi que ce soit à Nass : si un trait protégé a changé
(forme des yeux, nez, mâchoire, couleur de barbe, implantation des cheveux), le tirage est rejeté.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PANEL_H = 900
GAP = 24


def crop_top(img: Image.Image, top: float) -> Image.Image:
    img = img.convert("RGB")
    w, h = img.size
    if w >= h:  # photo carrée ou paysage : on garde tout
        return img
    return img.crop((0, 0, w, int(h * top)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("output", help="Image générée à vérifier")
    ap.add_argument("refs", nargs="+", help="Photo(s) de référence")
    ap.add_argument("--out", help="Planche de sortie (défaut : <sortie>-vs-ref.jpg)")
    ap.add_argument("--top", type=float, default=0.55, help="Fraction haute conservée sur les portraits")
    a = ap.parse_args()

    panels = []
    labels = ["SORTIE"] + [f"RÉF {i + 1}" for i in range(len(a.refs))]
    for path in [a.output] + a.refs:
        im = crop_top(Image.open(path), a.top)
        im = im.resize((int(im.width * PANEL_H / im.height), PANEL_H), Image.LANCZOS)
        panels.append(im)

    total_w = sum(p.width for p in panels) + GAP * (len(panels) + 1)
    sheet = Image.new("RGB", (total_w, PANEL_H + 70), (18, 18, 18))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except OSError:
        font = ImageFont.load_default()
    x = GAP
    for label, p in zip(labels, panels):
        sheet.paste(p, (x, 60))
        d.text((x, 16), label, fill=(240, 240, 240), font=font)
        x += p.width + GAP

    out = Path(a.out) if a.out else Path(a.output).with_name(Path(a.output).stem + "-vs-ref.jpg")
    sheet.save(out, quality=90)
    print(out)


if __name__ == "__main__":
    main()
