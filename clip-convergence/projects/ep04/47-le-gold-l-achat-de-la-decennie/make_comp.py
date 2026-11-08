"""Composition du clip 47 « Le gold, l'achat de la décennie ? » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Sa position, pas un appel : « pour moi, je me positionne là », capture d'achat dans le replay ; 3 900 ou 4 000, pas de grande différence quand on vise un retour ; « pour moi, le gold, c'est l'achat de la décennie », l'achat de ce Q4 2026, « évidemment pas de conseil en investissement ». Coupe de « si tu n'achètes pas là… BTC 60K / 45K » (07:38–07:49). Son écran or sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 47, "« Le gold, l'achat de la décennie ? »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 72
c.hook_html = "LE GOLD :<br><b>L'ACHAT DE LA DÉCENNIE ?</b>"
c.fix = {("s2", "Realement,"): "Réellement,", ("s4", "q4"): "Q4"}
c.moves = [(E[0], "SOLO_N+"), (E[1], "SOLO_E"), (E[2], "SOLO_N+")]
c.screen_windows = [(E[1], E[2])]
t_mieux, t_achat, t_conseils = find("s2", "mieux"), find("s4", "achat"), find("s4", "conseils")
c.kwc("kw-3900", "3 900 OU 4 000 :<br>PAS DE GRANDE DIFFÉRENCE", GREY, t_mieux - 0.1, E[1] - 0.3, size=58)
c.kwc("kw-achat", "L'ACHAT DE CE Q4 2026", GOLD_TXT, t_achat - 0.2, t_conseils - 0.9, size=72, top=1270)
c.kwc("kw-chute", "PAS DE CONSEIL<br>EN INVESTISSEMENT", GREY, t_conseils - 0.3, c.END_T + 0.45, size=66, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_mieux - 0.08, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3),
       ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-2", "pop", t_achat - 0.18, 0.26), ("sfx-pop-3", "pop", t_conseils - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
