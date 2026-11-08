"""Composition du clip 9 « La méthode IOC » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Pour réussir dans le far west, il l'a appelée IOC : investissement on-chain. Tu prends tes euros (600 € dans son exemple)…
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 9, "« La méthode IOC »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'LA MÉTHODE<br><b>IOC</b>'
c.fix = {("s1", "sexe."): "CEX.", ("s1", "sexe,"): "CEX,", ("s1", "sexe"): "CEX", ("s2", "sexe."): "CEX.", ("s2", "sexe,"): "CEX,", ("s2", "sexe"): "CEX", ("s3", "sexe."): "CEX.", ("s3", "sexe,"): "CEX,", ("s3", "sexe"): "CEX", ("s4", "sexe,"): "CEX,", ("s4", "sexe"): "CEX", ("s1", "OKEx"): "OKX", ("s2", "OKEx"): "OKX", ("s3", "sols,"): "SOL,", ("s3", "sols"): "SOL", ("s4", "sols"): "SOL", ("s2", "soldes."): "SOL.", ("s1", "fact"): "far", ("s1", "-well,"): "west,", ("s1", "Nas"): "Nass", ("s2", "Nas"): "Nass"}
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_ioc, t_onchain, t_euros = find("s2", "IOC"), find("s2", "investissement"), find("s4", "euros")
c.kwc("kw-ioc", "I · O · C", ORANGE, t_ioc - 0.2, t_onchain - 0.9, size=120, top=1256)
c.kwc("kw-onchain", "INVESTISSEMENT<br>ON-CHAIN", CYAN, t_onchain - 0.2, E[2] - 0.3, size=80)
c.kwc("kw-chute", "ÉTAPE 1 :<br>TES EUROS", WHITE, t_euros - 0.3, c.END_T + 0.45, size=84, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_ioc - 0.18, 0.32), ("sfx-pop-2", "pop", t_onchain - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-whoosh-3", "whoosh-short", E[2] - 0.2, 0.26), ("sfx-pop-3", "pop", t_euros - 0.28, 0.28)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
