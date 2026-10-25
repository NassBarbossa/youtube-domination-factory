"""Préparation des Shorts recyclés : recalage de l'EP.03 sur le replay local, extraction audio, transcription mot à mot.

Pour chaque Short : fenêtre de source (avec marge) -> windows/<id>.wav (16 kHz mono) + windows/<id>.words.json
(mots horodatés en temps SOURCE, via faster-whisper medium, français).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

FF = r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
HERE = Path(__file__).resolve().parent
OUT = HERE / "windows"
OUT.mkdir(exist_ok=True)

V = Path(r"C:\Users\User\Videos")
SRC = {
    "riche": V / "NassRiviera/youtube/FVajDtrHsPU.mp4",
    "pourquoi": V / "NassRiviera/youtube/njfEJFd7hQ8.mp4",
    "ioc": V / "NassRiviera/Video 3.mp4",
    "ep01": V / "NassRiviera/cONVERGENCE #&.mp4",
    "ep03_yt": V / "NassRiviera/youtube/PJaScgDfiMk.mp4",
    "ep03": V / "Convergence ep03 - replay monte.mp4",
}


def mmss(s):
    m, sec = s.split(":")
    return int(m) * 60 + float(sec)


# id, source, début, fin (minutage YouTube ; marge de 2 s ajoutée plus bas)
SHORTS = [
    ("01-100-euros-10-ans", "riche", "02:07", "03:56"),
    ("02-pourquoi-personne", "riche", "07:34", "09:38"),
    ("03-exercice-40-30-15-15", "pourquoi", "05:10", "07:52"),
    ("04-exchange-choisit", "ioc", "03:03", "04:34"),
    ("05-ath-de-bullshit", "ep01", "11:34", "12:44"),
    ("06-bitcoin-ne-tombait-pas", "ep01", "14:30", "15:54"),
    ("07-sentiment-baissier", "ep01", "10:22", "11:02"),
    ("08a-or-en-solde", "ep03", "24:07", "24:48"),
    ("08b-or-investisseur", "ep03", "26:06", "27:13"),
    ("09-faire-de-l-oseille", "ep03", "29:26", "30:50"),
    ("10-altseason", "ep03", "32:14", "33:51"),
]
SR = 16000


def pcm(path, start, dur):
    cmd = [FF, "-v", "error", "-ss", f"{max(start, 0):.3f}", "-t", f"{dur:.3f}", "-i", str(path),
           "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)


def align_ep03(t_yt):
    """Temps dans le replay local qui correspond à t_yt (secondes) de la version YouTube."""
    probe = pcm(SRC["ep03_yt"], t_yt, 12.0)
    lo = max(t_yt - 330, 0)
    hay = pcm(SRC["ep03"], lo, 400.0)
    n = len(hay) + len(probe)
    nfft = 1 << (n - 1).bit_length()
    corr = np.fft.irfft(np.fft.rfft(hay, nfft) * np.conj(np.fft.rfft(probe, nfft)), nfft)[: len(hay) - len(probe)]
    # normalisation par l'énergie locale pour éviter les faux pics
    e = np.sqrt(np.convolve(hay ** 2, np.ones(len(probe)), "valid")[: len(corr)]) + 1e-9
    score = corr / e / (np.linalg.norm(probe) + 1e-9)
    i = int(np.argmax(score))
    return lo + i / SR, float(score[i])


def main():
    only = set(sys.argv[1:])
    from faster_whisper import WhisperModel
    # CPU : sur ce PC, CUDA se charge mais cublas64_12.dll manque au moment d'encoder
    model = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=8)
    device = "cpu"
    manifest = []
    for sid, src, a, b in SHORTS:
        if only and sid not in only:
            continue
        start, end = mmss(a) - 2, mmss(b) + 2
        path = SRC[src]
        info = {"id": sid, "source": str(path), "yt_start": start, "yt_end": end}
        if src == "ep03":
            local, score = align_ep03(start + 2)
            off = local - (start + 2)
            info.update({"offset_vs_youtube": round(off, 3), "align_score": round(score, 3)})
            start, end = start + off, end + off
        info.update({"start": round(start, 3), "end": round(end, 3)})
        wav = OUT / f"{sid}.wav"
        subprocess.run([FF, "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{end - start:.3f}", "-i", str(path),
                        "-vn", "-ac", "1", "-ar", str(SR), str(wav)], check=True)
        # audio décodé par ffmpeg (la lecture de fichier de faster-whisper casse avec la version de PyAV installée)
        audio = pcm(path, start, end - start)
        segs, _ = model.transcribe(audio, language="fr", word_timestamps=True, vad_filter=False,
                                   beam_size=5, condition_on_previous_text=False)
        words = [{"w": w.word.strip(), "s": round(start + w.start, 3), "e": round(start + w.end, 3), "p": round(w.probability, 3)}
                 for seg in segs for w in (seg.words or [])]
        (OUT / f"{sid}.words.json").write_text(json.dumps(words, ensure_ascii=False, indent=0), encoding="utf-8")
        info["n_words"] = len(words)
        manifest.append(info)
        print(json.dumps(info, ensure_ascii=False), flush=True)
    (OUT / "manifest.json").write_text(json.dumps({"device": device, "shorts": manifest}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
