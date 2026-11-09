"""Composition du clip 70 « Une bonne situation financière ? » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Dernière question lue par Nass : faut-il une bonne situation financière pour commencer le trading ? Sadek : pour commencer, apprendre, ça n'a rien à voir ; pour l'exercer comme une activité, annexe ou principale, oui, il faut une bonne situation financière. Teaser court ; Sadek seul à l'image (Nass en punk), la voix de Nass sur la question.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 70, "« Une bonne situation financière ? »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("sadek", 760)
S["SOLO_E"] = solo_screen(860, 900, 506, cam="sadek")
c.hook_font = 76
c.hook_html = 'UNE BONNE SITUATION<br><b>FINANCIÈRE ?</b>'
c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+")]
t_rien, t_activite, t_oui = find("s2", "rien"), find("s3", "activité"), find("s3", "oui")
c.kwc("kw-rien", "POUR APPRENDRE :<br>RIEN À VOIR", GREY, t_rien - 0.2, t_activite - 0.9, size=70)
c.kwc("kw-activite", "EN FAIRE<br>UNE ACTIVITÉ ?", INK, t_activite - 0.2, t_oui - 0.9, size=72)
c.kwc("kw-chute", "OUI, IL FAUT UNE BONNE<br>SITUATION FINANCIÈRE", GREEN, t_oui - 0.3, c.END_T + 0.45, size=58, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_rien - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_activite - 0.18, 0.26), ("sfx-pop-3", "pop", t_oui - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
