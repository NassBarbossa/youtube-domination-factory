"""Génère les 15 projets de l'EP.03 (replay YouTube 720p, deux voix) : dossier, cut.json (bornes par cutfind), make_comp.py (thème convergence)."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "youtube-domination-factory/clip-convergence/scripts"))
import cutfind

ROOT = Path.home() / "youtube-domination-factory/clip-convergence"
TR = Path.home() / "youtube-domination-factory/context/transcripts/PJaScgDfiMk-words.json"
WORDS = cutfind.load(TR)
MODEL = ROOT / "projects/ep01/21-montrez-moi-des-preuves"
SCREENS = {"tv": [130, 105, 880, 495], "slide": [250, 110, 780, 439]}   # TradingView de Nass / slide « Vos questions » (sans les ronds)
SIZE = [900, 506]
CROPS = {"rond": dict(prescale=4.4, sharpen=True, crops={"nass": [30, 448, 210, 210], "sadek": [1040, 448, 210, 210]}),   # « à l'écran » : deux ronds de 210 px
         "full": dict(prescale=2.0, sharpen=True, crops={"nass": [36, 150, 464, 464], "sadek": [524, 100, 468, 468]}),    # fullcam : deux grandes fenêtres
         "punk": dict(prescale=2.0, sharpen=True, crops={"sadek": [524, 100, 468, 468]})}                                  # fin d'émission : Nass remplacé par son punk, Sadek seul

def bounds(first, last, after=0.0):
    i0 = next((i for i, w in enumerate(WORDS) if w[0] >= after - 0.05), 0)
    r1 = cutfind.find_seq(WORDS, first, i0); assert r1, ("début", first)
    r2 = cutfind.find_seq(WORDS, last, r1[0]); assert r2, ("fin", last, first)
    a, b = WORDS[r1[0]][0], WORDS[r2[1]][1]
    txt = " ".join(w[2] for w in WORDS[r1[0]:r2[1] + 1]).replace(" '", "'")
    return round(a, 2), round(b, 2), txt

HEAD = '''"""Composition du clip {n} « {title} » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

{doc}
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, {n}, "« {title} »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
{states}
c.hook_font = {hook_font}
c.hook_html = {hook!r}
'''
STATES = {"two": '''S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)''',
          "punk": '''S["H"] = solo("sadek", 760)
S["SOLO_E"] = solo_screen(860, 900, 506, cam="sadek")'''}
TAIL = '''
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
'''

CLIPS = []
def clip(slug, n, title, doc, hook, segs, body, after, hook_font=88, screen=(), screen_kind="tv", layout="rond", speakers=None):
    CLIPS.append(dict(slug=slug, n=n, title=title, doc=doc, hook=hook, segs=segs, body=body, after=after, hook_font=hook_font,
                      screen=screen, screen_kind=screen_kind, layout=layout, speakers=speakers or ["nass"] * len(segs)))
