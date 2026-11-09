only = sys.argv[1:]
for cl in CLIPS:
    if only and cl["slug"] not in only:
        continue
    d = ROOT / "projects/ep03" / cl["slug"]
    if not d.exists():
        subprocess.run([sys.executable, str(ROOT / "scripts/new_clip.py"), str(MODEL), str(d)], check=True, capture_output=True)
    segs, t0 = [], float(cl["after"])
    for i, ((f, l), sp) in enumerate(zip(cl["segs"], cl["speakers"]), 1):
        a, b, txt = bounds(f, l, after=t0)
        segs.append({"id": f"s{i}", "speaker": sp, "a": a, "b": b, "text": txt}); t0 = b
    scene = {"rond": "à l'écran : deux ronds caméra de 210 px en bas (Nass à gauche, Sadek à droite)", "full": "fullcam : deux grandes fenêtres caméra côte à côte",
             "punk": "fin d'émission : la fenêtre de Nass montre son punk, Sadek seul à l'image"}[cl["layout"]]
    cut = {"short": f"{cl['n']} — {cl['title']} (Convergence EP.03)", "source": "~/Videos/NassRiviera/youtube/PJaScgDfiMk.mp4",
           "transcript": "~/youtube-domination-factory/context/transcripts/PJaScgDfiMk-words.json", "raw_to_source": 0,
           "scene": scene, **CROPS[cl["layout"]], "segments": segs}
    if cl["screen"]:
        cut["screen"] = {"crop": SCREENS[cl["screen_kind"]], "size": SIZE, "segments": list(cl["screen"])}
    (d / "cut.json").write_text(json.dumps(cut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    states = STATES["punk" if cl["layout"] == "punk" else "two"]
    (d / "make_comp.py").write_text(HEAD.format(n=cl["n"], title=cl["title"], doc=cl["doc"], hook=cl["hook"], hook_font=cl["hook_font"], states=states) + cl["body"] + TAIL, encoding="utf-8")
    tot = sum(s["b"] - s["a"] for s in segs)
    print(f"{cl['slug']:42s} {len(segs)} morceaux, {tot:5.1f} s  {segs[0]['a']:.1f}→{segs[-1]['b']:.1f}  " + " ".join(f"[{s['a']},{s['b']}]" for s in segs))
