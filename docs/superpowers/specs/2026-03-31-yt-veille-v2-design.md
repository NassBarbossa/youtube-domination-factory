# YouTube Veille v2 — Design Spec

**Date** : 2026-03-31
**Statut** : En attente de validation
**Auteur** : Nass + Claude
**Remplace** : `2026-03-26-yt-veille-automation-design.md`

---

## Objectif

Refondre le système de veille YouTube pour :
1. Détecter les sujets trending US à répliquer en vidéo FR
2. Scorer chaque vidéo avec un composite basé sur 4 métriques expertes
3. Ne traiter (extraction topic + catégorisation) que les vidéos au-dessus du seuil
4. Permettre au LLM de générer un rapport éditorial à la demande
5. S'intégrer au bus de données de l'orchestrateur (`context/video-context.json`)

---

## Architecture

### Infra

- **Exécution** : VPS Hostinger (`72.62.253.227`)
- **Cron** : 1x/jour à 9h00 SGT (01:00 UTC)
- **BDD** : SQLite — un fichier `veille.db` sur le VPS
- **Source de données** : YouTube Data API v3 (données publiques)
- **Volume estimé** : 50 chaînes × 5 vidéos × 60 jours = ~15 000 lignes de snapshots, ~7-10 MB
- **Python** : 3.10+

### Pourquoi SQLite

- Le volume est petit (~15 000 lignes en 2 mois)
- Les JSON plats ne permettent pas les requêtes analytiques (trier, filtrer, agréger par topic)
- Le suivi historique (snapshots quotidiens) nécessite une structure relationnelle
- Zéro config, zéro serveur, un seul fichier

---

## Schéma BDD — SQLite

### Table `channels`

| Colonne | Type | Description |
|---|---|---|
| `channel_id` | TEXT PK | ID YouTube |
| `handle` | TEXT | Nom/handle de la chaîne |
| `subscribers` | INTEGER | Dernière valeur connue |
| `median_views` | REAL | Médiane des vues sur les 50 dernières vidéos |
| `avg_velocity` | REAL | Velocity moyenne des vidéos de la chaîne (vues/h sur les premiers jours) |
| `niche` | TEXT | Catégorie (claude-code, ai-tools, vibe-coding, etc.) |
| `added_at` | TEXT | Date d'ajout |
| `last_updated` | TEXT | Dernier update des stats |

### Table `videos`

| Colonne | Type | Description |
|---|---|---|
| `video_id` | TEXT PK | ID YouTube |
| `channel_id` | TEXT FK | Réf vers channels |
| `title` | TEXT | Titre de la vidéo |
| `description` | TEXT | Description complète |
| `tags` | TEXT | Tags (JSON array sérialisé) |
| `duration_seconds` | INTEGER | Durée en secondes |
| `published_at` | TEXT | Date de publication |
| `thumbnail_url` | TEXT | URL de la miniature |
| `category_id` | TEXT | Catégorie YouTube |
| `detected_at` | TEXT | Date du premier scrape |
| `topic` | TEXT | Sujet extrait (NULL si composite < 50) |
| `composite_score` | REAL | Score composite 0-100 (NULL avant calcul) |

### Table `snapshots`

| Colonne | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `video_id` | TEXT FK | Réf vers videos |
| `scraped_at` | TEXT | Date du scrape |
| `views` | INTEGER | Vues à cet instant |
| `likes` | INTEGER | Likes à cet instant |
| `comments` | INTEGER | Commentaires à cet instant |

Un snapshot par vidéo par jour. C'est cette table qui permet de calculer la view velocity (delta de vues entre deux scrapes successifs).

---

## Sourcing — API YouTube

### Données récupérées par vidéo

Un seul appel `videos.list` avec `part=snippet,statistics,contentDetails,topicDetails` :

| Donnée | Part API | Utilisée pour |
|---|---|---|
| Titre | snippet | Identification du sujet |
| Description | snippet | Identification du sujet |
| Tags | snippet | Identification du sujet |
| Date de publication | snippet | Calcul de la velocity |
| Thumbnail URL | snippet | Affichage |
| categoryId | snippet | Contexte |
| Durée | contentDetails | Contexte |
| Vues | statistics | Outlier, velocity, views/subs |
| Likes | statistics | Engagement rate |
| Commentaires | statistics | Engagement rate |
| Topics | topicDetails | Catégorisation secondaire |

### Données récupérées par chaîne

Appel `channels.list` avec `part=statistics` :

| Donnée | Utilisée pour |
|---|---|
| Abonnés | Views/subs ratio |
| Total vues | Contexte |
| Total vidéos | Contexte |

### Coût API estimé (50 chaînes)

- 50 × `channels.list` = 50 unités
- 50 × `playlistItems.list` = 50 unités
- ~250 vidéos × `videos.list` (batchées par 50) = 5 unités
- **Total : ~105 unités/jour** (1% du quota de 10 000)

---

## Scoring — Composite Score (/100)

### 4 métriques, pondération fixe

| Métrique | Poids | Calcul |
|---|---|---|
| **Outlier Score** | 40% | vues / médiane de la chaîne |
| **Velocity Ratio** | 25% | velocity vidéo / velocity moyenne de la chaîne |
| **Views/Subs Ratio** | 20% | vues / abonnés de la chaîne |
| **Engagement Rate** | 15% | (likes + commentaires) / vues × 100 |

### Sources des métriques

- **Outlier Score** : Paddy Galloway (consultant MrBeast), vidIQ (1.8M abonnés), 1of10.com
- **Velocity** : Sean Cannell (Think Media, 2.8M abonnés), Derral Eves ("The YouTube Formula", Wiley 2021)
- **Views/Subs** : 1of10.com (30% du sub count en 48h = signal fort)
- **Engagement** : vidIQ, Film Booth (700k abonnés)

### Normalisation — Seuils fixes avec interpolation linéaire

| Métrique | 0 | 25 | 50 | 75 | 100 |
|---|---|---|---|---|---|
| **Outlier Score** | ≤ 1x | 2x | 3x | 10x | ≥ 20x |
| **Velocity Ratio** | ≤ 1x | 2x | 3x | 8x | ≥ 15x |
| **Views/Subs Ratio** | ≤ 5% | 15% | 30% | 100% | ≥ 200% |
| **Engagement Rate** | ≤ 0.5% | 1.5% | 3% | 5% | ≥ 8% |

Interpolation linéaire entre les paliers. Capé à 100 au-dessus du max.

### Formule

```
composite = (outlier_norm × 0.40) + (velocity_norm × 0.25) + (views_subs_norm × 0.20) + (engagement_norm × 0.15)
```

Résultat : un score entre 0 et 100 par vidéo.

### Seuil de traitement

- **Composite > 50** → extraction du topic + catégorisation (étapes 3-4-5)
- **Composite ≤ 50** → reste dans la BDD, pas de traitement supplémentaire

Sur ~250 vidéos/jour, on estime ~15-30 vidéos au-dessus du seuil.

### Calcul de la velocity

La velocity d'une vidéo nécessite au minimum 2 snapshots :

```
velocity = (views_snapshot_N - views_snapshot_N-1) / heures_entre_les_2
```

La velocity moyenne d'une chaîne est calculée sur les vidéos avec suffisamment de snapshots. Les premiers jours de scrape seront moins fiables — stabilisation après ~1-2 semaines.

---

## Pipeline de traitement

### Cron daily (automatique)

```
1. Scrape 50 chaînes × 5 vidéos → SQLite (tables videos + snapshots)
2. Mise à jour stats chaînes (subscribers, median_views, avg_velocity)
3. Calcul du composite score pour chaque vidéo avec ≥ 2 snapshots
4. Si composite > 50 → extraction topic depuis titre + description (mots-clés)
5. Catégorisation du topic (claude-code, vibe-coding, ai-agents, ai-tools, ai-news, etc.)
6. Stockage du topic et du score dans la table videos
```

### Rapport LLM (à la demande, via `/yt-veille`)

```
1. Query SQLite : toutes les vidéos avec composite > 50, triées par score, sur les N derniers jours
2. Claude lit les données scorées
3. Claude interprète : regroupe par sujet, identifie les tendances, recommande les angles
4. Claude produit le rapport éditorial
```

---

## Intégration orchestrateur

Quand l'orchestrateur lance le Mode B (pas de topic fourni) :

1. yt-veille query la BDD pour les top vidéos récentes (composite > 50)
2. yt-veille (LLM) interprète et propose 3-5 idées
3. Nass choisit
4. yt-veille écrit dans `context/video-context.json` :

```json
{
  "veille": {
    "status": "idea_selected",
    "selected_idea": {
      "title": "Le titre provisoire de la vidéo FR",
      "source_video_id": "abc123",
      "source_channel": "AlexFinnOfficial",
      "composite_score": 87,
      "scores": {
        "outlier": 12.6,
        "velocity_ratio": 4.2,
        "views_subs_ratio": 1.23,
        "engagement_rate": 5.86
      },
      "topic": "claude-computer-use",
      "angle": "Pourquoi et comment ça change la donne pour les entrepreneurs",
      "format": "Tutorial",
      "hook_suggestion": "Claude peut maintenant contrôler ton ordinateur tout seul."
    }
  }
}
```

Le pipeline continue en Phase 1 (yt-script).

---

## Migration depuis la v1

### Ce qui change

| Avant (v1) | Après (v2) |
|---|---|
| JSON plats (channel_stats, last_check, backlog) | SQLite (`veille.db`) |
| Outlier ratio > 3x uniquement | Composite score /100 (4 métriques) |
| Pas de suivi historique des vues | Snapshots quotidiens |
| 6 chaînes | 50 chaînes |
| `part=statistics` seulement | `part=snippet,statistics,contentDetails,topicDetails` |
| Pas d'extraction de topic | Extraction mots-clés + catégorisation si score > 50 |
| Pas de rapport | LLM interprète les données à la demande |
| Pas de velocity | Velocity calculée via delta de snapshots |

### Ce qui reste

- Le cron daily sur le VPS
- L'API YouTube Data v3
- Le bus `context/video-context.json` pour l'orchestrateur
- Le script `discover_creators.py` (inchangé)
- La structure du SKILL.md (workflow manuel préservé)

### Migration des données existantes

Les données actuelles (6 chaînes, ~70 video IDs) seront importées dans SQLite lors du premier run. Les JSON plats seront conservés en backup mais plus utilisés.

---

## Structure des fichiers (après refonte)

```
youtube-domination-factory/
├── context/
│   ├── video-context.json          # Bus orchestrateur (inchangé)
│   └── archive/                    # Archives pipelines (inchangé)
├── yt-veille/
│   ├── SKILL.md                    # Mis à jour (workflow + rapport LLM)
│   ├── references/
│   │   └── sources.md
│   ├── memory/
│   │   ├── choices.json            # Feedback loop (inchangé)
│   │   └── lessons.json            # Feedback loop (inchangé)
│   └── scripts/
│       ├── daily_monitor.py        # Refait — scrape + scoring + SQLite
│       ├── discover_creators.py    # Inchangé
│       ├── youtube_api.py          # Étendu — récupère snippet + contentDetails + topicDetails
│       ├── database.py             # Nouveau — couche SQLite (init, insert, query)
│       ├── scoring.py              # Nouveau — normalisation + composite score
│       ├── topic_extractor.py      # Nouveau — extraction mots-clés + catégorisation
│       ├── json_io.py              # Conservé (pour channels.json, keywords.json)
│       ├── config/
│       │   ├── channels.json       # Étendu à 50 chaînes
│       │   └── keywords.json       # Inchangé
│       ├── data/
│       │   └── veille.db           # Nouveau — base SQLite
│       ├── .env.example
│       ├── .gitignore
│       └── requirements.txt
```

---

## Coût API — 50 chaînes

| Appel | Unités/jour |
|---|---|
| `channels.list` × 50 | 50 |
| `playlistItems.list` × 50 | 50 |
| `videos.list` × 5 batchs | 5 |
| **Total** | **~105** |
| **Quota disponible** | **10 000** |
| **% utilisé** | **~1%** |

---

## Hors scope (pour cette version)

- L'output (tableau HTML / Excel / format du rapport) — sera designé séparément
- Scraping Twitter/X, Reddit, HN, Anthropic blog
- Notifications (Telegram, email)
- Scoring LLM automatique dans le cron (le LLM intervient seulement à la demande)
- Mode cron autonome du SKILL.md (Sprint 2)
