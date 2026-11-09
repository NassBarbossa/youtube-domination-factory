"""Composition du clip 67 « Le trading est un jeu de menteurs » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Sadek : comprendre le carnet d'ordres est intéressant, s'y reposer est suicidaire ; ceux qui vous vendent le carnet d'ordres, le footprint, mentent ; maîtrisez le maximum de concepts, utilisez-en le moins, cherchez la convergence et la confluence ; « le trading est un jeu de menteurs : trois menteurs qui disent la même chose sans se connaître, c'est la vérité, et vous êtes là pour la trouver ». C'est le passage du titre et de la miniature de l'épisode. Nass est remplacé par son punk à l'image : Sadek seul.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 67, "« Le trading est un jeu de menteurs »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("sadek", 760)
S["SOLO_E"] = solo_screen(860, 900, 506, cam="sadek")
c.hook_font = 76
c.hook_html = 'LE TRADING EST<br><b>UN JEU DE MENTEURS</b>'
c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+"), (E[2], "SOLO_S")]
t_suicidaire, t_mentent, t_maitrisez, t_moins, t_trois, t_verite = find("s1", "suicidaire"), find("s2", "mentent"), find("s3", "maîtrisez"), find("s3", "moins"), find("s4", "trois"), find("s4", "vérité.")
c.hook_fade = t_suicidaire - 0.45
c.kwc("kw-suicidaire", "S'Y REPOSER :<br>SUICIDAIRE", RED, t_suicidaire - 0.1, E[0] - 0.3, size=72)
c.kwc("kw-mentent", "DES GENS<br>QUI MENTENT", GREY, t_mentent - 0.2, t_maitrisez - 0.9, size=72)
c.kwc("kw-maitrisez", "MAÎTRISER<br>LE MAXIMUM", INK, t_maitrisez - 0.2, t_moins - 0.9, size=72)
c.kwc("kw-moins", "EN UTILISER<br>LE MOINS", INK, t_moins - 0.2, E[2] - 0.3, size=72)
c.kwc("kw-trois", "TROIS MENTEURS,<br>LA MÊME CHOSE", GREY, t_trois - 0.2, t_verite - 0.9, size=66)
c.kwc("kw-chute", "VOUS ÊTES LÀ POUR<br>TROUVER LA VÉRITÉ", GREEN, t_verite - 0.3, c.END_T + 0.45, size=62, anim="rise")
SFX = [("sfx-pop-1", "pop", t_suicidaire - 0.08, 0.3), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_mentent - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_maitrisez - 0.18, 0.26), ("sfx-pop-4", "pop", t_moins - 0.18, 0.26),
       ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-5", "pop", t_trois - 0.18, 0.26), ("sfx-pop-6", "pop", t_verite - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
