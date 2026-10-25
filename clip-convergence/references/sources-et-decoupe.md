# Sources, recalage et découpe

Scripts dans `{repo}/clip-convergence/scripts/`. Lancer avec `python <script>.py` (ffmpeg et ffprobe dans le PATH, `pip install -r scripts/requirements.txt`). Tous acceptent des instants en secondes, en `mm:ss` ou en `h:mm:ss`.

## 1. Les fichiers d'un épisode

OBS enregistre dans le dossier vidéos de Windows (`%USERPROFILE%\Videos`). « Enregistrer le live.bat » lance deux enregistrements à la fois :

| Fichier | Contenu | Usage |
|---|---|---|
| `AAAA-MM-JJ hh-mm-ss vertical.mkv` | canevas 9:16 Aitum Vertical, 1080 × 1920, 60 i/s : caméra Nass en haut, écran ou deck au milieu, caméra Sadek en bas | **source n° 1**, image et son |
| `AAAA-MM-JJ hh-mm-ss.mkv` (ou `.mp4`) | canevas 16:9, 1920 × 1080, 60 i/s | secours (caméras plus petites) |
| `… - son egalise.*` | les mêmes, son égalisé au montage du replay | à préférer quand ils existent |
| replay monté, téléchargement YouTube (`Videos/NassRiviera/youtube/<id>.mp4`) | coupes internes, compression YouTube | **jamais pour l'image**, seulement comme repère de temps (minutage YouTube) |

**Trouver les fichiers :**
1. Partir de la date du live.
2. Comparer les durées avec `ffprobe`.
3. Prouver que c'est le même son avec `offset.py`, en visant un score d'au moins 0,9.

C'est ainsi qu'on a retrouvé le brut de l'EP.01.

**Pas d'enregistrement vertical** (EP.01) : prendre le brut 16:9. Dans la scène « 2 · Live », les caméras sont des fenêtres de 702 × 848 en x 50 et 784, y 108. Le replay 4K est un agrandissement avec de petits ronds : à éviter.

## 2. `projects/<ep>/EPISODE.md`

Un fichier par épisode, à lire avant tout. Le créer s'il manque, avec ces rubriques :

```
# Convergence EP.NN — <date du live>
## Sources        chemins (~/Videos/…), taille, cadence, son égalisé ou non
## Décalages      mesures offset.py : fichier A → fichier B, décalage, score, instants testés
## Zones          crops [x, y, w, h] des caméras (et de l'écran) dans la source, mesurés sur une image
## Transcription  chemin, base de temps (quel fichier), outil
## Candidats      tableau : n°, minutage, qui parle, idée, accroche (ses mots), durée, cadre, présence, statut
```

## 3. Transcription : une par épisode

- **Réutiliser** celle qui existe (EP.03 : `~/Videos/montage-ep03/transcript.json`, en temps du brut 16:9).
- **Sinon,** transcrire directement la source du montage, l'enregistrement vertical. Ainsi `raw_to_source` vaut 0. Commande, en arrière-plan car c'est long sur CPU :
  `python transcribe.py "<source>" projects/<ep>/transcript.json`
- **Lire un passage :** `python words.py <transcript.json> 28:00 31:00 --phrases`, une ligne par phrase avec son heure. Sans `--phrases`, chaque mot s'affiche avec ses bornes, pour écrire `a` et `b`.

## 4. Décalages

```
python offset.py <référence> <cible> <t1> <t2> [--guess D]
```

| Cas | Décalage | Exemple |
|---|---|---|
| Deux enregistrements OBS d'une même session | constant | EP.03 : vertical = brut − 1,76 s, score 0,99 |
| Brut et replay monté ou YouTube | change à chaque coupe du montage | YouTube ≈ brut − 244 s au début de l'EP.03 seulement |

**Mesurer au milieu du passage choisi :**
- `t` en pleine parole, à plus de 8 s d'une coupe du montage ;
- un score inférieur à 0,9 veut dire : changer d'instant.

## 5. Zones

1. Extraire une image : `ffmpeg -ss <t> -i "<source>" -frames:v 1 zone.png`.
2. Y mesurer chaque bloc caméra **à l'intérieur** des bordures, des étiquettes gravées (« NASS · SHINSEKAI ALPHA », « SADEK · IMPRIMANTE ») et du badge LIVE.

**Une émission change de mise en page en cours de route.** EP.03 : « trois bandes » (Nass, écran, Sadek) et « fullcam » (deux grandes caméras). Les zones vont donc **par mise en page**, dans `projects/<ep>/zones-<mise en page>.json` (même format `crops` que le `cut.json`), et chaque candidat note sa mise en page.

Valeurs de l'EP.03 (vertical) :

| Mise en page | Nass | Sadek | Écran |
|---|---|---|---|
| trois bandes | `[26, 26, 1028, 514]` | `[26, 1284, 1028, 516]` | `[20, 740, 880, 480]`, affiché en 1012 × 552 |
| fullcam | `[26, 26, 1028, 828]` | `[26, 984, 1028, 822]` | — |

D'un épisode à l'autre, on remesure.

## 6. Présence : les deux fauteuils occupés

```
python presence.py "<source>" <début> <fin> projects/<ep>/zones-<mise en page>.json --offset <raw_to_source>
```

Les instants sont donnés en temps de la transcription ; `--offset` les ramène au temps de la source (EP.03 : −1.76).

**Lancer avant de proposer un passage.** Un clip sans Sadek à l'image ne fonctionne pas : c'était le cas du 09 (0 visage sur 68 images). La sortie donne, par caméra, la part d'images avec un visage et la part d'images figées.

Résultat « À VÉRIFIER » :
- choisir un autre passage ;
- ou garder le passage et montrer l'écran ou le deck à la place du fauteuil vide, après accord de Nass.

## 7. `cut.json` (dans le dossier du projet)

```json
{
  "short": "NN — titre (Convergence EP.NN)",
  "source": "~/Videos/<enregistrement vertical>.mkv",
  "transcript": "~/Videos/…/transcript.json",
  "raw_to_source": 0,
  "prescale": 1.45,
  "crops": {"nass": [x, y, w, h], "sadek": [x, y, w, h]},
  "screen": {"crop": [x, y, w, h], "size": [1012, 552], "segments": ["s3a"]},
  "segments": [
    {"id": "s1", "speaker": "sadek", "a": 1690.88, "b": 1701.0, "text": "ce qui est dit, mot pour mot"}
  ]
}
```

- `a` et `b` sont en **temps de la transcription**. `raw_to_source` convertit vers la source (0 si la transcription a été faite sur la source).
- `text` donne les mots attendus. `qa_voice.py` s'y compare.
- `screen` ne sert que si Nass montre son écran pendant ces morceaux.
- **Contenu d'un clip :** une idée, 30 à 45 s de voix, morceaux coupés sur des fins de phrase. On retire les hésitations, les redites, les digressions et ce que le cadre exclut. On ne retire jamais une négation ni une nuance sur le risque.
- **Mots collés** (frontière sans pause) : le creux le plus proche peut tomber au milieu d'un mot. On cherche d'abord une autre frontière, une vraie fin de phrase. Sinon, on coupe juste avant le mot suivant, et `qa_voice.py` tranche.

## 8. Médias

| Étape | Commande | Résultat ou contrôle |
|---|---|---|
| Voix et caméras | `python build_media.py <projet>` | `assets/audio/voice.wav` (−14 LUFS), `assets/video/<cam>_<seg>.mp4`, `timeline.json`. Chaque couture est recalée sur le creux du son dans ±50 ms. Une fenêtre plus large saute par-dessus les petits mots (« que », « bien ») |
| Contrôle de la voix | `python qa_voice.py <projet>` | Chaque morceau doit s'entendre comme son `text`. Un mot coupé ou un mot du morceau suivant qui dépasse se corrige en déplaçant `a` / `b` de 0,05 à 0,2 s, puis on relance les deux étapes |
| Visages | `python face_track.py <projet>` | `timeline.json["faces"]`. À relancer après chaque `build_media.py`, qui réécrit `timeline.json` |
| Écran de Nass | `python build_screen.py <projet>` | `assets/video/screen_<seg>.mp4` (si `cut.json` a un bloc `screen`) |

## 9. Données des graphiques

- **Or :** Yahoo Finance `GC=F` via `yfinance`. Clôtures quotidiennes, record en séance avec sa date.
- **Cryptos :** CoinStats (MCP) ou CoinGecko.
- **Format :** le fichier va dans `assets/data/<actif>.json` avec la source, la date de chaque point et la date de récupération.
- **À l'écran :** la ligne « SOURCE : … ».
- **Valeur dite à l'antenne :** on garde le jour du live et on vérifie qu'elle est dans la fourchette de la séance (EP.03 : 4 180 $ dit, séance de 4 155,6 à 4 211,2 $).
