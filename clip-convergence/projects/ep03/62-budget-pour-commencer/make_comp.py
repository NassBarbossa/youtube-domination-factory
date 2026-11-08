"""Composition du clip 62 « Budget pour commencer ? » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Question du chat : budget pour commencer ? Nass, en investissement : 10 à 20 % de votre salaire par mois ; Sadek, en trading : le moins possible, « vous allez perdre de l'argent au début », ça prend les bonnes habitudes, n'allez pas mettre tout votre capital. Fin avant le passage en fullcam (31:46,8) ; « ne faites pas cette erreur-là » (31:46,5) tombe sur le changement de mise en page, non repris.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 62, "« Budget pour commencer ? »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 84
c.hook_html = 'BUDGET<br><b>POUR COMMENCER ?</b>'
c.fix = {("s3", "mois"): "moins", ("s3", "?"): ""}
S["H"] = solo("nass", 760)   # fauteuil de Sadek vide au début du passage (il revient pendant la question)
t_pct, t_moins, t_perdre, t_moins2 = find("s1", "10"), find("s3", "mois"), find("s3", "perdre"), find("s4", "capital")
c.hook_fade = t_pct - 0.45
c.moves = [(t_pct - 0.3, "SOLO_N"), (E[0], "SOLO_N+"), (E[1] - 1.3, "N"), (E[1], "SOLO_S"), (E[2], "SOLO_S+")]   # retour aux deux caméras 1,3 s avant Sadek
c.kwc("kw-pct", "INVESTIR : 10 À 20 %<br>DU SALAIRE PAR MOIS", INK, t_pct - 0.2, E[0] - 0.3, size=60)
c.kwc("kw-moins", "TRADING :<br>LE MOINS POSSIBLE", INK, t_moins - 0.2, t_perdre - 0.35, size=66)
c.kwc("kw-perdre", "VOUS ALLEZ PERDRE<br>AU DÉBUT", RED, t_perdre - 0.15, E[2] - 0.3, size=66)
c.kwc("kw-chute", "PAS TOUT<br>VOTRE CAPITAL", GREEN, t_moins2 - 0.3, c.END_T + 0.45, size=76, anim="rise")
SFX = [("sfx-pop-1", "pop", t_pct - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3),
       ("sfx-pop-2", "pop", t_moins - 0.18, 0.26), ("sfx-pop-3", "pop", t_perdre - 0.18, 0.3), ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-4", "pop", t_moins2 - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
