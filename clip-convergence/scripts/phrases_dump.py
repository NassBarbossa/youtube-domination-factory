"""Lit une transcription (format transcribe.py) et l'écrit en texte lisible : une ligne par phrase « mm:ss  texte »,
regroupée par blocs de 30 s pour le repérage des passages. Usage : python phrases_dump.py <transcript.json> [sortie.txt]"""
import json, sys
t = json.load(open(sys.argv[1]))
out = []
for s in t:
    m, sec = divmod(int(s["start"]), 60)
    out.append(f"{m:02d}:{sec:02d}  {s['text']}")
txt = "\n".join(out)
if len(sys.argv) > 2:
    open(sys.argv[2], "w").write(txt)
else:
    print(txt)
