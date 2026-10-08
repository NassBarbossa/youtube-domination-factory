---
name: yt-shorts-montage
description: Edit / produce vertical Shorts (1080×1920, YouTube Shorts, TikTok, Reels) from a validated yt-shorts-script, in Nass Riviera's crypto brand. Use when user says "monte le short", "montage short", "fais la vidéo du short", "edit short", "render short", "sous-titres short", or hands over a validated Shorts script and/or rushes to turn into a finished vertical video.
metadata:
  author: NassRiviera
  version: 0.1.0
  category: youtube-workflow
  tags: [shorts, montage, editing, hyperframes, vertical, captions, crypto]
  status: fondations — ressources de Nass à intégrer
---

# YT Shorts Montage — fabrication des Shorts

## Rôle

Transformer un script **validé** de `yt-shorts-script` (et, si besoin, les rushes face cam de Nass) en **Short fini** : vertical 1080×1920, sous-titré, aux couleurs de la marque, prêt à publier sur YouTube Shorts, TikTok et Reels.

Ce skill n'écrit pas les textes : il suit le script mot pour mot. Un changement de texte repasse par `yt-shorts-script` et la validation de Nass.

## Cadre commun (source : `CLAUDE.md`)

- **Charte** (section Slides de `CLAUDE.md`) : noir `#0B0B0B`, sable/or `#DBB17F`, crème `#F4EFE7`, bleu punk `#648596` ; Archivo Black + Public Sans ; punk pixel @punk6995, cartes crème à bord noir avec ombre pleine.
- **Règle halal** et **données réelles uniquement** : un graphique ou un chiffre affiché vient des `sources` du script (valeur, source, date). Jamais de graphique « illustratif » généré, jamais de capture retouchée.

Règles fixes de tout Short :
- **9:16 vertical, 1080×1920, 30 à 60 s.**
- **Jamais de musique, mais des sound effects** (règle de Nass) : des SFX sur les animations (pop, tick, whoosh de transition, impact, compteur, carillon…), choisis pour chaque moment, normalisés et équilibrés pour ne pas saturer.
- **Sous-titres gravés** sur toute la voix.
- **Disclaimer** « Pas un conseil en investissement. » en overlay, au minimum sur la fin.
- **Zones de sécurité** : rien d'important dans les ~250 px du bas ni sur la colonne de boutons à droite (interfaces TikTok / Reels / Shorts).
- **Hook lisible dans la première seconde** (texte à l'écran du bloc « Hook »).

## Outils déjà en place (réutiliser, ne pas recréer)

- **HyperFrames** (skills `/hyperframes`, `/motion-graphics`, `/embedded-captions`, `/reel-export`) : compositions verticales, sous-titres, export. Recette validée par Nass dans la mémoire « promo video playbook » (3 idées → snapshots → rendu, SFX rares et normalisés, musique synthé libre de droits).
- **Exemples dans ce repo** : `shows/emission-live/annonce-lancement/` (Short vertical 9:16 en HyperFrames) et `shows/emission-live/intro-banger/` (montage rythmé caméra).

## Méthode

Ressources de base : **`references/motion-graphics-guide.md`** (bloc « STYLE: Nass Riviera », 10 mouvements nommés, prompt Short 100 % texte, règles face cam IA et son) et **`references/motion-ressources.md`** (Claude Motion Tips + article laforet.dev). Deux pistes selon le champ `format` du script : **animation** (le cas principal, comme la vidéo d'annonce Convergence) ou **face cam IA** (Nass ne tourne pas : la face cam est générée par un modèle IA).

### Commun aux deux pistes (obligatoire)
1. **Entrée** : `yt-shorts-script/outputs/[serie]/[NN]-[slug].md` avec `statut: valide`.
2. **Brief en XML** (habitude 01) : traduire le script en brief `<art_direction>` (charte), `<references>`, `<timing>` (repris des timecodes du script), `<deliverable>` (1080×1920, 30 fps, durée). Le garder dans le dossier du projet (`brief.xml`).
3. **Test d'une seconde** (habitude 02) : rendre d'abord 1 s de l'effet le plus difficile du Short et le montrer à Nass **avant** de construire le reste.
4. **Projet** : un projet HyperFrames par Short dans `yt-shorts-montage/projects/[serie]/[NN]-[slug]/`.
5. **Planche d'images clés** (habitude 03) : début, chaque temps fort / transition, fin, chacune horodatée ; vérifier texte coupé, chevauchements, éléments qui disparaissent, zones de sécurité, sous-titres, disclaimer. **Attendre le feu vert de Nass avant le rendu final.**
6. **Rendu** : `yt-shorts-montage/exports/[serie]/[NN]-[slug].mp4`, puis ouvrir le fichier pour Nass.

### Piste A — Animation (motion design pur)
- Composition HyperFrames verticale aux couleurs de la marque (voir `/hyperframes`, `/motion-graphics`, `/hyperframes-keyframes`), sur le modèle de `shows/emission-live/annonce-lancement/`.
- Effets : piocher dans la bibliothèque open source de `references/motion-ressources.md` (Matter.js, Rough.js, PixiJS filters, Anime.js, p5.brush, thinking-orbs) en restant seekable et déterministe. Pour une idée de mouvement : galerie des 400+ vidéos Claude.
- Style : coller le bloc « STYLE: Nass Riviera (Editorial Grain) » sous le brief : mêmes tokens que les slides (`yt-script/references/slide-template.html`) + grain de pellicule animé, formes découpées légèrement tournées, filets sable, numéros d'étape ; hooks et récaps en Kinetic Type ; rendu en `--crf 23`.
- Son : **pas de musique, des sound effects** calés sur les animations (bundle media-use, sons générés en code, Freesound CC0 / Kenney), normalisés au pic puis dosés. Si le script a une voix : voir « Voix » ci-dessous.

### Piste B — Face cam IA
- Entrée : le MP4 de l'avatar IA (outil à préciser par Nass), posé dans le dossier du projet.
- Transcription locale (`npx hyperframes transcribe`) pour les sous-titres ; **coupes des silences sur la forme d'onde** (FFmpeg `silencedetect`), jamais sur les timestamps de la transcription.
- Règles du guide (section 4) : vidéo jamais modifiée, animation calée sur le mot exact, rien dans les 3 premières secondes, rien sur le visage / le tiers bas / les 10 % des bords.
- Habillage : `/embedded-captions` (sous-titres) et `/talking-head-recut` (cartes, chiffres sourcés, CTA), punch-in sur les phrases fortes (`/hyperframes-keyframes`) ; MediaPipe seulement si un suivi auto du visage devient nécessaire.
- **Mention « contenu généré par IA »** : cocher l'option de divulgation de chaque plateforme (YouTube, TikTok, Instagram) pour une face cam réaliste générée par IA.

### Voix
- Animation avec voix ou face cam IA : la voix vient de l'outil IA choisi par Nass (à préciser). Ne jamais générer une voix qui imite Nass sans son accord explicite pour ce Short.

## Points à préciser avec Nass
- Outil d'avatar / de voix IA pour la face cam (et pour les voix off des Shorts animés).
- Exemples de Shorts de référence (rythme, style de sous-titres) à ajouter dans `references/`.
