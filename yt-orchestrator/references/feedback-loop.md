# Feedback loop de l'orchestrateur

Détail chargé à la demande depuis `yt-orchestrator/SKILL.md` (Phase 0 : lecture des leçons ; Phase 5 : écriture de la mémoire). Chemins relatifs à la racine du repo `C:\Users\User\youtube-domination-factory`.

Seules les vidéos de la période crypto comptent : les leçons de l'ancienne niche IA ne s'appliquent pas (filtrer sur `niche: "crypto"`).

## 1. Mémoire des choix (Phase 5, écrite par l'orchestrateur)

Les agents ne touchent pas à `memory/` en mode autonome : l'orchestrateur ajoute une entrée à chaque fichier à la fin du pipeline, d'après les sections du JSON.

| Fichier | Source dans `video-context.json` | Format de l'entrée |
|---|---|---|
| `yt-script/memory/choices.json` | `script` | section « Feedback Loop » de `yt-script/SKILL.md` |
| `yt-titres-seo/memory/choices.json` | `titres_seo` | section « Feedback Loop » de `yt-titres-seo/SKILL.md` |
| `yt-miniature/memory/choices.json` | `miniature` | section « Feedback Loop » de `yt-miniature/SKILL.md` |
| `yt-veille/memory/choices.json` | `veille` (Mode B seulement) | section « Feedback Loop » de `yt-veille/SKILL.md` |

Chaque entrée porte `video_slug`, `niche: "crypto"` et `performance: null` (rempli plus tard par `yt-analytics/feedback_analyzer.py`). Les fichiers ont la forme `{"choices": [ … ]}` : ajouter, ne jamais écraser les entrées existantes. Ne remplir que les champs connus ; un champ qu'on ne peut pas déduire reste `null` (pas d'estimation présentée comme une mesure).

## 2. Journal des pipelines — `yt-orchestrator/memory/pipeline_runs.json`

Forme du fichier : `{"runs": [ … ]}`. Une entrée par pipeline terminé (ou abandonné, avec `status: "failed"`) :

```json
{
  "video_slug": "premiere-crypto-hors-echange",
  "niche": "crypto",
  "mode": "A",
  "funnel": "TOP",
  "status": "completed",
  "started_at": "<_meta.created_at>",
  "completed_at": "<_meta.completed_at>",
  "phases": {
    "0":    {"status": "completed"},
    "0.5":  {"status": "skipped"},
    "0.75": {"status": "completed", "retries": 0},
    "1":    {"status": "completed"},
    "2a":   {"status": "completed"},
    "2bc":  {"status": "completed"},
    "3":    {"status": "completed", "changes_requested": ["titre"]},
    "4":    {"status": "completed"},
    "5":    {"status": "completed"}
  },
  "validation_rounds": 1,
  "errors": [],
  "skills_used": {
    "titres_seo": {"title_style": "how-to", "char_count": 28},
    "miniature": {"concept": "<recommended_concept.name>", "has_face": true},
    "script": {"hook_type": "question", "structure": "tutorial"},
    "veille": null
  },
  "youtube_video_id": null,
  "performance": null
}
```

Les durées par phase se calculent à partir des `timestamp` de `pipeline_log` ; ne pas les inventer s'ils manquent. `youtube_video_id` est recopié depuis `_meta.youtube_video_id` quand Nass donne l'ID de la vidéo publiée.

## 3. Leçons de pipeline (meta) — `yt-orchestrator/memory/lessons.json`

À partir de `pipeline_runs.json` :

- **Goulot** : phase la plus longue en moyenne.
- **Taux de complétion** : pipelines terminés vs abandonnés.
- **Retries** : agents qui échouent le plus souvent.
- **Validation** : rounds de changements en Phase 3 ; au-delà de 2 en moyenne, recalibrer les agents en amont.
- **Vitesse** : durée totale du pipeline vs performance de la vidéo (hypothèse à tester : un sujet chaud perd de la valeur si le pipeline traîne).

Format d'une leçon : `{rule, evidence, action, sample_size, confidence, created_at}`.

## 4. Leçons croisées (cross) — même fichier

Après un passage de `feedback_analyzer.py` (ou quand Nass demande « analyse mes performances »), croiser les `choices.json` qui ont une `performance` :

| Croisement | Question |
|---|---|
| Titre × miniature | Quels duos titre + miniature ont le meilleur CTR ? |
| Hook du script × titre | Le type de hook tient-il la promesse du titre (rétention) ? |
| Veille × packaging | Quel style de titre marche selon la catégorie de sujet ? |
| Vitesse × performance | Les pipelines rapides font-ils mieux ? |

Stocker dans `cross_lessons[]` (`{rule, evidence, skills_involved[], sample_size, confidence, created_at}`), `winning_combos[]` et `losing_combos[]` (`{combo, avg_performance_index, count, confidence, example_video}`). Les preuves citées sont des moyennes réelles calculées sur les données ; jamais d'exemple chiffré inventé.

## 5. Niveaux de confiance

- `low` : moins de 5 pipelines crypto avec performance.
- `medium` : 5 à 15.
- `high` : plus de 15.

## 6. Usage en Phase 0

1. Lire `yt-orchestrator/memory/lessons.json` et les `memory/lessons.json` des skills.
2. S'il existe des leçons `medium` ou `high` issues de la période crypto, les ajouter en une ligne aux prompts des agents concernés et les mentionner à Nass (« Sur [N] vidéos, [combinaison] fait le mieux »).
3. Sinon, ne rien injecter.

## Point connu

`feedback_analyzer.py` cherche aujourd'hui l'ID vidéo dans un champ `video_id` au premier niveau des archives, alors que le contrat (`context/SCHEMA.md`) le place dans `_meta.youtube_video_id`. À aligner dans le script (hors périmètre de ce skill).
