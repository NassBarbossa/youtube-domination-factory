---
name: clip-convergence
description: Utiliser quand Nass veut des Shorts verticaux (YouTube Shorts, TikTok, Reels) tirés d'un épisode ou d'un replay de Convergence, son live crypto × or avec Sadek. Déclencheurs FR/EN — « clip convergence », « clips du live », « shorts du live », « découpe l'émission », « clip l'épisode 3 », « fais les shorts de Convergence », « clip the live ». Pas pour un Short créé de zéro (script, animation, face cam IA) → yt-shorts-montage ; pas pour une vidéo longue de la chaîne sans Sadek → yt-repurposing.
metadata:
  author: NassRiviera
  category: youtube-workflow
  tags: [shorts, clips, convergence, live, montage, hyperframes, vertical, captions]
  status: validé sur le pilote EP.03 « L'or est en solde » (2026-10-25, v2)
---

# Clip Convergence : les Shorts tirés du live

**Cadre** : lis d'abord `{repo}/_shared/cadre-nass.md`. Il prime pour le fond : règles halal, ton, liens, disclaimer. Pour l'image, la charte des clips est celle de Convergence (`references/deux-droites.md`) ; les chartes slides et miniatures du cadre ne s'appliquent pas ici.

`{repo}` désigne la racine du dépôt youtube-domination-factory (Mac : `~/youtube-domination-factory` · Windows : `C:\Users\User\youtube-domination-factory`). Les chemins relatifs partent de là. Les scripts sont dans `clip-convergence/scripts/` et se lancent avec `python`.

## Ce qu'est un clip Convergence

- **Le passage :** une idée qui tient seule, 30 à 45 s de voix plus ~4 s de fin. Format 1080 × 1920, 60 i/s.
- **L'image :** les deux caméras réelles de Nass et de Sadek, et l'écran réel de Nass quand il le montre.
- **Le son :** leurs vraies voix, sans musique.
- **Rien d'autre :** pas de B-roll, pas d'avatar ni de voix IA, pas d'icônes.
- **La DA « Les deux droites »** est la DA de tous les clips, validée par Nass. On ne refait pas trois concepts par clip ; on en propose trois seulement si Nass demande une autre DA. Détails dans `references/deux-droites.md`, exemple complet dans `examples/08-or-en-solde/`.

## Règles de Nass

1. **Disclaimer dans la légende, jamais à l'image.** Nass sur le pilote : « enlève pas un conseil en investissement ». La règle d'overlay de yt-shorts-montage ne s'applique pas ici.
2. **Nass montre son écran, on montre son écran.** S'il dit « là », « ce niveau-là » ou dessine sur le graphique, c'est son écran réel qu'on voit (`build_screen.py`). Le graphique redessiné ne sert que pour un chiffre dit sans écran : données réelles, datées, source à l'écran.
3. **On coupe, on ne réécrit pas.** Les mots de Nass et de Sadek restent les leurs, et l'accroche aussi. Les chiffres à l'écran sont réels ; la voix garde ce qui a été dit.
4. **Chaque coupe de parole tombe au milieu d'une bascule** de 0,6 s. Jamais de coupe sèche, au plus un plan par ~0,8 s.
5. **Pas de musique.** 4 à 5 SFX par clip, normalisés.
6. **Un pilote d'abord** quand on lance une série (« fais pas les 10, fais 1 au début »). Nass valide deux fois :
   - la liste des coupes (texte, minutages, voix montée à écouter) avant la composition ;
   - l'aperçu avant le rendu final.

## Ce qu'on ne clippe pas

- Le trading de Sadek et sa communauté « l'Imprimante » : levier, liquidation, CFD. Le casino et les paris.
- La politique.
- Les memecoins : les signaler à Nass, ne pas les traiter.
- Les certitudes et les prédictions (« c'est impossible », « ça va aller à… »), les promesses de gain, l'appel à acheter un actif précis.
- Un passage où un fauteuil est vide ou une caméra figée (`presence.py`).
- À l'image, les étiquettes gravées du live (« NASS · SHINSEKAI ALPHA », « SADEK · IMPRIMANTE », badge LIVE) restent hors des recadrages.

## Déroulé

**1. Épisode.**
- Lire `projects/<ep>/EPISODE.md` : sources, décalages, mises en page et zones, transcription, candidats.
- S'il manque, le créer avant tout.
- Trouver la source : l'enregistrement vertical OBS d'abord, sinon le brut 16:9. Le replay et YouTube ne servent qu'au repérage.
- Réutiliser la transcription de l'épisode, sinon `transcribe.py` sur la source, en arrière-plan.
- Mesurer les décalages avec `offset.py`.
- Méthode complète : `references/sources-et-decoupe.md`.

**2. Candidats.**
- Lire le passage avec `words.py --phrases`.
- Repérer sa mise en page (trois bandes, fullcam, écran…).
- Passer chaque candidat au filtre du cadre, puis à `presence.py` avec les zones de cette mise en page (`--offset` = `raw_to_source`).
- Le noter dans EPISODE.md avec son minutage, qui parle, l'idée, l'accroche dans ses mots, la durée, la mise en page, les points de cadre.
- **Nass choisit.**

**3. Coupes.**
- Projet : `npx hyperframes init clip-convergence/projects/<ep>/<NN>-<slug> --resolution portrait --non-interactive`.
- Y copier :
  - les polices `InterTight-var.ttf` et `IBMPlexMono-SemiBold.ttf` (`{repo}/shows/emission-live/assets/fonts/`) vers `assets/fonts/` ;
  - le logo `convergence-logo-clair.svg` (`…/assets/logo/`) vers `assets/` ;
  - les SFX `whoosh-short`, `pop` et `impact-bass-1` (`.mp3` du catalogue `/media-use`, `audio/assets/sfx/`) vers `assets/sfx/` ;
  - `examples/08-or-en-solde/make_comp.py` à la racine du projet.
- Écrire `cut.json`, puis lancer `build_media.py` et `qa_voice.py`. Chaque morceau doit s'entendre comme son texte ; sinon, ajuster et relancer.
- Lancer ensuite `face_track.py`, puis `build_screen.py` si Nass montre son écran. **Après chaque `build_media.py`, relancer ces deux scripts** : il réécrit `timeline.json`.
- **Liste des coupes à Nass**, avec le texte de chaque morceau et la voix montée à écouter.

**4. Données.** Un chiffre affiché vient de `assets/data/*.json`, avec source et dates.

**5. Composition.**
- Adapter les blocs `PROPRE AU CLIP` de `make_comp.py`.
- Si la mise en page diffère de celle du pilote (trois bandes), adapter aussi le bloc `PROPRE À LA MISE EN PAGE` (états). C'est le cas pour la fullcam ou pour un seul orateur.
- Lancer le script.
- Avant d'écrire du HTML de composition à la main : `/hyperframes` (contrat).

**6. Revue.**
- `check`, `snapshot --review`, images aux bascules ±0,12 s.
- Aperçu à Nass, puis attente de son retour.
- Détails : `references/revue-et-pieges.md`.

**7. Rendu.**
- `render --fps 60 --quality delivery` vers `clip-convergence/exports/<ep>/<NN>-<slug>.mp4`.
- Passer `qa_render.py`, puis ouvrir le fichier.
- Livrer la légende de chaque plateforme, avec le disclaimer (`references/revue-et-pieges.md`).

**8. Trace.**
- Dans le projet, écrire `SPEC.md` et `REVIEW.md` : choix, ce qui a été mesuré, plan le plus faible, retours de Nass.
- Dans EPISODE.md, mettre à jour le statut du candidat.
- Ajouter un piège nouveau à `references/revue-et-pieges.md`.

Le pilote 08 a été fait avant ce skill. Il est resté dans `{repo}/yt-shorts-montage/projects/recycles/08-or-en-solde/` (export dans `yt-shorts-montage/exports/recycles/`), avec sa copie de référence dans `examples/`. Les nouveaux clips vont dans `clip-convergence/projects/` et `clip-convergence/exports/`.

## Scripts

| Script | Rôle |
|---|---|
| `transcribe.py` | transcription mot à mot (faster-whisper, CPU) au format des autres scripts |
| `words.py` | lire une transcription entre deux instants (mots ou phrases) |
| `offset.py` | décalage entre deux fichiers du même son (corrélation audio, score) |
| `presence.py` | les deux fauteuils occupés ? visages et images figées par caméra |
| `build_media.py` | voix montée −14 LUFS, recadrages caméra, `timeline.json` |
| `qa_voice.py` | re-transcription de la voix montée, morceau par morceau |
| `face_track.py` | position du visage par morceau, pour cadrer sans trou |
| `build_screen.py` | écran réel de Nass, par morceau |
| `qa_render.py` | contrôle final : format, durée, sonie, crête |

Dépendances : `pip install -r clip-convergence/scripts/requirements.txt`, avec ffmpeg et ffprobe dans le PATH. Les médias lourds des projets (`assets/video`, `assets/audio`, `.hyperframes/`) et les exports restent hors git.
