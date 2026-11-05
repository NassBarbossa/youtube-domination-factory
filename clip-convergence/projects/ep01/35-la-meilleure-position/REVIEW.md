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
- (en attente)
