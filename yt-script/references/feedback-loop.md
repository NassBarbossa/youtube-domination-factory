# Feedback loop — détail (yt-script)

Référence chargée depuis `yt-script/SKILL.md`. Fichiers : `yt-script/memory/lessons.json` (lu avant d'écrire) et `yt-script/memory/choices.json` (complété après chaque script).

## Avant chaque script

1. Lire `yt-script/memory/lessons.json`.
2. Si des leçons ont `sample_size >= 3`, les intégrer : structure du hook, pacing, longueur des sections, anti-patterns à éviter. Les citer à Nass : « Tes vidéos avec [pattern] retiennent X % vs Y % sans ».
3. Sinon, écrire normalement.
4. Ne retenir que les vidéos de la période crypto : les leçons des anciennes vidéos IA / Claude Code ne s'appliquent pas à la nouvelle audience.

## Après chaque script terminé

Appel direct par Nass : ajouter une entrée dans `yt-script/memory/choices.json`. En pipeline, c'est l'orchestrateur qui écrit la mémoire des choix en Phase 5 (voir `yt-orchestrator/references/feedback-loop.md`) : ne pas l'écrire en double.

Format d'une entrée :

```json
{
  "video_slug": "slug-de-la-video",
  "date": "AAAA-MM-JJ",
  "script_file": "yt-script/outputs/slug.md",
  "funnel": "TOP|MIDDLE|BOTTOM",
  "hook_type": "curiosity-gap|bold-claim|question|story|stat",
  "hook_length_words": 25,
  "hook_length_seconds_est": 8,
  "has_branded_intro": false,
  "branded_intro_length_sec": 0,
  "num_sections": 6,
  "total_word_count": 1650,
  "estimated_duration_min": 11,
  "open_loops_count": 3,
  "has_escalation": true,
  "cta_position": "end",
  "early_cta": false,
  "uses_conclusion_words": false,
  "structure_type": "tutorial|story|deep-dive|comparison|news|reaction",
  "pacing_wpm_est": 160,
  "pattern_interrupts_count": 5,
  "shorts_moments_count": 3,
  "performance": null
}
```

## Critères d'analyse (pour le feedback analyzer)

Tous ces effets sont des **hypothèses à tester** sur la chaîne crypto : ils viennent de sources externes hors niche (vidIQ, TubeBuddy, Think Media, Paddy Galloway, Film Booth, Social Media Examiner) et n'ont pas été vérifiés sur les données de Nass. Ce sont des pistes de lecture, pas des faits.

| Facteur | Poids | Optimal supposé | Effet annoncé par la source (à vérifier) | Source annoncée |
|---|---|---|---|---|
| Hook < 5 s jusqu'à la promesse | Élevé | Oui | +15-20 % rétention à 30 s | vidIQ |
| Intro brandée | Élevé | < 3 s ou aucune | > 5 s = -10-15 % rétention | vidIQ / TubeBuddy |
| Cold open (pas d'intro) | Élevé | Oui | +25-30 % rétention 1ʳᵉ min | vidIQ |
| CTA dans les 15 premières s | Moyen | Non | -3-8 % de drop | vidIQ |
| Open loops | Élevé | Tous les 3-5 min | +10-20 % rétention mi-vidéo | Think Media |
| Escalade | Élevé | Chaque section > précédente | +20-40 % rétention 2ᵉ moitié | Paddy Galloway |
| Re-engagement hooks | Moyen | Toutes les 60-90 s | Micro-pics de rétention | Paddy Galloway |
| Mots « en conclusion » | Élevé | Jamais | Décrochage de 15-30 % | Paddy Galloway |
| Pacing (mots/min) | Moyen | 150-170 | < 130 = lent, > 190 = trop rapide | Social Media Examiner |
| Sujet unique / fil rouge | Élevé | 1 sujet clair | +20-30 % vs multi-sujet | non précisée |
| Structure numérotée | Moyen | Étapes / liste | +8-12 % rétention moyenne | vidIQ |
| Durée vidéo éducative | Moyen | 8-12 min | Rétention 45-55 % | Think Media |
| « Tu / vous » fréquent | Faible | Fréquent | +5-8 % rétention | Social Media Examiner |
| Aperçu du contenu < 10 s | Moyen | Oui | +8-12 % rétention | Film Booth |

## Anti-patterns à détecter

Bloquants (règles du cadre) :
- Promesse de gain, vocabulaire de jeu, levier / futures / short / prêt à intérêt, incitation au crédit.
- Chiffre ou prix sans source datée.
- Sujet memecoin non signalé à Nass.

À surveiller (hypothèses à tester) :
- « En conclusion » / « Pour résumer » / « Voilà » en fin de vidéo.
- Intro brandée > 5 s.
- CTA « abonne-toi » dans les 15 premières secondes.
- Section sans nouvelle info > 15 s.
- Pas d'open loop pendant > 5 min.
- Plusieurs sujets sans lien clair.

## Format des leçons (`lessons.json`)

```json
{
  "lessons": [
    {
      "rule": "Les hooks < 10 s avec curiosity gap retiennent X % vs Y % pour les hooks > 20 s",
      "evidence": "Basé sur N vidéos, corrélation hook_length_seconds avec retention_pct",
      "sample_size": 6,
      "confidence": "medium",
      "created_at": "AAAA-MM-JJ"
    }
  ],
  "structure_performance": {
    "tutorial": {"count": 0, "avg_retention": null, "avg_watch_time": null}
  }
}
```
