# YouTube Veille Automation — Design Spec

**Date** : 2026-03-26
**Statut** : En attente de validation
**Auteur** : Nass + Claude

---

## Objectif

Automatiser la veille YouTube pour détecter les nouvelles vidéos des créateurs suivis, identifier les outliers, et découvrir de nouveaux créateurs pertinents dans la niche AI/Claude Code/VibeCoding.

## Contexte

- La veille est actuellement 100% manuelle via le skill `yt-veille`
- Le skill définit des sources et un format de scoring (Relevance/Audience/Timing sur 5)
- Le repo `youtube-domination-factory` contient déjà la structure de pipeline avec `context/video-context.json`
- Audience cible : hommes 26-35, entrepreneurs/executives, non-techniques

## Architecture

### Infra

- **Exécution** : VPS Hostinger (`72.62.253.227`), cohabite avec `openclaw.service`
- **Cron** : 1x/jour à 9h00 SGT (UTC+8) = 01:00 UTC
- **Source de données** : YouTube Data API v3 exclusivement
- **Quota API** : ~620 unités/jour estimées sur 10 000 disponibles (6.2%)

### Sécurité

- Clé API YouTube et GitHub token stockés dans `.env` sur le VPS uniquement
- `.env` dans `.gitignore` — jamais commité
- Le code lit les secrets via `os.environ` uniquement
- Un fichier `.env.example` (sans secrets) sert de template

---

## Script 1 — `daily_monitor.py` (cron quotidien)

### Mission

Checker les dernières vidéos d'une liste prédéfinie de chaînes YouTube, détecter les nouveautés et les outliers, et pousser les résultats dans le repo.

### Flux

1. Lire `config/channels.json` — liste des chaînes à surveiller
2. Pour chaque chaîne :
   - API YouTube `channels.list` → stats chaîne (abonnés, total vues)
   - API YouTube `search.list` → dernières vidéos (titre, date, videoId)
   - API YouTube `videos.list` → stats vidéos (vues, likes, commentaires)
3. Comparer avec `data/last_check.json` → identifier les nouvelles vidéos depuis le dernier run
4. Détecter les outliers : vidéo avec vues > 3× la médiane des vues récentes de la chaîne
5. Écrire les nouveautés dans `context/backlog.json`
6. Mettre à jour `data/last_check.json` avec le timestamp du check
7. Mettre à jour `data/channel_stats.json` avec les stats historiques (pour calcul médiane)
8. Commit + push sur le repo GitHub

### Détection d'outliers

- Stocker les vues des N dernières vidéos par chaîne dans `channel_stats.json`
- Calculer la médiane des vues par chaîne
- Si une nouvelle vidéo a > 3× la médiane → flag comme outlier
- Les outliers sont marqués `"outlier": true` dans le backlog

### Coût API estimé

- 20 chaînes × `channels.list` = 20 unités
- 20 chaînes × `search.list` = 2 000 unités (100/recherche)
- ~100 vidéos × `videos.list` = 100 unités
- **Total : ~2 120 unités/jour** (21.2% du quota)

### Optimisation possible

- Utiliser `playlistItems.list` sur la playlist "uploads" au lieu de `search.list` → 1 unité au lieu de 100
- La playlist uploads a l'ID `UU` + channel_id (remplacer le premier `UC` par `UU`)
- Réduirait le coût à **~120 unités/jour** (1.2% du quota)

**Recommandation** : utiliser `playlistItems.list` pour le monitoring quotidien, garder `search.list` pour le discovery uniquement.

---

## Script 2 — `discover_creators.py` (manuel ou hebdo)

### Mission

Trouver de nouveaux créateurs YouTube pertinents dans la niche AI/Claude Code/VibeCoding et proposer leur ajout à la liste de monitoring.

### Flux

1. Lire `config/keywords.json` — mots-clés de recherche
2. Pour chaque mot-clé :
   - API YouTube `search.list` (type=channel + type=video) → chaînes et vidéos pertinentes
   - Filtrer les chaînes déjà dans `channels.json`
3. Pour chaque nouvelle chaîne trouvée :
   - API YouTube `channels.list` → stats (abonnés, fréquence de publication, date de création)
   - API YouTube `search.list` → dernières vidéos pour évaluer la pertinence
4. Scorer chaque chaîne candidate :
   - Pertinence niche (mots-clés dans titres/descriptions)
   - Taille (abonnés)
   - Activité (fréquence de publication)
5. Afficher les résultats triés par score
6. L'utilisateur valide → les chaînes approuvées sont ajoutées à `channels.json`

### Mots-clés initiaux

```json
{
  "keywords": [
    "Claude Code",
    "VibeCoding",
    "vibe coding",
    "AI tools tutorial",
    "build with AI",
    "Anthropic Claude",
    "AI automation business",
    "no code AI",
    "AI agent"
  ]
}
```

### Coût API estimé (par exécution)

- 9 mots-clés × `search.list` = 900 unités
- ~30 chaînes × `channels.list` = 30 unités
- ~30 chaînes × `search.list` (vidéos récentes) = 3 000 unités
- **Total : ~3 930 unités/exécution**

Optimisation : limiter à 5 mots-clés par run = ~2 200 unités.

---

## Structure des fichiers

```
yt-veille/
├── scripts/
│   ├── daily_monitor.py         # Script 1 — monitoring quotidien
│   ├── discover_creators.py     # Script 2 — découverte de créateurs
│   ├── config/
│   │   ├── channels.json        # Liste des chaînes à surveiller
│   │   └── keywords.json        # Mots-clés pour la découverte
│   ├── data/
│   │   ├── last_check.json      # Timestamp + IDs du dernier check
│   │   └── channel_stats.json   # Historique stats pour calcul médiane
│   ├── .env.example             # Template sans secrets
│   ├── .gitignore               # Exclut .env
│   └── requirements.txt         # Dépendances Python
├── context/
│   └── backlog.json             # Idées accumulées (output principal)
├── references/
│   └── sources.md               # (existant)
└── SKILL.md                     # (existant)
```

## Format de sortie — `backlog.json`

```json
{
  "last_updated": "2026-03-26T01:00:00Z",
  "items": [
    {
      "id": "VIDEO_ID",
      "title": "Why you NEED to be running local AI models",
      "channel": "Alex Finn",
      "channel_id": "UCfQNB91qRP_5ILeu_S_bSkg",
      "published": "2026-03-24T18:00:00Z",
      "views": 15230,
      "likes": 892,
      "comments": 134,
      "channel_subscribers": 68000,
      "thumbnail": "https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg",
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "outlier": true,
      "median_views": 4500,
      "outlier_ratio": 3.38,
      "detected_at": "2026-03-26T01:00:00Z",
      "source": "daily_monitor"
    }
  ]
}
```

## Cron setup (VPS)

```bash
# Crontab sur le VPS
# 9h00 SGT = 01:00 UTC
0 1 * * * cd /root/youtube-domination-factory/yt-veille/scripts && /usr/bin/python3 daily_monitor.py >> /var/log/yt-veille.log 2>&1
```

## Dépendances

```
# requirements.txt
google-api-python-client   # YouTube Data API
python-dotenv              # Lecture .env
```

## Chaînes initiales — `channels.json`

```json
{
  "channels": [
    {
      "handle": "AlexFinnOfficial",
      "channel_id": "UCfQNB91qRP_5ILeu_S_bSkg",
      "niche": "claude-code-ai",
      "added_at": "2026-03-26"
    }
  ]
}
```

## Hors scope

- Scraping X/Twitter (à ajouter dans une v2 si besoin)
- Scoring LLM automatique (phase suivante — le backlog sera scoré manuellement ou via le skill `yt-veille`)
- Notifications (Telegram, email) — le push GitHub suffit pour la v1
- Collecte Anthropic blog, Reddit, HN, Product Hunt (v2)
