"""Composition du clip 5 « Concentre-toi : le CEX » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Avant la méthode, une chose à comprendre. Les deux premières vidéos n'étaient pas techniques, là concentre-toi : tes premières cryptos, tu les achètes sur un CEX, un échange centralisé (OKX).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 5, "« Concentre-toi : le CEX »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'CONCENTRE-TOI :<br><b>LE CEX</b>'
c.fix = {("s1", "sexe."): "CEX.", ("s1", "sexe,"): "CEX,", ("s1", "sexe"): "CEX", ("s2", "sexe."): "CEX.", ("s2", "sexe,"): "CEX,", ("s2", "sexe"): "CEX", ("s3", "sexe."): "CEX.", ("s3", "sexe,"): "CEX,", ("s3", "sexe"): "CEX", ("s4", "sexe,"): "CEX,", ("s4", "sexe"): "CEX", ("s1", "OKEx"): "OKX", ("s2", "OKEx"): "OKX", ("s3", "sols,"): "SOL,", ("s3", "sols"): "SOL", ("s4", "sols"): "SOL", ("s2", "soldes."): "SOL.", ("s1", "fact"): "far", ("s1", "-well,"): "west,", ("s1", "Nas"): "Nass", ("s2", "Nas"): "Nass"}
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_conc, t_cex, t_centr = find("s2", "concentre"), find("s3", "sexe"), find("s4", "centralized")
c.kwc("kw-conc", "CONCENTRE-TOI.", ORANGE, t_conc - 0.2, t_cex - 0.9, size=92, top=1270)
c.kwc("kw-cex", "UN CEX", CYAN, t_cex - 0.2, t_centr - 0.9, size=110, top=1260)
c.kwc("kw-chute", "CEX =<br>ÉCHANGE CENTRALISÉ", WHITE, t_centr - 0.3, c.END_T + 0.45, size=64, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_conc - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_cex - 0.18, 0.3), ("sfx-whoosh-3", "whoosh-short", E[2] - 0.2, 0.26), ("sfx-pop-3", "pop", t_centr - 0.28, 0.28)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
