---
name: yt-calendrier
description: Planifie le calendrier éditorial YouTube (vidéos longues) et le pipeline de production de la chaîne crypto de Nass Riviera. Déclencheurs FR/EN — « calendrier », « planning vidéo », « quand publier », « plan de publication », « organise les prochaines vidéos », « schedule », « editorial calendar », « content plan ». Pas pour trouver des sujets → yt-veille ; pas pour analyser les stats → yt-analytics ; le rythme des Shorts natifs relève de yt-shorts-script.
metadata:
  author: NassRiviera
  category: youtube-workflow
  tags: [calendar, planning, schedule, editorial, crypto]
---

# YT Calendrier — calendrier éditorial et pipeline

**Cadre** : lis d'abord `{repo}/_shared/cadre-nass.md` (narrative, avatar, offres, ton, règles de fond, charte). Il prime sur ce fichier.

`{repo}` = racine du dépôt youtube-domination-factory (Mac : `~/youtube-domination-factory` · Windows : `C:\Users\User\youtube-domination-factory`) ; les chemins relatifs partent de là.

## Rôle

Stratège de contenu de Nass : penser en semaines et en mois, pas vidéo par vidéo. Donner du rythme, de la variété et une progression, en équilibrant actualité et éducation evergreen pour un débutant complet. Le live hebdo **Convergence** (avec Sadek) est un rendez-vous fixe.

## Rythme cible (à valider par Nass)

**Proposition de départ : 3 vidéos longues par semaine**, à ajuster selon la charge réelle (production + Convergence).

| Jour | Activité |
|---|---|
| Lundi | Analytics + préparation : perfs, choix des sujets, script en place |
| Mercredi | Vidéo principale : hook dans les 30 premières secondes (voir yt-script), contenu dense |
| Vendredi | 2e vidéo : format plus court ou tuto précis |
| Samedi | Engagement : réponses aux commentaires, communauté |
| Dimanche | 3e vidéo : format libre (questions de la communauté, retour d'expérience, coulisses) |

- **Convergence** : une fois par semaine (jour et heure à confirmer avec Nass). Le replay compte comme un contenu de la semaine.
- **Shorts découpés** dans les vidéos longues : suivent le planning de yt-repurposing (jours 1 à 3 après la vidéo) ; ici on note seulement leur date limite.
- **Shorts natifs** : ils ont leur propre rythme, géré par yt-shorts-script. Ne pas les planifier ici, sauf si Nass le demande.

## Workflow

### Step 1 : État des lieux

Demander à Nass :
- Fréquence actuelle ou visée
- Vidéos en cours (scriptées, tournées, montées)
- Événements à venir : annonces macro, décisions des banques centrales, conférences crypto, prochain Convergence
- Contraintes (voyages, semaines chargées, vacances)

### Step 2 : Mix de contenu

**Funnel** (répartition à valider par Nass, à recalibrer avec yt-analytics) :

| Niveau | Part des vidéos | Objectif | Exemples |
|---|---|---|---|
| TOP | ~60 % | Attirer des inconnus | « [Grosse actu crypto] : ce que ça change pour un débutant », « Ma première crypto achetée on-chain : voilà comment » |
| MIDDLE | ~30 % | Installer l'expertise, convertir en abonnés | « Acheter une crypto en dehors des échanges, pas à pas », « Pourquoi je n'achète pas tous les jours » |
| BOTTOM | ~10 % | Fidéliser | « Vos questions crypto — je réponds », « LIVE Convergence avec Sadek » |

Sujets TOP : partir de l'actualité, des questions de l'audience et des sujets de Nass. La veille automatique est en pause (désactivée par Nass) — ne pas la relancer sans qu'il le demande.

**Mix par type — proposition à valider par Nass** (à recalibrer ensuite avec yt-analytics) :

| Type | Part | Rôle | Exemple de sujet |
|---|---|---|---|
| Éducation débutant | 35 % | Evergreen, cœur de l'avatar (on part de l'immobilier et de la bourse) | « Crypto pour un investisseur immobilier : par où commencer » |
| Acheter en dehors des échanges | 25 % | La différenciation : pas à pas, sécurité, self-custody | « Ton premier achat on-chain, étape par étape », « Seed phrase : comment ne jamais la perdre » |
| Reconnaître un bon coin / pourquoi j'achète (rarement) | 20 % | La méthode : critères, patience, achats rares et réfléchis | « Comment je reconnais un bon coin », « Pourquoi je n'ai rien acheté ce mois-ci » (seulement si c'est vrai) |
| Actualité + Convergence | 15 % | Trafic d'actualité, crypto × or avec Sadek | « Ce que la décision de la Fed change pour ta crypto » |
| Questions de la communauté | 5 % | Engagement, fidélité | « Vos questions crypto — je réponds » |

Règles du mix :
- Un token jeune ou peu connu = position de petite taille, risque de tout perdre dit clairement, jamais de promesse de gain.
- Un sujet d'actualité qui touche à un interdit du cadre (levier, prêt à intérêt, jeu d'argent, crédit, memecoins) : soit on explique pourquoi on n'en fait pas, soit on le signale à Nass.
- Chaque mois, au moins une vidéo renvoie vers la formation offerte en 3 vidéos.

### Step 3 : Construire le calendrier

```
## Semaine [X] — [dates]

### Vidéo : [titre de travail]
- **Type** : Éducation débutant / Acheter en dehors des échanges / Reconnaître un bon coin / Actualité-Convergence / Communauté
- **Funnel** : TOP / MIDDLE / BOTTOM
- **Priorité** : haute (actualité) / moyenne (planifiée) / basse (backlog)
- **Statut** : idée / scriptée / tournée / montée / programmée / publiée
- **Publication** : [jour + heure]
- **Date limite repurposing** : [date — Shorts découpés, X, LinkedIn]
- **Notes** : [événement lié, suite d'une vidéo, etc.]
- **Cadre** : sujet conforme aux règles de fond ✓
```

### Step 4 : Horaires

- Jours souvent cités : mardi, jeudi, samedi ; horaires 14 h-16 h CET (bonnes pratiques générales, à recalibrer). L'avatar (25-40 ans, actif) regarde peut-être plutôt le soir et le week-end : vérifier dans YouTube Studio (« Quand vos spectateurs sont sur YouTube »).
- À éviter : lundi matin, vendredi soir.
- Exception : actualité crypto majeure (forte variation, hack, annonce réglementaire) → publier vite, ton pédagogique, ni panique ni hype.

### Step 5 : Vue pipeline

```
## Pipeline
### IDÉES (backlog)      - [ ] [sujet]
### SCRIPTÉES            - [ ] [sujet] — script fini [date]
### TOURNÉES             - [ ] [sujet] — tourné [date]
### MONTÉES              - [ ] [sujet] — montage fini [date]
### PROGRAMMÉES          - [ ] [sujet] — publication [date + heure]
### PUBLIÉES (4 sem.)    - [x] [sujet] — publiée [date] — [vues]
```

Le backlog de la chaîne est dans `context/backlog.json`.

## Règles

- Pas de planning détaillé au-delà de 4 semaines (le marché bouge trop vite).
- Backlog d'au moins 10 idées ; s'il baisse, le signaler et proposer de lancer yt-veille (recherche manuelle, la veille automatique reste en pause).
- Toujours un créneau « actualité » par semaine, échangeable si un gros sujet tombe.
- Pas trois vidéos lourdes d'affilée (risque d'épuisement).
- Suivre le mix : trop d'éducation → proposer un « acheter en dehors des échanges » ou un « bon coin » ; trop d'actualité → revenir à l'éducation.
- Une vidéo en retard vaut mieux qu'une vidéo bâclée.
- Signaler tout silence de plus de 10 jours sur la chaîne.
- KPI cibles : à recalibrer sur les données de la chaîne crypto (les anciens seuils venaient de la niche IA). Règle de titre conservée, à recalibrer sur la chaîne crypto : ≤ 30 caractères, 5 mots.
- Un sujet qui pose une question de fond (mécanisme de rendement flou, produit ambigu) : le signaler à Nass plutôt que de le planifier.

## Saisonnalité

| Période | Opportunité |
|---|---|
| Janvier | « Par où commencer en [année] », bilan de l'année (achats réels uniquement) |
| Avril-juin | Déclaration des cryptos en France (comptes à l'étranger, plus-values) — vérifier formulaires et dates de l'année |
| Printemps | Conférences crypto (dont Paris Blockchain Week, dates à vérifier) |
| Septembre | Rentrée : retour aux bases, relance de la formation offerte |
| Novembre-décembre | Bilan de l'année ; pas de contenu « promos d'exchange » type Black Friday |
| Toute l'année | Événements macro (Fed / BCE, inflation), Convergence |

## Mode manuel / autonome

Appelé directement par Nass : workflow classique ci-dessus, avec interaction. Ce skill n'a pas de section dans le pipeline de l'orchestrateur ; s'il est lancé par un agent, il ne pose pas de question et note les infos manquantes dans `open_questions[]`.
