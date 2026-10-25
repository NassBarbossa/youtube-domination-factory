# REVIEW — Short 08 « L'or est en solde » (pilote du concept C)

## Choix créatifs
- Pilote = Short 08 au lieu du 09 prévu : pendant toute la réponse du 09 (« faire de l'oseille »), le fauteuil de Sadek est vide.
- Concept retenu par Nass : C « Les deux droites ». Non construits : B « Le Terminal », A « Le Plateau » (STORYLINES.md).
- La droite or devient la vraie courbe de l'or ; sur « soldes », le −25 % devient un tampon « SOLDES · −25 % ».
- À l'écran, chiffres réels et datés (−25 %), même quand la voix dit « presque 30 % » / « 30 % » (paroles gardées telles quelles).
- Fin : les deux droites deviennent le V, puis glissent dans le V du logo officiel ; « Épisode 3 complet sur la chaîne » + disclaimer.

## Mesuré
- `hyperframes check` : ok, 0 erreur. Avertissements gardés : 14 × `nested_media_start_basis_ambiguous` (la scène démarre à 0,
  minutage local = global) ; 1 info `escaped_container` sur un soulignement de sous-titre (36,7 s, non visible à l'image).
- Coupes de voix contrôlées par re-transcription faster-whisper : aucun mot coupé.
- Lisibilité à 360 px (planche téléphone) : sous-titres, prix et mots clés lisibles.
- Son : mesuré sur le rendu (voir ci-dessous), pas écouté.

## Regardé seulement
- Chaque coupe à ±0,12 s : masquée par la bascule (flou de bougé), visages recentrés.

## Plan le plus faible
- Le bas de l'écran (≈ 1 550–1 920 px) reste du papier vide quand Sadek est en bas : sa caméra n'est pas assez haute pour
  remplir sans agrandir au-delà de 1,6× (flou). Zone couverte par l'interface TikTok / Shorts.
- Le long morceau s5a (11 s) repose sur le graphique (impulsions, flèche, zone −5 %).

## Pièges rencontrés (pour les 9 autres)
- `data-motion-blur="on"` fait disparaître un conteneur de sous-titres qui se déplace : `data-motion-blur="off"` sur #capwrap.
- OpenCV 5 n'a plus Haar : YuNet (`face_detection_yunet_2023mar.onnx`).
- faster-whisper + PyAV de ce PC : passer l'audio en numpy ; CUDA sans cublas64_12.dll : CPU int8.

## Retours de Nass (v2, 2026-10-25)
- « Quand je disais là, machin, je montrais le graphique » : pendant ses explications, son écran réel (TradingView + ses dessins)
  remplace le graphique redessiné ; le graphique redessiné reste sur les chiffres de Sadek. Tampon SOLDES et son pop retirés.
- Outro : « Pas un conseil en investissement. » retiré de l'image à sa demande → à mettre dans la légende du Short.
- Rendu v2 mesuré : 44,0 s, 1080×1920, 60 i/s, −15,4 LUFS, crête vraie −1,2 dBTP, aucun écrêtage.
