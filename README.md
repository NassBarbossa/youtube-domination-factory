# YouTube Domination Factory

Skills Claude Code qui produisent les vidéos de la chaîne YouTube **crypto** de Nass Riviera ([nassriviera.com](https://nassriviera.com)) : un sujet → script, slides, titres, miniature, description, Shorts, thread X et post LinkedIn, avec les validations de Nass aux étapes clés.

Le cadre éditorial (narrative, avatar, offres, ton, règles de fond, charte) est écrit une seule fois : [`_shared/cadre-nass.md`](_shared/cadre-nass.md).

## Démarrage

```
« Fais une vidéo sur comment acheter sa première crypto en dehors des échanges »  → yt-orchestrator (pipeline complet)
« Trouve-moi des idées de vidéo »                                                → yt-veille
« Écris le script sur … »                                                        → yt-script
« Écris un Short sur … »                                                         → yt-shorts-script
```

Chaque skill fonctionne aussi seul.

## Skills

| Skill | Rôle |
|---|---|
| `yt-orchestrator` | Pipeline complet d'une vidéo, fichier de contexte partagé |
| `yt-veille` | Idées de vidéos scorées (veille automatique en pause) |
| `yt-transcript` | Recherche concurrentielle : faits sourcés, angles couverts / manquants |
| `yt-script` | Script avec Nass + slides HTML (mode dictée « slide après ») |
| `yt-titres-seo` | 7 titres, mots-clés |
| `yt-miniature` | 3 concepts de miniature, brief Canva, image de fond via OpenRouter |
| `yt-description` | Description, timestamps, tags |
| `yt-repurposing` | Découpe d'une vidéo longue : Shorts, thread X @punk6995, LinkedIn |
| `yt-shorts-script` / `yt-shorts-montage` | Shorts natifs 30-60 s, montage HyperFrames 1080×1920 |
| `yt-analytics` | Analyse des stats YouTube, tableau de bord |
| `yt-calendrier` | Calendrier éditorial |

## Pipeline

```
0     Init : slug, funnel, contexte depuis le template
0.5   yt-veille (si pas de sujet) → Nass choisit                 pause
0.75  yt-transcript                                              agent
1     yt-script, avec Nass                                       pauses
2a    yt-titres-seo                                              agent
2b/c  yt-miniature + yt-description                              agents en parallèle
3     Validation titre / miniature / description                pause
4     yt-repurposing                                             agent
5     Récap, mémoire des choix
```

Contexte partagé : `context/video-context.json` (contrat : [`context/SCHEMA.md`](context/SCHEMA.md)). Les agents écrivent leur section dans `context/runs/<slug>/` ; seul l'orchestrateur fusionne.

## Installation

Le dépôt vit à `~/youtube-domination-factory` sur Mac et `C:\Users\User\youtube-domination-factory` sur Windows. Les skills désignent cette racine par `{repo}` ; les chemins relatifs partent de là. Si tu clones ailleurs, remplace ces deux chemins dans les fichiers `.md` (voir `TODO.md`).

Les skills sont branchés dans Claude Code par des liens vers le repo : une modif dans le repo est active immédiatement.

Mac :

```bash
cd ~/youtube-domination-factory
for d in yt-*/; do d=${d%/}; [ -f "$d/SKILL.md" ] && ln -sfn "../../youtube-domination-factory/$d" ~/.claude/skills/"$d"; done
```

Windows (PowerShell) :

```powershell
Get-ChildItem C:\Users\User\youtube-domination-factory -Directory -Filter 'yt-*' |
  ForEach-Object { New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\$($_.Name)" -Target $_.FullName }
```

Fichier `.env` à la racine (hors git) : `OPENROUTER_API_KEY=...` pour la génération d'images des miniatures.

## Veille automatique

En pause (cron désactivé par Nass). Le code reste dans `yt-veille/scripts/` (scraping quotidien, SQLite `veille.db` sur le VPS, scoring composite, rapport) pour le jour où elle est relancée.

## Structure

```
_shared/cadre-nass.md      cadre éditorial unique
yt-*/SKILL.md              un skill par dossier ; references/ (détails à la demande), memory/ (choix passés)
context/                   contexte du pipeline, template, schéma, archives
yt-veille/scripts/         veille automatique (Python, en pause)
yt-analytics/*.py          analyse des stats (local)
shows/                     assets du live Convergence
```
