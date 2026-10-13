#!/usr/bin/env python3
"""Build YouTube channel banners (2560x1440) with the key content inside the 1546x423 safe zone.

Three layouts, each written to outputs/banner/:
  1 grid-face   : brand grid bg + Nass cutout right + tagline + 3 pillars
  2 grid-word   : brand grid bg + big NASSIN CRYPTO wordmark + tagline (no face)
  3 series      : light bg + Nass left + the 3 training thumbnails as cards
Also writes a *-safe.jpg preview with the safe zone outlined, and a *-mobile.jpg crop.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from composite import chroma_key  # noqa: E402

W, H = 2560, 1440
SAFE_W, SAFE_H = 1546, 423
SX, SY = (W - SAFE_W) // 2, (H - SAFE_H) // 2  # 507, 508
ORANGE, CYAN, WHITE, DARK = "#FF6B35", "#00E5FF", "#FFFFFF", "#0A0A0A"
FONT = ROOT / "assets" / "fonts" / "Syne.ttf"
INTER = ROOT / "assets" / "fonts" / "Inter.ttf"
OUT = ROOT / "outputs" / "banner"
OUT.mkdir(parents=True, exist_ok=True)


def font(size, weight=800, path=FONT):
    f = ImageFont.truetype(str(path), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def fit(draw, s, max_w, size, weight=800, path=FONT):
    """Largest font size (<= size) whose rendered width fits max_w."""
    while size > 12:
        f = font(size, weight, path)
        if draw.textlength(s, font=f) <= max_w:
            return f
        size -= 2
    return font(size, weight, path)


def text(draw, xy, s, f, fill, anchor="la", stroke=0):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 230))


def grid_bg(brightness=1.0):
    im = Image.open(ROOT.parent / "yt-script" / "outputs" / "bg-nass-v2.jpg").convert("RGB")
    im = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS)
    top = (im.height - H) // 2
    im = im.crop((0, top, W, top + H))
    return ImageEnhance.Brightness(im).enhance(brightness).convert("RGBA")


def person(cutout, face_top, face_bottom, face_px):
    p = chroma_key(Image.open(ROOT / "outputs" / cutout))
    scale = face_px / ((face_bottom - face_top) * p.height)
    return p.resize((int(p.width * scale), int(p.height * scale)), Image.LANCZOS), face_top


def paste_person(bg, p, x_center, y_bottom, shadow=True):
    x, y = int(x_center - p.width / 2), int(y_bottom - p.height)
    if shadow:
        sh = Image.new("RGBA", bg.size, (0, 0, 0, 0))
        sh.paste(Image.new("RGBA", p.size, (0, 0, 0, 160)), (x + 12, y + 14), p)
        bg = Image.alpha_composite(bg, sh.filter(ImageFilter.GaussianBlur(22)))
    layer = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    layer.paste(p, (x, y), p)
    return Image.alpha_composite(bg, layer)


def save(im, name):
    rgb = im.convert("RGB")
    path = OUT / f"{name}.jpg"
    rgb.save(path, quality=90, optimize=True)
    prev = rgb.copy()
    ImageDraw.Draw(prev).rectangle((SX, SY, SX + SAFE_W, SY + SAFE_H), outline="#FF0000", width=6)
    prev.resize((1280, 720), Image.LANCZOS).save(OUT / f"{name}-safe.jpg", quality=85)
    rgb.crop((SX, SY, SX + SAFE_W, SY + SAFE_H)).save(OUT / f"{name}-mobile.jpg", quality=88)
    print(f"{path.name}: {path.stat().st_size // 1024} KB")


def banner_grid_face():
    bg = grid_bg(1.25)
    d = ImageDraw.Draw(bg)
    # safe-zone content: text left, Nass right
    x0 = SX + 30
    col = 1000
    f1 = fit(d, "INVESTIR SIMPLEMENT,", col, 118)
    text(d, (x0, SY + 60), "INVESTIR SIMPLEMENT,", f1, WHITE)
    text(d, (x0, SY + 175), "AVEC UNE MÉTHODE", f1, ORANGE)
    f2 = font(40, 600, INTER)
    cx = x0
    for i, (lbl, col) in enumerate([("GÉRER SON ARGENT", WHITE), ("DCA", CYAN), ("ON-CHAIN", ORANGE)]):
        text(d, (cx, SY + 345), lbl, f2, col)
        cx += d.textlength(lbl, font=f2) + 36
        if i < 2:
            text(d, (cx - 22, SY + 345), "·", f2, "#888888")
            cx += 18
    p, ft = person("cutout-smirk-denim.jpg", 0.133, 0.50, 250)
    bg = paste_person(bg, p, SX + SAFE_W - 215, SY + SAFE_H + 150)
    # outside safe zone: faint series line
    d = ImageDraw.Draw(bg)
    text(d, (W // 2, SY + SAFE_H + 230), "Formation offerte · 3 vidéos · nouvelle vidéo chaque semaine", font(40, 500, INTER), "#FFFFFFAA", "ma")
    save(bg, "banner-1-grid-face")


def banner_grid_word():
    bg = grid_bg(1.15)
    d = ImageDraw.Draw(bg)
    cx, cy = W // 2, SY + 150
    fw = fit(d, "NASSIN CRYPTO", 1440, 210)
    text(d, (cx, cy), "NASSIN CRYPTO", fw, WHITE, "mm")
    text(d, (cx, cy + 150), "Investir simplement, avec une méthode", fit(d, "Investir simplement, avec une méthode", 1300, 62, 700), ORANGE, "mm")
    f2 = font(36, 600, INTER)
    text(d, (cx, cy + 225), "Gérer son argent  ·  DCA  ·  Cryptos on-chain avant les autres", f2, "#FFFFFFDD", "mm")
    # thin brand line under wordmark
    d.rectangle((cx - 300, cy + 92, cx + 300, cy + 98), fill=ORANGE)
    d.rectangle((cx - 300, cy + 92, cx - 100, cy + 98), fill=CYAN)
    save(bg, "banner-2-grid-wordmark")


def banner_series():
    bg = Image.new("RGBA", (W, H), "#F4EFE6")
    # warm radial glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((W * 0.15, -200, W * 0.85, H + 200), fill=(255, 220, 180, 160))
    bg = Image.alpha_composite(bg, glow.filter(ImageFilter.GaussianBlur(200)))
    d = ImageDraw.Draw(bg)
    # three thumbnail cards on the right half of the safe zone
    thumbs = ["pourquoi-investir-2026-d-billet-v11-final.jpg", "comment-devenir-riche-a-wall-final.jpg", "investissement-on-chain-f-trading-final.jpg"]
    labels = ["LE CODE", "LE PERMIS", "LA FORMULE 1"]
    cw, ch, gap = 224, 126, 18
    x = SX + SAFE_W - 3 * cw - 2 * gap - 24
    y = SY + 110
    for t, lbl in zip(thumbs, labels):
        im = Image.open(ROOT / "outputs" / t).convert("RGBA").resize((cw, ch), Image.LANCZOS)
        sh = Image.new("RGBA", bg.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((x + 8, y + 10, x + cw + 8, y + ch + 10), 18, fill=(0, 0, 0, 110))
        bg = Image.alpha_composite(bg, sh.filter(ImageFilter.GaussianBlur(14)))
        mask = Image.new("L", (cw, ch), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw - 1, ch - 1), 18, fill=255)
        bg.paste(im, (x, y), mask)
        d = ImageDraw.Draw(bg)
        text(d, (x + cw // 2, y + ch + 28), lbl, fit(d, lbl, cw - 10, 24), DARK, "mm")
        x += cw + gap
    # Nass left + text
    p, ft = person("cutout-softsmile-blazer.jpg", 0.173, 0.50, 200)
    bg = paste_person(bg, p, SX + 150, SY + SAFE_H + 110)
    d = ImageDraw.Draw(bg)
    tx = SX + 320
    col = SAFE_W - 320 - (3 * cw + 2 * gap) - 60
    text(d, (tx, SY + 90), "FORMATION OFFERTE", fit(d, "FORMATION OFFERTE", col, 60), DARK)
    text(d, (tx, SY + 165), "Investir simplement,", fit(d, "Investir simplement,", col, 44, 700), ORANGE)
    text(d, (tx, SY + 215), "avec une méthode", fit(d, "avec une méthode", col, 44, 700), ORANGE)
    text(d, (tx, SY + 300), "Nouvelle vidéo chaque semaine", fit(d, "Nouvelle vidéo chaque semaine", col, 30, 500, INTER), "#333333")
    save(bg, "banner-3-series")


if __name__ == "__main__":
    banner_grid_face()
    banner_grid_word()
    banner_series()
