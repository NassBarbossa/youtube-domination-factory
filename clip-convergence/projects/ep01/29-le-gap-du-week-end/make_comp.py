"""Composition du clip 29 « Le gap du week-end » (Convergence EP.01, Sadek), comp_lib v6, variante écran seul.

Scène où Sadek partage son écran en plein cadre : aucune caméra exploitable, l'écran (le graphique de l'or avec le gap du
lundi) porte le clip, les mots clés au-dessus, les sous-titres dessous. Accroche « LE PLANCTON / DU LUNDI AU VENDREDI »
gardée tant qu'il le dit. Coupé avant « on a pris tous des shorts » (ses trades à lui, hors cadre).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GOLD_TXT, INK, RED, screen_only  # noqa: E402

c = Comp(HERE, 29, "« Le gap du week-end »")
seams, find = c.seams, c.find
SCR = screen_only(1000, 544)
c.STATES["H"] = SCR
c.screen_state = "H"
c.screen_windows = [(0, c.END_T)]
c.punch([seams[1], seams[3], seams[4]])
c.hook_html = 'LE PLANCTON<br><b class="or">DU LUNDI AU VENDREDI</b>'
c.hook_font = 84
c.hook_fade = find("s2", "samedi") - 0.35
c.skip_before = find("s2", "samedi") - 0.05
TOP = SCR["kw_top"]

t_samedi = find("s2", "samedi")
t_continuent = find("s3", "continuent")
t_gap = find("s4", "gap")
t_camoufler = find("s5", "camoufler")
t_vraiment = find("s6", "vraiment")

c.kw("kw-we", "SAMEDI-DIMANCHE :<br>LES INSTITUTIONS", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {INK}; font-size: 88px; line-height: 1;",
     t_samedi - 0.1, t_continuent - 0.4)
c.kw("kw-fluctue", "LE PRIX CONTINUE<br>À FLUCTUER", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {GOLD_TXT}; font-size: 88px; line-height: 1;",
     t_continuent - 0.1, seams[2] - 0.3, anim="rise")
c.kw("kw-gap", "UN GAP DE MARCHÉ", f"left: 0; right: 0; top: {TOP + 90}px; text-align: center; color: {INK}; font-size: 112px;",
     t_gap - 0.1, seams[3] - 0.3)
c.kw("kw-camoufler", "PLUS CAPABLES<br>DE CAMOUFLER", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {GOLD_TXT}; font-size: 92px; line-height: 1;",
     t_camoufler - 0.6, seams[4] - 0.3)
c.kw("kw-chute", "VENDEUR,<br>C'EST VRAIMENT VENDEUR", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {RED}; font-size: 84px; line-height: 1;",
     t_vraiment - 0.1, c.END_T + 0.05, anim="rise")
c.cap_cuts = [("s6", t_vraiment - 0.3, 1e9)]
c.cap_end_before = [t_vraiment - 0.2]

c.sfx = [
    ("sfx-pop-1", "pop", t_samedi - 0.08, 0.26),
    ("sfx-whoosh-1", "whoosh-short", seams[1] - 0.20, 0.30),
    ("sfx-pop-2", "pop", t_gap - 0.08, 0.30),
    ("sfx-whoosh-2", "whoosh", seams[3] - 0.22, 0.26),
    ("sfx-pop-3", "pop", t_vraiment - 0.08, 0.30),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"samedi {t_samedi} | gap {t_gap} | camoufler {t_camoufler} | chute {t_vraiment}")
