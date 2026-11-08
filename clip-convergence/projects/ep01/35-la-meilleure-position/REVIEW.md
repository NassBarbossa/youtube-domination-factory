# REVIEW — Short 35 « La meilleure des positions » (EP.01, v1 du 2026-10-28)

## Choix
- Premier clip EP.01 et premier clip construit sur le Mac. Source = téléchargement YouTube 1080p (le brut OBS est sur le PC
  Windows). À refaire depuis le brut quand il sera là : mêmes crops, `source` et `raw_to_source` (+68,9 s) à changer, puis
  `build_media.py` → `face_track.py` → `build_screen.py` → `make_comp.py` → rendu.
- Variante « écran + médaillons » de la DA (scène « À L'ÉCRAN », caméras rondes) : proposée à Nass avec ce clip, pas encore validée.
- Coupé pour le cadre : « je suis plus à la hausse sur les cryptos » (avis directionnel). Nass peut le remettre : c'est un
  morceau de 1183,42 à 1186,16 à insérer entre s2 et s3.
- Pas de chiffre à l'écran : le passage n'en a pas de vérifiable.

## Mesuré
- `hyperframes check` : 0 erreur, 12 avertissements `nested_media_start_basis_ambiguous` (attendus, scène à 0).
- Voix contrôlée par re-transcription mlx-whisper (`qa_voice_mlx.py`) : aucun mot coupé. « patienter » est dit bas (énergie
  5 fois plus faible que « là ») ; la re-transcription du morceau isolé le confirme.
- Rendu : 36,12 s, 1080 × 1920, 60 i/s, H.264 + AAC, −14,7 LUFS, crête vraie −1,4 dBTP, 9,9 Mo. Rendu en 3 min.
- Grossissement total des médaillons ≤ 1,6 (assertion dans make_comp.py).

## Regardé seulement
- 31 images : accroche à 0 s, chaque bascule à ±0,12 s (coupes masquées par le mouvement et le flou de bougé), le dessin de
  Nass sur l'écran à 5 s, PATIENTER seul à 16,5 s (le sous-titre « c'est mieux de » s'efface 0,08 s avant), fin V → logo → CTA.
- Pas écouté : le son est mesuré, pas écouté.

## Plan le plus faible
- La source YouTube à 30 i/s : les médaillons sont doublés à 60 i/s, et la compression YouTube se voit un peu sur Sadek (caméra
  sombre). Le brut OBS à 60 i/s corrigera les deux.
- Le médaillon de Sadek pendant les états E / E+ (en bas à droite, 300 px) : il regarde son écran, visage peu visible.
  `face_track.py` ne le détecte pas sur s1 à s4 ; il est bien là à l'image.
- Le morceau s1 (« si vous êtes des traders, des investisseurs ») : la re-transcription de la voix montée entend « pas des
  investisseurs ». À l'oreille de Nass.

## Retours de Nass
- 2026-11-07 : « Mets les caméras plus grosses, les positionnements c'est pas optimisé pour les formats courts. » → v2 : médaillons
  de 660 à 740 px pour celui qui parle (440 à 520 pour l'autre), prescale 2,4 en lanczos (échelle CSS ≈ 1), tout resserré
  entre y 70 et 1560, accroche descendue à 740. L'image des caméras est plus douce (source de ~300 px grossie 2,4 ×) ;
  rendu v2 mesuré bon. En attente de son avis sur la v2.
- 2026-11-07, sur la v2 (capture d'écran) : « les écrans sont mal positionnés, les ronds des caméras sont trop petits ».
  → v3 : pleine hauteur, celui qui parle fait 900 à 940 px, l'autre 620 à 650, plus de zone vide en bas ; prescale 3,2 +
  accentuation légère (`sharpen` dans cut.json) ; recadrages resserrés au-dessus des étiquettes gravées (rayon 132 / 135).
  Rendu v3 mesuré bon. En attente de son avis.
- 2026-11-07, maquette dessinée sur la capture de la v2 (« mets comme ça ») : médaillon de Nass posé sur la droite verte,
  droite verte en vraie diagonale (630 à gauche → 830 à droite), sous-titres dans la bande, droite or horizontale, Sadek
  grand au milieu de la moitié basse. → v4 : états S/S+ nass=(540, 420, 620-640), vert (630, 830), cap 870, or 960, sadek=
  (540, 1440, 800-840) ; N/N+ en miroir (Nass 800-840 à 480, vert (880, 1080), or 1210, Sadek 620-650 à 1560) ; accroche à 900.
  Rendu v4 mesuré bon. En attente de son avis.
- 2026-11-07, sur la v4 : « en bas il y a 10 km d'espace ; même espace au-dessus de ma caméra qu'en dessous de celle du bas,
  même nombre de pixels entre les caméras et les droites et entre les droites ». → v5 : mise en page calculée (`sym()` dans
  make_comp.py) : un seul écart e partout (haut, caméra→droite, bande des sous-titres, droite→caméra, bas), droites
  horizontales. Parole : parleur 740-760 px, l'autre 660, e = 100-104. Accroche : 620/620, bande de 3e (e = 97). Écran (35) :
  Nass 480-500, écran 900 × 491, Sadek 520, e = 66-71. Sous-titres 66 px. Rendu v5 mesuré bon. En attente de son avis.
- 2026-11-08, « retravaille la première » après la v6 du 36 → v6 : Nass seul dès l'ouverture de l'écran (état SOLO_E : caméra
  de 860 px en haut, écart 138, écran 900 × 491 puis sous-titres × 1,25 dans la bande, droites 1137 / 1782), puis SOLO_N sans
  écran pour « comme dirait un certain philosophe » (guillemets « » à l'encre dans la bande, trait or sur « position »). Retour
  aux deux caméras à 21,47 s (1,3 s avant Sadek) et les deux restent jusqu'à la fin : la chute est un échange, pas un
  monologue. SFX : whoosh (écran), pop (PATIENTER), whoosh grave (retour des deux caméras), impact. Corrigé au passage :
  « patienter » formait un groupe seul, le sous-titre « c'est mieux de » restait affiché sous le mot clé ; il s'efface
  maintenant 0,08 s avant. Rendu v6 mesuré bon. En attente de son avis.
