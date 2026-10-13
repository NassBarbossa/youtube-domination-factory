#!/usr/bin/env python3
"""Composite a green-screen cutout of Nass onto a generated background.

Usage:
  python3 yt-miniature/scripts/composite.py bg.jpg cutout.jpg out.jpg \
      --face-top 0.146 --face-bottom 0.443 --face-frac 0.29 --x-center 0.5 --bottom 1.0

--face-top / --face-bottom : where the face sits in the cutout (fractions of its height),
                             used to scale the person so the face = --face-frac of 720 px.
--x-center                 : horizontal position of the person's centre (fraction of 1280).
--bottom                   : where the cutout's bottom edge lands (fraction of 720; 1.0 = frame bottom).
A soft dark drop shadow is added behind the person for separation. Output is 1280x720.
"""
import argparse

from PIL import Image, ImageChops, ImageFilter


def chroma_key(img: Image.Image) -> Image.Image:
    """Return RGBA with pure-green background removed and green spill reduced."""
    rgb = img.convert("RGB")
    r, g, b = rgb.split()
    maxrb = ImageChops.lighter(r, b)
    # green dominance: g - max(r,b); background ~ 255, skin/cloth ~ <= 0
    diff = ImageChops.subtract(g, maxrb)  # clipped at 0
    # alpha = 255 where diff small, 0 where diff large; soft ramp between 25 and 90
    alpha = diff.point(lambda v: 255 if v < 25 else (0 if v > 90 else int(255 * (90 - v) / 65)))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    # despill: clamp green to max(r,b) wherever green dominates
    g2 = ImageChops.darker(g, maxrb.point(lambda v: min(255, v + 8)))
    out = Image.merge("RGBA", (r, g2, b, alpha))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("bg")
    ap.add_argument("cutout")
    ap.add_argument("out")
    ap.add_argument("--face-top", type=float, default=0.146)
    ap.add_argument("--face-bottom", type=float, default=0.443)
    ap.add_argument("--face-frac", type=float, default=0.29)
    ap.add_argument("--x-center", type=float, default=0.5)
    ap.add_argument("--bottom", type=float, default=1.0)
    ap.add_argument("--shadow", type=int, default=18, help="shadow blur radius (0 = none)")
    ap.add_argument("--pixel-art", action="store_true", help="nearest-neighbour scaling (CryptoPunk)")
    args = ap.parse_args()

    bg = Image.open(args.bg).convert("RGBA").resize((1280, 720), Image.LANCZOS)
    src = Image.open(args.cutout)
    if src.mode == "RGBA" and src.getextrema()[3][0] < 255:
        person = src  # already transparent (e.g. a PNG cutout or a CryptoPunk)
    else:
        person = chroma_key(src)

    face_h = (args.face_bottom - args.face_top) * person.height
    scale = (args.face_frac * 720) / face_h
    pw, ph = int(person.width * scale), int(person.height * scale)
    resample = Image.NEAREST if args.pixel_art else Image.LANCZOS
    person = person.resize((pw, ph), resample)

    x = int(args.x_center * 1280 - pw / 2)
    y = int(args.bottom * 720 - ph)

    layer = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    layer.paste(person, (x, y), person)

    if args.shadow:
        shadow = Image.new("RGBA", bg.size, (0, 0, 0, 0))
        sh = Image.new("RGBA", person.size, (0, 0, 0, 170))
        shadow.paste(sh, (x + 10, y + 12), person)
        shadow = shadow.filter(ImageFilter.GaussianBlur(args.shadow))
        bg = Image.alpha_composite(bg, shadow)

    out = Image.alpha_composite(bg, layer).convert("RGB")
    out.save(args.out, quality=94)
    print(f"Saved {args.out}: person {pw}x{ph} at ({x},{y}), face ~{int(face_h*scale)} px tall")


if __name__ == "__main__":
    main()
