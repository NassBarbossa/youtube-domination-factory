"""Composition du clip 15 « Que la paix soit sur vous » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Normalement c'est la fin, peut-être des petits bonus. Un commentaire, un partage. « C'était Nass, j'espère vous revoir dans le groupe… et surtout que la paix soit sur vous. »
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 15, "« Que la paix soit sur vous »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "QUE LA PAIX<br><b>SOIT SUR VOUS</b>"
c.fix = {("s1", "sexe."): "CEX.", ("s1", "sexe,"): "CEX,", ("s1", "sexe"): "CEX", ("s2", "sexe."): "CEX.", ("s2", "sexe,"): "CEX,", ("s2", "sexe"): "CEX", ("s3", "sexe."): "CEX.", ("s3", "sexe,"): "CEX,", ("s3", "sexe"): "CEX", ("s4", "sexe,"): "CEX,", ("s4", "sexe"): "CEX", ("s1", "OKEx"): "OKX", ("s2", "OKEx"): "OKX", ("s3", "sols,"): "SOL,", ("s3", "sols"): "SOL", ("s4", "sols"): "SOL", ("s2", "soldes."): "SOL.", ("s1", "fact"): "far", ("s1", "-well,"): "west,", ("s1", "Nas"): "Nass", ("s2", "Nas"): "Nass"}
c.moves = [(E[0], "SOLO_N+")]
t_revoir, t_surtout = find("s2", "revoir"), find("s2", "surtout")
c.kwc("kw-revoir", "ON SE REVOIT<br>DANS LE GROUPE", WHITE, t_revoir - 0.3, t_surtout - 1.1, size=72)
c.kwc("kw-chute", "QUE LA PAIX<br>SOIT SUR VOUS", ORANGE, t_surtout - 0.2, c.END_T + 0.45, size=80, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_revoir - 0.28, 0.26), ("sfx-pop-3", "pop", t_surtout - 0.18, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
