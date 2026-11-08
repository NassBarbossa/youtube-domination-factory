"""Composition du clip 63 « C'est quoi l'altseason ? » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

« Quand aura lieu l'altseason ? » : le commentaire qui trigger Nass depuis des années, parce que c'est un problème de définition : un altcoin, c'est tout coin alternatif à Bitcoin. Aujourd'hui il y a une inflation des cryptos (tout le monde peut créer la sienne en une seconde), la liquidité ne peut plus aller partout, elle se concentre dans quelques actifs. Coupes : memecoins à 5 000 de market cap (32:47–32:57, signalé), tokens nommés et « pas comme 2021 » (32:57–33:34).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 63, "« C'est quoi l'altseason ? »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 92
c.hook_html = "C'EST QUOI<br><b>L'ALTSEASON ?</b>"
c.fix = {("s1", "alt"): "altseason", ("s1", "season"): ""}
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]   # monologue de Nass : états solo, Sadek écoute hors champ
t_definition, t_alternative, t_inflation, t_liquidite, t_concentree = find("s2", "définition"), find("s3", "alternative"), find("s4", "inflation"), find("s4", "liquidité"), find("s4", "concentrée")
c.kwc("kw-definition", "UN PROBLÈME<br>DE DÉFINITION", INK, t_definition - 0.2, t_definition + 2.5, size=72)
c.kwc("kw-alt", "ALTCOIN = TOUT CE QUI<br>N'EST PAS BITCOIN", INK, t_alternative - 0.2, E[2] - 0.3, size=60)
c.kwc("kw-inflation", "UNE INFLATION<br>DES CRYPTOS", GREY, t_inflation - 0.2, t_liquidite - 0.9, size=72)
c.kwc("kw-liquidite", "LA LIQUIDITÉ NE PEUT<br>PLUS ALLER PARTOUT", GREY, t_liquidite - 0.2, t_concentree - 0.9, size=60)
c.kwc("kw-chute", "CONCENTRÉE DANS<br>QUELQUES ACTIFS", GREEN, t_concentree - 0.3, c.END_T + 0.45, size=70, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_definition - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_alternative - 0.18, 0.26), ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-3", "pop", t_inflation - 0.18, 0.26),
       ("sfx-pop-4", "pop", t_liquidite - 0.18, 0.26), ("sfx-pop-5", "pop", t_concentree - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
