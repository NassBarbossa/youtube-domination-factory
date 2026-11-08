# SPEC — Short 21 « Montrez-moi des preuves » (Convergence EP.01, DA « Les deux droites », mise en page monologue v6)

GOAL:    le spectateur retient la position de Nass : pendant que BTC s'éclatait, l'or montait, donc « montrez-moi des preuves »
         que le bitcoin est une réserve de valeur.
OUTPUT:  HyperFrames, 1080 × 1920, 60 i/s. 39,54 s (35,39 s de voix + 4,15 s de fin).
SOURCE:  téléchargement YouTube `ZjNa7wxwFkM` (1080p, 30 i/s), scène « À L'ÉCRAN », faute de brut OBS sur le Mac (brut =
         YouTube + 68,9 s sur le PC Windows). Transcription `context/transcripts/ZjNa7wxwFkM-words.json`.
CUT:     6 morceaux (cut.json), 14:18 → 14:57 YouTube, contrôlés par re-transcription (qa_voice_mlx.py). Nass seul.
         Écartés : « le fait que Trump lance son memecoin » (14:14, memecoin), le « donc » de 14:30 (1,7 s de blanc),
         « et c'était assez du coup » (14:38), la suite à 14:57 (« ça me rajoutait des choses au côté où j'étais bearish »).
LOOK:    papier, grille, encre ; droite verte = Nass. Accroche à deux caméras « LE BITCOIN, / RÉSERVE DE VALEUR ? » (88 px),
         puis SOLO_E : l'écran TradingView de Nass (BTC, l'or en bleu par-dessus) sous lui pendant qu'il compare ; SOLO_N
         pour « quand on dit l'or, le bitcoin c'est une réserve de valeur » ; SOLO_E à nouveau pour la chute.
STATES:  H · SOLO_E · SOLO_E+ (caméra 880, écran fixe) · SOLO_N · SOLO_N+ · SOLO_E.
MOTION:  bascules de 0,6 s aux 5 coutures ; « RÉSERVE DE VALEUR » gris dans la bande sur « réserve », barré rouge sur « pas de
         preuves » ; mot clé « MONTREZ-MOI / DES PREUVES » (112 px) sur « montrez-moi », pulse sur « c'est pas une réserve » ;
         mot clé or « L'OR MONTAIT » sous l'écran à la place des derniers sous-titres ; fin V → logo → CTA.
DATA:    aucun chiffre à l'écran ; l'écran est le vrai écran de Nass.
SOUND:   voix −14 LUFS ; 5 SFX : whoosh (écran), pop (barré), pop (MONTREZ-MOI), whoosh grave (écran revient), impact.
END:     V → logo + CTA « Épisode 1 complet sur la chaîne » ; disclaimer dans la légende.
BANNED:  fond sombre, glow, B-roll, musique, coupe sèche, chiffres non sourcés, memecoin (coupé).
