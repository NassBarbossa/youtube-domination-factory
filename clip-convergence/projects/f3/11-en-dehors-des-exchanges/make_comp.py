"""Composition du clip 11 « En dehors des exchanges, avant les autres » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Le récap de la méthode IOC : acheter des coins en dehors des exchanges et avant qu'ils soient connus de tous. Tes euros, des SOL, et c'est un exemple pour expliquer comment la méthode fonctionne. Coupe de la référence à l'exemple Peanut (07:51–07:56).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 11, "« En dehors des exchanges, avant les autres »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 66
c.hook_html = 'EN DEHORS DES EXCHANGES,<br><b>AVANT LES AUTRES</b>'
c.fix = {("s1", "sexe."): "CEX.", ("s1", "sexe,"): "CEX,", ("s1", "sexe"): "CEX", ("s2", "sexe."): "CEX.", ("s2", "sexe,"): "CEX,", ("s2", "sexe"): "CEX", ("s3", "sexe."): "CEX.", ("s3", "sexe,"): "CEX,", ("s3", "sexe"): "CEX", ("s4", "sexe,"): "CEX,", ("s4", "sexe"): "CEX", ("s1", "OKEx"): "OKX", ("s2", "OKEx"): "OKX", ("s3", "sols,"): "SOL,", ("s3", "sols"): "SOL", ("s4", "sols"): "SOL", ("s2", "soldes."): "SOL.", ("s1", "fact"): "far", ("s1", "-well,"): "west,", ("s1", "Nas"): "Nass", ("s2", "Nas"): "Nass"}
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_dehors, t_connus, t_sol = find("s1", "dehors"), find("s1", "connus"), find("s2", "soldes")
c.hook_fade = t_dehors - 0.45
c.kwc("kw-dehors", "EN DEHORS<br>DES EXCHANGES", ORANGE, t_dehors - 0.1, t_connus - 0.9, size=76)
c.kwc("kw-connus", "AVANT QU'ILS SOIENT<br>CONNUS DE TOUS", CYAN, t_connus - 0.3, t_sol - 0.9, size=68)
c.kwc("kw-chute", "EUROS → SOL<br>→ TOKENS", WHITE, t_sol - 0.3, c.END_T + 0.45, size=80, anim="rise")
SFX = [("sfx-pop-1", "pop", t_dehors - 0.08, 0.3), ("sfx-pop-2", "pop", t_connus - 0.28, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3),
       ("sfx-pop-3", "pop", t_sol - 0.28, 0.28), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
