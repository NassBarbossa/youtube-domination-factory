---
name: yt-shorts-script
description: Write native vertical Shorts scripts (YouTube Shorts, TikTok, Reels, 30-60 s) for Nass Riviera's crypto channel. Use when user says "script short", "écris un short", "idée de short", "shorts en rafale", "bombarde les shorts", "script tiktok", "script reel", "short script", or wants a short-form video written from scratch (not cut from a long video — that is yt-repurposing).
metadata:
  author: NassRiviera
  version: 0.1.0
  category: youtube-workflow
  tags: [shorts, tiktok, reels, script, crypto, vertical]
  status: fondations — ressources de Nass à intégrer
---

# YT Shorts Script — scripts de Shorts natifs

## Rôle

Écrire des **Shorts originaux** (tournés ou animés exprès, 30 à 60 s, format vertical 9:16) pour la chaîne crypto de Nass Riviera, en volume.

Frontières avec les autres skills :
- **`yt-repurposing`** découpe des Shorts **dans une vidéo longue existante**. Ici, on écrit un Short **à partir de zéro**.
- **`yt-shorts-montage`** prend le script produit ici et fabrique la vidéo. Ce skill ne fait pas de montage.

## Cadre commun (ne pas dupliquer : la source est `CLAUDE.md`)

À relire avant chaque série, dans `CLAUDE.md` :
- **Positionnement & avatar** : avatar client dans les mots de Nass (hommes 25-40 ans, investisseurs immobilier, débutants en crypto ; on vend l'achat on-chain avant que ce soit connu de tous).
- **Règle halal (non négociable)** : spot uniquement, aucun levier/short/lending/casino, tokens spéculatifs présentés comme paris risqués à petite taille, aucun chiffre inventé.
- **Content Voice** : direct, transparent, pédagogique. Les mots de Nass sont sacrés : quand il dicte, on garde ses mots (seules l'orthographe et les fautes de dictée évidentes sont corrigées, et on le dit).

Règles propres aux Shorts :
- **Disclaimer** « Pas un conseil en investissement. » présent dans chaque script (overlay prévu pour le montage).
- **Un Short = une seule idée.** Il doit se comprendre seul, sans avoir vu la chaîne.
- **Chiffres** : uniquement réels et datés (wallet public, données on-chain, bougies d'exchange), avec la source notée pour le montage.

## Méthode

> ⚠️ **Fondations.** Les techniques d'écriture (structures de hook, rythme, formats gagnants, exemples de référence) seront fournies par Nass et intégrées dans `references/`. En attendant, ne pas inventer de « framework maison » : demander à Nass ou s'appuyer uniquement sur ce qui est dans `references/`.

1. **Entrée** : un sujet donné par Nass, ou une idée issue de `yt-veille`, ou une série (ex. « 10 Shorts sur le wallet »).
2. **Écriture** : un script par Short au format de sortie ci-dessous.
3. **Validation** : Nass valide ou dicte ses corrections avant tout passage au montage.

## Format de sortie (contrat avec `yt-shorts-montage`)

Fichier : `yt-shorts-script/outputs/[serie]/[NN]-[slug].md` (une série = un dossier).

```markdown
---
slug: wallet-public-explique
serie: wallet
duree_cible: 45        # secondes
format: anime | facecam-ia | mixte   # anime = cas principal ; facecam-ia = avatar IA (Nass ne tourne pas)
voix: aucune | voix-ia             # voix-ia : outil choisi par Nass
statut: brouillon | valide
sources: []            # une ligne par chiffre affiché : valeur, source, date
effet_cle: ""          # l'effet visuel le plus difficile (testé en 1 s au montage)
---

# [Titre de travail du Short]

## Hook (0-3 s)
TEXTE À L'ÉCRAN : …
VOIX : …

## Corps
[00:03] VOIX : …   | ÉCRAN : …   | VISUEL : …
[00:12] VOIX : …   | ÉCRAN : …   | VISUEL : …

## Fin (CTA)
VOIX : …
ÉCRAN : … + « Pas un conseil en investissement. »

## Légende & hashtags
…
```

Marqueurs `VISUEL` reconnus par le montage : `[FACE CAM IA]` (avatar IA, Nass ne tourne pas), `[SCREEN]` (capture d'écran réelle), `[CHART]` (graphique de prix réel daté), `[PUNK]` (avatar @punk6995), `[TEXTE]` (typo plein écran). Tout autre besoin visuel est décrit en clair.

Mouvements nommés (vocabulaire commun avec le montage, voir `yt-shorts-montage/references/motion-graphics-guide.md`) : **Rise, Pop, Count-up, Checklist, Typewriter, Slide-in, Blur-in, Punch-in, Reframe, Bar fill**. Ex. : `VISUEL : [TEXTE] Kinetic, puis Punch-in sur « jamais »`.

Pas de musique dans les Shorts (mais des sound effects au montage) : ne jamais prévoir de musique dans le script.

## Ce que le montage attend du script
- Les **timecodes** du script deviennent le bloc `<timing>` du brief XML du montage : les écrire précisément.
- Pour chaque `[CHART]` ou chiffre affiché : la ligne correspondante dans `sources` (valeur, source, date).
- L'effet visuel le plus difficile du Short doit être signalé (`effet_cle:` dans l'en-tête) : c'est lui que le montage teste en 1 seconde avant tout.

## Ressources à venir (Nass)

`references/` accueillera les ressources fournies par Nass (méthodes de scripts courts, exemples, hooks). Chaque ressource ajoutée doit être citée dans la section « Méthode » ci-dessus.
