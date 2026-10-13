# Feedback loop — mémoire des choix de sujets

Chargé depuis `yt-veille/SKILL.md` (section « Mémoire des choix »). Fichiers : `yt-veille/memory/choices.json` et `yt-veille/memory/lessons.json`.

## Avant chaque session de veille

1. Lire `memory/lessons.json`.
2. Si des leçons existent (`sample_size` >= 3), ajuster la recherche :
   - prioriser les catégories de sujets au meilleur hit rate ;
   - signaler les filons confirmés ;
   - alerter sur les catégories qui ne convertissent pas ;
   - mentionner : « Hit rate actuel : X % — les sujets [catégorie] performent le mieux ».
3. Pas assez de données : chercher normalement.

## Après chaque décision de sujet

Logger dans `memory/choices.json` :

```json
{
  "video_slug": "slug-de-la-video",
  "date_detected": "AAAA-MM-JJ",
  "date_decided": "AAAA-MM-JJ",
  "date_published": "AAAA-MM-JJ",
  "days_lag_detect_to_publish": 3,
  "source": "web|onchain|audience|convergence|nass|1of10|daily_monitor",
  "source_channel": "[chaîne, si l'idée vient d'une vidéo]",
  "source_video_id": "[id, si applicable]",
  "source_video_views": null,
  "source_channel_avg_views": null,
  "outlier_score": null,
  "topic_category": "presale-early|airdrop|onchain|bons-coins|crypto-security|crypto-beginner|bitcoin|etf-institutions|regulation-tax|defi|altcoins|solana|ethereum|macro|crypto-news|tutorial|comparison",
  "decision": "make_video|skip",
  "skip_reason": null,
  "toast_score": {
    "timeliness": 4,
    "originality": 3,
    "audience_alignment": 5,
    "searchability": 3,
    "thumbnail_title_potential": 4,
    "total": 19
  },
  "performance": null
}
```

`daily_monitor` ne sert que si la veille automatique est relancée par Nass (en pause). Le champ `performance` est rempli après publication, à partir des analytics.

## Critères d'analyse (après publication)

| Métrique | Calcul | Repère (hypothèse à recalibrer sur la chaîne crypto) |
|---|---|---|
| Performance Index | vues_vidéo / moyenne_vues_chaîne | > 1,5 = hit |
| Replication Rate | vues_vidéo / vues_outlier_source | 5-15 % = succès |
| Hit Rate global | vidéos_au_dessus_moyenne / total | > 50 % = bon |
| Temps de réaction moyen | moyenne(days_lag_detect_to_publish) | < 3 jours = bon |
| CTR vs moyenne | CTR_vidéo − CTR_moyen_chaîne | > 0 = bon sujet |
| View Velocity (48 h) | vues_48h / abonnés | > 5 % = bon |

**Score TOAST prédictif** (1 à 5 chacun, total /25) :
- **T**imeliness : le sujet est-il d'actualité maintenant ?
- **O**riginality : notre angle est-il unique ?
- **A**udience alignment : colle-t-il à l'avatar ?
- **S**earchability : y a-t-il de la demande en recherche ?
- **T**humbnail/Title potential : peut-on le packager de façon accrocheuse ?

Hypothèse à tester : un total > 18 annonce une surperformance. Une fois assez de données, calculer la corrélation entre TOAST et Performance Index pour valider ou ajuster.

## Repères de performance (hypothèses à recalibrer)

| Métrique | Mauvais | Acceptable | Bon | Excellent |
|---|---|---|---|---|
| Hit Rate | < 30 % | 30-50 % | 50-70 % | > 70 % |
| Performance Index moyen | < 0,8 | 0,8-1,2 | 1,2-2,0 | > 2,0 |
| Replication Rate | < 1 % | 1-5 % | 5-15 % | > 15 % |
| Temps de réaction moyen | > 7 j | 3-7 j | 1-3 j | < 24 h |

## Format des leçons

Exemple de format (valeurs fictives, à remplacer par les vraies données) :

```json
{
  "lessons": [
    {
      "rule": "[règle observée]",
      "evidence": "[X/Y vidéos de la catégorie ont dépassé la moyenne de la chaîne]",
      "sample_size": 5,
      "confidence": "low|medium|high",
      "created_at": "AAAA-MM-JJ"
    }
  ],
  "topic_performance": {
    "[catégorie]": {"count": 0, "avg_performance_index": null, "hit_rate": null}
  },
  "hit_rate": null,
  "avg_days_lag": null
}
```
