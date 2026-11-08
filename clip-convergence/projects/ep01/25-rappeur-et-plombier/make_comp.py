"""Composition du clip 25 « Un ancien rappeur et un ancien plombier » (Convergence EP.01), comp_lib v6.

Le disclaimer de l'émission, avec humour. Accroche « IL FAUDRAIT ÊTRE / SACRÉMENT BÊTE », Nass seul, la slide réelle du live
(« Il faudrait être sacrément bête de suivre bêtement les conseils… ») sous lui pendant qu'il la dit, puis ENCORE PLUS BÊTE et
la chute UN ANCIEN RAPPEUR (vert) / ET UN ANCIEN PLOMBIER (or). Le texte « pas un conseil en investissement » reste dans la
voix et la légende, jamais en mot clé (règle de Nass). Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GOLD_TXT, GREEN, INK, RED, solo_screen  # noqa: E402

c = Comp(HERE, 25, "« Un ancien rappeur et un ancien plombier »")
seams, find = c.seams, c.find
S = c.STATES
S["SOLO_E"] = solo_screen(860, 900, 496)   # la slide du live est plus large que le graphique (1180 × 650 → 900 × 496)

c.moves = [
    (seams[0], "SOLO_N"),    # s2 : « on partage juste ce qu'on fait »
    (seams[1], "SOLO_E"),    # s3 : la slide « Il faudrait être sacrément bête… »
    (seams[2], "SOLO_N+"),   # s4 : « ça serait quand même assez bête de votre part »
    (seams[3], "SOLO_N"),    # s5 : « et il faudrait encore plus bête… »
]
c.screen_windows = [(seams[1], seams[2])]
c.hook_html = 'IL FAUDRAIT ÊTRE<br><b class="red">SACRÉMENT BÊTE</b>'
c.hook_css = f"#hook .h1 b.red {{ color: {RED}; }}"

t_partage = find("s2", "partage")
t_bete = find("s4", "bête")
t_encore = find("s5", "encore")
t_un = find("s5", "un")                       # « nous sommes un ancien rappeur »
t_et = round(find("s5", "ancien", 1) - 0.3, 3)   # « et un ancien plombier »

c.kw("kw-partage", "ON PARTAGE JUSTE<br>CE QU'ON FAIT", f"left: 0; right: 0; top: 1206px; text-align: center; color: {INK}; font-size: 92px; line-height: 1.02;",
     t_partage, seams[1] - 0.3, anim="rise")
c.kw("kw-bete", "ASSEZ BÊTE<br>DE VOTRE PART", f"left: 0; right: 0; top: 1206px; text-align: center; color: {INK}; font-size: 96px; line-height: 1;",
     t_bete, seams[3] - 0.3)
c.kw("kw-encore", "ENCORE PLUS BÊTE", f"left: 0; right: 0; top: 1280px; text-align: center; color: {RED}; font-size: 104px;",
     t_encore, t_un - 0.3)
c.kw("kw-rappeur", "UN ANCIEN RAPPEUR", f"left: 0; right: 0; top: 1214px; text-align: center; color: {GREEN}; font-size: 92px;",
     t_un, c.END_T + 0.05)
c.kw("kw-plombier", "ET UN ANCIEN PLOMBIER", f"left: 0; right: 0; top: 1330px; text-align: center; color: {GOLD_TXT}; font-size: 84px;",
     t_et, c.END_T + 0.05)
c.cap_cuts = [("s5", t_un, 1e9)]
c.cap_end_before = [t_un]

c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.34),
    ("sfx-whoosh-2", "whoosh", seams[1] - 0.22, 0.30),      # la slide
    ("sfx-pop-1", "pop", t_encore + 0.02, 0.28),
    ("sfx-pop-2", "pop", t_un + 0.02, 0.30),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"slide {seams[1]}-{seams[2]} | encore {t_encore} | chute {t_un} / {t_et}")
