"""Lit une transcription entre deux instants (temps de la transcription) : repérer un passage, choisir les coupes.

Usage : python words.py <transcript.json> <début> <fin> [--phrases]
  instants en s, mm:ss ou h:mm:ss
  sans --phrases : chaque mot avec [début-fin], 6 par ligne (pour écrire a / b dans cut.json)
  --phrases      : une ligne par phrase avec son heure (pour lire et sélectionner)
"""
import argparse
import json

from common import seconds

ap = argparse.ArgumentParser()
ap.add_argument("transcript")
ap.add_argument("start")
ap.add_argument("end")
ap.add_argument("--phrases", action="store_true")
a = ap.parse_args()
lo, hi = seconds(a.start), seconds(a.end)
segs = json.load(open(a.transcript, encoding="utf-8"))
if a.phrases:
    for s in segs:
        if lo <= s["start"] <= hi:
            m, sec = divmod(s["start"], 60)
            print(f"{s['start']:8.2f}  {int(m):3d}:{sec:05.2f}  {s['text']}")
else:
    words = [w for s in segs for w in s["words"] if lo <= w["s"] <= hi]
    for i in range(0, len(words), 6):
        print("  ".join(f"{w['w'].strip()}[{w['s']:.2f}-{w['e']:.2f}]" for w in words[i:i + 6]))
