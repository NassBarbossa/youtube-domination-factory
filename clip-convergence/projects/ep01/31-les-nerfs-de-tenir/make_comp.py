"""Composition du clip 31 « Avoir les nerfs de tenir » (Convergence EP.01, Sadek), comp_lib v6.

Accroche « BEAUCOUP DE TRADERS / VONT LÂCHER », Sadek seul (SOLO_S), mots clés or : AVOIR LES NERFS DE TENIR, LES ACTIFS ONT UN
HISTORIQUE, NE PAS SE LAISSER DÉBORDER. Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GOLD_TXT, INK  # noqa: E402

c = Comp(HERE, 31, "« Avoir les nerfs de tenir »")
seams, find = c.seams, c.find
c.moves = [
    (seams[0], "SOLO_S"),    # s2 : « comme ce qui s'est passé sur le BTC »
    (seams[1], "SOLO_S+"),   # s3 : « il y a un moment où il faut avoir les nerfs »
    (seams[2], "SOLO_S"),    # s4 : « il ne faut pas se laisser déborder »
]
c.z_front = [(0, "sadek")]
c.hook_html = 'BEAUCOUP DE TRADERS<br><b class="or">VONT LÂCHER</b>'
c.hook_font = 88

t_nerfs = find("s3", "nerfs")
t_actifs = find("s3", "actifs")
t_laisser = find("s4", "laisser")

c.kw("kw-nerfs", "AVOIR LES NERFS<br>DE TENIR", f"left: 0; right: 0; top: 1200px; text-align: center; color: {GOLD_TXT}; font-size: 100px; line-height: 1;",
     t_nerfs - 0.3, t_actifs - 0.4)
c.kw("kw-actifs", "LES ACTIFS ONT<br>UN HISTORIQUE", f"left: 0; right: 0; top: 1200px; text-align: center; color: {INK}; font-size: 96px; line-height: 1;",
     t_actifs - 0.1, seams[2] - 0.3, anim="rise")
c.kw("kw-deborder", "NE PAS SE LAISSER<br>DÉBORDER", f"left: 0; right: 0; top: 1200px; text-align: center; color: {GOLD_TXT}; font-size: 92px; line-height: 1;",
     t_laisser - 0.5, c.END_T + 0.05)

c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.34),
    ("sfx-pop-1", "pop", t_nerfs - 0.28, 0.28),
    ("sfx-pop-2", "pop", t_actifs - 0.08, 0.26),
    ("sfx-whoosh-2", "whoosh", seams[2] - 0.22, 0.26),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"nerfs {t_nerfs} | actifs {t_actifs} | déborder {t_laisser}")
