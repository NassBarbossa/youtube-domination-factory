"""Composition du clip 11 « Le DCA, ce n'est pas un secret » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

La méthode s'appelle le DCA, Dollar Cost Averaging : investir tous les mois dans quelque chose qui prend de la valeur avec le temps. Nass refuse le marketing du « secret ».
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 11, "« Le DCA, ce n'est pas un secret »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 76
c.hook_html = "LE DCA,<br><b>CE N'EST PAS UN SECRET</b>"
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_dca, t_tous, t_secret, t_insulte = find("s1", "DCA"), find("s2", "tous"), find("s3", "marketing") - 0.2, find("s4", "insulte")
c.hook_fade = t_dca - 0.45
c.kwc("kw-dca", "DCA =<br>DOLLAR COST AVERAGING", ORANGE, t_dca - 0.1, E[0] - 0.3, size=64)
c.kwc("kw-tous", "TOUS LES MOIS", WHITE, t_tous - 0.2, t_secret - 0.9, size=92, top=1270)
c.kwc("kw-secret", '<span class="no">UN SECRET</span>', MUTED, t_secret - 0.2, t_insulte - 0.6, size=84, top=1270)
c.ill_css = NO_CSS
c.kwc("kw-chute", "CE SERAIT<br>UNE INSULTE", CYAN, t_insulte - 0.3, c.END_T + 0.45, size=88, anim="rise")
SFX = [("sfx-pop-1", "pop", t_dca - 0.08, 0.3), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_tous - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-3", "pop", t_secret - 0.18, 0.26), ("sfx-pop-4", "pop", t_insulte - 0.28, 0.28)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
