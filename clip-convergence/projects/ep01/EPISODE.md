# Convergence EP.01 — live du 2026-10-05

## Sources

| Rôle | Fichier | Format |
|---|---|---|
| Brut OBS 16:9 (meilleure source) | `~/Videos/2026-10-05 14-36-21.mp4` | 1920 × 1080, 60 i/s, 44 min. **Retrouvé le 2026-10-25** avec `offset.py` |
| Replay | `~/Videos/NassRiviera/cONVERGENCE #&.mp4` | 3840 × 2160, 30 i/s, 38 min. C'est le brut **agrandi** : à ne pas utiliser pour l'image |
| Vertical | aucun | Aitum Vertical n'enregistrait pas encore |

## Décalages

| Mesure | Résultat |
|---|---|
| replay → brut | **brut = replay + 68,9 s** (`offset.py` à 11:40 et 15:00 du replay : scores 1,000 et 0,966). À revérifier au passage choisi |

## Zones (brut 16:9)

Les trois passages candidats sont dans la scène **« À L'ÉCRAN »** :
- l'écran TradingView est grand, au centre (fenêtre du navigateur ≈ x 176–1744, y 100–950) ;
- les caméras sont des **ronds d'environ 330 px** en bas à gauche (Nass) et en bas à droite (Sadek).

Les ronds sont trop petits pour remplir les cadres des « deux droites » sans flou. Ces clips se construisent donc **sur l'écran réel**, avec les ronds en médaillon. C'est une variante de la DA, **à proposer à Nass avant de construire**.

Crops exacts à mesurer sur une image (`ffmpeg -ss <t> -i … -frames:v 1`).

## Transcription

Pas de transcription complète. Des fenêtres sont transcrites dans `{repo}/yt-shorts-montage/projects/recycles/windows/0[5-7]-*.words.json`, en temps du replay. Pour un clip :
- soit `transcribe.py` sur le brut, sur la fenêtre du passage (`--start` / `--end`) ;
- soit ajouter 68,9 s aux temps des fenêtres.

## Candidats

Minutages : replay, puis brut (= replay + 68,9 s).

| N° | Passage | Minutage | Qui | Statut |
|---|---|---|---|---|
| 05 | « Le monde est en ATH de bullshit » | replay 11:34–12:44 · brut 12:43–13:53 | Nass | à faire (présence à vérifier sur les ronds) |
| 06 | « Le Bitcoin ne tombait pas » | replay 14:30–15:54 · brut 15:39–17:03 | Nass | à faire |
| 07 | « Sentiment baissier » | replay 10:22–11:02 · brut 11:31–12:11 | Sadek | à faire |
