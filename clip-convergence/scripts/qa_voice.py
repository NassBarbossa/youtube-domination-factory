"""Contrôle de la voix montée : re-transcription (faster-whisper, CPU) pour repérer un mot coupé ou en trop aux coutures.

Usage : python qa_voice.py <dossier_projet>
Pour chaque morceau : ce qu'on entend, puis le texte attendu (champ "text" du cut.json). Un mot coupé, avalé ou qui
dépasse du morceau suivant se voit à la première ou à la dernière place : ajuster a / b de 0,05 à 0,2 s et relancer.
"""
import json
import sys
from pathlib import Path

from faster_whisper import WhisperModel

from common import pcm

proj = Path(sys.argv[1])
tl = json.loads((proj / "timeline.json").read_text(encoding="utf-8"))
audio = pcm(proj / "assets/audio/voice.wav")
model = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=8)
segs, _ = model.transcribe(audio, language="fr", word_timestamps=True, beam_size=5, condition_on_previous_text=False)
words = [w for s in segs for w in (s.words or [])]
for seg in tl["segments"]:
    ws = [w.word.strip() for w in words if seg["out_start"] - 0.05 <= w.start < seg["out_end"]]
    print(f"{seg['id']:5} {seg['out_start']:6.2f}-{seg['out_end']:6.2f} | {' '.join(ws)}")
    print(f"      attendu : {seg['text']}")
