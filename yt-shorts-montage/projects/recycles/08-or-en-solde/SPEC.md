# SPEC — Short 08 « L'or est en solde » (Convergence EP.03, concept C « Les deux droites »)

GOAL:    le spectateur retient « l'or est 25 % sous son record ; pour un investisseur long terme, le prix d'entrée
         au dollar près n'est pas le plus important », et veut voir l'épisode complet.
OUTPUT:  HyperFrames, 1080 × 1920, 60 i/s. 44,0 s (39,85 s de voix + 4,15 s de fin) = 2 640 images.
SOURCE:  enregistrement vertical OBS/Aitum de l'EP.03, son égalisé (vertical = brut 16:9 − 1,76 s, vérifié par corrélation
         audio, score 0,98) ; transcription mot à mot de la session du 19/10 (`Videos/montage-ep03/transcript.json`).
CUT:     8 morceaux (cut.json), coupes recalées sur le creux du son ±50 ms, contrôlées par re-transcription (qa_voice.py).
         Sadek : prix / « question de moment ». Nass : correction de 30 %, soldes, long terme, investisseur, −5 %.
         Écartés (cadre) : « l'or n'ira pas à 2 100, c'est impossible », la « guerre atomique », trading avec liquidation.

LOOK:    papier #F2EFE8 + grille #E6E1D6 1 px / 96 px ; encre #0B0E11 ; droite verte #0F8A5F = Nass, droite or #C98A0B = Sadek,
         12 px bouts ronds ; texte or #A07006 (contraste ≥ 3:1) ; rouge #C8323F seulement pour −25 % / SOLDES ; gris #565D6B.
         Inter Tight 800 (accroche 104 px, sous-titres 70 px, mots clés 96–104 px), IBM Plex Mono 600 (étiquettes ≥ 28 px rendus).
DATA:    or GC=F (Yahoo Finance, clôtures quotidiennes 21/10/2024 → 19/10/2026) ; record en séance 5 586,2 $ le 29/01/2026 ;
         4 180 $ dit à l'antenne le 19/10/2026 (séance 4 155,6–4 211,2 $) ; −25 % = 4 180 / 5 586 − 1. Fichier assets/data/or-gcf.json.

STATES:  H accroche · CS graphique pendant que Sadek parle (Nass replié) · A Sadek parle · B Nass parle · CN graphique pendant que
         Nass parle · CN+ punch-in (Nass 1,44, Sadek 1,36). Visages recentrés par morceau (face_track.py, YuNet), sans trou.
MOTION:  chaque coupe de parole tombe au milieu d'une bascule de 0,6 s power3.inOut (droites + découpes + caméras + sous-titres
         ensemble) ; flou de bougé au rendu sur la scène, coupé sur les sous-titres ; mots clés expo.out 0,45–0,5 s ;
         fin : les droites forment un grand V (0,7 s) puis glissent dans le V du vrai logo SVG (0,5 s).
SOUND:   voix −14 LUFS / −1,5 dBTP ; 5 SFX (whoosh ×2 prises différentes, pop ×2, impact) normalisés au pic, tronqués, ~−9 dB.
BANNED:  fond sombre, glow, dégradés, cartes verre, pastilles, logo collé dans un coin, coupes sèches, musique,
         « IMPRIMANTE » / trading de Sadek, chiffres non sourcés, sous-titres sur un visage ou hors de la bande 168–1330.
