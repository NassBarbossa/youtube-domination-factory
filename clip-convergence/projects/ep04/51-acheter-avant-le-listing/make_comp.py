"""Composition du clip 51 « Acheter avant le listing » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Ce qu'il partage dans la formation offerte : opérer des cryptos en dehors des échanges, achetées avant d'être listées sur un échange grand public (elles n'y arriveront sans doute jamais, trop petites). Analysées graphiquement comme l'or : pas un memecoin à 10 K, un truc en place depuis des semaines. Écran Axiom (memecoin) hors clip : caméra seule.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 51, "« Acheter avant le listing »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 88
c.hook_html = 'ACHETER AVANT<br><b>LE LISTING</b>'
ws = c.SEG["s2"]["words"]
for i, w in enumerate(ws[:-1]):
    if w["w"].strip() == "même" and ws[i + 1]["w"].strip().startswith("coin"):
        w["w"] = " meme"  # « même coin » → « meme coin », les deux « de la même façon » restent
c.moves = [(E[0], "SOLO_N+")]
t_dehors, t_avant, t_gold, t_meme, t_semaines = find("s1", "dehors"), find("s1", "avant"), find("s2", "gold"), find("s2", "meme"), find("s2", "semaines")
c.hook_fade = t_dehors - 0.45
c.kwc("kw-dehors", "EN DEHORS<br>DES ÉCHANGES", INK, t_dehors - 0.1, t_avant - 0.9, size=72)
c.kwc("kw-avant", "AVANT LE LISTING", GREEN, t_avant - 0.2, E[0] - 0.3, size=80, top=1270)
c.kwc("kw-gold", "ANALYSÉ COMME L'OR", GOLD_TXT, t_gold - 0.2, t_meme - 0.9, size=72, top=1270)
c.kwc("kw-meme", "PAS UN MEMECOIN<br>À 10 K", GREY, t_meme - 0.2, t_semaines - 0.9, size=66)
c.kwc("kw-chute", "EN PLACE DEPUIS<br>DES SEMAINES", GREEN, t_semaines - 0.3, c.END_T + 0.45, size=66, anim="rise")
SFX = [("sfx-pop-1", "pop", t_dehors - 0.08, 0.26), ("sfx-pop-2", "pop", t_avant - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3),
       ("sfx-pop-3", "pop", t_gold - 0.18, 0.26), ("sfx-pop-4", "pop", t_meme - 0.18, 0.26), ("sfx-pop-5", "pop", t_semaines - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
