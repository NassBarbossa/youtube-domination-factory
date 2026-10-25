# Sources de veille — niche crypto

Narrative, avatar et règles de fond : `_shared/cadre-nass.md`. On ne tire jamais d'idée d'un contenu levier, futures/perps, short, marge, lending à intérêt, casino ou marché de prédiction (voir `SKILL.md`).

## Sources primaires
- **Sujets apportés par Nass** : toujours en premier.
- **Données on-chain / nouveaux tokens** : DexScreener (nouvelles paires, volumes), Dune (dashboards), Arkham / Nansen (smart money, wallets), DefiLlama (TVL, flux par chaîne), Token Unlocks (déblocages à venir).
- **Prix et capitalisations** : CoinGecko ; CoinStats (actus, prix) si le connecteur est disponible. Toujours noter la date.
- **Annonces de listing** des grands exchanges (Binance, Coinbase, OKX) : repérer ce qui était achetable on-chain avant d'être listé.
- **Recherche YouTube** : `yt-dlp --flat-playlist --print "%(id)s %(title)s %(channel)s %(view_count)s" "ytsearch10:<requête>"` (ou WebSearch) pour voir ce qui marche sur un thème.

## Source manuelle optionnelle
- **1of10.com** : outliers YouTube (crypto US notamment). Compte payant, pas d'accès automatique : Nass consulte et colle ce qu'il a repéré.

## Chaînes de référence
Liste complète, tiers et IDs : `scripts/config/channels.json` (77 chaînes actives au 2026-10-14 : 28 FR, 34 US, 15 ES ; plus `a_verifier` et `exclus`, que les scripts ignorent). Outliers du moment : `python {repo}/yt-veille/scripts/outliers_rss.py` lit le flux RSS de chaque chaîne (sans clé API) et écrit `outputs/veille-<date>-outliers.md` ; méthode et seuils dans `SKILL.md`, étape 1. La liste sert aussi à la veille automatique, en pause.
- **FR, Tier 1** : Hasheur, Hasheur Live, Cryptoast, Journal du Coin, Grand Angle Bitcoin, Paul Finance, Finary (pont investisseurs « classiques » / crypto), CoinAcademy
- **FR, Tier 2-3** : Julien Roman, Crypto Le Trone, Cryptoast Academy & Podcast, Monsieur-TK, Cryptolyze, Crypto Flash, Chantal Läng, Jonathan Nowak, Crypto et Bourse pour tous, FinTales, Matthieu Louvet, Lexa Moon, Crypto Logique, bitcoin fr, Cryptorecherche, Alex Doyon, Milenium Finance, K-Bour Crypto, Seiya
- **US, Tier 1** (vues médianes ≥ 30 k) : Coin Bureau, Altcoin Daily, Lark Davis, Mark Moss, Gareth Soloway, Paul Barron Network, Knightron Crypto, MMCrypto, Blockchain Backer, Alessio Rastani, The House Of Crypto, Jason Pizzino, Money Rules - Investing Tips, No Bs Crypto, Levi
- **US, Tier 2-3** : Bankless, Benjamin Cowen, Raoul Pal, On-Chain Mind, EllioTrades, Ivan on Tech, The Defiant, Checkonchain, 99Bitcoins, Crypto Sensei, CryptosRUs, Crypto Capital Venture, What Bitcoin Did, Crypto Zombie, Good Evening Crypto, Tyler S, Adam Livingston, Crypto Rover, Boxmining
- **ES** (ajoutées le 2026-10-14) : Plan BTC, Bitcoin y Criptos, Nico Cabrera, Sergi Andrés - Abogado Cripto, Healthy Pockets, Bitcoin hoy, Fran Ruiz, Alejo Rolls | Análisis de Bitcoin, CdeCripto, ERIKA ESPINAL, Informe Crypto, Criptoniano, Value Index · Bitcoin y Mercados, Edu Heras, KManuS88
- **Exclues** (trading à levier / live trading) : Crypto Banter, Merov Crypto, Benjamin Deleuze, Thibaut Crypto, DataDash
- Ancienne liste IA : `scripts/config/channels_ia_archive.json`
- **Candidats EN/ES (collecte du 2026-10-13)** : `yt-veille/references/chaines-en-es-2026-10-13.md` (483 chaînes anglophones, 212 hispanophones, abonnés, vues médianes, cadence, signaux) et `scripts/config/channels_candidates_en_es.json`. À faire valider par Nass avant d'entrer dans `channels.json`.


## Sources secondaires
- **Médias FR** : cryptoast.fr, journalducoin.com, cointribune.com, coinacademy.fr, The Big Whale
- **Médias US** : The Block, CoinDesk, The Defiant, newsletter Bankless
- **X/Twitter** : comptes on-chain et narratifs (suivi manuel de Nass, persona @punk6995)
- **Reddit** : r/CryptoCurrency, r/Bitcoin, r/solana, r/CryptoFR (questions de débutants = sujets)
- **Google Trends / recherche YouTube FR** : « acheter bitcoin », « crypto débutant », « wallet », « fiscalité crypto »

## Régulation et fiscalité (questions concrètes de l'avatar)
- AMF (liste des PSAN/PSCA agréés MiCA, alertes arnaques)
- impots.gouv.fr (déclaration des comptes crypto à l'étranger, formulaire 3916-bis ; plus-values, formulaire 2086)
- Règlement MiCA (calendrier d'application, statut des exchanges en Europe)

## Communauté Nass
- Commentaires YouTube, communauté privée, questions du live hebdo « Convergence »
