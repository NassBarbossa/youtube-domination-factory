"""Génère les logos Convergence en SVG vectoriel (texte converti en tracés)."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "logo")
font = TTFont(os.path.join(HERE, "InterTight-SemiBold.ttf"))
gs = font.getGlyphSet()
cmap = font.getBestCmap()
upm = font["head"].unitsPerEm
cap = font["OS/2"].sCapHeight or int(upm * 0.727)
TRACK = 0.32 * upm          # espacement des lettres (comme le board : 0.32em)

COLORS = {
    "clair":      dict(txt="#0B0E11", o="#C98A0B", v="#0F8A5F"),
    "sombre":     dict(txt="#F2EFE8", o="#E2A93B", v="#2BB37C"),
    "mono-noir":  dict(txt="#0B0E11", o="#0B0E11", v="#0B0E11"),
    "mono-blanc": dict(txt="#FFFFFF", o="#FFFFFF", v="#FFFFFF"),
}

def glyph_path(ch, x):
    name = cmap[ord(ch)]
    pen = SVGPathPen(gs)
    # y vers le bas en SVG : on retourne l'axe, la ligne de base est à y = cap
    tp = TransformPen(pen, (1, 0, 0, -1, x, cap))
    gs[name].draw(tp)
    return pen.getCommands(), gs[name].width

def build(variant):
    c = COLORS[variant]
    x = 0
    parts = []
    for ch in "CON":
        d, w = glyph_path(ch, x); parts.append(d); x += w + TRACK
    # Le V : deux traits qui se rejoignent sur la ligne de base
    sw = 0.165 * cap
    vw = 1.0 * cap
    x0, x1, xm = x + sw / 2, x + vw - sw / 2, x + vw / 2
    ytop, ybot = sw / 2, cap - sw / 2
    v_or = f'<line x1="{x0:.1f}" y1="{ytop:.1f}" x2="{xm:.1f}" y2="{ybot:.1f}" stroke="{c["o"]}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
    v_vert = f'<line x1="{x1:.1f}" y1="{ytop:.1f}" x2="{xm:.1f}" y2="{ybot:.1f}" stroke="{c["v"]}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
    x += vw + TRACK
    for i, ch in enumerate("ERGENCE"):
        d, w = glyph_path(ch, x); parts.append(d)
        x += w + (TRACK if i < 6 else 0)
    width = x
    pad = 0.06 * cap
    vb = f"{-pad:.0f} {-pad:.0f} {width + 2 * pad:.0f} {cap + 2 * pad:.0f}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
           f'<title>Convergence</title>'
           f'<path fill="{c["txt"]}" d="{" ".join(parts)}"/>{v_or}{v_vert}</svg>')
    path = os.path.join(OUT, f"convergence-logo-{variant}.svg")
    open(path, "w", encoding="utf-8").write(svg)
    return path, (width + 2 * pad) / (cap + 2 * pad)

def icon(name, rounded, size=1024):
    r = 0.22 * size if rounded == "carre" else size / 2
    shape = (f'<rect width="{size}" height="{size}" rx="{r:.0f}" fill="#0B0E11"/>' if rounded == "carre"
             else f'<circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="#0B0E11"/>')
    s = size / 64
    if rounded == "carre":
        a, b, m, sw = (17, 15), (47, 15), (32, 49), 6.5
    else:
        a, b, m, sw = (19, 17), (45, 17), (32, 47), 5.5
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{shape}'
           f'<line x1="{a[0]*s}" y1="{a[1]*s}" x2="{m[0]*s}" y2="{m[1]*s}" stroke="#E2A93B" stroke-width="{sw*s}" stroke-linecap="round"/>'
           f'<line x1="{b[0]*s}" y1="{b[1]*s}" x2="{m[0]*s}" y2="{m[1]*s}" stroke="#2BB37C" stroke-width="{sw*s}" stroke-linecap="round"/></svg>')
    path = os.path.join(OUT, f"convergence-icone-{name}.svg")
    open(path, "w", encoding="utf-8").write(svg)
    return path

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for v in COLORS:
        p, ratio = build(v)
        print(p, f"ratio {ratio:.2f}")
    print(icon("carre", "carre"))
    print(icon("rond", "rond"))
