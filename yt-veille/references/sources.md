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
Liste complète, tiers et IDs : `scripts/config/channels.json` (40 chaînes actives au 2026-10-07, plus `a_verifier` et `exclus`). Aussi utilisée par la veille automatique, en pause.
- **FR, Tier 1** : Hasheur, Hasheur Live, Cryptoast, Journal du Coin, Grand Angle Bitcoin, Paul Finance, Finary (pont investisseurs « classiques » / crypto), CoinAcademy
- **FR, Tier 2-3** : Julien Roman, Crypto Le Trone, Cryptoast Academy & Podcast, Monsieur-TK, Cryptolyze, Crypto Flash, Chantal Läng, Jonathan Nowak, Crypto et Bourse pour tous, FinTales, Matthieu Louvet, Lexa Moon, Crypto Logique, bitcoin fr, Cryptorecherche, Alex Doyon, Milenium Finance, K-Bour Crypto, Seiya
- **US** : Coin Bureau, Altcoin Daily, Lark Davis (Tier 1) ; Bankless, Benjamin Cowen, Raoul Pal, On-Chain Mind (Tier 2) ; EllioTrades, Ivan on Tech, The Defiant, Checkonchain, 99Bitcoins (Tier 3)
- **Exclues** (trading à levier / live trading) : Crypto Banter, Merov Crypto, Benjamin Deleuze, Thibaut Crypto, DataDash
- Ancienne liste IA : `scripts/config/channels_ia_archive.json`

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
