# Feedback loop — miniatures

Chargé par `yt-miniature/SKILL.md`. Les règles opérationnelles du SKILL.md (aucun texte ou 5 mots max, visage 35-50 %, 2 éléments focaux max, charte du cadre) priment : ce fichier sert à les mesurer et à les faire évoluer avec les données de la chaîne.

## Avant chaque conception

1. Lire `yt-miniature/memory/lessons.json`.
2. Si des leçons existent avec `sample_size >= 3` :
   - privilégier les styles dont le CTR est supérieur à la moyenne ;
   - le dire à Nass : « Tes miniatures avec [pattern] font en moyenne X % de CTR » (X = valeur réelle de `lessons.json`).
3. Ne prendre en compte que les entrées `"niche": "crypto"` de `choices.json` : les miniatures de l'ancienne niche IA (`"niche": "ia"`, charte orange / cyan) ne sont pas comparables.
4. Pas assez de données : concevoir normalement.

## Après chaque choix de concept

En mode manuel, logger dans `yt-miniature/memory/choices.json` (en mode pipeline, l'orchestrateur le fait en Phase 5) :

```json
{
  "video_slug": "slug-de-la-video",
  "date": "AAAA-MM-JJ",
  "niche": "crypto",
  "concept_chosen": "[nom du concept]",
  "concepts_rejected": ["[concept 2]", "[concept 3]"],
  "has_face": true,
  "has_punk": false,
  "face_size_pct": 45,
  "face_expression": "focused",
  "dominant_color": "#DBB17F",
  "color_name": "sable",
  "text_on_thumbnail": false,
  "text_word_count": 0,
  "text_content": null,
  "num_focal_points": 2,
  "has_real_chart": false,
  "figure_source": null,
  "has_border_glow": false,
  "background_style": "black-dusk-mountains",
  "title_thumbnail_synergy": "complement",
  "ab_test_winner": null,
  "notes": "[retours de Nass]",
  "performance": null
}
```

`performance` est rempli plus tard, quand les analytics arrivent (yt-analytics).

## Critères d'analyse — hypothèses à tester

Repères issus d'études toutes niches confondues. Ce ne sont **pas des règles** : hypothèses à recalibrer sur la chaîne crypto. Quand un repère diffère de la règle du SKILL.md, la règle du SKILL.md s'applique tant que les données de la chaîne ne disent pas autre chose.

| Facteur | Hypothèse | Source citée |
|---------|-----------|--------------|
| Visage présent | plus de clics avec visage | YouTube Creator Academy |
| Taille du visage | 30-60 % du cadre | Justin Briggs |
| Expression | surprise, joie > neutre | YouTube Creator Academy |
| Direction du regard | vers le centre ou vers le texte | vidIQ |
| Texte | 3-5 mots max, lisible sur mobile ; ou aucun texte (1of10.com) | Justin Briggs, 1of10.com |
| Couleur dominante | chaude > froide | Justin Briggs, Paddy Galloway |
| Luminosité | score > 120 sur 0-255 | Justin Briggs |
| Contraste | ≥ 4,5:1 sujet / fond | Justin Briggs |
| Éléments focaux | 3 max | Paddy Galloway |
| Espace négatif | 20-30 % du cadre | Paddy Galloway |
| Cohérence titre / miniature | complémentaires, jamais dupliqués | Covington et al. |
| Contour lumineux sur le sujet | léger bonus | vidIQ, TubeBuddy |
| Punk vs visage | à mesurer | A/B tests internes |
| Graphique réel présent | à mesurer | A/B tests internes |

## Format des leçons

```json
{
  "lessons": [
    {
      "rule": "[pattern observé sur la chaîne]",
      "evidence": "[CTR moyen réel du pattern A] vs [CTR moyen réel du pattern B]",
      "sample_size": 0,
      "confidence": "low"
    }
  ],
  "concept_performance": {
    "face-sand-black": {"count": 0, "avg_ctr": null},
    "punk-dusk-mountains": {"count": 0, "avg_ctr": null}
  }
}
```

Niveaux de confiance : `low` < 5 vidéos · `medium` 5-10 vidéos · `high` > 10 vidéos.
