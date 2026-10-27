"""Miniature « face à face » : deux portraits chroma, fond PIL sombre à deux lueurs, texte géant en bas, tags OR / BITCOIN."""
import os, sys
sys.path.insert(0, "yt-miniature/scripts")
from compose_podcast import chroma, FONTS
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
import numpy as np

W, H, S = 1280, 720, 2
left, right, out, line = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
LF = float(sys.argv[5]) if len(sys.argv) > 5 else 0.35  # taille du visage gauche (fraction du cadre)
RF = float(sys.argv[6]) if len(sys.argv) > 6 else 0.35
LX = float(sys.argv[7]) if len(sys.argv) > 7 else 0.23
RX = float(sys.argv[8]) if len(sys.argv) > 8 else 0.77
GOLD, ORANGE, CREAM, INK = (214, 160, 40), (255, 107, 53), (245, 242, 235), (10, 10, 12)

canvas = Image.new("RGBA", (W * S, H * S), (12, 12, 14, 255))
glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
gd.ellipse([-200 * S, 80 * S, 560 * S, 760 * S], fill=(190, 130, 30, 120))
gd.ellipse([720 * S, 80 * S, 1480 * S, 760 * S], fill=(230, 90, 40, 110))
canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120 * S)))

def place(path, xc, face_frac, flip=False):
    p = chroma(Image.open(path));
    if flip: p = p.transpose(Image.FLIP_LEFT_RIGHT)
    p = p.crop(p.getbbox())
    h = int(H * S * face_frac / 0.30)  # visage ≈ 30 % de la hauteur du portrait
    p = p.resize((int(p.width * h / p.height), h), Image.LANCZOS)
    x = int(xc * W * S - p.width / 2); y = H * S - h + int(0.02 * H * S)
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 200), (x, y), p.split()[3])
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(40 * S)))
    canvas.alpha_composite(p, (x, y))

# la personne qui mène (gauche, plus grande) est posée en dernier, donc devant
place(right, RX, RF)
place(left, LX, LF)

# voile sombre en bas pour le texte
veil = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); vd = ImageDraw.Draw(veil)
for i in range(240 * S):
    a = int(210 * (i / (240 * S)) ** 1.6)
    vd.line([(0, H * S - 240 * S + i), (W * S, H * S - 240 * S + i)], fill=(5, 5, 8, a))
canvas.alpha_composite(veil)

d = ImageDraw.Draw(canvas)
f_tag = ImageFont.truetype(str(FONTS / "IBMPlexMono-SemiBold.ttf"), 30 * S)
TAGS = os.environ.get("VS_TAGS", "1") == "1"  # VS_TAGS=0 : pas d'étiquettes OR / BITCOIN
lines = line.split("|")
cx = W * S // 2; maxw = 0.92 * W * S
def fit(txt, size):
    while True:
        f = ImageFont.truetype(str(FONTS / "InterTight-var.ttf"), size * S); f.set_variation_by_axes([900])
        if d.textlength(txt, font=f) <= maxw or size <= 60:
            return f, size
        size -= 4
sizes = [fit(ln, 136)[1] for ln in lines]; size = min(sizes)
f_big, size = fit(max(lines, key=len), size)
lh = int(size * 1.02) * S
ty = H * S - 150 * S - lh * (len(lines) - 1) // 2
for ln in lines:
    d.text((cx + 5 * S, ty + 7 * S), ln, font=f_big, fill=(0, 0, 0, 160), anchor="mm")
    d.text((cx, ty), ln, font=f_big, fill=CREAM, anchor="mm", stroke_width=6 * S, stroke_fill=INK)
    ty += lh
if TAGS:
  for text, x, col in (("OR", 0.22, GOLD), ("BITCOIN", 0.78, ORANGE)):
    tw = d.textlength(text, font=f_tag); xx = x * W * S
    d.rounded_rectangle([xx - tw / 2 - 18 * S, 420 * S, xx + tw / 2 + 18 * S, 472 * S], radius=6 * S, fill=col)
    d.text((xx, 446 * S), text, font=f_tag, fill=INK, anchor="mm")
d.text((int(0.52 * W * S), 56 * S), "CONVERGENCE · ÉP. 01", font=f_tag, fill=(150, 150, 150), anchor="mm")
final = canvas.convert("RGB").resize((W, H), Image.LANCZOS)
final = ImageEnhance.Contrast(final).enhance(1.05)
final.save(out, quality=94); final.resize((256, 144), Image.LANCZOS).save(out.replace(".jpg", "-preview256.jpg"), quality=85)
print(out)
