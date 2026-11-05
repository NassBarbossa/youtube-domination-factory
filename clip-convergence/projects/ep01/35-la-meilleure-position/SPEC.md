# SPEC — Short 35 « La meilleure des positions » (Convergence EP.01, DA « Les deux droites », variante écran + médaillons)

GOAL:    le spectateur retient « à la résistance, mieux vaut patienter : ne pas prendre de position, c'est la meilleure des
         positions », entend les deux voix, et veut voir l'épisode complet.
OUTPUT:  HyperFrames, 1080 × 1920, 60 i/s. 36,11 s (31,96 s de voix + 4,15 s de fin).
SOURCE:  **téléchargement YouTube `ZjNa7xwFkM` (1080p, 30 i/s), faute de brut OBS sur le Mac** (le brut 16:9 est sur le PC
         Windows, `~/Videos/2026-10-05 14-36-21.mp4`, brut = YouTube + 68,9 s). Même mise en page « À L'ÉCRAN » dans les deux
         fichiers : les crops se reportent tels quels, seul `source` et `raw_to_source` changent dans `cut.json`.
         Transcription : `context/transcripts/ZjNa7wxwFkM-words.json` (mlx-whisper large-v3-turbo, temps YouTube).
CUT:     6 morceaux (cut.json), 19:31 → 20:13 YouTube, coupes recalées sur le creux du son ±50 ms, contrôlées par
         re-transcription (qa_voice_mlx.py). Nass : traders / investisseurs, break de structure → retest → on envoie,
         giga résistance → patienter, « comme dirait un certain philosophe ». Sadek : la phrase du philosophe. Nass : « Exactement ».
         Écartés (cadre) : « je suis plus à la hausse sur les cryptos » (1183,4–1186,2, avis directionnel), « pour des
         investisseurs on en a parlé avant » (redite), « je serais plus favorable à la hausse » (1163,7–1169,3).

LOOK:    papier #F2EFE8 + grille ; encre #0B0E11 ; droite verte = Nass, droite or = Sadek. **Variante** : dans la scène
         « À L'ÉCRAN » de l'EP.01, les caméras sont des ronds de ~330 px, trop petits pour les cadres du pilote 08. Les deux
         caméras rondes deviennent des médaillons (cercle vert / or de 14 px, crops `[52, 687, 298, 298]` et `[1564, 680, 304, 304]`,
         étiquettes NASS / SADEK gravées hors du crop), posés sur le papier au-dessus de la droite verte et sous la droite or.
         L'écran réel de Nass (TradingView BTC, crop `[380, 230, 1155, 630]` → 1012 × 552, sans la watchlist ni le compte)
         occupe la bande quand il explique (son dessin break / retest à 5 s).
STATES:  H accroche (médaillons centrés, « LA MEILLEURE / DES POSITIONS », POSITIONS en or : c'est Sadek qui conclut) ·
         E Nass explique à l'écran (Nass en haut à gauche, écran, sous-titres sous l'écran, Sadek en bas à droite) ·
         E+ punch-in · N Nass parle · S Sadek parle. Grossissement total ≤ 1,6 (vérifié par assertion dans make_comp.py).
MOTION:  chaque coupe de parole au milieu d'une bascule de 0,6 s power3.inOut (droites + médaillons + sous-titres) ;
         flou de bougé au rendu, coupé sur les sous-titres ; mot clé PATIENTER (104 px, souligné vert) remplace le dernier
         sous-titre de s3 ; fin : grand V → V du logo → « Épisode 1 complet sur la chaîne ».
DATA:    aucun chiffre à l'écran (le passage n'en a pas de vérifiable). « 100 % » reste dans la voix et les sous-titres.
SOUND:   voix −14 LUFS / −1,5 dBTP ; 4 SFX : whoosh (ouverture de l'écran), pop (PATIENTER), whoosh grave (passage à Sadek),
         impact (droites → logo). Pas de musique.
END:     V → logo + CTA ; disclaimer dans la légende, pas à l'image.
BANNED:  fond sombre, glow, B-roll, musique, coupe sèche, étiquettes du live dans les médaillons, chiffres non sourcés,
         sous-titres sur un visage ou hors de la bande.
