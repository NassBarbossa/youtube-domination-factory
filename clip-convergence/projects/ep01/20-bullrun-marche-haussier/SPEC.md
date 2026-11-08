# SPEC — Short 20 « Bullrun = marché haussier » (Convergence EP.01, DA « Les deux droites », mise en page monologue v6)

GOAL:    le spectateur retient que « bullrun » veut dire « marché haussier », que la question « c'est reparti ? » est un
         problème de définition, et la pique finale : « vous ne voyez pas devant vous qu'il est déjà en train de repartir ? ».
OUTPUT:  HyperFrames, 1080 × 1920, 60 i/s. 41,16 s (37,01 s de voix + 4,15 s de fin).
SOURCE:  téléchargement YouTube `ZjNa7wxwFkM` (1080p, 30 i/s), scène « À L'ÉCRAN », faute de brut OBS sur le Mac (brut =
         YouTube + 68,9 s sur le PC Windows). Transcription `context/transcripts/ZjNa7wxwFkM-words.json`.
CUT:     6 morceaux (cut.json), 12:48 → 13:18 puis 15:42 → 15:51 YouTube, contrôlés par re-transcription (qa_voice_mlx.py).
         Nass seul. Écartés : « Et donc pour moi on a eu cette grosse correction » (13:19, enchaîne sur le 34, chiffres à
         vérifier), « Donc là maintenant achetez-la » (15:51, appel à acheter).
LOOK:    papier, grille, encre ; droite verte = Nass. Accroche à deux caméras (« TU PENSES QUE / C'EST REPARTI ? », vert :
         c'est Nass qui conclut), puis Nass seul (SOLO_N, 900 px), SOLO_N+ sur « Mais pour moi, un bullrun », puis SOLO_E :
         son écran TradingView BTC (crop 380/230/1155/630, 900 × 491) sous lui pour « vous ne voyez pas devant vous ».
STATES:  H · SOLO_N · SOLO_N+ · SOLO_E. Écarts égaux (sym / solo / solo_screen).
MOTION:  bascules de 0,6 s aux coutures ; bulles « ? » qui poppent à chaque « tu penses… » (4) ; définition BULLRUN =
         MARCHÉ HAUSSIER qui s'écrit sur « bullrun pour moi c'est un marché haussier » et pulse sur « Mais pour moi, un
         bullrun » ; mot clé de chute « DÉJÀ EN TRAIN DE REPARTIR » sous l'écran à la place des derniers sous-titres ;
         fin V → logo → CTA.
DATA:    aucun chiffre à l'écran.
SOUND:   voix −14 LUFS ; 4 SFX : whoosh (Nass seul), pop (BULLRUN), whoosh grave (l'écran s'ouvre), impact.
END:     V → logo + CTA ; disclaimer dans la légende.
BANNED:  fond sombre, glow, B-roll, musique, coupe sèche, chiffres non sourcés, appel à acheter (coupé).
