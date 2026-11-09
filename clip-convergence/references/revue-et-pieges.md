# Revue, rendu, publication et pièges

## Avant de montrer à Nass

Les commandes HyperFrames se lancent dans le dossier du projet.

1. **Contrôle :** `npx hyperframes check --json` doit donner 0 erreur. Deux avertissements sont acceptés :
   - `nested_media_start_basis_ambiguous`, un par vidéo. La scène démarre à 0, donc le temps local égale le temps global.
   - `escaped_container` sur le soulignement d'un sous-titre, s'il ne se voit pas à l'image.
2. **Planches :** `npx hyperframes snapshot --review` produit les temps forts, une bande de 5 images autour de chaque coupe et une planche à la largeur d'un téléphone. On regarde chaque image.
3. **Images ciblées :** `npx hyperframes snapshot --at <t,…>` aux instants suivants :
   - 0,0 : accroche lisible, deux visages visibles ;
   - chaque bascule, à t − 0,12, t et t + 0,12 : coupe cachée par le mouvement, pas de trou de papier, visages recentrés ;
   - chaque mot clé à + 0,5 s, chaque événement du graphique ou de l'écran ;
   - la fin : `END_T` + 0,4 (grand V), + 1,2 (logo), + 2,0 (CTA), et D − 0,1.
4. **Points à vérifier sur chaque image :**
   - sous-titres dans la bande et jamais sur un visage ;
   - texte d'au moins 28 px une fois rendu, lisible sur la planche téléphone ;
   - aucune étiquette du live dans les cadres ;
   - aucune info privée sur l'écran partagé : adresse, solde, notification, onglet perso.
5. **Voix :** `qa_voice.py` est passé.
6. **Aperçu :** `npx hyperframes preview --background`, puis on donne l'URL du projet à Nass. **Pas de rendu final avant son retour.** Ses retours vont dans `REVIEW.md`.

## Rendu et contrôle

```
npx hyperframes render --fps 60 --quality delivery --workers 4 --output {repo}/clip-convergence/exports/<ep>/<NN>-<slug>.mp4
python {repo}/clip-convergence/scripts/qa_render.py <fichier.mp4> --duration <D>
```

- `qa_render.py` vérifie le format (1080 × 1920, 60 i/s, H.264 + AAC), la durée, la sonie (−16 à −13 LUFS ; le pilote est à −15,4) et la crête vraie (≤ −1 dBTP).
- Un clip de 44 s se rend en environ 2 min 30.
- En cas de manque de mémoire : `NODE_OPTIONS=--max-old-space-size=8192`.
- Ensuite, on ouvre le fichier pour Nass et on écrit ce qui a été **mesuré** et ce qui a été seulement **regardé**.

## Légende de publication (à livrer avec le MP4)

| Plateforme | Contenu |
|---|---|
| YouTube Shorts | titre de 40 à 60 caractères, dans ses mots ; description = une phrase + **« Pas un conseil en investissement. »** ; pas de hashtag ; vidéo associée = le replay de l'épisode (sinon `https://www.youtube.com/@NassinCrypto/streams`) |
| TikTok, Reels | phrase d'accroche + « Épisode complet sur la chaîne YouTube Nassin Crypto (lien en bio). » + **« Pas un conseil en investissement. »** + 3 à 5 hashtags (`#crypto #bitcoin` + le sujet) |
| Partout | le fichier exporté, jamais une version retéléchargée ; le disclaimer dans la légende, pas à l'image |

## Pièges déjà rencontrés

| Symptôme | Cause et correction |
|---|---|
| Les sous-titres disparaissent pendant une bascule | `data-motion-blur="on"` efface un conteneur de texte qui bouge : `data-motion-blur="off"` sur `#capwrap` |
| `gsap_css_transform_conflict` | pas de transform CSS sur un élément animé par GSAP : état de départ en `fromTo(…, 0)` |
| Un élément caché en CSS ne s'affiche jamais | un `tl.set` à t = 0 est ignoré au rendu : état initial visible en CSS, ou `fromTo` |
| Fondu d'un `.clip` sans effet | animer l'opacité d'un enfant (`#chart-body`), pas du `.clip` |
| Un mot du morceau suivant dans les sous-titres (« donc », « ou ») | filtre des mots en `< b − 0,02` (déjà dans `build_media.py`) |
| Un petit mot avalé à une couture | fenêtre du creux trop large : ±50 ms (déjà dans `build_media.py`) |
| Coupe sèche sur la caméra de Sadek en CN / CN+ | Sadek doit bouger aussi (échelle 1,30 → 1,36) |
| Mince bande de Nass en haut de l'état CS | replier complètement son cadre (droite verte 8 → 36) |
| Deux mots clés qui se chevauchent | les empiler (un en haut à droite, un en bas à gauche de la bande) |
| Un mot clé en serif | lui donner la classe `.kw`, qui porte la police |
| Le V reste en grand au-dessus du logo (« CON ERGENCE ») | faire glisser les droites sur les coordonnées du V du logo, retirer les `<line>` du SVG |
| Visages décentrés quand quelqu'un se penche | `face_track.py` par morceau, jamais un cadrage fixe pour tout le clip |
| Contraste refusé | or texte `#A07006` au lieu de `#C98A0B`, gris `#565D6B` |
| Texte refusé car trop petit | au moins 28 px rendus (minimum du check) ; 32 à 34 px pour les étiquettes Plex Mono |
| `<svg>` invisible au rendu | jamais 0 en largeur ou en hauteur, même avec `overflow: visible` |
| faster-whisper plante (PyAV, `metadata_errors`) | lui passer l'audio décodé par ffmpeg en numpy (déjà dans les scripts) |
| CUDA sans `cublas64_12.dll` | CPU int8 (déjà dans les scripts) |
| OpenCV 5 n'a plus de Haar | YuNet (`assets/models/face_detection_yunet_2023mar.onnx`, OpenCV Zoo) |
| Accents illisibles dans la console Windows | `common.py` passe la sortie en UTF-8 |
| `offset.py` lent | décodage de tout le fichier : passer `--guess` dès qu'on connaît le décalage à quelques secondes près |
| Décalage YouTube réutilisé tel quel | il peut changer d'un passage à l'autre : le mesurer au passage choisi |
| Zones fausses (visage coupé à la bouche) | la mise en page OBS a changé pendant l'émission : prendre les zones de la mise en page du passage |
| `make_comp.py` plante sur `faces` | `build_media.py` relancé sans `face_track.py` derrière |
| Un mot clé qui remplace un sous-titre apparaît par-dessus lui | le groupe de sous-titres précédent s'efface à `PAT_T − 0,08` (clip 35) |
| L'anneau or de Sadek mesuré trop grand (watchlist et étiquette SADEK de la même couleur) | restreindre la zone de mesure à l'intérieur du rond et au-dessus de l'étiquette, rayon = largeur / 2 |
| `snapshot` dans une chaîne `&&` avec `grep` : la chaîne s'arrête | ne pas conditionner la suite sur un `grep` de la sortie |
| Pas de brut OBS sur la machine | construire la v1 depuis le téléchargement YouTube 1080p (même mise en page), le dire dans SPEC / REVIEW, refaire depuis le brut ensuite : `source` et `raw_to_source` seuls changent |
| Sur Mac, faster-whisper n'est pas installé | `qa_voice_mlx.py` (mlx-whisper, GPU) ; scripts OpenCV via `uv run --python 3.12 --with numpy,opencv-python` |
| Une languette verte ou or sous un médaillon | l'étiquette gravée NASS / SADEK mord sur le bas du cercle : rayon du crop = haut de l'étiquette + 2 px − centre |
| Le mot clé remplace un mot qui formait un groupe de sous-titres à lui seul | le groupe précédent reste affiché sous le mot clé (35 v5, « c'est mieux de » sous PATIENTER) | quand le groupe du mot clé est vidé, c'est le groupe précédent du même morceau qui s'efface avant le mot clé (`PAT_GI = gi - 1`) |

## Série du 2026-11-09 (EP.03 depuis le replay YouTube 720p) : pièges rencontrés

- **Le replay n'est pas le brut** : la mise en page du live change (ronds + TradingView, ronds + slide, fullcam, punk). Repérer les bascules à la frame (`ffmpeg -ss`) avant de couper ; un morceau ne traverse jamais une bascule (clip 62 : « ne faites pas cette erreur-là » tombait sur la bascule fullcam, retiré).
- **Regarder les visages, pas seulement les coutures** : `face_track.py` donne la position médiane par morceau. Un visage à x ≈ 25 px sur un rond de 210 = la personne est hors de sa caméra (Nass penché vers son écran, 18:00–18:33 et 24:51–25:12). Réponse : écran seul (`screen_only`, même boîte d'écran que l'état solo si on alterne) ou l'autre caméra seule. Zéro visage détecté = fauteuil vide (Sadek, 29:28–31:15) : accroche et états solo de l'autre.
- **Mots clés = états solo** (règle EP.01 retrouvée à la dure) : dans les états à deux caméras (N, S, E), la bande ne contient que les sous-titres ; un mot clé posé là tombe sur la caméra du bas (contraste 1,1:1 au check). Celui qui parle longtemps passe en SOLO_N / SOLO_S, retour aux deux caméras 1,3 s avant que l'autre parle.
- **Punk** : à partir de 38:20 la fenêtre de Nass montre son avatar ; Sadek porte seul les clips (crops « punk », `solo("sadek", 760)` en accroche).
- **Un rendu à la fois** : deux `hyperframes render` en parallèle (ou un rendu + des `step`) font échouer ffmpeg (`VIDEO_EXTRACTION_FAILED`, `Runtime.evaluate timed out`). Tuer les `preview --foreground` orphelins avant de relancer.
- **Mot clé en fin de morceau** : s'il porte le dernier mot d'un morceau, il reste moins d'une seconde à l'écran (`line_unread`) ; le prolonger dans le morceau suivant jusqu'au mot clé d'après − 0,9 s.
- **Transcription YouTube** : « rennes » pour « range », « mois » pour « moins », « la alt season », un « ? » parasite en tête de morceau : `c.fix` par segment, et `find` sur le token sans apostrophe (« or, » pour « l'or, », « indécision » pour « d'indécision »).
