"""Composition du clip 2 « Le verdict : du surplace » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

Le verdict du challenge, sans fard : ça ne s'est pas passé comme prévu, parti d'environ 10 300 $, + 1,2 % en 20 jours. « C'est du surplace. » Les chiffres sont les siens.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 2, "« Le verdict : du surplace »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'LE VERDICT ?<br><b>DU SURPLACE.</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_prevu, t_pire, t_12 = find("s1", "prévu."), find("s1", "pire"), find("s3", "1")
c.hook_fade = t_prevu - 0.45
c.kwc("kw-prevu", "PAS COMME PRÉVU", WHITE, t_prevu - 0.1, t_pire - 0.9, size=76, top=1270)
c.kwc("kw-pire", "PIRE QUE ÇA ?", MUTED, t_pire - 0.2, E[1] - 0.3, size=84, top=1270)
c.kwc("kw-chute", "+ 1,2 % EN 20 JOURS :<br>DU SURPLACE", ORANGE, t_12 - 0.3, c.END_T + 0.45, size=64, anim="rise")
SFX = [("sfx-pop-1", "pop", t_prevu - 0.08, 0.26), ("sfx-pop-2", "pop", t_pire - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_12 - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
