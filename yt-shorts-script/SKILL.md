---
name: yt-shorts-script
description: Écrit des Shorts natifs verticaux (YouTube Shorts, TikTok, Reels, 30-60 s) pour la chaîne crypto de Nass Riviera, à partir de zéro, en série. Déclencheurs : « script short », « écris un short », « idée de short », « shorts en rafale », « bombarde les shorts », « script tiktok », « script reel », « short script ». Pas pour découper des Shorts dans une vidéo longue → yt-repurposing ; pas pour fabriquer la vidéo du Short → yt-shorts-montage.
metadata:
  author: NassRiviera
  category: youtube-workflow
  tags: [shorts, tiktok, reels, script, crypto, vertical]
  status: fondations — méthode de Nass à intégrer dans references/
---

# YT Shorts Script — scripts de Shorts natifs

**Cadre** : lis d'abord `C:\Users\User\youtube-domination-factory\_shared\cadre-nass.md` (narrative, avatar, offres, ton, règles de fond, charte). Il prime sur ce fichier.

Chemins relatifs = relatifs à la racine du repo `C:\Users\User\youtube-domination-factory`.

## Rôle

Écrire des **Shorts originaux** (tournés ou animés exprès, 30 à 60 s, vertical 9:16), en volume. `yt-repurposing` découpe des Shorts dans une vidéo longue ; `yt-shorts-montage` fabrique la vidéo à partir du script produit ici.

Règles propres aux Shorts :
- **Un Short = une seule idée**, compréhensible seul, sans avoir vu la chaîne.
- **Disclaimer** « Pas un conseil en investissement. » dans chaque script (overlay de fin).
- **Chiffres** : réels et datés (transaction on-chain, bougies d'exchange, CoinGecko/DexScreener), source notée dans `sources` pour le montage.
- **Pas de musique** dans le script (le montage met des sound effects).

## Méthode

**Fondations** : la méthode d'écriture (structures de hook, rythme, formats gagnants, exemples) sera fournie par Nass dans `references/`. Ne pas inventer de méthode maison : s'appuyer sur ce qui est dans `references/`, sinon demander à Nass. Ressources disponibles : aucune pour l'instant (voir `references/README.md`).

1. **Entrée** : un sujet de Nass, une idée de `yt-veille`, ou une série (ex. « 10 Shorts sur le wallet »).
2. **Écriture** : un script par Short au format ci-dessous. Quand Nass dicte, ses mots sont gardés tels quels.
3. **Validation** : Nass valide ou dicte ses corrections avant tout montage (`statut: valide`).

## Format de sortie (contrat avec `yt-shorts-montage`)

Fichier : `yt-shorts-script/outputs/[serie]/[NN]-[slug].md` (une série = un dossier).

```markdown
---
slug: c-est-quoi-un-wallet
serie: wallets
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

Marqueurs `VISUEL` reconnus par le montage : `[FACE CAM IA]` (avatar IA), `[SCREEN]` (capture d'écran réelle), `[CHART]` (graphique de prix réel daté), `[PUNK]` (avatar @punk6995), `[TEXTE]` (typo plein écran). Tout autre besoin visuel est décrit en clair.

Mouvements nommés (vocabulaire commun avec le montage, définis dans `yt-shorts-montage/references/motion-graphics-guide.md`) : **Kinetic Type, Rise, Pop, Count-up, Checklist, Typewriter, Slide-in, Blur-in, Punch-in, Reframe, Bar fill**. Ex. : `VISUEL : [TEXTE] Kinetic Type, puis Punch-in sur « jamais »`.

CTA de fin : selon le funnel du cadre (formation offerte, sa suite, ou communauté privée / Convergence), liens en placeholder `[lien …]`.

## Ce que le montage attend du script
- **Timecodes précis** : ils deviennent le bloc `<timing>` du brief XML du montage.
- Pour chaque `[CHART]` ou chiffre affiché : sa ligne dans `sources` (valeur, source, date).
- `effet_cle` renseigné : c'est l'effet que le montage teste en 1 seconde avant tout.
