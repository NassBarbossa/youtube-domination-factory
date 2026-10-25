---
name: yt-repurposing
description: Découpe une vidéo YouTube longue (script ou vidéo publiée) en Shorts recyclés TikTok/Reels, thread X @punk6995 et post LinkedIn. Déclencheurs FR/EN — « repurpose », « découpe en shorts », « découpe la vidéo », « thread X », « post LinkedIn », « adapte le contenu », « clip it », « repurpose this video ». Pas pour écrire des Shorts originaux (natifs, sans vidéo longue) → yt-shorts-script.
metadata:
  author: NassRiviera
  category: youtube-workflow
  tags: [repurposing, shorts, twitter, linkedin, multi-platform, crypto]
---

# YT Repurposing — une vidéo longue, plusieurs plateformes

**Cadre** : lis d'abord `{repo}/_shared/cadre-nass.md` (narrative, avatar, offres, ton, règles de fond, charte). Il prime sur ce fichier.

`{repo}` = racine du dépôt youtube-domination-factory (Mac : `~/youtube-domination-factory` · Windows : `C:\Users\User\youtube-domination-factory`) ; les chemins relatifs partent de là.

## Mission

Transformer une vidéo YouTube longue en :
1. 1 à 3 Shorts découpés dans la vidéo, recyclés en TikTok et Instagram Reels
2. 1 thread X sur @punk6995
3. 1 post LinkedIn (angle patrimoine), ou aucun si le sujet ne s'y prête pas
4. Optionnel : carrousel, extrait newsletter, teaser du live Convergence

Chaque plateforme a son langage : jamais de copier-coller, jamais le titre de la vidéo repris tel quel.

Épisode du live Convergence (Nass + Sadek) : le choix et le montage des Shorts passent par `clip-convergence` ; ce skill garde le thread X, le post LinkedIn et le planning.

## Application du cadre à ce skill

- Disclaimer « Pas un conseil en investissement. » une fois par contenu : overlay ou légende du Short, dernier tweet du thread, fin du post LinkedIn.
- Pas de « spot, zéro levier, halal » plaqué dans les contenus ; pas d'appel à acheter un token précis, jamais d'adresse de contrat (CA) présentée comme une invitation à acheter.
- Chiffres affichés = réels et datés, source notée (transaction on-chain, bougies d'exchange, CoinGecko/DexScreener/CoinStats).
- Un token jeune évoqué = position de petite taille, risque de tout perdre dit clairement. Un sujet qui touche aux memecoins : le signaler à Nass au lieu de le traiter.
- CTA selon `request.funnel` : TOP → formation offerte · MIDDLE → suite de la formation offerte · BOTTOM → communauté privée + Convergence. Liens pris dans la table « Liens » du cadre, placeholder `[lien …]` pour ceux qui manquent, jamais inventés.

## Workflow

### Step 1 : Script mining

Extraire du script :
- **Moments citables** : affirmations fortes, chiffres réels, prises de position (« l'exchange, c'est souvent là où tu achètes en dernier »)
- **Insights autonomes** : compréhensibles sans le reste de la vidéo
- **Moments de démo** : achat on-chain à l'écran, transaction sur l'explorateur
- **Arcs narratifs** : un achat rare expliqué (pourquoi celui-là, pourquoi maintenant, pourquoi pas les autres), une erreur de débutant

### Step 2 : Shorts (1-3, découpés dans la vidéo longue)

```
## Short [X] : [Titre de travail]

**Source** : section du script [X] (timestamp XX:XX - XX:XX)
**Hook** (2 premières secondes, 5-7 mots) : [voir formules]
**Contenu** (40-50 s) : [le point clé, condensé]
**Punchline / CTA** (5 dernières secondes) : [renvoi vers la vidéo complète]
**Texte à l'écran** : [phrase clé]
**Disclaimer** : overlay « Pas un conseil en investissement. » (dès qu'on parle d'un actif, d'un achat ou d'un prix)
**Durée** : 45-59 s
**Sous-titres** : obligatoires (intégrés au montage ou auto-caption)

### Notes de découpe
- [ ] Découpable directement / à recadrer en vertical
- [ ] Démo écran (wallet, explorateur) lisible en vertical
- [ ] Aucune adresse, seed phrase ou info privée visible
```

**Formules de hook (5-7 mots, première frame)** :

| Formule | Exemple |
|---|---|
| « Stop scrolling si tu [action] » | « Stop scrolling si tu achètes sur exchange » |
| « [Action concrète] en [temps] » | « Ton premier wallet en 10 minutes » |
| « Personne ne te dit ça sur [sujet] » | « Personne ne te dit ça sur les listings » |
| « Attends la fin » | « J'ai acheté avant le listing — attends la fin » |
| « [Chiffre] [chose] que tu fais mal » | « 3 erreurs de débutant en crypto » |
| « J'ai testé [X] — voici le résultat » | « J'ai testé un DEX — voici le résultat » |

Si le hook ne tient pas en 5-7 mots, il est trop compliqué. Un hook chiffré n'utilise que des chiffres réels et datés.

**Sélection** : on garde un moment seulement s'il fonctionne sans le reste de la vidéo, accroche dans les 2 premières secondes, chute avant 60 s, donne envie d'être partagé et respecte le cadre.

**Recyclage TikTok / Reels** :
- Fichier exporté du montage (sans filigrane), pas re-téléchargé depuis YouTube
- Légende : 1 phrase d'accroche + disclaimer + hashtags (voir règle ci-dessous)
- CTA : formation offerte ou chaîne YouTube (lien en bio), jamais un achat précis
- Texte dans la zone sûre (ni en bas, ni à droite, couverts par l'interface)
- Aucune promesse de gain, aucun « lien pour acheter ce token » (contenu financier très encadré sur ces plateformes)

### Step 3 : Thread X (@punk6995)

Compte crypto de Nass (avatar punk pixel Barbossa). Ton plus crypto-natif que YouTube : phrases courtes, vocabulaire on-chain autorisé (wallet, DEX, listing), toujours direct et posé. Pas de shill, pas de « gm ser x100 ».

**Le lien de la vidéo va dans un reply séparé, jamais dans le thread** (les liens externes réduiraient la portée — hypothèse à tester).

```
## Thread X : [Sujet]

**Tweet 1 (hook)** — 71-100 car. : affirmation forte ou question, tient seul
**Tweets 2-5 (valeur)** — 71-100 car. chacun : un insight par tweet, chiffres réels, retours à la ligne
**Tweet 6 (CTA sans lien)** : raison de regarder la vidéo (« Je montre l'achat on-chain en entier, étape par étape ») + question ouverte + « Pas un conseil en investissement. »
**Reply séparé** : « Vidéo complète ici » + [lien vidéo]
```

Règles : chaque tweet tient seul ; pas de numérotation « 1/ » ; flèches (→) ou puces ; 6 tweets max + le reply ; finir par une question ouverte ; répondre aux premiers commentaires.

**Signaux de l'algo X (hypothèses à tester, sources non vérifiées)** : les replies pèsent bien plus que les likes ; les bookmarks comptent ; les 30 premières minutes décident de la portée ; au-delà de 5-8 posts par jour, la visibilité baisserait.

### Step 4 : Post LinkedIn (angle patrimoine)

Une partie de l'avatar (25-40 ans, cadres ou entrepreneurs, déjà investisseurs en immobilier) est sur LinkedIn. On parle patrimoine, diversification, méthode, transparence ; on part de l'immobilier et de la bourse pour expliquer la crypto. Jamais de crédit encouragé, jamais de rendement promis, pas de jargon de trader.

Si le sujet n'a pas d'angle patrimonial : pas de post (`linkedin_full` vide, `linkedin_format_bonus: "none"`) et le dire.

Génération via la Content Machine : voir `references/content-machine.md`.

```
## Post LinkedIn

**Hook** (≤ 210-235 car., avant « …voir plus ») : constat, chiffre réel, prise de position
  ex. « J'ai des amis qui ont trois appartements et zéro euro en crypto. Ils m'ont tous posé la même question. »
**Corps** (1300-1600 car.) : angle patrimoine, pont immobilier/bourse → crypto, expérience de Nass, preuves vérifiables, 1 phrase par ligne, disclaimer en fin
**CTA** : question ouverte + [lien vidéo]
**Hashtags** : 3-5 en fin de post
**Format bonus** (si pertinent) : carrousel PDF (étapes, comparatif immo vs crypto), sondage (« Tu as déjà de la crypto dans ton patrimoine ? »), image 1200×627 (schéma, transaction)
```

Règles : un cran plus posé que YouTube ; 1-2 emojis max ; à la première personne ; commencer par l'insight, jamais par « Je viens de publier une vidéo sur… ».

**Repères LinkedIn (hypothèses à tester, sources non vérifiées)** : carrousels PDF et sondages auraient la meilleure portée ; lecture majoritairement mobile (d'où 1 phrase par ligne) ; 1300-1600 caractères serait la zone la plus engageante, au-delà de 2000 l'engagement baisserait.

Images : single 1200×627, carrousel 1200×1200 ou 1080×1350, vertical préféré. Les crops viennent de la miniature 1280×720 (yt-miniature).

### Hashtags — une règle par plateforme

| Plateforme | Règle |
|---|---|
| Short YouTube | Aucun hashtag requis |
| TikTok / Reels | 3-5 en fin de légende (#crypto #bitcoin + sujet) |
| X | Aucun hashtag |
| LinkedIn | 3-5 en fin de post, jamais au début |

### Step 5 : Livraison

Dans l'ordre : Shorts (instructions de découpe + notes TikTok/Reels), thread X prêt à copier, post LinkedIn prêt à copier (ou « pas de post », justifié), planning.

**Planning de publication** (à recalibrer sur la chaîne crypto) :
- Jour 0 : la vidéo sort
- Jour 0 (+2 h) : thread X
- Jour 1 : post LinkedIn
- Jours 1-3 : un Short par jour, jamais le jour même (ils renvoient vers la vidéo), republié le même jour sur TikTok et Reels

### Step 6 : Export du document

Créer un document `[Repurposing] {titre de la vidéo}` via Google Drive (`create_file`) ou Claude Docs, selon ce qui est connecté. Contenu en texte brut : SHORTS (titre, hook, contenu, punchline, texte à l'écran, source), THREAD X (+ reply lien), POST LINKEDIN, PLANNING. Annoncer le lien à Nass. Si aucun connecteur n'est disponible, livrer le texte et le dire (en autonome : `open_questions[]`).

## Limites de caractères

| Plateforme | Limite | Zone visée |
|---|---|---|
| Titre de Short | 100 | 40-60 |
| Hook de Short | — | 5-7 mots |
| Tweet | 280 | 71-100 |
| Thread X | 6 tweets + 1 reply | ~80 car./tweet |
| Hook LinkedIn | 210-235 | 140-210 |
| Post LinkedIn | 3000 | 1300-1600 |

## Exemples

**Bon hook de Short** : « J'ai acheté ce token on-chain trois semaines avant son listing. »
→ Visuel, précis. Seulement si c'est vrai, transaction on-chain datée à l'appui, et avec la suite qui dit le risque (petite taille, possibilité de tout perdre) et que ce genre d'achat reste rare.

**Mauvais hook de Short** : « Aujourd'hui je vais vous parler du Bitcoin. » → zéro curiosité.

**Bonne ouverture de thread** :
« Je n'achète pas de crypto tous les jours.

De temps en temps, quand il y a une vraie opportunité.

Et presque jamais sur un exchange.

Voici comment je fais le tri →»

**À ne jamais faire** : « Nouvelle vidéo ! Ce token va faire x100, CA dans le thread 🚀 » → promo pure, promesse de gain, appel à acheter.

## Mode autonome (lancé par yt-orchestrator, Phase 4)

- Lire `context/video-context.json` en **lecture seule** : `script.slug`, `script.structure` (dont `shorts_moments[]`), `titres_seo.winning_title` (titre validé, à utiliser dans les CTA), `request.funnel`.
- Dérouler Steps 1 à 6 sans interaction. LinkedIn : une seule proposition (voir `references/content-machine.md`).
- Écrire la section dans `context/runs/<slug>/repurposing.json` et renvoyer ce JSON dans le message final. Ne jamais écrire dans `context/video-context.json`.
- Aucune question : toute info manquante ou tout doute (sujet memecoin, chiffre non sourcé, connecteur absent) va dans `open_questions[]`.

```json
{
  "status": "completed",
  "shorts": [
    {
      "number": 1,
      "title": "",
      "hook": "",
      "content": "",
      "punchline": "",
      "text_overlay": "",
      "source_timestamp": "MM:SS - MM:SS"
    }
  ],
  "x_thread_hook": "",
  "x_thread_full": "6 tweets max, sans lien",
  "x_reply_link": "Vidéo complète ici : [lien vidéo]",
  "linkedin_hook": "",
  "linkedin_full": "",
  "linkedin_format_bonus": "carousel|poll|image|none",
  "posting_schedule": {
    "day_0_youtube": "",
    "day_0_x_thread": "",
    "day_1_linkedin": "",
    "day_1_3_shorts": ""
  },
  "google_doc_url": null,
  "open_questions": []
}
```

## Mode manuel

Appelé directement par Nass : workflow classique ci-dessus, avec interaction (Nass valide les Shorts retenus et choisit entre les deux variantes LinkedIn).
