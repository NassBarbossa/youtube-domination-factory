# REVIEW — Short 36 « Arrêter le TGV en pleine route » (EP.01, v1 du 2026-11-07)

## Choix
- Deuxième clip de l'EP.01, choisi par Claude faute de choix de Nass (il a dit « fais-moi un autre short ») : deux voix,
  cadre propre, même mise en page que le 35 donc mêmes crops.
- Sans écran : ni Sadek ni Nass ne montrent leur graphique dans ce passage. Beaucoup de papier à l'image : c'est le cas
  « orateurs sans écran » de la DA, à juger par Nass.
- `make_comp.py` dérivé de celui du 35 (états S+ / N+ ajoutés, écran retiré, mot de chute à la place de PATIENTER).

## Mesuré
- `hyperframes check` : 0 erreur, 8 avertissements `nested_media_start_basis_ambiguous` (attendus).
- Voix (`qa_voice_mlx.py`) : aucun mot coupé après avoir avancé le début de s1 de 0,14 s (« Je ne » était avalé).
- Rendu : 36,87 s, 1080 × 1920, 60 i/s, H.264 + AAC, −13,9 LUFS, crête vraie −1,4 dBTP, 7,9 Mo. Rendu en 2 min 25.

## Regardé seulement
- 24 images : accroche, chaque couture à ±0,12 s, « des bougies », « your friend », le mot de chute à 31,9 s, fin V → logo → CTA.

## Plan le plus faible
- Source YouTube 30 i/s, à refaire depuis le brut OBS (voir `../35-la-meilleure-position/HANDOFF-windows.md`, même méthode).
- Sadek regarde son écran pendant toute sa partie (visage de trois quarts, caméra sombre).

## Retours de Nass
- 2026-11-07 : « Mets les caméras plus grosses, les positionnements c'est pas optimisé pour les formats courts. » → v2 : médaillons
  de 660 à 740 px pour celui qui parle (440 à 520 pour l'autre), prescale 2,4 en lanczos (échelle CSS ≈ 1), tout resserré
  entre y 70 et 1560, accroche descendue à 740. L'image des caméras est plus douce (source de ~300 px grossie 2,4 ×) ;
  rendu v2 mesuré bon. En attente de son avis sur la v2.
- 2026-11-07, sur la v2 (capture d'écran) : « les écrans sont mal positionnés, les ronds des caméras sont trop petits ».
  → v3 : pleine hauteur, celui qui parle fait 900 à 940 px, l'autre 620 à 650, plus de zone vide en bas ; prescale 3,2 +
  accentuation légère (`sharpen` dans cut.json) ; recadrages resserrés au-dessus des étiquettes gravées (rayon 132 / 135).
  Rendu v3 mesuré bon. En attente de son avis.
- 2026-11-07, maquette dessinée sur la capture de la v2 (« mets comme ça ») : médaillon de Nass posé sur la droite verte,
  droite verte en vraie diagonale (630 à gauche → 830 à droite), sous-titres dans la bande, droite or horizontale, Sadek
  grand au milieu de la moitié basse. → v4 : états S/S+ nass=(540, 420, 620-640), vert (630, 830), cap 870, or 960, sadek=
  (540, 1440, 800-840) ; N/N+ en miroir (Nass 800-840 à 480, vert (880, 1080), or 1210, Sadek 620-650 à 1560) ; accroche à 900.
  Rendu v4 mesuré bon. En attente de son avis.
- 2026-11-07, sur la v4 : « en bas il y a 10 km d'espace ; même espace au-dessus de ma caméra qu'en dessous de celle du bas,
  même nombre de pixels entre les caméras et les droites et entre les droites ». → v5 : mise en page calculée (`sym()` dans
  make_comp.py) : un seul écart e partout (haut, caméra→droite, bande des sous-titres, droite→caméra, bas), droites
  horizontales. Parole : parleur 740-760 px, l'autre 660, e = 100-104. Accroche : 620/620, bande de 3e (e = 97). Écran (35) :
  Nass 480-500, écran 900 × 491, Sadek 520, e = 66-71. Sous-titres 66 px. Rendu v5 mesuré bon. En attente de son avis.
- 2026-11-07, sur la v5 : « les dispositions sont bien. Quand il y a des monologues, ça sert à rien de laisser les deux cams :
  tu reviens sur la cam 1 seconde avant que l'autre parle et tu laisses une cam ; nouvelle disposition, texte en dessous ;
  des animations, le train quand il dit TGV, la tendance est ton ami… » → v6 : états SOLO_S / SOLO_N (une caméra de 900-940 px
  en haut, écart 130, bande 1160-1790 avec zone d'illustrations 1180-1480 et sous-titres à 1600 agrandis × 1,25) ; retour aux
  deux caméras à 14,96 s (1,3 s avant Nass), Nass seul à 16,66 s. Illustrations SVG à l'encre dans la bande : niveau or +
  3 bougies, la 4e verte casse le niveau (« casse un niveau… bougies ») ; TGV qui entre à toute vitesse et pile avec un
  signal rouge (« TGV… route ») ; tendance verte qui se dessine + flèche, pulse sur « friend », flèche rouge à rebours sur
  « contre tendance » ; mot clé de chute sur deux lignes au centre de la bande. SFX : whoosh (Sadek seul), whoosh grave (train),
  pop (friend), impact. Rendu v6 mesuré bon. Le 35 reste en v5 (deux caméras) : à passer en monologue + écran une fois la v6 validée.
