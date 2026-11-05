# À faire sur le PC Windows — réel 35 « La meilleure des positions » (Convergence EP.01)

Message pour la session Claude du PC Windows (`C:\Users\User\youtube-domination-factory`). Écrit sur le Mac le 2026-11-05.

## Où on en est

- La **v1** de ce réel a été construite et rendue sur le Mac le 2026-10-28, **depuis le téléchargement YouTube 1080p 30 i/s**
  (`ZjNa7wxwFkM`), parce que le brut OBS de l'EP.01 est sur ce PC. Le rendu n'est pas versionné (`clip-convergence/exports/`
  est ignoré) ; Nass l'a reçu dans la conversation du Mac.
- Tout le projet est dans ce dossier : `cut.json` (6 morceaux, temps YouTube), `make_comp.py` (variante « écran + médaillons »
  de la DA), `SPEC.md`, `REVIEW.md`, `compositions/`, `index.html`, `timeline.json`. Les médias (`assets/video`, `assets/audio`,
  `assets/sfx/*-n.wav`) se régénèrent avec les scripts.
- Lire d'abord : `clip-convergence/SKILL.md`, `clip-convergence/references/deux-droites.md` (section « Variante écran +
  médaillons »), `clip-convergence/references/revue-et-pieges.md`, puis `SPEC.md` et `REVIEW.md` ici.

## Ce que Nass doit encore trancher (ne pas décider à sa place)

1. La variante « écran + médaillons » (caméras rondes de la scène « À L'ÉCRAN ») : validée ou non.
2. La coupe de « je suis plus à la hausse sur les cryptos » (YouTube 1183,42–1186,16, avis directionnel). S'il la veut,
   ajouter un morceau entre `s2` et `s3` dans `cut.json`.
3. Le morceau `s1` : la re-transcription de la voix montée entend « pas des investisseurs ». À son oreille.

## Refaire le réel depuis le brut OBS (objectif de cette session)

1. **Le brut** : `C:\Users\User\Videos\2026-10-05 14-36-21.mp4` (1920 × 1080, 60 i/s, 44 min ; retrouvé le 2026-10-25,
   voir `clip-convergence/projects/ep01/EPISODE.md`). Vérifier avec `ffprobe`.
2. **Le décalage** au passage (jamais réutiliser une valeur mesurée ailleurs) : il faut le fichier YouTube comme référence.
   S'il n'est pas sur ce PC : `yt-dlp -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b" -o "%(id)s.%(ext)s" https://youtu.be/ZjNa7wxwFkM`
   dans `%USERPROFILE%\Videos\NassRiviera\youtube\`. Puis :
   `python clip-convergence/scripts/offset.py "<YouTube>" "<brut>" 1180 1200 --guess 68.9` (score attendu ≥ 0,9 ; valeur
   attendue ≈ +68,9 s : brut = YouTube + 68,9).
3. **`cut.json`** : changer seulement `source` (le brut) et `raw_to_source` (la valeur mesurée, positive). `transcript` reste
   `~/youtube-domination-factory/context/transcripts/ZjNa7wxwFkM-words.json` (sur Windows, `~` = `C:\Users\User`, donc le
   chemin tombe juste). Les morceaux `a` / `b` restent en temps YouTube.
4. **Les zones** : même mise en page sur le brut et sur YouTube. Vérifier sur une image du brut (`ffmpeg -ss 1253 -i "<brut>"
   -frames:v 1 zone.png`) que les ronds sont au même endroit : Nass centre ≈ (200, 836) rayon 167, Sadek ≈ (1716, 832)
   rayon 170, écran TradingView `[380, 230, 1155, 630]`. Sinon, remesurer et corriger `crops` et `screen.crop` dans `cut.json`
   (méthode : `references/sources-et-decoupe.md` § 5, et la mesure des anneaux dans `revue-et-pieges.md`).
5. **Les scripts**, depuis la racine du repo (`pip install -r clip-convergence/scripts/requirements.txt`, ffmpeg dans le PATH) :
   ```
   python clip-convergence/scripts/build_media.py clip-convergence/projects/ep01/35-la-meilleure-position
   python clip-convergence/scripts/qa_voice.py    clip-convergence/projects/ep01/35-la-meilleure-position
   python clip-convergence/scripts/face_track.py  clip-convergence/projects/ep01/35-la-meilleure-position
   python clip-convergence/scripts/build_screen.py clip-convergence/projects/ep01/35-la-meilleure-position
   ```
   `qa_voice.py` : chaque morceau doit s'entendre comme son `text`. Sinon, bouger `a` / `b` de 0,05 à 0,2 s et relancer
   les quatre scripts (`build_media.py` réécrit `timeline.json`).
6. **La composition**, dans le dossier du projet : `python make_comp.py`, puis `npm run check` (0 erreur ; les avertissements
   `nested_media_start_basis_ambiguous` sont attendus), puis `npx hyperframes snapshot --at 0,2.42,2.54,2.66,5,9.76,9.88,10,16.5,17.26,17.38,17.5,22.65,22.77,22.89,27.18,27.3,27.42,32.36,33.16,33.96,36`
   et regarder chaque image (coupes cachées par la bascule, aucun trou, sous-titres jamais sur un visage, rien de privé sur
   l'écran). Si les coutures ont bougé de plus de 0,05 s, `make_comp.py` a tout recalculé : rien à éditer à la main.
7. **L'aperçu** à Nass (`npx hyperframes preview --background`), **attendre son retour**, puis :
   ```
   npx hyperframes render --fps 60 --quality delivery --workers 4 --output ..\..\..\exports\ep01\35-la-meilleure-position.mp4
   python ..\..\..\scripts\qa_render.py ..\..\..\exports\ep01\35-la-meilleure-position.mp4 --duration 36.11
   ```
   (`--duration` = la valeur `durée` imprimée par `make_comp.py`.)
8. **La trace** : retours de Nass dans `REVIEW.md`, statut du candidat 35 dans `clip-convergence/projects/ep01/EPISODE.md`,
   nouveau piège éventuel dans `references/revue-et-pieges.md`. Puis commit et push (push = branche `rebrand/crypto` +
   merge fast-forward dans `master` + push de `master`).

## Aussi sur ce PC

- **EP.04** (Nass seul, 2026-10-26) : retrouver le brut OBS et l'enregistrement vertical (`%USERPROFILE%\Videos\2026-10-26 …`),
  les noter dans `clip-convergence/projects/ep04/EPISODE.md` avec leurs durées et le décalage YouTube → brut (`offset.py`).
- **EP.03** : les sources sont déjà sur ce PC (voir `projects/ep03/EPISODE.md`) ; candidats 11 à 21 repérés sur le Mac dans
  `context/transcripts/passages-2026-10-27.md` (texte exact : `passages-detail-2026-10-27.md`). Nass choisit avant tout clip.
- Les transcriptions mot à mot des 7 vidéos de la chaîne (temps YouTube) sont dans `context/transcripts/<id>-words.json`.
