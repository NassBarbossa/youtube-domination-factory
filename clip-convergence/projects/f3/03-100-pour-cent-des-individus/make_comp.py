"""Composition du clip 3 « 100 % doivent le faire, la Formule 1 non » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Ce que tout le monde doit faire (les deux premières vidéos) et ce qui n'est pas pour tout le monde (piloter la Formule 1). Puis : « tout le monde peut réussir si tu te donnes les moyens ». La slide « Gérer son capital + Investir intelligemment » sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 3, "« 100 % doivent le faire, la Formule 1 non »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 70
c.hook_html = '100 % DOIVENT LE FAIRE.<br><b>LA FORMULE 1, NON.</b>'
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N"), (E[2], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_f1, t_dur, t_moyens = find("s2", "Formule"), find("s3", "dur"), find("s4", "moyens")
c.kwc("kw-dur", "TROP DUR<br>POUR BEAUCOUP", MUTED, t_dur - 0.4, t_moyens - 0.9, size=76)
c.kwc("kw-chute", "SI TU TE DONNES<br>LES MOYENS", ORANGE, t_moyens - 0.3, c.END_T + 0.45, size=80, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3), ("sfx-pop-1", "pop", t_dur - 0.38, 0.26),
       ("sfx-whoosh-3", "whoosh-short", E[2] - 0.2, 0.26), ("sfx-pop-2", "pop", t_moyens - 0.28, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
