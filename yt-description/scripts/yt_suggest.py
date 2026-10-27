#!/usr/bin/env python3
"""Collect real YouTube search suggestions (French, FR) for seed keywords: the "alphabet method" automated.

Usage:
  python3 yt-description/scripts/yt_suggest.py investir crypto DCA --alphabet --out suggestions.json

For each seed it queries YouTube's suggest endpoint for the seed alone, then seed + " " + each
letter a-z (with --alphabet). Prints suggestions sorted by how often they appear (a proxy for
demand) and saves everything as JSON.
"""
import argparse
import json
import string
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter

URL = "https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&hl=fr&gl=FR&q="


def suggest(q: str) -> list[str]:
    req = urllib.request.Request(URL + urllib.parse.quote(q), headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
    body = raw[raw.index("(") + 1 : raw.rindex(")")]
    data = json.loads(body)
    return [s[0] for s in data[1]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("seeds", nargs="+")
    ap.add_argument("--alphabet", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()

    results: dict[str, list[str]] = {}
    counter: Counter = Counter()
    for seed in a.seeds:
        queries = [seed] + ([f"{seed} {c}" for c in string.ascii_lowercase] if a.alphabet else [])
        for q in queries:
            try:
                s = suggest(q)
            except Exception as e:  # noqa: BLE001
                print(f"! {q}: {e}", file=sys.stderr)
                continue
            results[q] = s
            counter.update(s)
            time.sleep(0.15)
    if a.out:
        json.dump({"results": results, "ranked": counter.most_common()}, open(a.out, "w"), ensure_ascii=False, indent=1)
    for term, n in counter.most_common(80):
        print(f"{n:3d}  {term}")


if __name__ == "__main__":
    main()
