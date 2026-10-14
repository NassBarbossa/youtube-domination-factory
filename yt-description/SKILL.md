---
name: yt-description
description: Écrit la description YouTube (hook, timestamps, offres, sources, bio) et les tags d'une vidéo de la chaîne crypto de Nass Riviera. Déclencheurs : « écris la description », « description YouTube », « tags vidéo », « write description », « YouTube description », « SEO description ». Pas pour le titre et le choix des mots-clés principaux → yt-titres-seo ; pas pour les posts X/LinkedIn → yt-repurposing.
metadata:
  author: NassRiviera
  category: youtube-workflow
  tags: [description, tags, seo, youtube, crypto]
---

# YT Description

**Cadre** : lis d'abord `{repo}/_shared/cadre-nass.md` (narrative, avatar, offres, ton, règles de fond, charte). Il prime sur ce fichier.

Tu écris des descriptions qui servent à la fois l'algorithme et le spectateur : une mini landing page qui vend la vidéo, nourrit la recherche YouTube et renvoie vers les offres de Nass (formation offerte, communauté privée, Convergence).

`{repo}` = racine du dépôt youtube-domination-factory (Mac : `~/youtube-domination-factory` · Windows : `C:\Users\User\youtube-domination-factory`) ; les chemins relatifs partent de là.

## Workflow

### 1. Collecte

Depuis le script ou le brief :
- titre et mots-clés (depuis yt-titres-seo si disponibles) ;
- sujets clés et timestamps (structure du script) ;
- outils, wallets, explorateurs, docs officielles et données citées (URLs) ;
- transactions ou adresses montrées à l'écran (à lier sur l'explorateur) ;
- funnel de la vidéo (TOP / MIDDLE / BOTTOM) pour choisir l'offre mise en avant.

### 2. Enrichissement des mots-clés (autocomplétion YouTube)

Enrichir le mot-clé principal avec les vraies requêtes YouTube :

1. **Autocomplétion** : WebFetch sur `https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=fr&q=<mot+clé+a>` (espaces → `+`), en faisant varier la lettre finale (a, b, c…) et en testant aussi le mot-clé seul. La réponse est une liste JSON de suggestions = requêtes réelles.
2. **Recherches associées** et questions qui reviennent dans les résultats sur le mot-clé principal.

Objectif : 3 à 5 mots-clés longue traîne intégrés naturellement (pas de bourrage : chaque mot-clé sert une phrase utile). Exemples typiques pour l'avatar : « comment acheter de la crypto quand on débute », « wallet crypto pour débutant », « crypto ou immobilier », « acheter une crypto avant son listing ». Jamais de volume de recherche inventé.

### 3. Rédaction

Structure :

```
[LIGNES 1-2 : hook PAS / AIDA / BAB + mot-clé principal dans la 1re phrase — ce qui s'affiche dans les résultats]
[LIGNE 3 : proposition de valeur — pourquoi regarder]

[TIMESTAMPS]
0:00 - Hook
X:XX - [Titre de section]
...

[RESSOURCES & LIENS — propres à la vidéo]
- Outil / wallet / explorateur mentionné : [URL]
- Transaction montrée dans la vidéo : [lien explorateur — Solscan, Etherscan…]
- Vidéo liée : [URL]

[SOURCES & RÉFÉRENCES — propres à la vidéo]
- [Doc officielle / donnée on-chain citée] : [URL]
- [Article / rapport mentionné] : [URL]

[BLOC FIXE — mots de Nass (2026-10-14), à coller tel quel, sans retouche]
Je m'appelle Nass. Investisseur et entrepreneur depuis 10 ans, premiers bitcoins en 2017, je vis de mes investissements depuis 6 ans.

Formation offerte : https://youtube.com/playlist?list=PLH8HsDRAJ7R8&si=jjiYTJrG2VJlceau

Sur cette chaîne, j'explique comment investir simplement, avec une méthode : gérer son argent, investir chaque mois (DCA) et acheter des cryptos on-chain avant les autres. Du bon sens, de vrais chiffres et mes propres résultats.

Suis-moi sur mes différents réseaux 👇
📊 Site : https://nassriviera.com/
✈️ Telegram → https://t.me/punk6995trades
📸 Instagram → https://www.instagram.com/nass.riviera/
📲 X / Twitter → https://x.com/punk6995

💬 Dis-moi en commentaire où tu en es : jamais investi, déjà en DCA, ou déjà on-chain ?
👍 Abonne-toi pour la suite !!

⚠️ Ceci n'est pas un conseil en investissement. Les cryptos sont des actifs volatils : n'investis que ce que tu peux te permettre de perdre.

#crypto #investir #memecoins
```

Le bloc fixe est la bio et les liens de Nass : il se colle tel quel, dans cet ordre, sans rien reformuler ni ajouter. Seuls le hook, les timestamps, les ressources et les sources changent d'une vidéo à l'autre. Le disclaimer est déjà dans le bloc fixe : ne pas le répéter.

### Hook (lignes 1-3) : un framework par description

| Framework | Structure | Quand | Exemple |
|-----------|-----------|-------|---------|
| PAS | Problème → Agitation → Solution | Tutos | « Tu veux acheter de la crypto mais tu n'y comprends rien → et sur un exchange, tu achètes après tout le monde → je te montre comment acheter on-chain, en dehors des échanges » |
| AIDA | Attention → Intérêt → Désir → Action | Actus | « Le halving vient de passer → voici ce qui change concrètement → et pourquoi ça ne veut pas dire acheter tout de suite » |
| BAB | Avant → Après → Pont | Parcours | « Avant : 100 % immobilier → Après : une première crypto achetée on-chain → voici par où commencer » |

Le mot-clé principal apparaît dans la première phrase. Le hook ne promet jamais de gain.

### CTA

L'offre mise en avant suit le funnel du cadre (TOP → formation offerte · MIDDLE → la suite de la formation offerte · BOTTOM → communauté privée et Convergence). Le CTA de fin s'adapte au type de vidéo :

| Type de vidéo | CTA principal | CTA secondaire |
|---------------|---------------|----------------|
| Tuto | « Commence par la formation offerte en 3 vidéos (lien ci-dessus) » | « Abonne-toi pour le prochain tuto » |
| Actu | « Dis-moi en commentaire ce que tu en penses » | « On en parle en live dans Convergence, avec Sadek » |
| Deep dive / analyse | « Partage à un ami qui investit déjà dans l'immo et qui n'a jamais touché à la crypto » | « Abonne-toi si tu veux aller plus loin » |
| Live Convergence | « Rejoins le prochain live Convergence » | « La communauté privée, pour aller plus loin » |
| Comparatif | « Dis-moi en commentaire quel wallet tu utilises » | « Abonne-toi pour les prochains tests » |

### Sources & références

Minimum 2 sources vérifiables : docs officielles, transactions et adresses sur explorateur, données de marché datées (CoinGecko, CoinMarketCap…), articles qui ont inspiré l'angle. Pas de liens morts. Les liens affiliés vont dans « Ressources & liens », signalés comme affiliés, jamais déguisés en sources.

### 4. Tags (15-20, 500 caractères max, les plus importants en premier)

1. **Exact match** (3-5) : les phrases exactes que les gens tapent.
2. **Larges** (3-5) : crypto, bitcoin, investir…
3. **Chaîne** (3-5) : tags récurrents ci-dessous.
4. **Longue traîne** (3-5) : phrases de niche, dont les mots-clés de l'étape 2.

Tags récurrents de la chaîne : crypto, cryptomonnaie, investir en crypto, crypto débutant, bitcoin, acheter de la crypto, wallet crypto, investissement on-chain, on-chain, nass riviera.

Consigne interne : jamais de tags, de mots-clés ou de liens liés au levier, aux futures, au short, au lending ou au casino, même s'ils ont du volume.

### 5. Livraison

- La description complète, prête à coller.
- Les tags, séparés par des virgules.
- L'aperçu des 150 premiers caractères.
- La check-list : disclaimer présent une fois, aucune promesse de gain, aucun chiffre non sourcé, aucun lien ou tag interdit.

## Règles

- **Les 150 premiers caractères** s'affichent dans les résultats : mot-clé principal et valeur en tête. Le titre gagnant fait ≤ 30 caractères, la description compense en SEO.
- **Disclaimer** : « Pas un conseil en investissement. », une seule fois, juste après les timestamps (visible sans dérouler).
- **Longueur** : 300 à 500 mots, et sous 5 000 caractères (limite YouTube).
- Écrire pour les humains d'abord : pas de bourrage de mots-clés.
- Toujours des timestamps (YouTube met en avant les vidéos chapitrées).
- 1-2 hashtags max (#crypto + un hashtag du sujet, ex. #bitcoin ou #solana).
- Pas de mention « spot, zéro levier, halal » dans le texte (le cadre s'applique en silence), sauf si c'est le sujet de la vidéo.
- Langue = langue de la vidéo (français par défaut, accents corrects).

## Mode autonome (lancé par yt-orchestrator, Phase 2c)

yt-titres-seo (Phase 2a) a déjà tourné : ses sorties sont disponibles.

- **Entrée** (lecture seule) : `context/video-context.json` → `_meta.slug`, `request.funnel`, `script.slug`, `script.file_path`, `script.structure.timestamps_raw[]`, `titres_seo.winning_title`, `titres_seo.primary_keyword`, `titres_seo.secondary_keywords[]` (contrat complet : `context/SCHEMA.md`). Ne jamais écrire dans ce fichier : seul l'orchestrateur fusionne.
- **Travail** : workflow ci-dessus sans interaction (enrichissement des mots-clés, description, tags, vérification de la check-list ; corriger avant d'écrire si un point échoue).
- **Sortie** : écrire `context/runs/<slug>/description.json` et renvoyer ce JSON dans le message final.
- **Info manquante** (lien, timestamp, source) : ne pas poser de question, garder le placeholder et la noter dans `open_questions[]`.

```json
{
  "status": "completed",
  "description_full": "[description complète — 300 à 500 mots]",
  "first_150_chars": "[150 premiers caractères]",
  "hook_framework": "PAS|AIDA|BAB",
  "tags": ["tag1", "tag2", "tag3"],
  "enriched_keywords": ["longue traîne 1", "longue traîne 2", "longue traîne 3"],
  "sources": ["https://source1", "https://source2"],
  "cta_type": "tuto|actu|deep-dive|live|comparatif",
  "open_questions": []
}
```

## Mode manuel

Appelé directement par Nass : workflow classique ci-dessus, avec interaction.
