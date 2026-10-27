# Feedback loop — détail (yt-script)

Référence chargée depuis `yt-script/SKILL.md`. Fichiers : `yt-script/memory/lessons.json` (lu avant d'écrire) et `yt-script/memory/choices.json` (complété après chaque script).

## Avant chaque script

1. Lire `yt-script/memory/lessons.json`.
2. Si des leçons ont `sample_size >= 3`, les intégrer : structure du hook, longueur des sections, anti-patterns à éviter. Lire aussi, s'il existe, `yt-analytics/history/studio-retention.json` : pourcentage à 30 s et premier creux des dernières vidéos. Les citer à Nass : « Tes vidéos avec [pattern] retiennent X % vs Y % sans ».
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
  "title_promise_slide": 1,
  "hook_length_words": 25,
  "hook_length_seconds_est": 8,
  "credentials_position": "none|after-payoff|before-payoff",
  "outbound_cta_in_hook": false,
  "has_branded_intro": false,
  "branded_intro_length_sec": 0,
  "num_sections": 6,
  "dictated_word_count": 375,
  "slides_count": 37,
  "target_duration_min": 11,
  "published_duration_sec": null,
  "open_loops_count": 3,
  "has_escalation": true,
  "cta_position": "end",
  "early_cta": false,
  "uses_conclusion_words": false,
  "structure_type": "tutorial|story|deep-dive|comparison|news|reaction",
  "intro_30s_pct": null,
  "first_dip_sec": null,
  "pattern_interrupts_count": 5,
  "shorts_moments_count": 3,
  "performance": null
}
```

## Critères d'analyse (pour le feedback analyzer)

Ce qui a été mesuré (Prepublish : 349 vidéos de 36 chaînes de 10 k à 6,6 M d'abonnés, puis réplication préenregistrée sur 941 vidéos de 96 chaînes de 1 000 à 20 000 abonnés ; liens dans `veille-scripts-2026-10-20.md`) :

| Signal d'ouverture (45 premières secondes) | Hits | Flops | Sur petites chaînes |
|---|---|---|---|
| Reprend la promesse du titre | 87,0 % | 77,9 % | 79,2 % contre 80,4 % : plus de différence |
| Ne donne aucune raison de continuer | 10,2 % | 16,3 % | non mesuré |
| Ouvre sur un bloc de contexte | 18,6 % | 26,2 % | non mesuré |
| Affirmation concrète d'entrée | 33,3 % | 25,0 % | 22,2 % contre 19,8 % : plus de différence |
| Salutation d'entrée | 7,3 % | 11,6 % | 16,6 % contre 23,3 % : seul signal répété |
| Débit (mots/min) | 181 | 180 | 169 contre 170 : nul |
| Mot du premier payoff | 14 | 15 | nul |

Conclusion des auteurs pour les petites chaînes : « hook anatomy is unlikely to be why a small channel's video underperforms; topic and packaging are the prime suspects ». Le débit est donc retiré des critères, et le temps jusqu'au point aussi. Le tableau ci-dessous garde les **hypothèses à tester** venues de sources hors niche (vidIQ, TubeBuddy, Think Media, Paddy Galloway, Film Booth, Social Media Examiner) : aucun de leurs chiffres n'a été retrouvé dans une source primaire le 20 octobre 2026. Ce sont des pistes de lecture, pas des faits.

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
| Sujet unique / fil rouge | Élevé | 1 sujet clair | +20-30 % vs multi-sujet | non précisée |
| Structure numérotée | Moyen | Étapes / liste | +8-12 % rétention moyenne | vidIQ |
| Durée | Moyen | celle que le contenu demande | comparer à la médiane de la chaîne (26,8 % et 29,7 % sur 9:29 et 11:10 au 13 octobre 2026), pas à un repère externe | données de la chaîne |
| « Tu / vous » fréquent | Faible | Fréquent | +5-8 % rétention | Social Media Examiner |
| Aperçu du contenu < 10 s | Moyen | Oui | +8-12 % rétention | Film Booth |

## Anti-patterns à détecter

Bloquants (règles du cadre) :
- Promesse de gain, vocabulaire de jeu, levier / futures / short / prêt à intérêt, incitation au crédit.
- Chiffre ou prix sans source datée.
- Sujet memecoin non signalé à Nass.

À surveiller (hypothèses à tester) :
- « En conclusion » / « Pour résumer » / « Voilà » en fin de vidéo.
- Intro brandée > 5 s, ou bloc de légitimité avant le premier payoff.
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
