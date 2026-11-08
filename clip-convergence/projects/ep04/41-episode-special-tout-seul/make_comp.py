"""Composition du clip 41 « Épisode spécial : tout seul » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

L'intro de l'épisode solo : à cause du changement d'heure, Nass et Sadek ne se sont pas accordé leurs violons. Épisode mené tranquillement, pas de débat : « je ne vais pas débattre tout seul, c'est un peu bizarre ».
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 41, "« Épisode spécial : tout seul »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 88
c.hook_html = 'ÉPISODE SPÉCIAL :<br><b>TOUT SEUL</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_heure, t_sadek, t_debat, t_debattre = find("s2", "changement"), find("s2", "Sadek"), find("s3", "débat"), find("s3", "débattre")
c.hook_fade = t_heure - 0.45
c.kwc("kw-heure", "LE CHANGEMENT<br>D'HEURE", GREY, t_heure - 0.1, t_sadek - 0.9, size=72)
c.kwc("kw-sadek", "SANS SADEK", INK, t_sadek - 0.2, E[1] - 0.3, size=88, top=1270)
c.kwc("kw-chute", "DÉBATTRE TOUT SEUL ?<br>UN PEU BIZARRE", GREEN, t_debat - 0.2, c.END_T + 0.45, size=66, anim="rise")  # « débat » et « débattre » à 1 s : une seule chute
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_heure - 0.08, 0.26), ("sfx-pop-2", "pop", t_sadek - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_debat - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
