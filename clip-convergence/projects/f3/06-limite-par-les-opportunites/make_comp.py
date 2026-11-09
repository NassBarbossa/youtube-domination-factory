"""Composition du clip 6 « Limité par le nombre d'opportunités » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Un échange centralisé expliqué : eux choisissent quelles cryptos sont disponibles, ils mettent acheteurs et vendeurs en relation. Donc tu es limité par le nombre d'opportunités.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 6, "« Limité par le nombre d'opportunités »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'SUR UN CEX,<br><b>TU ES LIMITÉ</b>'
c.fix = {("s1", "sexe."): "CEX.", ("s1", "sexe,"): "CEX,", ("s1", "sexe"): "CEX", ("s2", "sexe."): "CEX.", ("s2", "sexe,"): "CEX,", ("s2", "sexe"): "CEX", ("s3", "sexe."): "CEX.", ("s3", "sexe,"): "CEX,", ("s3", "sexe"): "CEX", ("s4", "sexe,"): "CEX,", ("s4", "sexe"): "CEX", ("s1", "OKEx"): "OKX", ("s2", "OKEx"): "OKX", ("s3", "sols,"): "SOL,", ("s3", "sols"): "SOL", ("s4", "sols"): "SOL", ("s2", "soldes."): "SOL.", ("s1", "fact"): "far", ("s1", "-well,"): "west,", ("s1", "Nas"): "Nass", ("s2", "Nas"): "Nass"}
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_dec, t_relation, t_limite = find("s1", "choisir"), find("s2", "relation"), find("s4", "limité")
c.hook_fade = t_dec - 0.45
c.kwc("kw-dec", "EUX CHOISISSENT<br>LES CRYPTOS", WHITE, t_dec - 0.1, t_relation - 0.9, size=72)
c.kwc("kw-rel", "ACHETEURS ↔ VENDEURS", CYAN, t_relation - 0.3, t_limite - 0.9, size=56, top=1270)
c.kwc("kw-chute", "LIMITÉ PAR LE NOMBRE<br>D'OPPORTUNITÉS", ORANGE, t_limite - 0.4, c.END_T + 0.45, size=64, anim="rise")
SFX = [("sfx-pop-1", "pop", t_dec - 0.08, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_relation - 0.28, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-whoosh-3", "whoosh-short", E[2] - 0.2, 0.26), ("sfx-pop-3", "pop", t_limite - 0.38, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
