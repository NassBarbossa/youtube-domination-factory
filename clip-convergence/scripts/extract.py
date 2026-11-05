#!/usr/bin/env python3
"""Imprime le texte d'un transcript (format words.json) entre deux bornes.
Usage : extract.py <words.json> mm:ss-mm:ss [mm:ss-mm:ss ...]
Chaque plage est imprimée en un paragraphe (phrases qui chevauchent la plage)."""
import json, sys

def ts(s):
    m, sec = s.split(":"); return int(m) * 60 + float(sec)

segs = json.load(open(sys.argv[1]))
for rng in sys.argv[2:]:
    a, b = (ts(x) for x in rng.split("-"))
    txt = " ".join(s["text"] for s in segs if s["end"] > a and s["start"] < b)
    print(f"[{rng}] {txt}\n")
