#!/usr/bin/env python3
"""Assemble une miniature podcast (Convergence) : fond + deux détourages + texte central. Pillow + numpy.

Usage :
  python3 yt-miniature/scripts/compose_podcast.py bg.jpg gauche.jpg droite.jpg out.jpg \
      --lines "BITCOIN N'EST PAS|UNE VALEUR|REFUGE" --ep "ÉP. 01" --accent gold --theme dark --left-accent green \
      --lead left --drop 0.18 --scale 1.0 --lx 0.11 --rx 0.89 --grade warm

Détourages : portraits 3:4 sur fond chroma vert #00FF00, ou PNG déjà transparent ; buste ancré en bas du cadre.
--lead left|right|none  la personne qui porte l'épisode est plus grande (l'autre à --other 0.88) et un peu plus
                        éclairée ; « poids égal aux deux » est l'erreur n° 1 des miniatures de podcast (1of10).
--grade warm|cool|none  un seul étalonnage appliqué à tout (fond + personnes) pour fondre deux rendus différents.
--lb / --rb             luminosité de chaque personne (1.0 = inchangée) pour l'accorder au fond.
Ombres : halo doux derrière chaque personne + ombre de contact sur la table (--contact 0 pour l'enlever).
Texte : Inter Tight 900, dernière ligne en bloc accent ; sous-titre IBM Plex Mono « CONVERGENCE · ÉPISODE NN ».
Sorties : out.jpg (1280×720) et out-preview256.jpg (contrôle à taille de fil).
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[2]
FONTS = REPO_ROOT / "shows" / "emission-live" / "assets" / "fonts"
W, H, S = 1280, 720, 2
INK, CREAM, GOLD, GREEN = (11, 14, 17), (242, 239, 232), (201, 138, 11), (15, 138, 95)


def chroma(im: Image.Image) -> Image.Image:
    """RGBA : fond vert #00FF00 retiré (clé G - max(R,B)), despill, érosion légère contre la frange."""
    if im.mode == "RGBA" and im.getextrema()[3][0] < 255:
        return im
    arr = np.asarray(im.convert("RGB")).astype(int)
    R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
    green = G - np.maximum(R, B)
    alpha = np.clip((60 - green) * 6, 0, 255).astype("uint8")
    out = arr.copy()
    out[..., 1] = G - np.clip(green, 0, None) * 0.9
    rgba = Image.fromarray(np.dstack([np.clip(out, 0, 255).astype("uint8"), alpha]), "RGBA")
    al = rgba.split()[3].filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    rgba.putalpha(al)
    return rgba


def brightness(p: Image.Image, k: float) -> Image.Image:
    if abs(k - 1.0) < 1e-3:
        return p
    rgb = ImageEnhance.Brightness(p.convert("RGB")).enhance(k)
    rgb.putalpha(p.split()[3])
    return rgb


def grade(img: Image.Image, mode: str) -> Image.Image:
    """Même étalonnage sur toute l'image (fond et personnes) : dominante + contraste léger."""
    if mode == "none":
        return img
    mult = {"warm": (1.05, 1.0, 0.94), "cool": (0.95, 1.0, 1.06)}[mode]
    rgb = img.convert("RGB")
    arr = np.asarray(rgb).astype(float)
    for c, m in enumerate(mult):
        arr[..., c] *= m
    rgb = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.04)
    return rgb.convert("RGBA")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bg"); ap.add_argument("left"); ap.add_argument("right"); ap.add_argument("out")
    ap.add_argument("--lines", default="LE TRADING EST|UN JEU DE|MENTEURS", help="Lignes séparées par |, la dernière en bloc accent")
    ap.add_argument("--ep", default="ÉP. 03")
    ap.add_argument("--accent", choices=["gold", "green"], default="gold")
    ap.add_argument("--theme", choices=["cream", "dark"], default="dark")
    ap.add_argument("--left-accent", choices=["gold", "green"], default="green", help="Couleur du halo gauche (thème sombre)")
    ap.add_argument("--flip-left", action="store_true"); ap.add_argument("--flip-right", action="store_true")
    ap.add_argument("--scale", type=float, default=1.0, help="Hauteur des personnes en fraction du cadre")
    ap.add_argument("--lead", choices=["left", "right", "none"], default="none")
    ap.add_argument("--other", type=float, default=0.88, help="Taille relative de la personne qui ne mène pas")
    ap.add_argument("--lx", type=float, default=0.11); ap.add_argument("--rx", type=float, default=0.89)
    ap.add_argument("--drop", type=float, default=0.18, help="Descente des corps sous le bord bas (fraction du cadre)")
    ap.add_argument("--lb", type=float, default=1.0); ap.add_argument("--rb", type=float, default=1.0)
    ap.add_argument("--grade", choices=["warm", "cool", "none"], default="none")
    ap.add_argument("--contact", type=int, default=1, help="1 = ombre de contact sur la table, 0 = aucune")
    ap.add_argument("--text-y", type=int, default=175, help="Haut du bloc texte (px sur 720)")
    a = ap.parse_args()

    acc = {"gold": GOLD, "green": GREEN}[a.accent]
    dark = a.theme == "dark"
    canvas = Image.open(a.bg).convert("RGB").resize((W * S, H * S), Image.LANCZOS).convert("RGBA")

    if dark:
        glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        cols = {"gold": (201, 138, 11, 150), "green": (15, 138, 95, 150)}
        lc = cols[a.left_accent]; rc = cols["green" if a.left_accent == "gold" else "gold"]
        for xc, col in ((a.lx, lc), (a.rx, rc)):
            gd.ellipse([xc * W * S - 260 * S, H * S - 520 * S, xc * W * S + 260 * S, H * S + 150 * S], fill=col)
        canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90 * S)))

    def place(path: str, xc: float, flip: bool, mult: float, bright: float):
        p = chroma(Image.open(path))
        if flip:
            p = p.transpose(Image.FLIP_LEFT_RIGHT)
        p = p.crop(p.getbbox())
        h = int(H * S * a.scale * mult); w = int(p.width * h / p.height)
        p = brightness(p.resize((w, h), Image.LANCZOS), bright)
        x = int(xc * W * S - w / 2); y = H * S - h + int(a.drop * H * S)
        halo = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        halo.paste((0, 0, 0, 150), (x, y), p.split()[3])
        halo = halo.filter(ImageFilter.GaussianBlur(30 * S))
        contact = None
        if a.contact:
            contact = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            cd = ImageDraw.Draw(contact)
            cy = min(H * S - 6 * S, y + h - int(0.03 * h))
            cd.ellipse([x + int(0.1 * w), cy - int(0.06 * h), x + int(0.9 * w), cy + int(0.06 * h)], fill=(0, 0, 0, 170))
            contact = contact.filter(ImageFilter.GaussianBlur(18 * S))
        return p, x, y, halo, contact

    lm = 1.0 if a.lead in ("left", "none") else a.other
    rm = 1.0 if a.lead in ("right", "none") else a.other
    lb = a.lb * (0.93 if a.lead == "right" else 1.0)
    rb = a.rb * (0.93 if a.lead == "left" else 1.0)
    persons = [place(a.left, a.lx, a.flip_left, lm, lb), place(a.right, a.rx, a.flip_right, rm, rb)]
    if a.lead == "left":
        persons.reverse()  # la personne qui mène est composée en dernier, donc devant
    for p, x, y, halo, contact in persons:
        canvas.alpha_composite(halo)
        if contact is not None:
            canvas.alpha_composite(contact)
        canvas.alpha_composite(p, (x, y))

    canvas = grade(canvas, a.grade)

    d = ImageDraw.Draw(canvas)
    f_big = ImageFont.truetype(str(FONTS / "InterTight-var.ttf"), 72 * S); f_big.set_variation_by_axes([900])
    f_key = ImageFont.truetype(str(FONTS / "InterTight-var.ttf"), 86 * S); f_key.set_variation_by_axes([900])
    f_sub = ImageFont.truetype(str(FONTS / "IBMPlexMono-SemiBold.ttf"), 22 * S)
    txt_col = CREAM if dark else INK; stroke = INK if dark else CREAM
    cx = W * S // 2; y = a.text_y * S
    lines = a.lines.split("|")
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1
        f = f_key if last else f_big
        tw = d.textlength(ln, font=f); th = (96 if last else 76) * S
        if last:
            pad = 22 * S
            box = [cx - tw / 2 - pad, y, cx + tw / 2 + pad, y + th]
            d.rounded_rectangle([box[0] + 6 * S, box[1] + 8 * S, box[2] + 6 * S, box[3] + 8 * S], radius=8 * S, fill=(0, 0, 0, 110))
            d.rounded_rectangle(box, radius=8 * S, fill=acc)
            d.text((cx, y + th / 2), ln, font=f, fill=INK if a.accent == "gold" else CREAM, anchor="mm")
        else:
            d.text((cx + 4 * S, y + th / 2 + 5 * S), ln, font=f, fill=(0, 0, 0, 120), anchor="mm")
            d.text((cx, y + th / 2), ln, font=f, fill=txt_col, anchor="mm", stroke_width=5 * S, stroke_fill=stroke)
        y += th + 8 * S
    sub = "CONVERGENCE · ÉPISODE " + a.ep.split()[-1]
    sw = d.textlength(sub, font=f_sub)
    d.rounded_rectangle([cx - sw / 2 - 16 * S, y + 10 * S, cx + sw / 2 + 16 * S, y + 50 * S], radius=5 * S, fill=INK)
    d.text((cx, y + 30 * S), sub, font=f_sub, fill=(154, 163, 173), anchor="mm")

    final = canvas.convert("RGB").resize((W, H), Image.LANCZOS)
    final.save(a.out, quality=94)
    preview = Path(a.out).with_name(Path(a.out).stem + "-preview256.jpg")
    final.resize((256, 144), Image.LANCZOS).save(preview, quality=85)
    print(f"{a.out} (+ {preview.name})")


if __name__ == "__main__":
    main()
