"""Composition du clip 1 « J'abandonne mon challenge » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

L'annonce : il abandonne son challenge, et il le dit avec la carte de la transparence (« je pense que je suis l'un des plus transparents »). J'ai tout partagé, c'est l'heure du bilan. Coupe de la phrase sur les wallets publics (00:16–00:23).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 1, "« J'abandonne mon challenge »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "J'ABANDONNE<br><b>MON CHALLENGE</b>"
c.fix = {("s1", "tous"): "to", ("s1", "en"): "100K", ("s1", "cas."): ""}
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N+")]
t_transp, t_partage, t_bilan = find("s2", "transparence"), find("s3", "partagé"), find("s4", "bilan")
c.kwc("kw-transp", "LA CARTE DE<br>LA TRANSPARENCE", CYAN, t_transp - 0.3, t_partage - 0.9, size=72)
c.kwc("kw-partage", "J'AI TOUT PARTAGÉ", WHITE, t_partage - 0.2, t_bilan - 0.9, size=76, top=1270)
c.kwc("kw-chute", "L'HEURE<br>DU BILAN", ORANGE, t_bilan - 0.3, c.END_T + 0.45, size=92, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_transp - 0.28, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_partage - 0.18, 0.26), ("sfx-pop-3", "pop", t_bilan - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
