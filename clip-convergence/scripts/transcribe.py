"""Transcription mot à mot d'une source (ou d'une fenêtre) avec faster-whisper, au format lu par les autres scripts.

Usage : python transcribe.py <source> <sortie.json> [--start S] [--end E] [--model medium] [--device cpu]
Sortie : [{start, end, text, words: [{w, s, e}]}] en temps de la source, réécrite au fil de l'eau (un arrêt garde
ce qui est fait). Une émission entière prend longtemps sur CPU : lancer en arrière-plan, une fois par épisode.
"""
import argparse
import json
import os
from pathlib import Path

from common import pcm, seconds

ap = argparse.ArgumentParser()
ap.add_argument("source")
ap.add_argument("out")
ap.add_argument("--start", default="0")
ap.add_argument("--end")
ap.add_argument("--model", default="medium")
ap.add_argument("--device", default="cpu")
a = ap.parse_args()
t0 = seconds(a.start)
dur = seconds(a.end) - t0 if a.end else None

from faster_whisper import WhisperModel  # noqa: E402

# audio décodé par ffmpeg et passé en numpy : le décodage interne de faster-whisper (PyAV) plante sur certains PC
audio = pcm(a.source, t0, dur)
# CPU int8 : sur le PC Windows, CUDA se charge mais cublas64_12.dll manque au moment d'encoder
model = WhisperModel(a.model, device=a.device, compute_type="int8" if a.device == "cpu" else "float16",
                     cpu_threads=os.cpu_count() or 4)
segs, _ = model.transcribe(audio, language="fr", word_timestamps=True, beam_size=5, condition_on_previous_text=False)
out, total, out_path = [], len(audio) / 16000, Path(a.out)
for i, s in enumerate(segs):
    out.append({"start": round(s.start + t0, 2), "end": round(s.end + t0, 2), "text": s.text.strip(),
                "words": [{"w": w.word, "s": round(w.start + t0, 2), "e": round(w.end + t0, 2)} for w in (s.words or [])]})
    if i % 40 == 0:
        out_path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
        print(f"{s.end:8.1f} / {total:.0f} s", flush=True)
out_path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
print(f"{len(out)} phrases -> {out_path}")
