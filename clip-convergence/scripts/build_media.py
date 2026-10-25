"""Médias d'un clip à partir de son cut.json (dans le dossier du projet HyperFrames).

- Coupes recalées sur le creux d'énergie du son le plus proche (jamais sur le seul minutage de la transcription).
- assets/audio/voice.wav : morceaux de voix mis bout à bout (fondus de 8 ms), normalisés à -14 LUFS / -1,5 dBTP.
- assets/video/<cam>_<seg>.mp4 : recadrage de chaque caméra, pré-agrandi (lanczos), 60 i/s, GOP 1 s, poignées de H s.
- timeline.json : temps de sortie de chaque morceau + mots horodatés (temps du clip).

Usage : python build_media.py <dossier_projet>
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

from common import FF, load_cut, pcm

SR = 48000
H = 0.30  # poignées vidéo (s)


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def quietest(src, t_lo, t_hi):
    """Instant (temps source) du creux d'énergie (fenêtres de 10 ms) dans [t_lo, t_hi]."""
    a = pcm(src, t_lo, t_hi - t_lo, sr=16000)
    w = 160
    n = len(a) // w
    if n == 0:
        return (t_lo + t_hi) / 2
    e = (a[: n * w].reshape(n, w) ** 2).mean(axis=1)
    i = int(np.argmin(e))
    return t_lo + (i + 0.5) * w / 16000


def main(proj):
    proj = Path(proj)
    cfg = load_cut(proj)
    src, off = cfg["source"], cfg["raw_to_source"]
    words_all = [w for seg in json.load(open(cfg["transcript"], encoding="utf-8")) for w in seg["words"]]
    (proj / "assets/audio").mkdir(parents=True, exist_ok=True)
    (proj / "assets/video").mkdir(parents=True, exist_ok=True)

    segs, chunks, t_out = [], [], 0.0
    for s in cfg["segments"]:
        a, b = s["a"] + off, s["b"] + off  # temps source
        # fenêtres serrées autour de la frontière : une fenêtre large saute par-dessus un mot court (« que », « bien »)
        a2 = quietest(src, a - 0.05, a + 0.05) - 0.01
        b2 = quietest(src, b - 0.03, b + 0.05) + 0.02
        audio = pcm(src, a2, b2 - a2, sr=SR, ch=2).copy()
        f = int(0.008 * SR)
        ramp = np.linspace(0, 1, f, dtype=np.float32)[:, None]
        audio[:f] *= ramp
        audio[-f:] *= ramp[::-1]
        chunks.append(audio)
        dur = len(audio) / SR
        # seulement les mots dits dans le morceau (pas le mot suivant, coupé au montage)
        ws = [w for w in words_all if s["a"] - 0.05 <= w["s"] < s["b"] - 0.02]
        for w in ws:
            w2 = dict(w)
            w2["s"] = round(t_out + (w["s"] + off - a2), 3)
            w2["e"] = round(min(t_out + (w["e"] + off - a2), t_out + dur), 3)
            w2["seg"] = s["id"]
            s.setdefault("words", []).append(w2)
        segs.append({**s, "src_a": round(a2, 3), "src_b": round(b2, 3), "out_start": round(t_out, 3),
                     "out_end": round(t_out + dur, 3), "dur": round(dur, 3)})
        t_out += dur
        print(f"{s['id']:5} {s['speaker']:6} source {a2:9.3f}-{b2:9.3f}  sortie {segs[-1]['out_start']:6.2f}-{segs[-1]['out_end']:6.2f}")

    # voix : bout à bout puis normalisation (2 passes loudnorm)
    raw = proj / "assets/audio/voice_raw.wav"
    data = np.concatenate(chunks)
    with wave.open(str(raw), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((np.clip(data, -1, 1) * 32767).astype("<i2").tobytes())
    meas = subprocess.run([FF, "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json",
                           "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(meas[meas.rindex("{"): meas.rindex("}") + 1])
    run([FF, "-v", "error", "-y", "-i", str(raw), "-af",
         f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
         f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
         "-ar", str(SR), str(proj / "assets/audio/voice.wav")])
    raw.unlink()

    # vidéos : chaque caméra, chaque morceau, avec poignées
    k = cfg.get("prescale", 1.45)
    for s in segs:
        for cam, (x, y, w, h) in cfg["crops"].items():
            out = proj / f"assets/video/{cam}_{s['id']}.mp4"
            W, Hh = int(round(w * k / 2) * 2), int(round(h * k / 2) * 2)
            run([FF, "-v", "error", "-y", "-ss", f"{s['src_a'] - H:.3f}", "-t", f"{s['dur'] + 2 * H:.3f}", "-i", src,
                 "-vf", f"crop={w}:{h}:{x}:{y},scale={W}:{Hh}:flags=lanczos,fps=60,format=yuv420p",
                 "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-g", "60", "-keyint_min", "60",
                 "-movflags", "+faststart", str(out)])
        print("vidéos", s["id"], "ok")

    tl = {"duration_voice": round(t_out, 3), "handle": H, "prescale": k, "segments": segs}
    (proj / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    print("voix", round(t_out, 2), "s ->", proj / "assets/audio/voice.wav")


if __name__ == "__main__":
    main(sys.argv[1])
