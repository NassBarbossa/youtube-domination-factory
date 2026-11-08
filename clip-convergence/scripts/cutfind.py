"""Trouve les bornes a/b d'un passage dans une transcription mot à mot.

Usage : python3 cutfind.py <transcript.json> "premiers mots" "derniers mots" [--after mm:ss]
Affiche a (début du premier mot) et b (fin du dernier mot) en secondes, plus le texte entre les deux.
Les mots sont comparés en minuscules, sans ponctuation ; les premiers mots sont cherchés après --after (défaut 0).
"""
import json, re, sys
from pathlib import Path

def norm(w):
    return re.sub(r"[^\w']", "", w.lower().replace("’", "'"))

def load(p):
    d = json.loads(Path(p).expanduser().read_text(encoding="utf-8"))
    if isinstance(d, list) and d and isinstance(d[0], dict) and "words" in d[0]:
        words = [w for seg in d for w in seg["words"]]
    else:
        words = d["words"] if isinstance(d, dict) and "words" in d else d
    out = []
    for w in words:
        t = w.get("w") or w.get("word") or w.get("text")
        s, e = w.get("s", w.get("start")), w.get("e", w.get("end"))
        if t is None or s is None:
            continue
        out.append((float(s), float(e), t.strip()))
    return out

def mmss(x):
    m, s = divmod(int(x), 60); return f"{m}:{s:02d}"

def find_seq(words, seq, start_i=0):
    seq = [norm(x) for x in seq.split() if norm(x)]
    n = len(seq)
    # les tokens à apostrophe ("c" + "'est") : on compare sur la concaténation glissante
    toks = [norm(w[2]) for w in words]
    for i in range(start_i, len(toks)):
        j, k, buf = i, 0, ""
        ok = True
        while k < n and j < len(toks):
            buf += toks[j]
            if buf == seq[k]:
                k += 1; buf = ""
            elif not seq[k].startswith(buf):
                ok = False; break
            j += 1
        if ok and k == n:
            return i, j - 1
    return None

if __name__ == "__main__":
    args = sys.argv[1:]
    after = 0.0
    if "--after" in args:
        k = args.index("--after"); mm = args[k + 1]; args = args[:k] + args[k + 2:]
        m, s = mm.split(":"); after = int(m) * 60 + float(s)
    tr, first, last = args[0], args[1], args[2]
    words = load(tr)
    i0 = next((i for i, w in enumerate(words) if w[0] >= after), 0)
    r1 = find_seq(words, first, i0)
    if not r1:
        sys.exit(f"premiers mots introuvables : {first!r}")
    r2 = find_seq(words, last, r1[0])
    if not r2:
        sys.exit(f"derniers mots introuvables : {last!r}")
    a, b = words[r1[0]][0], words[r2[1]][1]
    txt = " ".join(w[2] for w in words[r1[0]:r2[1] + 1]).replace(" '", "'")
    print(f"{a:.2f} {b:.2f}  ({mmss(a)}–{mmss(b)}, {b - a:.1f} s)\n{txt}")
