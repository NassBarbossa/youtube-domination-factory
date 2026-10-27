---
name: yt-titres-seo
description: Génère des titres YouTube optimisés pour la recherche et le clic (7 titres de 30 à 60 caractères parmi 9 formules, type searchable ou intriguing, mot-clé principal et secondaires, retitrage et test A/B d'une vidéo publiée) pour la chaîne crypto de Nass Riviera. Déclencheurs : « titre vidéo », « trouve un titre », « titre YouTube », « optimise le titre », « retitre », « test A/B titre », « find a title », « SEO title », « title ideas ». Pas pour la description et les tags → yt-description ; pas pour le texte de la miniature → yt-miniature.
metadata:
  author: NassRiviera
  category: youtube-workflow
  tags: [titles, seo, youtube, crypto]
---

# YT Titres SEO

**Cadre** : lis d'abord `{repo}/_shared/cadre-nass.md` (narrative, avatar, offres, ton, règles de fond, charte). Il prime sur ce fichier.

Tu écris les titres YouTube de Nass Riviera : un titre qui se positionne en recherche et qui se fait cliquer, sans jamais trahir le contenu de la vidéo. Les mots sont ceux que tape un débutant (« crypto », « bitcoin », « acheter », « wallet », « investir »), pas du jargon de trader. Les règles de longueur et de forme viennent de sources lues le 20 octobre 2026 et des titres publiés de la chaîne : `references/veille-titres-2026-10-20.md`.

`{repo}` = racine du dépôt youtube-domination-factory (Mac : `~/youtube-domination-factory` · Windows : `C:\Users\User\youtube-domination-factory`) ; les chemins relatifs partent de là.

## Workflow

### 1. Analyse de l'entrée

Extraire du script ou du brief :
- le sujet et le mot-clé principal ;
- l'intention de l'audience (apprendre, découvrir, résoudre, comparer) ;
- l'angle différenciant (acheter hors des échanges, reconnaître un bon coin, acheter rarement, pont immobilier → crypto…) ;
- le déclencheur émotionnel (curiosité, peur de l'erreur, opportunité, surprise) ;
- le **type de titre**, que YouTube distingue : **searchable**, ce que l'avatar tape (tutoriel, geste on-chain, « c'est quoi un wallet ») ; **intriguing**, ce qui fait cliquer dans le fil (actu, avis, live, question ouverte). Au 13 octobre 2026, la recherche fait 3 % du trafic de la chaîne et 73 % des vues viennent des abonnés, de la playlist et de la page de chaîne : par défaut un titre intriguing, mot-clé devant quand même.

### 2. Mots-clés

- **Mot-clé principal** : ce que les gens tapent vraiment dans YouTube.
- **Mots-clés secondaires** : 3 à 5 variantes et longue traîne.
- **Titres concurrents** : ce qui se positionne déjà sur le sujet.
- **Signal de volume** : Élevé / Moyen / Faible, estimation qualitative (jamais de volume chiffré inventé).

Vérifier les mots-clés avec l'autocomplétion YouTube (WebFetch) : `https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=fr&q=<mot+clé+a>` (remplacer les espaces par `+`, parcourir quelques lettres).

Réservoir de départ (débutants FR) :

| Famille | Exemples |
|---------|----------|
| Découverte | crypto, crypto débutant, c'est quoi la crypto, bitcoin, comment investir en crypto, investir en crypto 2026 |
| Achat | acheter du bitcoin, acheter de la crypto, où acheter de la crypto, acheter une crypto avant son listing |
| Wallet / on-chain | wallet crypto, portefeuille crypto, wallet on-chain, Phantom, MetaMask, Ledger, seed phrase, DEX |
| Écosystèmes | Solana, Ethereum, altcoin, nouvelle crypto |
| Pont avec l'avatar | crypto ou immobilier, diversifier son patrimoine, investir quand on a déjà de l'immobilier |
| Sécurité / erreurs | arnaque crypto, erreur crypto débutant, sécuriser ses cryptos |

Jamais de mot-clé principal lié au levier, aux futures, au short, à la marge, au lending ou au trading spéculatif.

### 3. Génération : 7 titres pris parmi les 9 formules

Écrire **7 titres**, chacun construit sur l'une des 9 formules ci-dessous (au moins 5 formules différentes sur les 7).

| ID | Formule | Exemple |
|----|---------|---------|
| T1 | [Action concrète] en [temps] (sans [obstacle]) | « Mon 1er wallet en 10 min » |
| T2 | J'ai testé [X] pour toi — voici la vérité | « J'ai testé 3 wallets — la vérité » |
| T3 | [Grosse actu] : ce que ça change vraiment | « Halving : ce que ça change vraiment » |
| T4 | [Ce que tu fais] te coûte [perte] | « Ton exchange te fait acheter tard » |
| T5 | Pourquoi j'achète [X] (et pas le reste) | « Pourquoi j'ai acheté ce coin » |
| T6 | Stop [mauvaise pratique] — fais ça à la place | « Stop acheter tous les jours » |
| T7 | L'erreur que [groupe] fait avec [sujet] | « L'erreur des pros de l'immo en crypto » |
| T8 | [Preuve réelle et vérifiable] — voici comment | « Acheter hors exchange, preuve à l'appui » |
| T9 | [Sujet] en [année] : [la question qu'il se pose déjà] ? | « Or ou Bitcoin en 2026, que choisir ? » |

Notes :
- **T5** : un achat expliqué, jamais une invitation à copier. Il porte sur un achat réel de Nass, rare et réfléchi.
- **T8** : uniquement une preuve réelle (transaction on-chain, données de prix datées). Jamais de chiffre inventé, jamais de projection.
- **T9** : la question existe déjà chez l'avatar (l'autocomplétion la montre). C'est la forme de 4 des 5 titres publiés en octobre 2026, et le point d'interrogation est le signal le plus fort en éducation et finance dans les données lues. L'année seulement si le sujet est daté.

Exemples d'angles dans la narrative (à adapter, sans chiffres inventés) : « Acheter sa crypto hors des exchanges », « Reconnaître un bon coin », « Pourquoi j'achète si rarement », « Ton exchange arrive après tout le monde ».

### Mécanismes psychologiques (au moins 2 sur 3 par titre)

| Mécanisme | Description | Exemple |
|-----------|-------------|---------|
| Envie de résoudre | Créer une incertitude que le clic résout | Miniature qui montre un achat on-chain daté sans expliquer comment |
| Information gap | Écart entre ce que le spectateur sait et veut savoir | « Où j'achète avant le listing » > « Comment acheter de la crypto » |
| Biais négatif | Le cerveau priorise les menaces | « Ton exchange te fait acheter tard » > « Apprends à acheter on-chain » |

Le biais négatif pointe une erreur ou un coût réel (acheter tard, se faire arnaquer, perdre sa seed phrase), jamais une panique de marché.

### Check des 4 questions (au moins 2 sur 4)

1. **Gap** : qu'est-ce que je sais qu'ils ne savent pas ?
2. **Erreur** : en quoi ça défie leurs croyances (« la crypto, ça s'achète sur Binance ») ?
3. **Menace** : quelle perte font-ils maintenant (acheter après tout le monde, frais cachés, arnaques) ?
4. **Effort** : est-ce simple à consommer pour un débutant complet ?

### 4. Scoring

- **SEO** (1-5) : mots-clés recherchés par un débutant ?
- **Clic** (1-5) : cliquerais-tu dans un fil ?
- **Fidélité** (1-5) : correspond au contenu réel ?
- **Voix de Nass** (1-5) : direct, transparent, pas hype ?
- **Conformité** (OK / KO) : un KO élimine le titre (voir plus bas).

Le type décide du départage : SEO d'abord pour un titre searchable, Clic d'abord pour un titre intriguing.

### 5. Livraison

Tableau des 7 titres : titre (caractères + mots), formule (T1-T8), mécanismes activés, questions validées, une phrase sur pourquoi il fonctionne. Puis un **top 3** justifié (meilleur équilibre, meilleur clic, meilleur SEO), le **mot-clé principal** et les **mots-clés secondaires** (transmis à yt-description ; le titre gagnant est transmis à yt-miniature pour que la miniature le complète sans le répéter). Le top 3 est aussi la liste des candidats d'un test A/B (voir « Retitrage et test A/B »).

## Règles

- **30 à 60 caractères.** La promesse tient dans les 5 premiers mots : c'est ce qui reste quand YouTube tronque (« viewers may only see part of your title »). Les cinq titres publiés en octobre 2026 font 41 à 57 caractères ; les grandes bases donnent 30 à 60 caractères et 5 à 8 mots, et la seule corrélation longueur / performance mesurée est nulle (sources : `references/veille-titres-2026-10-20.md`).
- **Suffixe de marque ou d'épisode à la fin, jamais au début** (YouTube : « save episode numbers and branding for the end »). Replays Convergence : « [Question de l'épisode] CONVERGENCE [EP.NN] », sans le mot « podcast » (YouTube demande de l'enlever) ; le nom de l'invité va dans la description et les tags, dans le titre seulement si l'épisode porte sur lui.
- Langage simple et parlé ; si un terme technique est indispensable, le plus connu (« wallet », « bitcoin »).
- Émotion négative quand c'est pertinent (erreur, coût, arnaque), sans alarmisme de marché.
- Pas de listes « N cryptos à acheter ». Un chiffre réel et sourcé ou un délai concret (« en 10 min », « depuis 2017 ») est un plus en finance.
- Un mot en majuscules au plus, hors suffixe de marque ; pas de « !! », pas d'emoji (YouTube : « limit ALL CAPS and emoji »).
- Pas de clickbait trompeur : la vidéo tient la promesse.
- Le mot-clé principal apparaît naturellement, de préférence au début.
- Pas de mots creux (« incroyable », « dingue », « tu ne vas pas y croire »).
- Chiffres précis plutôt que promesses vagues (« 10 min » > « vite ») ; un chiffre de prix ou de performance n'apparaît que s'il est réel et sourcé.
- Si la vidéo porte sur un actif ou un outil précis (Bitcoin, Solana, Phantom…), son nom va dans le titre.
- L'année (« en 2026 ») pour un sujet daté : marché, actu, « que choisir cette année ». Jamais sur un tutoriel intemporel (wallet, seed phrase) : un titre daté vieillit en douze mois.
- Langue = langue de la vidéo (français par défaut, accents corrects).

Hypothèses à tester (pas des règles, voir `references/feedback-loop.md`) : chiffre impair, un ou deux mots forts, crochets, cadrage négatif.

## Conformité (application du cadre aux titres)

Un titre est éliminé, quel que soit son score, s'il :
- promet un gain (« deviens riche en 30 jours », « x100 garanti », « la crypto qui va exploser ») ;
- affiche un chiffre non vérifiable ;
- évoque levier, futures, short, marge, lending ou crédit ;
- utilise du vocabulaire de jeu (« pari », « jackpot », « all-in »…) ;
- porte sur un memecoin : dans ce cas, ne pas titrer et signaler le sujet à Nass.

Les titres de la formation offerte (« Pourquoi investir en 2026 », « Comment devenir riche », « L'investissement on-chain ») sont les mots de Nass : ils restent tels quels, sans délai ni montant ajouté.

## Retitrage et test A/B (vidéo déjà publiée)

Quand : une vidéo à fortes impressions et faible CTR (CTR lu dans Studio par `yt-analytics`), ou un titre qui ne dit pas le sujet (ép. 01 de Convergence : « CONVERGENCE [EP.01] : Podcast investissement w/ Sadek »).

1. Lire les données de la vidéo : impressions, CTR, part de la recherche et mots tapés. Si la recherche a amené des vues, garder ce mot-clé.
2. Produire 3 titres distincts dans la forme (question, affirmation, coût), pas trois variantes du même : des options trop proches font durer le test sans gagnant.
3. Proposer le test « Test & compare » de YouTube Studio (sur ordinateur, fonctionnalités avancées activées) : jusqu'à 3 titres, gagnant désigné au temps de visionnage et non au CTR, résultat en deux semaines au plus, « Winner », « Performed Same » ou « Inconclusive ». YouTube conseille de tester d'abord des vidéos anciennes ; les archives de lives sont éligibles ; changer le titre pendant le test l'arrête.
4. Dire à Nass qu'avec quelques centaines d'impressions le résultat sera souvent « Inconclusive » : dans ce cas on garde le titre le plus fidèle au contenu.
5. Logger dans `memory/choices.json` : `title_type`, `ab_test_candidates`, `ab_test_result`, `ab_test_winner`.

## Exemples

**Titre fort** : « Acheter sa crypto avant le listing, sans exchange » (49 caractères, 8 mots, intriguing, T8 si la transaction est montrée)
- SEO 4 : « acheter », « crypto », « listing », « exchange » sont des mots de l'avatar ; la promesse tient dans les 5 premiers mots.
- Clic 5 : promesse d'un accès en avance, gap fort, et « sans exchange » défie la croyance « la crypto, ça s'achète sur Binance ».
- Fidélité 5 : si la vidéo montre réellement un achat on-chain avant le listing, transaction à l'appui.
- Voix de Nass 5 : c'est exactement ce qu'il propose, sans hype.
- Conformité OK. Gap ✓ Erreur ✓.

**Titre fort** : « Or ou Bitcoin en 2026, que choisir ? CONVERGENCE [EP.03] » (56 caractères, 10 mots, T9, intriguing ; publié le 20 octobre 2026)
- La question existe déjà chez l'avatar, l'année est justifiée (sujet de marché), la marque est à la fin, un seul mot-clé fort par moitié de titre.

**Titre faible** : « Cette Crypto Va Faire x100 !!! »
- SEO 2, Clic 3 (attire le mauvais public), Fidélité 1, Voix 1.
- Conformité **KO** : promesse de gain → éliminé.

## Mode autonome (lancé par yt-orchestrator, Phase 2a)

La Phase 2a tourne **avant** yt-miniature et yt-description, qui lisent ta sortie.

- **Entrée** (lecture seule) : `context/video-context.json` → `_meta.slug`, `request.funnel`, `script.slug`, `script.file_path`, `script.structure.hook`, `script.word_count` (contrat complet : `context/SCHEMA.md`). Ne jamais écrire dans ce fichier : seul l'orchestrateur fusionne.
- **Travail** : workflow ci-dessus sans interaction ; générer 7 titres, éliminer les KO, choisir le `winning_title`.
- **Sortie** : écrire `context/runs/<slug>/titres_seo.json` et renvoyer ce JSON dans le message final.
- **Info manquante** : ne pas poser de question, la noter dans `open_questions[]`.

```json
{
  "status": "completed",
  "winning_title": "[30 à 60 caractères, promesse dans les 5 premiers mots, suffixe de marque à la fin]",
  "title_type": "searchable|intriguing",
  "all_titles": ["titre1", "titre2", "titre3", "titre4", "titre5", "titre6", "titre7"],
  "primary_keyword": "[mot-clé principal]",
  "secondary_keywords": ["mot-clé 1", "mot-clé 2", "mot-clé 3"],
  "open_questions": []
}
```

## Mode manuel

Appelé directement par Nass : workflow classique ci-dessus, avec interaction (présentation des 7 titres, Nass choisit).

## Feedback loop

Avant de générer, lire `yt-titres-seo/memory/lessons.json`. Après le choix de Nass, logger dans `yt-titres-seo/memory/choices.json` en mode manuel ; en mode pipeline, c'est l'orchestrateur qui logge en Phase 5. Format, critères d'analyse et hypothèses à tester : `yt-titres-seo/references/feedback-loop.md`.
