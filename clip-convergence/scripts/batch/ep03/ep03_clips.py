
clip("56-un-range-bien-degoutant", 56, "Un range bien dégoûtant",
 "Nass sur le graphique : depuis le 28 septembre, rien ne s'est passé, on est dans un range bien dégoûtant ; un peu de résilience acheteuse, on le casse peut-être aujourd'hui, mais « on n'est pas sorti de l'auberge ». Son écran TradingView sous lui.",
 "UN RANGE<br><b>BIEN DÉGOÛTANT</b>",
 [("en daily là tu vois bien", "il s'est rien passé"), ("depuis lundi 28 on était là", "dans un range bien dégoûtant"), ("depuis le 28 septembre depuis l'immense chute", "on n'est pas sorti de l'auberge")],
 '''SCR = screen_only(900, 506, kw_h=915)   # même boîte d'écran que SOLO_E (sy 1141) : Nass est hors de sa caméra sur s1-s2
S["H"] = SCR
c.screen_state = "H"
TOP = SCR["kw_top"]
c.fix = {("s2", "rennes"): "range"}
t_rien, t_auberge = find("s2", "grand"), find("s3", "auberge")
c.hook_fade = E[1] - 0.3
c.moves = [(E[1], "SOLO_E"), (t_auberge - 1.1, "H")]
c.screen_windows = [(0, c.END_T)]
c.punch([seams[0]])
c.kwc("kw-rien", "PAS GRAND-CHOSE", GREY, t_rien - 0.3, E[1] - 0.3, size=72, top=TOP + 700)
c.kwc("kw-chute", "PAS SORTI<br>DE L'AUBERGE", GREEN, t_auberge - 0.5, c.END_T + 0.45, size=84, top=TOP + 330, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh", E[1] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", t_auberge - 1.32, 0.26), ("sfx-pop-1", "pop", t_auberge - 0.48, 0.3)]
''', after=1079, hook_font=92, screen=("s1", "s2", "s3"))

clip("57-pile-ou-face", 57, "Pile ou face",
 "Sadek sur le range : « on s'est fait éclater » la semaine d'avant, trop d'indécision, à l'achat comme à la vente tu es touché, c'est pile ou face ; décision de se concentrer sur l'éducatif ; « j'ai pas envie de trader tant qu'on sort pas de cette zone, j'ai besoin d'une tendance ». Coupe de « je pourrais te montrer les retraits » (19:06–19:18).",
 "PILE<br><b>OU FACE</b>",
 [("on s'est fait éclater", "la semaine d'avant"), ("parce qu'en fait ce qui se passe", "c'est un peu pile ou face"), ("donc là on a pris la décision", "faire comprendre aux gens"), ("j'ai pas envie de trader tant qu'on sort pas", "d'une tendance")],
 '''S["H"] = solo("sadek", 760)   # Nass est penché hors de sa caméra sur tout le passage : Sadek seul
c.fix = {("s1", "?"): ""}
c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+"), (E[2], "SOLO_S")]
t_indecision, t_pile, t_educatif, t_besoin = find("s2", "indécision"), find("s2", "pile"), find("s3", "éducatif"), find("s4", "besoin")
c.kwc("kw-indecision", "TROP<br>D'INDÉCISION", GREY, t_indecision - 0.2, t_pile - 0.9, size=72)
c.kwc("kw-pile", "PILE OU FACE", RED, t_pile - 0.2, t_pile + 1.4, size=84, top=1270)
c.kwc("kw-educatif", "PLUS D'ÉDUCATIF", INK, t_educatif - 0.2, E[2] - 0.3, size=76, top=1270)
c.kwc("kw-chute", "J'AI BESOIN<br>D'UNE TENDANCE", GREEN, t_besoin - 0.3, c.END_T + 0.45, size=76, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_indecision - 0.18, 0.26), ("sfx-pop-2", "pop", t_pile - 0.18, 0.3),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_educatif - 0.18, 0.26), ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-4", "pop", t_besoin - 0.28, 0.3)]''',
 after=1121, hook_font=104, speakers=["sadek"] * 4)

clip("58-si-les-actions-chutent", 58, "Si les actions chutent ?",
 "Nass demande les corrélations ; Sadek : si les actions chutent, il voit l'or monter, le Bitcoin continuer une montée tranquille en escalier, une rotation de liquidités ; les actions ne chutent jamais vraiment, elles corrigent. Coupe avant « vous ne reverrez jamais le NAS100 à 16 000 » (certitude).",
 "SI LES ACTIONS<br><b>CHUTENT ?</b>",
 [("quand les actions chutent est ce que toi", "des corrélations communes"), ("alors si les actions chutent je vois plus l'or monter", "en escalier"), ("je pense qu'il y aura une rotation de liquidités", "c'est totalement différent")],
 '''c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+")]   # Sadek seul dès sa réponse : les mots clés vivent dans la bande solo
t_or, t_bitcoin, t_rotation, t_corrigent = find("s2", "or"), find("s2", "bitcoin"), find("s3", "rotation"), find("s3", "corrigent")
c.kwc("kw-or", "L'OR MONTE", GOLD_TXT, t_or - 0.2, t_bitcoin - 0.9, size=84, top=1270)
c.kwc("kw-bitcoin", "LE BITCOIN<br>EN ESCALIER", INK, t_bitcoin - 0.2, E[1] - 0.3, size=72)
c.kwc("kw-rotation", "UNE ROTATION<br>DE LIQUIDITÉS", GREY, t_rotation - 0.2, t_corrigent - 0.9, size=70)
c.kwc("kw-chute", "LES ACTIONS NE CHUTENT PAS,<br>ELLES CORRIGENT", GREEN, t_corrigent - 0.3, c.END_T + 0.45, size=58, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_or - 0.18, 0.26), ("sfx-pop-2", "pop", t_bitcoin - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_rotation - 0.18, 0.26), ("sfx-pop-4", "pop", t_corrigent - 0.28, 0.3)]''',
 after=1287, hook_font=92, speakers=["nass", "sadek", "sadek"])

clip("59-au-milieu-de-range-on-temporise", 59, "Au milieu de range, on temporise",
 "Sadek, côté investissement : acheter sur les supports, revendre sur les résistances ; au milieu de range, ça peut partir dans les deux sens, ce n'est pas une zone où se presser et cliquer partout : temporiser, analyser, attendre une direction claire et la suivre. Coupe de « ou alors shorter pour ceux qui shortent ». L'écran or de Nass pendant l'explication.",
 "AU MILIEU<br><b>DE RANGE</b>",
 [("Là, pour clôturer la partie investissement", "et plutôt revendre"), ("sur les résistances.", "dans les deux sens."), ("Donc, que ça soit sur BTC", "de cliquer de partout."), ("C'est plutôt des zones où", "suivre la direction qui est donnée.")],
 '''S["SOLO_ES"] = solo_screen(860, 900, 506, cam="sadek")   # Sadek seul avec l'écran de Nass (Nass ne parle pas dans ce clip)
c.screen_state = "SOLO_ES"
t_supports, t_temporiser, t_direction = find("s1", "supports"), find("s4", "temporiser"), find("s4", "direction")
c.moves = [(t_supports - 0.3, "SOLO_S"), (E[0], "SOLO_ES"), (E[2], "SOLO_S+")]
c.screen_windows = [(E[0], E[2])]
c.hook_fade = t_supports - 0.45
c.kwc("kw-supports", "ACHETER SUR LES SUPPORTS,<br>REVENDRE SUR LES RÉSISTANCES", INK, t_supports - 0.1, E[0] - 0.3, size=54)
c.kwc("kw-temporiser", "TEMPORISER,<br>ANALYSER", GREY, t_temporiser - 0.2, t_direction - 0.9, size=76)
c.kwc("kw-chute", "ATTENDRE UNE<br>DIRECTION CLAIRE", GREEN, t_direction - 0.3, c.END_T + 0.45, size=72, anim="rise")
SFX = [("sfx-pop-1", "pop", t_supports - 0.08, 0.26), ("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_temporiser - 0.18, 0.26), ("sfx-pop-3", "pop", t_direction - 0.28, 0.3)]''',
 after=1406, hook_font=104, screen=("s2", "s3"), speakers=["sadek"] * 4)

clip("60-l-or-est-en-solde", 60, "L'or est en solde",
 "Sadek : pas une question de zone, une question de moment ; en investissement, acheter de l'or à ce prix est un très bon prix, en trading avec peu de marge de manœuvre, attention. Nass sur son graphique : du point haut on est sur une correction de 30 %, « les soldes » entre guillemets ; en achat long terme, se positionner là n'est pas très risqué ; le prix d'entrée exact n'est pas le plus important quand vous êtes investisseur. Reprise en DA du pilote 08 (validé le 2026-10-25). « L'or n'ira pas à 2 100, c'est impossible » (24:51) et la guerre atomique restent hors clip.",
 "L'OR EST<br><b>EN SOLDE</b>",
 [("ce n'est pas une question de zone", "c'est un très bon prix."), ("Quand on est dans de l'investissement", "c'est un très mauvais moment."), ("vous regardez, quand vous descendez du point haut", "entre guillemets."), ("Donc ce qui veut dire c'est que dans une optique d'achat long terme", "à ce niveau-là."), ("ce n'est pas le plus important", "quand vous êtes des investisseurs.")],
 '''SCR = screen_only(900, 506)   # Nass est hors de sa caméra sur s3-s4 : son écran seul, mots clés dans la zone haute
S["SCR"] = SCR
c.screen_state = "SCR"
TOP = SCR["kw_top"]
t_moment, t_trading, t_soldes, t_important = find("s1", "moment"), find("s2", "trading"), find("s3", "soldes"), find("s5", "important")
c.moves = [(t_moment - 0.3, "SOLO_S"), (E[0], "SOLO_S+"), (E[1], "SCR"), (E[3], "SOLO_N+")]
c.screen_windows = [(E[1], E[3])]
c.punch([seams[2]])
c.hook_fade = t_moment - 0.45
t_correction = find("s3", "correction")
c.kwc("kw-correction", "UNE CORRECTION", GREY, t_correction - 0.2, t_soldes - 0.9, size=92, top=TOP + 100)
c.kwc("kw-soldes", "« LES SOLDES »", GOLD_TXT, t_soldes - 0.2, E[3] - 0.3, size=100, top=TOP + 100)
c.kwc("kw-moment", "UNE QUESTION<br>DE MOMENT", INK, t_moment - 0.1, E[0] - 0.3, size=72)
c.kwc("kw-trading", "EN TRADING :<br>ATTENTION", RED, t_trading - 0.2, E[1] - 0.3, size=72)
c.kwc("kw-chute", "PAS LE PLUS IMPORTANT<br>QUAND VOUS INVESTISSEZ", GREEN, t_important - 0.3, c.END_T + 0.45, size=58, anim="rise")
SFX = [("sfx-pop-1", "pop", t_moment - 0.08, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_trading - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3), ("sfx-whoosh-3", "whoosh", E[3] - 0.22, 0.26), ("sfx-pop-3", "pop", t_important - 0.28, 0.3)]''',
 after=1454, hook_font=104, screen=("s3", "s4"), speakers=["sadek", "sadek", "nass", "nass", "nass"])

clip("61-apprends-moi-a-faire-de-l-oseille", 61, "Apprends-moi à faire de l'oseille",
 "Question du chat lue par Nass : deux points de vue ; Sadek, focalisez-vous sur le trading ; Nass, développer des compétences monnayables, une activité digitale, et pendant que vous charbonnez, un pourcentage de vos rentrées dans les marchés : l'or, le Bitcoin, le S&P 500. Coupe de « partir de la France… en Asie avec 600–800 € » (30:04–30:33).",
 "APPRENDS-MOI À FAIRE<br><b>DE L'OSEILLE</b>",
 [("apprends moi à faire de l'oseille", "points de vue différents"), ("Sadek lui il est dans une approche", "faites de l'argent avec le trading."), ("Moi, je suis dans une optique", "qui sont monnayables,"), ("il faut que vous ayez une activité digitale", "que ça soit le SP500")],
 '''c.fix = {("s4", "SP500"): "S&P 500"}
S["H"] = solo("nass", 760)   # fauteuil de Sadek vide sur ce passage (aucun visage détecté) : Nass seul
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_deux, t_trading, t_competences, t_pourcentage, t_or = find("s1", "deux"), find("s2", "trading"), find("s3", "compétences"), find("s4", "pourcentage"), find("s4", "or,")
c.kwc("kw-deux", "DEUX POINTS DE VUE", GREY, t_deux - 0.2, E[0] - 0.3, size=76, top=1270)
c.kwc("kw-trading", "SADEK :<br>LE TRADING", INK, t_trading - 0.2, E[1] - 0.3, size=72)
c.kwc("kw-competences", "MOI : DES COMPÉTENCES<br>MONNAYABLES", INK, t_competences - 0.2, E[2] - 0.3, size=60)
c.kwc("kw-pourcentage", "UN POURCENTAGE<br>DANS LES MARCHÉS", GREY, t_pourcentage - 0.2, t_or - 0.9, size=66)
c.kwc("kw-chute", "L'OR, LE BITCOIN,<br>LE S&amp;P 500", GOLD_TXT, t_or - 0.3, c.END_T + 0.45, size=72, anim="rise")
SFX = [("sfx-pop-1", "pop", t_deux - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_trading - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_competences - 0.18, 0.26), ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-4", "pop", t_pourcentage - 0.18, 0.26), ("sfx-pop-5", "pop", t_or - 0.28, 0.3)]''', after=1768, hook_font=72)

clip("62-budget-pour-commencer", 62, "Budget pour commencer ?",
 "Question du chat : budget pour commencer ? Nass, en investissement : 10 à 20 % de votre salaire par mois ; Sadek, en trading : le moins possible, « vous allez perdre de l'argent au début », ça prend les bonnes habitudes, n'allez pas mettre tout votre capital. Fin avant le passage en fullcam (31:46,8) ; « ne faites pas cette erreur-là » (31:46,5) tombe sur le changement de mise en page, non repris.",
 "BUDGET<br><b>POUR COMMENCER ?</b>",
 [("Budget pour commencer", "de votre activité par mois"), ("après pour le trading", "combien pour commencer ?"), ("Le mois possible", "les bonnes habitudes directement"), ("donc le moins possible", "dans le trading")],
 '''c.fix = {("s3", "mois"): "moins", ("s3", "?"): ""}
S["H"] = solo("nass", 760)   # fauteuil de Sadek vide au début du passage (il revient pendant la question)
t_pct, t_moins, t_perdre, t_moins2 = find("s1", "10"), find("s3", "mois"), find("s3", "perdre"), find("s4", "capital")
c.hook_fade = t_pct - 0.45
c.moves = [(t_pct - 0.3, "SOLO_N"), (E[0], "SOLO_N+"), (E[1] - 1.3, "N"), (E[1], "SOLO_S"), (E[2], "SOLO_S+")]   # retour aux deux caméras 1,3 s avant Sadek
c.kwc("kw-pct", "INVESTIR : 10 À 20 %<br>DU SALAIRE PAR MOIS", INK, t_pct - 0.2, E[0] - 0.3, size=60)
c.kwc("kw-moins", "TRADING :<br>LE MOINS POSSIBLE", INK, t_moins - 0.2, t_perdre - 0.35, size=66)
c.kwc("kw-perdre", "VOUS ALLEZ PERDRE<br>AU DÉBUT", RED, t_perdre - 0.15, E[2] - 0.3, size=66)
c.kwc("kw-chute", "PAS TOUT<br>VOTRE CAPITAL", GREEN, t_moins2 - 0.3, c.END_T + 0.45, size=76, anim="rise")
SFX = [("sfx-pop-1", "pop", t_pct - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3),
       ("sfx-pop-2", "pop", t_moins - 0.18, 0.26), ("sfx-pop-3", "pop", t_perdre - 0.18, 0.3), ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-4", "pop", t_moins2 - 0.28, 0.3)]''',
 after=1870, hook_font=84, speakers=["nass", "nass", "sadek", "sadek"])

clip("63-c-est-quoi-l-altseason", 63, "C'est quoi l'altseason ?",
 "« Quand aura lieu l'altseason ? » : le commentaire qui trigger Nass depuis des années, parce que c'est un problème de définition : un altcoin, c'est tout coin alternatif à Bitcoin. Aujourd'hui il y a une inflation des cryptos (tout le monde peut créer la sienne en une seconde), la liquidité ne peut plus aller partout, elle se concentre dans quelques actifs. Coupes : memecoins à 5 000 de market cap (32:47–32:57, signalé), tokens nommés et « pas comme 2021 » (32:57–33:34).",
 "C'EST QUOI<br><b>L'ALTSEASON ?</b>",
 [("quand aura lieu la alt season", "qui m'a trigger"), ("parce que j'ai compris avec le temps", "un problème de définition"), ("donc déjà il faut se rappeler", "alternative coin altcoin"), ("Maintenant, il y a une inflation des cryptos", "qui valent vraiment le coup.")],
 '''c.fix = {("s1", "alt"): "altseason", ("s1", "season"): ""}
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]   # monologue de Nass : états solo, Sadek écoute hors champ
t_definition, t_alternative, t_inflation, t_liquidite, t_concentree = find("s2", "définition"), find("s3", "alternative"), find("s4", "inflation"), find("s4", "liquidité"), find("s4", "concentrée")
c.kwc("kw-definition", "UN PROBLÈME<br>DE DÉFINITION", INK, t_definition - 0.2, t_definition + 2.5, size=72)
c.kwc("kw-alt", "ALTCOIN = TOUT CE QUI<br>N'EST PAS BITCOIN", INK, t_alternative - 0.2, E[2] - 0.3, size=60)
c.kwc("kw-inflation", "UNE INFLATION<br>DES CRYPTOS", GREY, t_inflation - 0.2, t_liquidite - 0.9, size=72)
c.kwc("kw-liquidite", "LA LIQUIDITÉ NE PEUT<br>PLUS ALLER PARTOUT", GREY, t_liquidite - 0.2, t_concentree - 0.9, size=60)
c.kwc("kw-chute", "CONCENTRÉE DANS<br>QUELQUES ACTIFS", GREEN, t_concentree - 0.3, c.END_T + 0.45, size=70, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_definition - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_alternative - 0.18, 0.26), ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-3", "pop", t_inflation - 0.18, 0.26),
       ("sfx-pop-4", "pop", t_liquidite - 0.18, 0.26), ("sfx-pop-5", "pop", t_concentree - 0.28, 0.3)]''', after=1935, hook_font=92, layout="full")

clip("64-le-trading-c-est-dur", 64, "L'investissement c'est facile, le trading c'est dur",
 "Question du chat : est-ce que c'est dur le trading ? Nass : l'investissement c'est facile, le trading c'est dur. Sadek : totalement d'accord, très difficile, émotionnellement (« si des fois je suis un peu à cran, c'est que c'est très difficile »), jamais il dira que c'est facile ; par contre quand ça paye et que tu sais minimiser ton exposition, c'est génial. Son trade en lots (34:58) reste hors clip.",
 "L'INVESTISSEMENT C'EST FACILE,<br><b>LE TRADING C'EST DUR</b>",
 [("Est-ce que c'est dur le trading ?", "le trading, c'est dur."), ("Oui, je suis totalement d'accord", "c'est très difficile, le trading."), ("Jamais de la vie", "C'est génial.")],
 '''c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+")]
t_emotion, t_jamais, t_genial = find("s2", "Émotionnellement"), find("s3", "Jamais"), find("s3", "génial")
c.kwc("kw-emotion", "ÉMOTIONNELLEMENT<br>TRÈS DIFFICILE", RED, t_emotion - 0.2, E[1] - 0.3, size=66)
c.kwc("kw-jamais", "JAMAIS JE NE DIRAI<br>QUE C'EST FACILE", INK, t_jamais - 0.2, t_genial - 1.3, size=60)
c.kwc("kw-chute", "QUAND ÇA PAYE :<br>C'EST GÉNIAL", GREEN, t_genial - 1.1, c.END_T + 0.45, size=76, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_emotion - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_jamais - 0.18, 0.26), ("sfx-pop-3", "pop", t_genial - 0.28, 0.3)]''', after=2069, hook_font=60, layout="full", speakers=["nass", "sadek", "sadek"])

clip("65-payer-pour-apprendre", 65, "Payer pour apprendre ?",
 "Sadek : you have to pay to learn, ça dépend avec qui ; ceux qui ne veulent pas payer paieront plus cher au final, en temps ; rien contre la gratuité, c'est votre argent, ça dépend si vous avez du capital. Puis : contre le copy trading, « ce n'est pas du tout ce que je veux pour vous, je veux transmettre et que vous soyez autonomes ». « J'en fournis parce que c'est un service qui vous intéresse » (37:41–37:47, son offre) reste hors clip.",
 "PAYER<br><b>POUR APPRENDRE ?</b>",
 [("You have to pay to learn", "c'est très bien aussi."), ("Pour ceux qui ne veulent pas payer", "perdre plus de temps."), ("mais moi j'ai rien contre le fait", "si vous avez du capital ou pas"), ("moi je suis contre le copy trading,", "moi je suis contre le copy trading,"), ("très clairement, ce n'est pas du tout ce que je veux pour vous", "soyez autonome.")],
 '''c.moves = [(E[0], "SOLO_S+"), (E[2], "SOLO_S"), (E[3], "SOLO_S+")]
t_payer, t_gratuite, t_copy, t_autonome = find("s2", "payer"), find("s3", "gratuité"), find("s4", "copy"), find("s5", "autonome")
c.kwc("kw-payer", "VOUS PAIEREZ PLUS CHER :<br>EN TEMPS", RED, t_payer - 0.2, E[1] - 0.3, size=58)
c.kwc("kw-gratuite", "RIEN CONTRE<br>LA GRATUITÉ", GREY, t_gratuite - 0.2, E[2] - 0.3, size=72)
c.kwc("kw-copy", "CONTRE LE<br>COPY TRADING", INK, t_copy - 0.2, t_autonome - 1.5, size=72)
c.kwc("kw-chute", "JE VEUX QUE VOUS<br>SOYEZ AUTONOMES", GREEN, t_autonome - 1.3, c.END_T + 0.45, size=68, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_payer - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_gratuite - 0.18, 0.26), ("sfx-whoosh-3", "whoosh", E[3] - 0.22, 0.26), ("sfx-pop-3", "pop", t_copy - 0.18, 0.26), ("sfx-pop-4", "pop", t_autonome - 0.28, 0.3)]''',
 after=2161, hook_font=92, layout="full", speakers=["sadek"] * 5)

clip("66-vendeur-de-formation-arnaqueur", 66, "Vendeur de formation = arnaqueur ?",
 "Nass : même en 2026, les formations sont mal vues en France, « vendeur de formation, forcément un arnaqueur », alors qu'il y a tout sur YouTube ; plein de gens ont des techniques différentes (lui l'investissement et le trading on-chain, Sadek les marchés traditionnels), le temps que vous cherchez, vous vous perdez ; si la personne est légitime, c'est plus simple de la suivre pour gagner du temps. Pas d'appel à acheter : il dit lui-même qu'il ne vend plus de formation.",
 "VENDEUR DE FORMATION<br><b>= ARNAQUEUR ?</b>",
 [("même en 2026", "symptomatique de la France"), ("quand t'es vendeur de formation", "il y a tout sur Youtube"), ("qu'il y a plein de gens qui ont des techniques", "Qu'est-ce qui va plus vous plaire ?"), ("c'est plus simple si vous trouvez que la personne", "de faire votre avis"), ("si la personne est légitime, c'est plus simple", "si vous n'avez pas l'habitude")],
 '''t_symptomatique, t_arnaqueur, t_moi, t_sadek, t_legitime, t_temps = find("s1", "symptomatique"), find("s2", "arnaqueur"), find("s3", "moi"), find("s3", "Sadek"), find("s4", "légitime"), find("s5", "temps")
c.hook_fade = t_symptomatique - 0.45
c.moves = [(t_symptomatique - 0.3, "SOLO_N"), (E[0], "SOLO_N+"), (E[1], "SOLO_N"), (E[2], "SOLO_N+"), (E[3], "SOLO_N")]
c.kwc("kw-symptomatique", "SYMPTOMATIQUE<br>DE LA FRANCE", GREY, t_symptomatique - 0.2, E[0] - 0.3, size=66)
c.kwc("kw-arnaqueur", "« FORCÉMENT<br>UN ARNAQUEUR »", RED, t_arnaqueur - 0.2, E[1] - 0.3, size=66)
c.kwc("kw-moi", "MOI : L'INVESTISSEMENT<br>ON-CHAIN", INK, t_moi - 0.2, t_sadek - 0.9, size=60)
c.kwc("kw-sadek", "SADEK : LES MARCHÉS<br>TRADITIONNELS", INK, t_sadek - 0.2, E[2] - 0.3, size=60)
c.kwc("kw-legitime", "UNE PERSONNE<br>LÉGITIME", GREY, t_legitime - 0.2, E[3] - 0.3, size=72)
c.kwc("kw-chute", "PLUS SIMPLE,<br>POUR GAGNER DU TEMPS", GREEN, t_temps - 0.3, c.END_T + 0.45, size=64, anim="rise")
SFX = [("sfx-pop-1", "pop", t_symptomatique - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_arnaqueur - 0.18, 0.3),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_moi - 0.18, 0.26), ("sfx-pop-4", "pop", t_sadek - 0.18, 0.26),
       ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-5", "pop", t_legitime - 0.18, 0.26), ("sfx-whoosh-4", "whoosh", E[3] - 0.22, 0.26), ("sfx-pop-6", "pop", t_temps - 0.28, 0.3)]''',
 after=2181, hook_font=66, layout="full")

clip("67-le-trading-est-un-jeu-de-menteurs", 67, "Le trading est un jeu de menteurs",
 "Sadek : comprendre le carnet d'ordres est intéressant, s'y reposer est suicidaire ; ceux qui vous vendent le carnet d'ordres, le footprint, mentent ; maîtrisez le maximum de concepts, utilisez-en le moins, cherchez la convergence et la confluence ; « le trading est un jeu de menteurs : trois menteurs qui disent la même chose sans se connaître, c'est la vérité, et vous êtes là pour la trouver ». C'est le passage du titre et de la miniature de l'épisode. Nass est remplacé par son punk à l'image : Sadek seul.",
 "LE TRADING EST<br><b>UN JEU DE MENTEURS</b>",
 [("C'est intéressant d'avoir une compréhension", "de se reposer que dessus."), ("Donc, tous ceux qui vous disent", "sont des gens qui mentent."), ("Moi, ce que je dis en trading", "de la confluence."), ("Le trading est un jeu de menteur.", "pour trouver la vérité.")],
 '''c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+"), (E[2], "SOLO_S")]
t_suicidaire, t_mentent, t_maitrisez, t_moins, t_trois, t_verite = find("s1", "suicidaire"), find("s2", "mentent"), find("s3", "maîtrisez"), find("s3", "moins"), find("s4", "trois"), find("s4", "vérité.")
c.hook_fade = t_suicidaire - 0.45
c.kwc("kw-suicidaire", "S'Y REPOSER :<br>SUICIDAIRE", RED, t_suicidaire - 0.1, E[0] - 0.3, size=72)
c.kwc("kw-mentent", "DES GENS<br>QUI MENTENT", GREY, t_mentent - 0.2, t_maitrisez - 0.9, size=72)
c.kwc("kw-maitrisez", "MAÎTRISER<br>LE MAXIMUM", INK, t_maitrisez - 0.2, t_moins - 0.9, size=72)
c.kwc("kw-moins", "EN UTILISER<br>LE MOINS", INK, t_moins - 0.2, E[2] - 0.3, size=72)
c.kwc("kw-trois", "TROIS MENTEURS,<br>LA MÊME CHOSE", GREY, t_trois - 0.2, t_verite - 0.9, size=66)
c.kwc("kw-chute", "VOUS ÊTES LÀ POUR<br>TROUVER LA VÉRITÉ", GREEN, t_verite - 0.3, c.END_T + 0.45, size=62, anim="rise")
SFX = [("sfx-pop-1", "pop", t_suicidaire - 0.08, 0.3), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_mentent - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_maitrisez - 0.18, 0.26), ("sfx-pop-4", "pop", t_moins - 0.18, 0.26),
       ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-5", "pop", t_trois - 0.18, 0.26), ("sfx-pop-6", "pop", t_verite - 0.28, 0.3)]''',
 after=2412, hook_font=76, layout="punk", speakers=["sadek"] * 4)

clip("68-vous-etes-tous-meilleurs-que-moi", 68, "Vous êtes tous meilleurs que moi",
 "Sadek, dernière question : ça ne sert à rien de demander ce qu'on pense d'un tel ou un tel ; il ne répondra jamais, « vous êtes tous des bons et moi je suis là pour être le meilleur » ; « vous êtes tous meilleurs que moi, moi je suis là pour être meilleur que vous ». Sadek seul (Nass en punk).",
 "VOUS ÊTES TOUS<br><b>MEILLEURS QUE MOI</b>",
 [("Dernière question, les gars.", "Posez-nous des questions."), ("Je ne vais jamais répondre", "un tel c'est pas bon"), ("vous êtes tous meilleurs que moi", "meilleur que vous")],
 '''c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+")]
t_bons, t_meilleur, t_moi = find("s2", "bons"), find("s2", "meilleur"), find("s3", "moi")
c.kwc("kw-bons", "VOUS ÊTES<br>TOUS DES BONS", GREY, t_bons - 0.2, t_meilleur - 0.9, size=72)
c.kwc("kw-meilleur", "MOI, JE SUIS LÀ<br>POUR ÊTRE LE MEILLEUR", INK, t_meilleur - 0.2, E[1] - 0.3, size=58)
c.kwc("kw-chute", "MEILLEUR<br>QUE VOUS", GREEN, t_moi - 0.3, c.END_T + 0.45, size=84, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_bons - 0.18, 0.26), ("sfx-pop-2", "pop", t_meilleur - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_moi - 0.28, 0.3)]''', after=2469, hook_font=80, layout="punk", speakers=["sadek"] * 3)

clip("69-c-est-quoi-un-carnet-d-ordres", 69, "C'est quoi un carnet d'ordres ?",
 "Sadek réexplique : en trading, les ordres sont votre manière de passer vos commandes au marché ; exécution au marché, vous êtes pris au prix affiché ; un carnet d'ordres répertorie tous les ordres passés et montre les zones de réaction, là où beaucoup d'ordres attendent. Coupe de ses exemples de prix (39:39–39:59). Sadek seul (Nass en punk).",
 "C'EST QUOI<br><b>UN CARNET D'ORDRES ?</b>",
 [("j'ai déjà répondu plein de fois", "passer vos commandes au marché"), ("vous pouvez passer un ordre", "si je clique sur acheter, mon ordre est pris"), ("Donc c'est un carnet d'ordre.", "beaucoup d'ordres en attendant.")],
 '''c.moves = [(E[0], "SOLO_S+"), (E[1], "SOLO_S")]
t_commandes, t_execution, t_repertorier, t_zones = find("s1", "commandes"), find("s2", "exécution"), find("s3", "répertorier"), find("s3", "zones")
c.kwc("kw-commandes", "VOS COMMANDES<br>AU MARCHÉ", INK, t_commandes - 0.2, E[0] - 0.3, size=72)
c.kwc("kw-execution", "EXÉCUTION<br>AU MARCHÉ", GREY, t_execution - 0.2, E[1] - 0.3, size=72)
c.kwc("kw-repertorier", "TOUS LES ORDRES<br>PASSÉS AU MARCHÉ", INK, t_repertorier - 0.2, t_zones - 0.9, size=62)
c.kwc("kw-chute", "LES ZONES<br>DE RÉACTION", GREEN, t_zones - 0.3, c.END_T + 0.45, size=80, anim="rise")
SFX = [("sfx-pop-1", "pop", t_commandes - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_execution - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_repertorier - 0.18, 0.26), ("sfx-pop-4", "pop", t_zones - 0.28, 0.3)]''',
 after=2358, hook_font=76, layout="punk", speakers=["sadek"] * 3)

clip("70-une-bonne-situation-financiere", 70, "Une bonne situation financière ?",
 "Dernière question lue par Nass : faut-il une bonne situation financière pour commencer le trading ? Sadek : pour commencer, apprendre, ça n'a rien à voir ; pour l'exercer comme une activité, annexe ou principale, oui, il faut une bonne situation financière. Teaser court ; Sadek seul à l'image (Nass en punk), la voix de Nass sur la question.",
 "UNE BONNE SITUATION<br><b>FINANCIÈRE ?</b>",
 [("est-ce que c'est important", "une bonne situation financière"), ("alors pour commencer le trading", "n'a rien à voir"), ("pour commencer à exercer", "bien vrai")],
 '''c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+")]
t_rien, t_activite, t_oui = find("s2", "rien"), find("s3", "activité"), find("s3", "oui")
c.kwc("kw-rien", "POUR APPRENDRE :<br>RIEN À VOIR", GREY, t_rien - 0.2, t_activite - 0.9, size=70)
c.kwc("kw-activite", "EN FAIRE<br>UNE ACTIVITÉ ?", INK, t_activite - 0.2, t_oui - 0.9, size=72)
c.kwc("kw-chute", "OUI, IL FAUT UNE BONNE<br>SITUATION FINANCIÈRE", GREEN, t_oui - 0.3, c.END_T + 0.45, size=58, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_rien - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_activite - 0.18, 0.26), ("sfx-pop-3", "pop", t_oui - 0.28, 0.3)]''', after=2680, hook_font=76, layout="punk", speakers=["nass", "sadek", "sadek"])
