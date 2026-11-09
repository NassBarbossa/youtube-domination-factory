"""Composition du clip 13 « Le syndrome de l'objet brillant » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

Si c'est si simple, pourquoi personne ne le fait ? Première raison : le syndrome de l'objet brillant. E-commerce, IA, trading… vous commencez, vous arrêtez, au lieu d'une seule chose : 100 € par mois.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 13, "« Le syndrome de l'objet brillant »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "LE SYNDROME DE<br><b>L'OBJET BRILLANT</b>"
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N"), (E[3], "SOLO_N+")]
t_ecom, t_ia, t_trad = find("s3", "-commerce"), find("s3", "IA"), find("s3", "trading")
t_seule, t_arretez = find("s4", "seule"), find("s5", "arrêtez")
ROW = "left: 0; right: 0; text-align: center; color: %s; font-size: 66px; line-height: 1;"
for i, (t, w, k) in enumerate([(t_ecom, "L'E-COMMERCE", "ecom"), (t_ia, "L'IA", "ia"), (t_trad, "LE TRADING", "trad")]):
    c.kw(f"kw-{k}", f'<span class="no">{w}</span>', (ROW % WHITE) + f" top: {1262 + i * 84}px;", t - 0.05, t_seule - 0.6)
c.ill_css = NO_CSS
c.kwc("kw-seule", "UNE SEULE CHOSE :<br>100 € TOUS LES MOIS", ORANGE, t_seule - 0.3, t_arretez - 1.4, size=72)
c.kwc("kw-chute", "VOUS COMMENCEZ,<br>VOUS ARRÊTEZ", RED_Y, t_arretez - 0.7, c.END_T + 0.45, size=80, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-1", "pop", t_ecom, 0.26), ("sfx-pop-2", "pop", t_ia, 0.26),
       ("sfx-pop-3", "pop", t_trad, 0.26), ("sfx-pop-4", "pop", t_seule - 0.28, 0.3), ("sfx-pop-5", "pop", t_arretez - 0.68, 0.28)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
