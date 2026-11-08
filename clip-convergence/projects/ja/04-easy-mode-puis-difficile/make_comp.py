"""Composition du clip 4 « Easy mode, puis difficile » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

Revenu un peu trop tard : juillet 2026 easy mode, août encore easy, début septembre ça allait, puis « ça s'est compliqué, c'est redevenu un marché difficile ».
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 4, "« Easy mode, puis difficile »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'EASY MODE,<br><b>PUIS DIFFICILE</b>'
c.moves = [(E[0], "SOLO_N+")]
t_juillet, t_aout, t_sept, t_redevenu = find("s1", "juillet"), find("s1", "août"), find("s2", "septembre"), find("s2", "redevenu")
c.hook_fade = t_juillet - 0.45
c.kwc("kw-juillet", "JUILLET 2026 :<br>EASY MODE", CYAN, t_juillet - 0.1, t_aout - 0.9, size=72)
c.kwc("kw-aout", "AOÛT :<br>ENCORE EASY", CYAN, t_aout - 0.2, E[0] - 0.3, size=76)
c.kwc("kw-sept", "SEPTEMBRE :<br>ÇA SE COMPLIQUE", WHITE, t_sept - 0.2, t_redevenu - 0.9, size=66)
c.kwc("kw-chute", "UN MARCHÉ<br>DIFFICILE", ORANGE, t_redevenu - 0.2, c.END_T + 0.45, size=88, anim="rise")
SFX = [("sfx-pop-1", "pop", t_juillet - 0.08, 0.26), ("sfx-pop-2", "pop", t_aout - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3),
       ("sfx-pop-3", "pop", t_sept - 0.18, 0.26), ("sfx-pop-4", "pop", t_redevenu - 0.18, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
