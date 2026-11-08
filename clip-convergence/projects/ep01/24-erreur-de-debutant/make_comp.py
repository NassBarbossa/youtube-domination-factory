"""Composition du clip 24 « Une erreur classique de débutant » (Convergence EP.01, Sadek), comp_lib v6.

Sadek raconte sa perte de la semaine. Accroche « UNE ERREUR CLASSIQUE / DE DÉBUTANT », Sadek seul tout du long ; les montants
qu'il dit (− 11 000 $, − 3 000 $) s'affichent quand il les dit : ce sont ses chiffres, pas des données de marché. Coupé pour le
cadre : « sur un setup bitcoin en vente », « j'ai triplé mes lots », « sur 800 pips » (vocabulaire CFD) ; la leçon reste
entière. Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GOLD_TXT, GREY, INK, RED  # noqa: E402

c = Comp(HERE, 24, "« Une erreur classique de débutant »")
seams, find = c.seams, c.find
c.moves = [
    (seams[0], "SOLO_S"),    # s2 : « J'ai perdu 11 000 dollars »
    (seams[1], "SOLO_S+"),   # s3 : « en forçant un setup »
    (seams[2], "SOLO_S"),    # s4 : « une erreur classique de débutant »
    (seams[3], "SOLO_S+"),   # s5 : « triplé mon exposition »
    (seams[4], "SOLO_S"),    # s6 : « je perdais 3 000 dollars »
    (seams[5], "SOLO_S+"),   # s7 : « moins 11 000 »
    (seams[6], "SOLO_S"),    # s8 : « des anciens rappeurs et des anciens plombiers »
]
c.z_front = [(0, "sadek")]
c.hook_html = 'UNE ERREUR CLASSIQUE<br><b class="or">DE DÉBUTANT</b>'
c.hook_font = 88

t_11k = find("s2", "11")
t_forcant = find("s3", "forçant")
t_accepte = find("s3", "accepté")
t_erreur = find("s4", "erreur")
t_triple = find("s5", "triplé")
t_3k = find("s6", "3")
t_11k2 = find("s7", "11")
t_on = find("s8", "on")

c.kw("kw-11k", "− 11 000 $", f"left: 0; right: 0; top: 1200px; text-align: center; color: {RED}; font-size: 136px;", t_11k, seams[1] - 0.3)
c.kw("kw-forcant", "EN FORÇANT<br>UN SETUP", f"left: 0; right: 0; top: 1200px; text-align: center; color: {INK}; font-size: 96px; line-height: 1;",
     t_forcant, t_accepte - 0.4)
c.kw("kw-accepte", "PAS ACCEPTÉ<br>D'ÊTRE EN PERTE", f"left: 0; right: 0; top: 1200px; text-align: center; color: {GOLD_TXT}; font-size: 92px; line-height: 1;",
     t_accepte - 0.1, seams[2] - 0.3, anim="rise")
c.kw("kw-erreur", "ERREUR CLASSIQUE<br>DE DÉBUTANT", f"left: 0; right: 0; top: 1200px; text-align: center; color: {RED}; font-size: 96px; line-height: 1;",
     t_erreur, seams[3] - 0.3)
c.kw("kw-triple", "EXPOSITION × 3", f"left: 0; right: 0; top: 1270px; text-align: center; color: {GOLD_TXT}; font-size: 112px;",
     t_triple, seams[4] - 0.3)
c.kw("kw-3k", "− 3 000 $", f"left: 0; right: 0; top: 1190px; text-align: center; color: {GREY}; font-size: 96px;", t_3k, t_on - 0.12)
c.kw("kw-11k2", "− 11 000 $", f"left: 0; right: 0; top: 1300px; text-align: center; color: {RED}; font-size: 136px;", t_11k2, t_on - 0.12)
c.kw("kw-chute", "DES ANCIENS RAPPEURS<br>ET DES ANCIENS PLOMBIERS",
     f"left: 0; right: 0; top: 1220px; text-align: center; color: {GOLD_TXT}; font-size: 76px; line-height: 1.05;", t_on, c.END_T + 0.05, anim="rise", attrs="data-layout-allow-overlap")
c.cap_cuts = [("s8", t_on, 1e9)]
c.cap_end_before = [t_on]

c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.34),
    ("sfx-pop-1", "pop", t_11k + 0.02, 0.30),
    ("sfx-pop-2", "pop", t_erreur + 0.02, 0.28),
    ("sfx-pop-3", "pop", t_11k2 + 0.02, 0.30),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"11k {t_11k} | erreur {t_erreur} | ×3 {t_triple} | 3k {t_3k} 11k {t_11k2} | chute {t_on}")
