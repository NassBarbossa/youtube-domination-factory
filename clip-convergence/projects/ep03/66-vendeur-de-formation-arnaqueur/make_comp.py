"""Composition du clip 66 « Vendeur de formation = arnaqueur ? » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Nass : même en 2026, les formations sont mal vues en France, « vendeur de formation, forcément un arnaqueur », alors qu'il y a tout sur YouTube ; plein de gens ont des techniques différentes (lui l'investissement et le trading on-chain, Sadek les marchés traditionnels), le temps que vous cherchez, vous vous perdez ; si la personne est légitime, c'est plus simple de la suivre pour gagner du temps. Pas d'appel à acheter : il dit lui-même qu'il ne vend plus de formation.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 66, "« Vendeur de formation = arnaqueur ? »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 66
c.hook_html = 'VENDEUR DE FORMATION<br><b>= ARNAQUEUR ?</b>'
t_symptomatique, t_arnaqueur, t_moi, t_sadek, t_legitime, t_temps = find("s1", "symptomatique"), find("s2", "arnaqueur"), find("s3", "moi"), find("s3", "Sadek"), find("s4", "légitime"), find("s5", "temps")
c.hook_fade = t_symptomatique - 0.45
c.moves = [(t_symptomatique - 0.3, "SOLO_N"), (E[0], "SOLO_N+"), (E[1], "SOLO_N"), (E[2], "SOLO_N+"), (E[3], "SOLO_N")]
c.kwc("kw-symptomatique", "SYMPTOMATIQUE<br>DE LA FRANCE", GREY, t_symptomatique - 0.2, E[0] - 0.3, size=66)
c.kwc("kw-arnaqueur", "« FORCÉMENT<br>UN ARNAQUEUR »", RED, t_arnaqueur - 0.2, E[1] - 0.3, size=66)
c.kwc("kw-moi", "MOI : L'INVESTISSEMENT<br>ON-CHAIN", INK, t_moi - 0.2, t_sadek - 0.9, size=60)
c.kwc("kw-sadek", "SADEK : LES MARCHÉS<br>TRADITIONNELS", INK, t_sadek - 0.2, E[2] - 0.3, size=60)
c.kwc("kw-legitime", "UNE PERSONNE<br>LÉGITIME", GREY, t_legitime - 0.2, E[3] - 0.3, size=72)
c.kwc("kw-chute", "PLUS SIMPLE,<br>POUR GAGNER DU TEMPS", GREEN, t_temps - 0.3, c.END_T + 0.45, size=64, anim="rise")
SFX = [("sfx-pop-1", "pop", t_symptomatique - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_arnaqueur - 0.18, 0.3),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_moi - 0.18, 0.26), ("sfx-pop-4", "pop", t_sadek - 0.18, 0.26),
       ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-5", "pop", t_legitime - 0.18, 0.26), ("sfx-whoosh-4", "whoosh", E[3] - 0.22, 0.26), ("sfx-pop-6", "pop", t_temps - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
