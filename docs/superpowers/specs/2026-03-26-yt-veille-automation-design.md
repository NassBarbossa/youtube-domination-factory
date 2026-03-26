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
- **Quota API** : ~42 unités/jour estimées sur 10 000 disponibles (0.4%) — utilise `playlistItems.list` + batching `videos.list`
- **Timestamps** : tous en UTC
- **Python** : 3.10+ (Ubuntu 22.04 natif)

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
   - API YouTube `channels.list` → stats chaîne (abonnés, total vues) — 1 unité
   - API YouTube `playlistItems.list` sur la playlist uploads (`UU` + channel_id sans le `UC`) → dernières vidéos (titre, date, videoId) — 1 unité
   - Si `playlistItems.list` échoue → fallback sur `search.list` (100 unités) et log un warning
   - API YouTube `videos.list` → stats vidéos (vues, likes, commentaires) — batch jusqu'à 50 IDs par appel = 1 unité
3. Comparer avec `data/last_check.json` → identifier les nouvelles vidéos depuis le dernier run
4. Détecter les outliers : vidéo avec vues > 3× la médiane des vues récentes de la chaîne
5. Dédupliquer par `videoId` avant d'ajouter au backlog (évite les doublons si `last_check.json` est reset)
6. Écrire les nouveautés dans `context/backlog.json` (à la racine du projet, à côté de `video-context.json`)
7. Mettre à jour `data/last_check.json` avec le timestamp du check
8. Mettre à jour `data/channel_stats.json` avec les stats historiques (pour calcul médiane)
9. `git pull --rebase` puis commit + push sur le repo GitHub. Si le rebase échoue → `git rebase --abort`, log l'erreur, exit 1

### Détection d'outliers

- Stocker les vues des N dernières vidéos par chaîne dans `channel_stats.json`
- Calculer la médiane des vues par chaîne
- Si une nouvelle vidéo a > 3× la médiane → flag comme outlier
- Les outliers sont marqués `"outlier": true` dans le backlog
- **Nouvelles chaînes (< 5 vidéos en historique)** : pas de détection d'outlier, toutes les vidéos sont ajoutées normalement le temps de constituer l'historique

### Gestion des erreurs

- **API YouTube 403/429 (quota)** : log l'erreur, skip la chaîne, continuer les autres
- **API YouTube 500** : retry 1x après 5s avec backoff, puis skip
- **Fichiers JSON corrompus/manquants** : recréer un fichier vide par défaut, log un warning
- **Écriture fichiers** : écrire dans un fichier temporaire puis renommer (atomic write) pour éviter les corruptions si le script crash mid-write
- **Git push échoue** : `git pull --rebase`, si conflit → `git rebase --abort`, log erreur, exit 1
- **Exit code non-zero** : le cron log l'erreur dans `/var/log/yt-veille.log`

### Logging

- Utiliser le module Python `logging` avec `RotatingFileHandler` (max 5 Mo, 3 fichiers de rotation)
- Niveaux : INFO (run normal), WARNING (fallback, chaîne skippée), ERROR (échec critique)
- Format : `[2026-03-26 01:00:00] INFO: Checked 20 channels, 5 new videos, 1 outlier`

### Coût API estimé (avec `playlistItems.list` + batching `videos.list`)

- 20 chaînes × `channels.list` = 20 unités
- 20 chaînes × `playlistItems.list` = 20 unités
- ~100 vidéos × `videos.list` (batchées par 50) = 2 unités
- **Total : ~42 unités/jour** (0.4% du quota)

Note : les estimates supposent ~20 chaînes à terme. Au lancement, 1 seule chaîne = ~3 unités/jour.

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
youtube-domination-factory/          # Racine du projet
├── context/
│   ├── video-context.json           # (existant) Pipeline vidéo en cours
│   ├── backlog.json                 # (nouveau) Idées accumulées par la veille
│   └── backlog-archive/             # (nouveau) Archive des entrées > 90 jours
│       └── YYYY-MM.json
├── yt-veille/
│   ├── SKILL.md                     # (existant)
│   ├── references/
│   │   └── sources.md               # (existant)
│   └── scripts/
│       ├── daily_monitor.py         # Script 1 — monitoring quotidien
│       ├── discover_creators.py     # Script 2 — découverte de créateurs
│       ├── config/
│       │   ├── channels.json        # Liste des chaînes à surveiller
│       │   └── keywords.json        # Mots-clés pour la découverte
│       ├── data/
│       │   ├── last_check.json      # Timestamp + IDs du dernier check
│       │   └── channel_stats.json   # Historique stats pour calcul médiane
│       ├── .env.example             # Template sans secrets
│       ├── .gitignore               # Exclut .env
│       └── requirements.txt         # Dépendances Python
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

## Backlog pruning

- Les entrées de plus de 90 jours sont archivées dans `context/backlog-archive/YYYY-MM.json`
- Le backlog actif ne contient que les 90 derniers jours

## Hors scope

- Scraping X/Twitter (à ajouter dans une v2 si besoin)
- Scoring LLM automatique (phase suivante — le backlog sera scoré manuellement ou via le skill `yt-veille`)
- Notifications (Telegram, email) — le push GitHub suffit pour la v1
- Collecte Anthropic blog, Reddit, HN, Product Hunt (v2)
