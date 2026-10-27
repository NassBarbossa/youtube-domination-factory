# Feedback loop — titres

Chargé par `yt-titres-seo/SKILL.md`. Les règles du SKILL.md (30 à 60 caractères, promesse dans les 5 premiers mots, suffixe de marque à la fin, formule T9 question, type searchable / intriguing) viennent des sources lues le 20 octobre 2026 et des titres publiés de la chaîne (`veille-titres-2026-10-20.md`). Ce fichier sert à les mesurer et à les faire évoluer avec les vraies données de la chaîne : elles changent quand dix vidéos auront dépassé 1 000 impressions chacune, pas avant.

## Avant chaque génération

1. Lire `yt-titres-seo/memory/lessons.json`.
2. Si des leçons existent avec `sample_size >= 3` :
   - privilégier les styles dont le CTR est supérieur à la médiane de la chaîne ;
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
  "youtube_video_id": null,
  "title_chosen": "Le titre choisi",
  "title_proposed": "Le titre du top 3 dont il est parti, s'il l'a modifié",
  "titles_rejected": ["Titre 2", "Titre 3", "Titre 4", "Titre 5", "Titre 6", "Titre 7"],
  "formula": "T1|T2|T3|T4|T5|T6|T7|T8|T9",
  "title_type": "searchable|intriguing",
  "style": "chiffre|question|how-to|contrarian|curiosity-gap|story|descriptif",
  "char_count": 56,
  "word_count": 10,
  "has_year": true,
  "has_number": false,
  "number_type": "odd|even|money|time|null",
  "has_power_words": false,
  "power_words_used": [],
  "has_brackets": true,
  "brand_suffix": true,
  "keyword_position": 1,
  "framing": "positive|negative|neutral",
  "ab_test_candidates": [],
  "ab_test_result": "winner|performed_same|inconclusive|null",
  "ab_test_winner": null,
  "performance": null
}
```

`performance` est rempli plus tard, quand les analytics arrivent (yt-analytics : impressions et CTR lus dans Studio, jamais estimés).

## Critères d'analyse

Ce qui vient des sources du 20 octobre 2026 (toutes hors de la chaîne, donc à vérifier ici) :

| Facteur | Ce que disent les sources | Statut sur la chaîne |
|---|---|---|
| Longueur | 30 à 50 caractères (air.io, 18 080 chaînes) ; moins de 60, médiane 8 mots chez les meilleurs (Subsub, 120 703 titres) ; corrélation longueur / performance nulle (ytgrowth, 28 947 vidéos) | Règle. Les 5 titres publiés font 41 à 57 caractères |
| Question | signal fort en éducation et finance « quand le spectateur a déjà la question » (air.io) | Règle (T9). 4 titres publiés sur 5 |
| Mot-clé devant, marque à la fin | YouTube ; premiers 40 % du titre (air.io) ; 3 à 5 premiers mots (Humble & Brag) | Règle |
| Majuscules | négatif en éducation (air.io) ; un mot au plus (Humble & Brag) ; YouTube « limit ALL CAPS and emoji » | Règle |
| Chiffre réel, délai concret | les chiffres précis et les délais font mieux en finance (air.io) | Règle, sous conformité |
| Année dans le titre | [2026] positif en finance et éducation (air.io) ; durée de vie 12 mois (Humble & Brag) | Règle : sujets datés seulement |
| Cadrage négatif | marche quand il aide à éviter une erreur, l'indignation fabriquée sous-performe (air.io) | Hypothèse, déjà la nuance du skill |
| Chiffre impair, petites listes | léger avantage (Humble & Brag) | Hypothèse |
| Mots forts | 1 ou 2, « three or more start to feel like spam » (Humble & Brag) | Hypothèse |
| Crochets | léger bonus (Humble & Brag, air.io) | Hypothèse |
| Titre complémentaire de la miniature | 1 à 2 points de CTR chez une agence (Humble & Brag) | Hypothèse |
| Titre court (≤ 30 caractères) | 5 mots = meilleur engagement médian (1of10, Outlier Score) ; contredit par les autres sources et par les titres publiés | Retiré des règles le 20 octobre 2026 |

Le feedback analyzer compare chaque facteur au CTR réel par titre, à volume d'impressions comparable (un CTR sur 73 impressions ne compte pas).

## Format des leçons

```json
{
  "lessons": [
    {
      "rule": "[pattern observé sur la chaîne]",
      "evidence": "[CTR médian réel du pattern A] vs [CTR médian réel du pattern B], impressions comparables",
      "sample_size": 0,
      "confidence": "low|medium|high",
      "created_at": "AAAA-MM-JJ",
      "last_validated": "AAAA-MM-JJ"
    }
  ],
  "style_performance": {
    "question": {"count": 0, "median_ctr": null, "median_impressions": null}
  }
}
```

Niveaux de confiance : `low` < 5 vidéos · `medium` 5-10 vidéos · `high` > 10 vidéos, chacune au-dessus de 1 000 impressions.
