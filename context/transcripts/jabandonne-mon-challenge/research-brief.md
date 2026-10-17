# Brief de recherche — « J'abandonne mon challenge »

Slug : `jabandonne-mon-challenge` · Funnel : TOP (posé par défaut, non confirmé) · Date de recherche : 2026-10-16.

Sujet : Nass arrête son challenge public après 4 semaines de surplace, explique qu'il faut s'adapter au marché, qu'il « connaît sa ligue » (80 % de perdants / 20 % de gagnants, pyramide top 20 % → 10 % → 1 % → 0,1 %), et choisit la patience en attendant de meilleures conditions.

Méthode : pas de `veille.db` sur le VPS (commande muette, veille non relancée). Recherche yt-dlp (9 requêtes FR + 4 EN), transcripts via `uv run yt-transcript/scripts/get_transcript.py` (la lib n'est pas dans le Python système ; `uv` fait le travail). Falco : l'API a refusé, sous-titres auto FR récupérés avec yt-dlp puis aplatis (texte brut conservé). Stats : sources primaires ouvertes quand c'était possible (dashboards Dune, PDF AMF, communiqué ESMA) ; sinon presse spécialisée citant Dune, marquée non vérifiée.

Signal cadre : le sujet touche aux memecoins et à Pump.fun (hors narrative de la chaîne) et au challenge (abandonné dans le cadre). Cette vidéo est la vidéo de clôture : elle parle du challenge pour le fermer. À confirmer avec Nass que c'est bien l'exception voulue.

## Vidéos analysées

| # | Chaîne | Titre | Video ID | Vues | Date | Langue |
|---|--------|-------|----------|------|------|--------|
| 1 | Falco | CES 7 ERREURS M'ont Fait PERDRE -23,468€ en TRADING MEMECOIN (ne fais pas pareil...) | VS96nwO_P_g | 4 434 | 2024-11-27 | FR |
| 2 | Morgano2.0 | Day 13 memecoin trading: I lost everything | uN1aJOZwWQQ | 30 277 | 2026-10-03 | EN |
| 3 | Khye (Khye Unscripted) | I Quit *MEMECOINS*, Here's Why. | RCqgK2R7jqs | 1 933 | 2025-11-11 | EN |
| 4 | OnChain Education | The Memecoin Era is Over (Stop Trading Memecoins) | 8BAgtuL7-ss | 3 182 | 2025-11-06 | EN |
| 5 | Ethan Prosper | 5 Things I Wish I Knew Before Trading Memecoins (Learn From My Mistakes) | 2WX5kk_XYng | 29 399 | 2025-11-03 | EN |

Récupérés mais non retenus : threadguy `YD807o2EUCg` (résumé de stream, 28 min de bavardage actions/NFL, rien d'exploitable sur l'arrêt du trading) ; starwifpump `LGBmX78sK5M` (tutoriel de trading, pas un bilan). Fichiers conservés dans le dossier.

Terrain FR : quasi vierge. Aucune vidéo FR « j'arrête mon challenge crypto » trouvée. Falco est la seule vidéo FR memecoin avec un bilan chiffré de pertes, et elle sert à vendre un Discord. Les résultats FR sont pollués par le prop-firm (Ilan Bialylew, Gautier Smith) et par Kryptoo (vlogs sans rapport).

## Faits clés

### Stats demandées par Nass : part des wallets perdants sur Pump.fun / memecoins Solana

| Fait | Source | Vérifié (source primaire, date) |
|------|--------|---------------------------------|
| Part mensuelle de wallets Pump.fun en profit réalisé : plancher 30,08 % (juin 2025), sommet 79,54 % (juin 2026), 75,38 % (juil. 2026), 59,84 % (août 2026, mois incomplet, 862 734 wallets). Donc 40 à 70 % de perdants selon le mois. | Dune, dashboard « Pump.fun Trader Profitability » de coingecko_content, dune.com/coingecko_content/pump-fun-annual-trader-profitability | OUI, dashboard ouvert le 2026-10-16 |
| Distribution août 2026 (même dashboard) : profit 0-500 $ = 51,45 % ; 500-1 000 $ = 3,08 % ; > 1 000 $ = 5,31 % ; perte < 500 $ = 38,80 % ; perte 500-1 000 $ = 0,64 % ; perte > 1 000 $ = 0,71 %. | Idem | OUI, 2026-10-16 (pourcentages recalculés à partir des comptes) |
| Avril 2026 : 73,28 % de wallets profitables sur 3 142 559 ; 65,14 % ont gagné entre 1 et 500 $ ; 5,37 % plus de 1 000 $ ; 25,23 % ont perdu moins de 500 $. | CoinGecko Research, « Pump.fun Traders Are Making a Comeback » (màj 2026-05-07), même dashboard Dune | OUI pour le dashboard (ouvert) ; les chiffres d'avril sont repris de l'article de l'auteur du dashboard |
| Méthode du dashboard : PnL réalisé seulement (positions non vendues exclues, donc pertes sous-estimées), flux nettés par wallet, bots et wash trading non filtrés, 1 wallet ≠ 1 personne. | Idem, notes de méthodologie | OUI |
| Janv. 2025, cumul depuis le lancement : 13,55 M de wallets ; 55 296 (0,41 %) ont réalisé > 10 000 $ ; 0,048 % > 100 000 $ ; 293 (0,002 %) > 1 M$. « Réaliser 10 000 $ fait de vous un wallet du top 0,412 % » (Adam Tehc). | Cointelegraph 2025-01-11, citant le Dune d'Adam Tehc (post X du 10 janv.) | NON : le dashboard d'Adam Tehc ouvert le 2026-10-16 n'affiche que revenus et frais ; la vue « Alpha Wallets » n'a pas été lue. Critique d'Alon (Pump.fun) : achats post-bonding Raydium exclus, non-réalisé exclu |
| Juin 2025, fenêtre 6 mois : 62,5 % des wallets en perte ; > 4,2 M wallets ; profits 1-10 k$ ≈ 4,5 % ; 10-100 k$ ≈ 1 % ; 100 k$-1 M$ = 4 705 (0,1 %) ; > 1 M$ = 311 (< 0,01 %). | crypto.news 2025-06-05, citant Dune jhackworth (query 5233371) | NON : le dashboard jhackworth/pumpfun ouvert le 2026-10-16 ne contient pas de PnL ; l'article a des incohérences internes (244 130 « profitables » ≠ 27,2 %) |
| Mars 2026 : ~1,4 M de wallets, 49 à 50,6 % en perte ; 96 % en perte OU sous 500 $ de profit (le « 96 % de perdants » viral est une erreur de lecture) ; 2 wallets > 1 M$ dans le mois. | BeInCrypto, DailyCoin, mexc, citant le Dune de @oladee | NON (dashboard non localisé) |
| Août 2026, « 94 % des traders memecoin Solana perdants sur 90 jours » : 304 161 wallets actifs, 19 003 (6,25 %) en profit, 88 % des gagnants < 100 $, 25 wallets > 10 000 $ (données FOMO app), perte médiane 120 $, pertes totales estimées 1,26 Md$. | Cointribune 2026-08-20, Cryptopolitan, HTX | NON : aucune source primaire nommée pour les 304 161 wallets ; chiffre repris d'un dashboard non identifié |
| « 3 % des utilisateurs de Pump.fun ont gagné plus de 1 000 $ » (cumul). | The Defiant ; Solana Compass 2026-06-10 citant « dashboards Dune » | NON |
| Taux de graduation Pump.fun : ~1,4 % historique ; 0,7 % fin févr. 2025 ; pic 2,1 % en juin 2024. | Solana Compass 2026-06-10 (Dune adam_tehc), The Block févr. 2025 | NON |
| Dashboard jhackworth : ~34,7 M d'adresses cumulées, ~22,9 M de tokens lancés, 20 208 tokens lancés le jour consulté, 312,6 M$ de frais cumulés. | Dune jhackworth/pumpfun | OUI, 2026-10-16 (ordres de grandeur, données adresses tronquées) |
| Dashboard Adam Tehc : 1,546 Md$ de revenus cumulés Pump.fun, ~1,5 M$/jour de frais pumpdotfun + ~1 M$/jour pumpswap début oct. 2026. | Dune adam_tehc, dashboard « Pump.Fun » | OUI, 2026-10-16 |

### Stats « officielles » de régulateurs (trading actif des particuliers, hors crypto)

| Fait | Source | Vérifié |
|------|--------|---------|
| AMF, étude 2009-2012 sur 14 799 clients actifs de prestataires agréés (Forex, CFD) : plus de 89 % de clients perdants sur 4 ans ; résultat moyen -10 887 € ; médian -1 843 € ; 13 224 clients ont perdu 175 M€ au total, 1 575 ont gagné 13,8 M€. « Entre 2009 et 2012, 90 % des clients ont été perdants. » | AMF, Lettre de l'Observatoire de l'épargne n° 10, octobre 2014 (PDF) | OUI, PDF lu le 2026-10-16 |
| AMF, même étude : plus on est actif, plus on perd. ≥ 250 ordres sur 4 ans (52 % des clients) : -18 741 € en moyenne ; ≥ 1 000 ordres (23 %) : -31 349 €. Pas d'effet d'apprentissage : chez les traders actifs les 4 années, le taux de perdants passe de 82 % (2009) à 88 % (2009-2012), perte moyenne 26 745 €. « Les traders les plus actifs et réguliers voient leurs pertes se creuser. » | Idem | OUI |
| ESMA, 27 mars 2018 : « 74-89 % des comptes de particuliers perdent de l'argent » sur les CFD, pertes moyennes 1 600 à 29 000 € par client. Origine du bandeau obligatoire des brokers. | ESMA, communiqué de presse (esma.europa.eu/node/84933) | OUI, lu le 2026-10-16 |

### Chiffres des concurrents (jamais des faits)

| Chiffre | Source | Statut |
|---------|--------|--------|
| « 99 % des traders sont non rentables » | Ethan Prosper (2WX5kk_XYng), Falco (« 99 % des personnes qui tradent... font de l'argent, c'est tout ») | Non sourcé, ne pas reprendre |
| « 1 SOL → 700 000 $ en 7 mois » | Ethan Prosper | Chiffre de gain d'un concurrent, jamais un fait |
| « -23 468 € » de pertes | Falco (titre) | Témoignage invérifiable |
| Portefeuille de 6,5 SOL à 0,005 SOL (7 cents), -800 $ en sept., gains cumulés 300 $ | Morgano2.0 | Témoignage, non vérifié |
| « Liquidation du 10 octobre : 20 Md$ de capital spéculatif effacés » | OnChain Education | Non recoupé ici |

## La pyramide de Nass face aux données

Pyramide dictée : 80 % de perdants · top 20 % légèrement au-dessus du break-even (quelques centaines $/mois) · top 10 % à 5-10 k$+/mois · top 1 % à six chiffres/mois · top 0,1 % à des millions/mois.

| Étage de Nass | Ce que disent les données | Verdict |
|---------------|---------------------------|---------|
| 80 % de perdants | Pump.fun, PnL réalisé mensuel : 27 % de perdants (avr. 2026), 40 % (août 2026), ~70 % (juin 2025). Fenêtre 6 mois (juin 2025) : 62,5 %. Étude 90 jours (août 2026, non vérifiée) : 94 %. Régulateurs (CFD/Forex) : 89 % AMF, 74-89 % ESMA. | NON confirmé comme constante sur Pump.fun. Entre 27 % et 94 % selon la fenêtre et la méthode. Le « 80 % » tient comme simplification honnête si Nass dit « selon le mois, entre 4 sur 10 et 9 sur 10 » et cite l'AMF pour le trading actif en général |
| Top 20 % : quelques centaines $/mois | 51 % (août 2026) à 65 % (avr. 2026) des wallets gagnent entre 1 et 500 $ dans le mois. 88 % des gagnants de l'étude 90 jours font moins de 100 $. | Confirmé dans l'esprit, mais c'est la majorité des wallets, pas 20 %. La vraie leçon : presque tous les « gagnants » gagnent des miettes |
| Top 10 % : 5-10 k$+/mois | Seulement 5,31 % des wallets dépassent 1 000 $ dans le mois (août 2026). Plus de 10 000 $ réalisés : 0,41 % en cumul (Adam Tehc), ~1 % sur 6 mois (jhackworth). | NON confirmé. 5-10 k$ c'est le top ~1 %, pas le top 10 % |
| Top 1 % : six chiffres/mois | > 100 000 $ réalisés en cumul : 0,048 % (Adam Tehc) à 0,1 % (jhackworth), et c'est du cumul depuis 2024, pas du mensuel. | NON confirmé. Six chiffres c'est le top 0,05-0,1 %, en cumul |
| Top 0,1 % : des millions/mois | > 1 M$ réalisés en cumul : 293 à 311 wallets, soit 0,002 à 0,01 %. En mars 2026, 2 wallets sur 1,4 M dans le mois. | NON confirmé. Les millions c'est le top 0,01 % au mieux, et sur toute la vie du wallet |

Pyramide appuyée par les données (à proposer à Nass, `[PROP]`) : perdants 40 à 70 % selon le mois · gagnants de miettes (1-500 $) ~50 à 65 % · plus de 1 000 $ dans le mois ~5 % · plus de 10 000 $ réalisés ~0,4 à 1 % · plus de 100 000 $ ~0,05 à 0,1 % · plus de 1 M$ ~0,002 à 0,01 %. Réserve à dire à l'écran : ce sont des wallets, pas des personnes (multi-wallets, bots), et du PnL réalisé.

Le fait le plus utile pour l'angle « patience » : sur le même dashboard, la part de wallets gagnants passe de 30 % (juin 2025) à 80 % (juin 2026) en un an. Le régime de marché explique l'essentiel du résultat, pas le talent. Nass qui attend « les conditions où il est performant » est exactement ce que ces courbes suggèrent. Deuxième fait : l'AMF montre que les plus actifs perdent le plus et qu'il n'y a pas d'apprentissage avec le temps. Un argument de régulateur pour « acheter rarement ».

## Angles couverts par les concurrents

- Les émotions, le FOMO, le revenge trading comme cause n°1 des pertes — Falco, Morgano2.0
- L'over-trading (« fixe-toi un objectif et ferme l'ordinateur ») — Falco
- Le marché a changé : PvP, bundles, insiders, KOLs et streamers qui vendent sur leurs abonnés, copy-traders comme exit liquidity — Khye, OnChain Education, Ethan Prosper (en creux)
- « Tu es le produit / l'exit liquidity », « le jeu est truqué contre toi » — OnChain Education, Khye, Falco
- Arrêter les new pairs et pivoter : coins migrés (Khye), tokens utilitaires et DCA long terme (OnChain Education)
- La transparence comme différenciation (« je n'ai ni side wallets ni copy-traders ») — Khye
- La confession brute, filmée à chaud, « j'ai tout perdu » — Morgano2.0
- Savoir quitter la table — OnChain Education (métaphore poker, exclue chez nous)
- « 99 % des traders perdent » balancé sans source — Ethan Prosper, Falco
- Upsell d'outils, bots, Discord, groupes payants — Falco, Ethan Prosper

## Angles manquants (opportunités)

- Personne ne montre un vrai chiffre sourcé : aucun concurrent n'affiche un dashboard Dune, l'AMF ou l'ESMA. Tous disent « 99 % » ou « la plupart » sans preuve.
- Personne ne découpe la pyramide des gains (part > 1 k$, > 10 k$, > 100 k$, > 1 M$). La « ligue » avec des étages chiffrés est un terrain vide.
- Personne ne relie le résultat au régime de marché : la part de gagnants qui oscille de 30 % à 80 % selon le mois, donc « le moment » compte plus que « la méthode ».
- Personne ne cite un régulateur : l'AMF (89 % de perdants, les plus actifs perdent le plus, pas d'apprentissage) donne la version « officielle » que Nass demandait, et elle vaut pour tout trading actif, pas seulement les memecoins.
- Personne ne parle à un investisseur classique : l'avatar a de l'immobilier, un peu de bourse. Le parallèle « on n'achète pas un appartement par semaine » n'existe nulle part.
- Personne n'explique la réserve wallet ≠ personne, PnL réalisé ≠ réel. Le dire rend Nass plus crédible que tous.
- Personne n'arrête sans vendre autre chose derrière : Falco et Ethan Prosper vendent un Discord, OnChain Education un groupe payant. Un arrêt sans upsell d'outil est en soi différenciant.
- Aucune vidéo FR sur ce sujet précis.

## Citations utilisables

- « Le marché ne s'adapte pas à toi. » (« the market doesn't adapt to you ») — Morgano2.0, uN1aJOZwWQQ
- « Je ne suis pas le seul à avoir perdu. Tout le monde a perdu. Je n'ai rien de spécial. » — Morgano2.0
- « Si tu trades encore des memecoins tous les jours, tu es le business model. Tu es le produit. » — OnChain Education, 8BAgtuL7-ss
- « Arrête de jouer au jeu des memecoins et commence à jouer le long terme. » — OnChain Education (reformuler : « jouer » exclu du vocabulaire)
- « Ce n'est que de la liquidité qui passe d'une personne à une autre et revient à la première. » — Khye, RCqgK2R7jqs
- « Les seuls qui gagnent gros prennent l'argent de leurs spectateurs. » — Khye
- « Je ne serai pas rentable tous les jours et c'est normal. Même le meilleur trader du monde fait des pertes. Ceux qui vous diront le contraire vous vendent du rêve. » — Falco, VS96nwO_P_g
- « Entre 2009 et 2012, 90 % des clients ont été perdants sur ces marchés. Par ailleurs, les apprentis traders qui ont "persévéré" n'ont fait qu'aggraver leurs pertes au fil du temps. » — AMF, Lettre de l'Observatoire n° 10, oct. 2014 (source primaire)
- « 74-89 % of retail accounts typically lose money on their investments » — ESMA, 27/03/2018 (source primaire)
- « Realizing $10,000 makes you a top 0.412 % wallet » — Adam Tehc via Cointelegraph, janv. 2025 (non vérifié)

## Recommandation d'angle pour Nass

Angle : « J'arrête, et voici les chiffres qui m'ont décidé. » Nass fait ce qu'aucun concurrent ne fait : il ferme son challenge en montrant le tableau de bord réel, pas un ressenti. Structure proposée : (1) l'annonce et le bilan 4 semaines, chiffres de Nass datés et sourcés ; (2) « ma ligue » avec la pyramide corrigée par les données, en gardant la simplification 80/20 à l'oral mais en affichant les vrais étages (5 % au-dessus de 1 000 $, 0,4 % au-dessus de 10 000 $, 0,01 % millionnaires) et la réserve wallets/personnes ; (3) la preuve que le moment compte plus que la méthode : part de gagnants de 30 % à 80 % selon le mois sur le même dashboard, plus l'AMF qui montre que les plus actifs perdent le plus ; (4) la conclusion dans la narrative : on n'achète pas tous les jours, on achète rarement, quand les conditions sont là, comme pour un bien immobilier. CTA TOP : la formation offerte en 3 vidéos.

Ce que ça apporte face aux concurrents : ils expliquent l'échec par les émotions ou par les insiders ; Nass l'explique par le régime de marché et sa place dans la distribution, chiffres primaires à l'appui. Le spectateur repart intelligent (il sait lire une distribution et un régime), pas humilié. Réserve halal : pas de métaphore poker/casino/« quitter la table », pas de « pari » ; on parle d'achats, de patience, de conditions de marché. Réserve cadre : memecoins et Pump.fun apparaissent comme le terrain qu'on quitte, pas comme un sujet à creuser ; à valider avec Nass.
