---
name: yt-shorts-montage
description: Fabrique les Shorts verticaux (1080×1920, YouTube Shorts, TikTok, Reels) de la chaîne crypto de Nass Riviera à partir d'un script yt-shorts-script validé : composition HyperFrames, sous-titres, sound effects, disclaimer, rendu. Déclencheurs : « monte le short », « montage short », « fais la vidéo du short », « sous-titres short », « rends le short », « edit short », « render short ». Pas pour écrire ou modifier le texte d'un Short → yt-shorts-script ; pas pour découper une vidéo longue → yt-repurposing.
metadata:
  author: NassRiviera
  category: youtube-workflow
  tags: [shorts, montage, editing, hyperframes, vertical, captions, crypto]
  status: fondations — style de montage de Nass à intégrer dans references/
---

# YT Shorts Montage — fabrication des Shorts

**Cadre** : lis d'abord `C:\Users\User\youtube-domination-factory\_shared\cadre-nass.md` (narrative, avatar, offres, ton, règles de fond, charte). Il prime sur ce fichier.

Chemins relatifs = relatifs à la racine du repo `C:\Users\User\youtube-domination-factory`.

## Rôle

Transformer un script **validé** de `yt-shorts-script` (et, si besoin, une face cam IA) en Short fini, prêt à publier. Ce skill suit le script mot pour mot : un changement de texte repasse par `yt-shorts-script` et la validation de Nass.

Données réelles uniquement : un graphique ou un chiffre affiché vient des `sources` du script (valeur, source, date). Jamais de graphique « illustratif » généré, jamais de capture retouchée.

## Règles fixes de tout Short

- **Vertical 1080×1920, 30 à 60 s, rendu à 60 i/s.**
- **Jamais de musique, mais des sound effects sur les animations** (règle de Nass) : pop, tick, whoosh de transition, impact, compteur, carillon…, choisis pour chaque moment, normalisés et dosés pour ne pas saturer.
- **Rythme** (retours de Nass sur les Shorts déjà faits) : transitions fluides d'environ 0,6 s ; 1 plan par ~0,8 s max.
- **Style par défaut : « Editorial Grain »** — tokens de la charte (mêmes que les slides) + grain de pellicule animé. Bloc STYLE complet dans `references/motion-graphics-guide.md`.
- **Sous-titres gravés** sur toute la voix.
- **Disclaimer** « Pas un conseil en investissement. » en overlay, au minimum sur la fin.
- **Zones de sécurité** : rien d'important dans les ~250 px du bas ni sur la colonne de boutons à droite.
- **Hook lisible dès la première seconde** (texte à l'écran du bloc « Hook »).

## Ressources

- **`references/motion-graphics-guide.md`** : bloc « STYLE: Nass Riviera (Editorial Grain) », mouvements nommés, prompt Short 100 % texte, règles face cam IA, son, export.
- **`references/motion-ressources.md`** : effets open source, galeries d'inspiration, trois habitudes de travail (brief XML, test d'une seconde, planche d'images clés), pipeline laforet.dev.
- **Fondations** : le style de montage de Nass (exemples de Shorts de référence, sous-titres, rythme) arrivera dans `references/`. Ne pas inventer de style maison au-delà de ce qui est écrit ici et dans `references/`.
- Outils à réutiliser : skills `/hyperframes`, `/motion-graphics`, `/hyperframes-keyframes`, `/embedded-captions`, `/talking-head-recut`, `/reel-export`, `/media-use` (SFX). Exemples dans le repo : `shows/emission-live/annonce-lancement/` (vertical 9:16 HyperFrames) et `shows/emission-live/intro-banger/` (montage rythmé). La recette « promo video playbook » (3 idées → snapshots → rendu, SFX rares et normalisés) s'applique, **sans musique** pour les Shorts.

## Méthode

Deux pistes selon le champ `format` du script : **animation** (cas principal) ou **face cam IA** (Nass ne tourne pas).

### Commun aux deux pistes
1. **Entrée** : `yt-shorts-script/outputs/[serie]/[NN]-[slug].md` avec `statut: valide`.
2. **Brief XML** (habitude 01) : `<art_direction>` (charte + Editorial Grain), `<references>`, `<timing>` (timecodes du script), `<deliverable>` (1080×1920, 60 i/s, durée, sans musique, avec SFX). Le garder dans le projet (`brief.xml`).
3. **Test d'une seconde** (habitude 02) : rendre d'abord 1 s de l'`effet_cle` et le montrer à Nass avant de construire le reste.
4. **Projet** : un projet HyperFrames par Short dans `yt-shorts-montage/projects/[serie]/[NN]-[slug]/`.
5. **Planche d'images clés** (habitude 03) : début, chaque temps fort / transition, fin, horodatées ; vérifier texte coupé, chevauchements, éléments qui disparaissent, zones de sécurité, sous-titres, disclaimer. Attendre le feu vert de Nass avant le rendu final.
6. **Rendu** : `yt-shorts-montage/exports/[serie]/[NN]-[slug].mp4` (60 i/s), puis ouvrir le fichier pour Nass.

### Piste A — Animation
- Composition HyperFrames verticale sur le modèle de `shows/emission-live/annonce-lancement/`.
- Bloc STYLE Editorial Grain collé sous le brief ; hooks et récaps en Kinetic Type.
- Effets : bibliothèque de `references/motion-ressources.md` (Matter.js, Rough.js, PixiJS filters, Anime.js, p5.brush, thinking-orbs), toujours seekable et déterministe.
- Son : sound effects calés sur les animations (SFX media-use, sons générés en code, Freesound CC0 / Kenney), normalisés puis dosés. Voix éventuelle : voir « Voix ».

### Piste B — Face cam IA
- Entrée : le MP4 de l'avatar IA (outil à préciser par Nass), posé dans le dossier du projet.
- Transcription locale (`npx hyperframes transcribe`) pour les sous-titres ; coupes des silences sur la forme d'onde (FFmpeg `silencedetect`), jamais sur les timestamps de la transcription.
- Règles du guide (section 4) : vidéo jamais modifiée, animation calée sur le mot exact, rien dans les 3 premières secondes, rien sur le visage / le tiers bas / les 10 % des bords.
- Habillage : `/embedded-captions` (sous-titres), `/talking-head-recut` (cartes, chiffres sourcés, CTA), punch-in sur les phrases fortes (`/hyperframes-keyframes`).
- Cocher l'option de divulgation « contenu généré par IA » de chaque plateforme (YouTube, TikTok, Instagram).

### Voix
La voix vient de l'outil choisi par Nass (à préciser). Ne jamais générer une voix qui imite Nass sans son accord explicite pour ce Short.

## Points à préciser avec Nass
- Outil d'avatar / de voix IA.
- Exemples de Shorts de référence (rythme, style de sous-titres) à ajouter dans `references/`.
