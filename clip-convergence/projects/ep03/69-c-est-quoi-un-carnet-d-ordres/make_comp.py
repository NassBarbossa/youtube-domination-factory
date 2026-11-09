"""Composition du clip 69 « C'est quoi un carnet d'ordres ? » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Sadek réexplique : en trading, les ordres sont votre manière de passer vos commandes au marché ; exécution au marché, vous êtes pris au prix affiché ; un carnet d'ordres répertorie tous les ordres passés et montre les zones de réaction, là où beaucoup d'ordres attendent. Coupe de ses exemples de prix (39:39–39:59). Sadek seul (Nass en punk).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 69, "« C'est quoi un carnet d'ordres ? »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("sadek", 760)
S["SOLO_E"] = solo_screen(860, 900, 506, cam="sadek")
c.hook_font = 76
c.hook_html = "C'EST QUOI<br><b>UN CARNET D'ORDRES ?</b>"
c.moves = [(E[0], "SOLO_S+"), (E[1], "SOLO_S")]
t_commandes, t_execution, t_repertorier, t_zones = find("s1", "commandes"), find("s2", "exécution"), find("s3", "répertorier"), find("s3", "zones")
c.kwc("kw-commandes", "VOS COMMANDES<br>AU MARCHÉ", INK, t_commandes - 0.2, E[0] - 0.3, size=72)
c.kwc("kw-execution", "EXÉCUTION<br>AU MARCHÉ", GREY, t_execution - 0.2, E[1] - 0.3, size=72)
c.kwc("kw-repertorier", "TOUS LES ORDRES<br>PASSÉS AU MARCHÉ", INK, t_repertorier - 0.2, t_zones - 0.9, size=62)
c.kwc("kw-chute", "LES ZONES<br>DE RÉACTION", GREEN, t_zones - 0.3, c.END_T + 0.45, size=80, anim="rise")
SFX = [("sfx-pop-1", "pop", t_commandes - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_execution - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_repertorier - 0.18, 0.26), ("sfx-pop-4", "pop", t_zones - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
