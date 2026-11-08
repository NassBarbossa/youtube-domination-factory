"""Composition du clip 26 « Changement de structure, c'est ultra simple » (Convergence EP.01, Sadek), comp_lib v6, écran seul.

Sadek montre sur son graphique : des plus hauts de plus en plus hauts (1, 2, 3), l'inversion, les faux market structure
shift, le vrai qui s'avère par le bas, le support qui pète, « chute des ténèbres ». L'écran porte le clip ; les mots clés
au-dessus comptent les hauts avec lui. Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GOLD, GOLD_TXT, INK, RED, screen_only  # noqa: E402

c = Comp(HERE, 26, "« Changement de structure, c'est ultra simple »")
seams, find = c.seams, c.find
SCR = screen_only(1000, 544, hook=240)
c.STATES["H"] = SCR
c.screen_state = "H"
c.screen_windows = [(0, c.END_T)]
c.punch([seams[2], seams[4], seams[6], seams[7]])
c.hook_html = 'CHANGEMENT<br>DE STRUCTURE :<br><b class="or">ULTRA SIMPLE</b>'
c.hook_font = 80
TOP = SCR["kw_top"]

t_hauts = find("s2", "hauts")
t_h1, t_h2, t_h3 = find("s3", "haut"), find("s3", "deuxième"), find("s3", "troisième")
t_inverse = find("s4", "inverse")
t_pas = find("s5", "pas")
t_par = find("s6", "par")
t_bas = find("s7", "bas")
t_support = find("s8", "support")
t_pete = find("s9", "pété")
t_chute = find("s9", "chute")

c.kw("kw-hauts", "DES PLUS HAUTS<br>DE PLUS EN PLUS HAUTS", f"left: 0; right: 0; top: {TOP + 60}px; text-align: center; color: {INK}; font-size: 76px; line-height: 1;",
     seams[0] + 0.15, seams[1] - 0.2)
for i, (t, lab) in enumerate([(t_h1, "1<sup>er</sup> HAUT"), (t_h2, "2<sup>e</sup> HAUT"), (t_h3, "3<sup>e</sup> HAUT")]):
    c.kw(f"kw-h{i + 1}", lab, f"left: {90 + i * 310}px; width: 280px; top: {TOP + 100}px; text-align: center; color: {GOLD_TXT}; font-size: 64px; "
         f"padding: 18px 0; border: 8px solid {GOLD}; border-radius: 24px;", t - 0.05, seams[2] - 0.3)
c.kw("kw-inverse", "ON INVERSE<br>LA TENDANCE", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {GOLD_TXT}; font-size: 92px; line-height: 1;",
     t_inverse - 0.1, seams[3] - 0.3)
c.kw("kw-pas", "PAS AVÉRÉS", f"left: 0; right: 0; top: {TOP + 90}px; text-align: center; color: {RED}; font-size: 120px;",
     t_pas - 0.05, seams[4] - 0.3)
c.kw("kw-par", "S'AVÈRE<br>PAR LE BAS", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {GOLD_TXT}; font-size: 96px; line-height: 1;",
     find("s6", "market") - 0.05, seams[5] - 0.3)
c.kw("kw-bas", "DES BAS<br>DE PLUS EN PLUS BAS", f"left: 0; right: 0; top: {TOP + 60}px; text-align: center; color: {INK}; font-size: 80px; line-height: 1;",
     seams[5] + 0.1, seams[6] - 0.3, anim="rise")
c.kw("kw-support", "UN SUPPORT", f"left: 0; right: 0; top: {TOP + 90}px; text-align: center; color: {INK}; font-size: 120px;",
     t_support - 0.1, t_pete - 0.05)
c.kw("kw-pete", "VOTRE SUPPORT<br>A PÉTÉ", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {RED}; font-size: 96px; line-height: 1;",
     t_pete + 0.2, t_chute - 0.1, anim="fade", attrs="data-layout-allow-overlap")
c.kw("kw-chute", "CHUTE<br>DES TÉNÈBRES", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {RED}; font-size: 100px; line-height: 1;",
     t_chute - 0.15, c.END_T + 0.45, attrs="data-layout-allow-overlap")
c.cap_cuts = [("s9", t_chute - 0.05, 1e9)]
c.cap_end_before = [t_chute]
c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.30),
    ("sfx-pop-1", "pop", t_h1 - 0.03, 0.24), ("sfx-pop-2", "pop", t_h2 - 0.03, 0.24), ("sfx-pop-3", "pop", t_h3 - 0.03, 0.24),
    ("sfx-pop-4", "pop", t_pas - 0.03, 0.30),
    ("sfx-whoosh-2", "whoosh", seams[6] - 0.22, 0.26),
    ("sfx-pop-5", "pop", t_chute + 0.02, 0.32),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"hauts {t_h1} {t_h2} {t_h3} | pas {t_pas} | par {t_par} | support {t_support} pété {t_pete} | chute {t_chute}")
