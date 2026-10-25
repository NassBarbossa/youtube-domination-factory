# SPEC — Short 09 « Apprends-moi à faire de l'oseille » (Convergence EP.03, concept C « Les deux droites »)

GOAL:    le spectateur retient « une compétence numérique monnayable + vivre là où c'est moins cher + un pourcentage
         de ses revenus dans l'or, le Bitcoin, le S&P 500 », et veut voir l'épisode complet.
OUTPUT:  HyperFrames, 1080 × 1920, 60 i/s.
TIME:    durée fixée par la liste de coupes (cible 38–46 s) × 60 = ~2 500 images. Pas de musique : la voix est l'horloge.

SOURCE:  enregistrement vertical OBS/Aitum de l'EP.03, son égalisé (1080 × 1920, 60 i/s) :
         bloc caméra Nass en haut, deck/écran au milieu, bloc caméra Sadek en bas. Recalage audio sur la version YouTube.
         On recadre à l'intérieur des blocs caméra (sans les étiquettes gravées NASS/SADEK/LIVE ni les bordures).

LOOK:    sol papier #F2EFE8 + grille #E6E1D6 1 px tous les 96 px (convergence.css) ; encre #0B0E11 ;
         droite verte #0F8A5F = Nass, droite or #C98A0B = Sadek, trait 12 px bouts ronds ; les deux couleurs ne servent
         qu'aux droites, au mot actif des sous-titres (couleur de celui qui parle) et à la fin.
         Titres / sous-titres : Inter Tight 800, sous-titres 76 px (min 56), interlettrage −1 % ; accroche 92 px.
         Étiquettes : IBM Plex Mono 600, 26 px, +14 % d'interlettrage (NASS, SADEK, EN ASIE, EN FRANCE) — prénoms seuls.
         Pas d'ombre portée sur la vidéo ; les panneaux vidéo sont des découpes nettes du papier, bord = la droite.
OBJECTS: deux personnes réelles (Nass qui parle, Sadek qui écoute), la question du chat en bulle style deck (« @ … »),
         une égalité de deux montants dits par Nass (pas un graphique inventé), le V de Convergence qui devient le logo.

LAYOUT (état « Nass parle ») :
         panneau Nass : y 0 → droite verte (de (0, 900) à (1080, 1000)), recadrage ~1,6× ;
         bande papier entre les droites : droite or de (0, 1290) à (1080, 1150) ; sous-titres centrés dans la bande ;
         panneau Sadek : sous la droite or → 1920, visage placé vers y 1250–1450.
         Zone UI : rien à lire au-dessus de y 168 ni sous y 1330 ; rien sous la colonne de boutons à droite (x > 960, y > 900).
         État « Sadek réagit » : bande remontée (verte de (0, 380) à (1080, 470), or de (0, 760) à (1080, 640)), Sadek prend l'écran.
         État « chiffre » : les droites s'écartent (verte ~(0, 560)→(1080, 620), or ~(0, 1340)→(1080, 1280)), égalité dans la bande.

MOTION:  bascule de la bande (droites + découpes en même temps) 0,6 s power3.inOut, centrée sur le mot ;
         punch-in visage 1,00 → 1,10 en 0,6 s power2.inOut, tenu, retour sur une fin de phrase ;
         mots clés : entrée expo.out 0,5 s (échelle 1,25 → 1, opacité 0 → 1), sortie 0,2 s power2.in ;
         sous-titres : groupes de 2–3 mots, mot actif coloré, apparition par mot en 0,07 s, aucun déplacement ;
         flou de bougé au rendu (data-motion-blur) sur les déplacements rapides, jamais de filtre CSS sur la vidéo ;
         au plus un plan toutes les ~0,8 s ; pas de coupe sèche : les coupes de parole tombent sous une bascule ou un mot clé.
         Fin : les deux droites pivotent et se rejoignent (0,7 s power3.inOut) → V qui se trace comme le logo (dash 0,8 s)
         → mot-symbole CONVERGENCE, puis « Épisode complet sur la chaîne » et le disclaimer, tenus 2,5 s.

SHOTS (à caler sur la liste de coupes) :
         0,0–~2,0  accroche : bulle « @ apprends-moi à faire de l'oseille » posée dans la bande, Nass la lit → la bulle s'efface
                   sur « compétences » ; son : rien.
         ~2–9      Nass : développer des compétences monnayables ; punch-in sur « monnayables » ; mot clé COMPÉTENCES MONNAYABLES.
         ~9–15     les exemples (réseaux sociaux, montage vidéo, vente en ligne) tombent un par un sur la droite verte, Plex Mono ;
                   son : un tick discret au premier.
         ~15–18    bascule vers Sadek qui écoute (masque une coupe), retour ; son : zip à l'aller.
         ~18–28    « je vis en Asie » → les droites s'ouvrent : 600–800 € (EN ASIE) = 2 000–3 000 € (EN FRANCE), mots de Nass ;
                   son : tick à l'arrivée du signe =.
         ~28–36    « un pourcentage de votre rentrée d'argent » → L'OR · LE BITCOIN · LE S&P 500, un mot par ~0,8 s.
         fin       convergence des droites → V → logo, CTA, disclaimer ; son : clic quand les droites se touchent.

SOUND:   voix seule, −14 LUFS intégrés, crête ≤ −1 dBTP ; 4–5 SFX en tout, chacun normalisé au pic, tronqué 0,3–0,6 s,
         posé 1 image après son événement, 3–6 dB sous la voix.

BANNED:  fond sombre/vide, glow, néon, particules, dégradés, cartes verre ; tout centré qui glisse vers le haut en fondu ;
         pastilles arrondies ; étiquettes « 01 / 02 » ; logo collé dans un coin ; trois cartes en rang ; texte qui bouge
         pendant qu'on le lit ; coupes sèches et secousses d'une image ; musique ; « IMPRIMANTE » et tout ce qui touche
         au trading de Sadek ; chiffres non dits par Nass.

QA:      image 0 (accroche lisible, visage visible) ; chaque bascule ±0,2 s (pas de saut) ; l'égalité (lisible à 360 px) ;
         les trois mots finaux ; la fin (V = logo) ; aucune lecture hors de la bande 168–1330 ; sous-titres jamais sur un visage.
