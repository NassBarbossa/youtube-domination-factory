# Feedback loop — titres

Chargé par `yt-titres-seo/SKILL.md`. Les règles opérationnelles du SKILL.md (≤ 30 caractères, 5 mots max, pas de listes chiffrées) priment : ce fichier sert à mesurer et à faire évoluer ces règles avec les vraies données de la chaîne.

## Avant chaque génération

1. Lire `yt-titres-seo/memory/lessons.json`.
2. Si des leçons existent avec `sample_size >= 3` :
   - privilégier les styles dont le CTR est supérieur à la moyenne de la chaîne ;
   - éviter les patterns qui sous-performent ;
   - le dire à Nass : « Tes titres avec [pattern] font en moyenne X % de CTR » (X = valeur réelle de `lessons.json`).
3. Les leçons de la période IA / Claude Code (avant le passage 100 % crypto) ne valent pas pour la chaîne crypto : les ignorer ou les marquer « à revalider ».
4. Pas assez de données : générer normalement.

## Après chaque choix de titre

En mode manuel, logger dans `yt-titres-seo/memory/choices.json` (en mode pipeline, l'orchestrateur le fait en Phase 5) :

```json
{
  "video_slug": "slug-de-la-video",
  "date": "AAAA-MM-JJ",
  "niche": "crypto",
  "title_chosen": "Le titre choisi",
  "titles_rejected": ["Titre 2", "Titre 3", "Titre 4", "Titre 5", "Titre 6", "Titre 7"],
  "formula": "T1|T2|T3|T4|T5|T6|T7|T8",
  "style": "chiffre|question|how-to|contrarian|curiosity-gap|story|descriptif",
  "char_count": 23,
  "word_count": 4,
  "has_number": false,
  "number_type": "odd|even|money|time|null",
  "has_power_words": false,
  "power_words_used": [],
  "has_brackets": false,
  "keyword_position": 1,
  "framing": "positive|negative|neutral",
  "performance": null
}
```

`performance` est rempli plus tard, quand les analytics arrivent (yt-analytics).

## Critères d'analyse — hypothèses à tester

Repères issus d'études YouTube toutes niches confondues. Ce ne sont **pas des règles** : ce sont des hypothèses à tester sur la chaîne crypto. Plusieurs contredisent la règle opérationnelle (≤ 30 caractères) ; on ne change la règle que si les données de la chaîne le montrent.

| Facteur | Hypothèse | Source citée |
|---------|-----------|--------------|
| Longueur (caractères) | 40-60 caractères | SubSub.io |
| Longueur (mots) | 6-10 mots | Semrush, SubSub.io |
| Chiffre dans le titre | un chiffre impair (3, 5, 7) attirerait plus de clics | TunePocket |
| Power words | 1-2 = bon, 3+ = spam | Increv, Humble&Brag |
| Framing négatif | plus de vues médianes | Quasa.io |
| Position du mot-clé | dans les 5 premiers mots | Increv |
| Crochets | léger bonus | Humble&Brag |
| Majuscules | pénalité au-delà de 3 mots | SubSub.io |
| Emojis (vidéo longue) | pénalité | SubSub.io |
| Titre court (≤ 30 car.) | plus de vues qu'un titre long | 1of10.com |

## Format des leçons

```json
{
  "lessons": [
    {
      "rule": "[pattern observé sur la chaîne]",
      "evidence": "[CTR moyen réel du pattern A] vs [CTR moyen réel du pattern B]",
      "sample_size": 0,
      "confidence": "low|medium|high",
      "created_at": "AAAA-MM-JJ",
      "last_validated": "AAAA-MM-JJ"
    }
  ],
  "style_performance": {
    "descriptif": {"count": 0, "avg_ctr": null, "avg_views": null}
  }
}
```

Niveaux de confiance : `low` < 5 vidéos · `medium` 5-10 vidéos · `high` > 10 vidéos.
