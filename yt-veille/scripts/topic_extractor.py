"""Extract topic from video title and description using keyword matching."""
import re

# Ordered by priority — more specific patterns first.
# Niche CRYPTO (rebrand 2026-10-07). Ancienne liste IA : voir git history / config/*_ia_archive.json.
# "non-halal" passe en premier : toute vidéo qui touche au levier, aux dérivés, au prêt à intérêt
# ou aux jeux d'argent est étiquetée ainsi et ne doit JAMAIS devenir une idée de vidéo (cf. SKILL.md).
TOPIC_KEYWORDS = [
    ("non-halal", [
        "levier", "leverage", "leveraged", "futures trading", "trading futures", "crypto futures",
        "perpetual", "perpétuel", "perps", "short squeeze", "shorter", "vendre à découvert",
        "margin trading", "trading sur marge", "liquidation price", "copy trading",
        "options binaires", "binary options", "crypto lending", "lending crypto", "prêt crypto",
        "emprunter contre", "borrow against", "casino", "paris sportif", "sports betting",
        "betting", "prediction market", "marché de prédiction", "polymarket",
    ]),
    ("presale-early", [
        "presale", "pre-sale", "prévente", "pré-vente", "avant listing", "before listing",
        "launchpad", "pépite", "pepite", "hidden gem", "crypto gem", "early gem", "100x", "x100",
    ]),
    ("airdrop", ["airdrop"]),
    ("memecoin", ["memecoin", "meme coin", "mèmecoin", "pump.fun", "pumpfun"]),
    ("onchain", [
        "on-chain", "onchain", "smart money", "whale", "baleine", "wallet tracker",
        "dexscreener", "dex screener",
    ]),
    ("crypto-security", [
        "ledger", "trezor", "cold wallet", "seed phrase", "phrase de récupération",
        "self-custody", "auto-conservation", "piraté", "hack", "arnaque", "scam", "phishing",
    ]),
    ("crypto-beginner", [
        "débutant", "debutant", "beginner", "première crypto", "premier bitcoin",
        "acheter du bitcoin", "how to buy bitcoin", "comment acheter",
    ]),
    ("etf-institutions", ["etf", "blackrock", "institutionnel", "institutional", "wall street"]),
    ("regulation-tax", [
        "mica", "clarity act", "la sec", "the sec", "fiscalité", "impôt", "impots",
        "déclaration crypto", "crypto tax", "régulation", "regulation",
    ]),
    ("defi", ["defi", "staking", "uniswap", "hyperliquid", "dex "]),
    ("altcoins", ["altcoin", "altseason", "alt season"]),
    ("solana", ["solana"]),
    ("ethereum", ["ethereum"]),
    ("bitcoin", ["bitcoin", "btc"]),
    ("macro", ["fed ", "inflation", "dette", "récession", "recession", "gold", "l'or "]),
    ("crypto-news", ["actu crypto", "crypto news", "news crypto", "actualité crypto", "bull run", "bullrun"]),
]


def extract_topic(title: str, description: str) -> str:
    """Extract topic from title + first 500 chars of description."""
    text = (title + " " + description[:500]).lower()
    for topic, keywords in TOPIC_KEYWORDS:
        for kw in keywords:
            if kw.lower() in text:
                return topic
    return "other"
