#!/usr/bin/env python3
"""Add brand text to a generated thumbnail base (Syne 800, Nass Riviera colors).

Usage:
  python3 yt-miniature/scripts/overlay.py base.jpg out.jpg \
      --line "2026" --line "LE SECRET" \
      --colors "#FF6B35,#FFFFFF" --x 70 --y 70 --sizes 230,96

Each --line is one row of text. --colors and --sizes are comma lists matched to
lines (last value repeats). Text is drawn top-left at (x, y) with a soft drop
shadow, then the image is resized to 1280x720 and a 256x144 preview is saved
next to the output (mobile-size check).
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = Path(__file__).resolve().parent.parent / "assets" / "fonts" / "Syne.ttf"
ORANGE, CYAN, WHITE = "#FF6B35", "#00E5FF", "#FFFFFF"


def font(size: int) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONT), size)
    try:
        f.set_variation_by_axes([800])
    except Exception:
        pass
    return f


def spread(values: str, n: int, cast):
    parts = [cast(v) for v in values.split(",")] if values else []
    return [parts[i] if i < len(parts) else (parts[-1] if parts else None) for i in range(n)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("out")
    ap.add_argument("--line", action="append", default=[])
    ap.add_argument("--colors", default=WHITE)
    ap.add_argument("--sizes", default="120")
    ap.add_argument("--x", type=int, default=70)
    ap.add_argument("--y", type=int, default=70)
    ap.add_argument("--gap", type=int, default=12)
    ap.add_argument("--align", choices=["left", "center"], default="left")
    ap.add_argument("--max-width", type=int, default=1140, help="Shrink a line until it fits this width (px)")
    ap.add_argument("--stroke", type=int, default=0, help="Dark outline width in px (use on light backgrounds)")
    args = ap.parse_args()

    img = Image.open(args.base).convert("RGB").resize((1280, 720), Image.LANCZOS)
    n = len(args.line)
    colors = spread(args.colors, n, str)
    sizes = spread(args.sizes, n, int)

    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd, td = ImageDraw.Draw(shadow), ImageDraw.Draw(text_layer)

    y = args.y
    for line, color, size in zip(args.line, colors, sizes):
        f = font(size)
        box = td.textbbox((0, 0), line, font=f)
        while box[2] - box[0] > args.max_width and size > 20:
            size -= 2
            f = font(size)
            box = td.textbbox((0, 0), line, font=f)
        w, h = box[2] - box[0], box[3] - box[1]
        x = args.x if args.align == "left" else (1280 - w) // 2
        sd.text((x + 6 - box[0], y + 8 - box[1]), line, font=f, fill=(0, 0, 0, 200))
        td.text((x - box[0], y - box[1]), line, font=f, fill=color, stroke_width=args.stroke, stroke_fill=(0, 0, 0, 230))
        y += h + args.gap

    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    out = Image.alpha_composite(img.convert("RGBA"), shadow)
    out = Image.alpha_composite(out, text_layer).convert("RGB")

    out_path = Path(args.out)
    out.save(out_path, quality=92)
    preview = out_path.with_name(out_path.stem + "-preview256" + out_path.suffix)
    out.resize((256, 144), Image.LANCZOS).save(preview, quality=90)
    print(f"Saved {out_path} and {preview}")


if __name__ == "__main__":
    main()
