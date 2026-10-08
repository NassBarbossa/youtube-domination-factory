from topic_extractor import extract_topic, TOPIC_KEYWORDS

def test_extract_topic_bitcoin():
    assert extract_topic("Le Bitcoin vient de casser son record", "Analyse du BTC...") == "bitcoin"

def test_extract_topic_airdrop():
    assert extract_topic("FLOP AI : il y a un AIRDROP à jouer", "") == "airdrop"

def test_extract_topic_presale_early():
    assert extract_topic("Cette pépite crypto avant tout le monde", "Achetée avant listing...") == "presale-early"

def test_extract_topic_onchain():
    assert extract_topic("Ce que font les whales cette semaine", "Analyse on-chain...") == "onchain"

def test_extract_topic_beginner():
    assert extract_topic("Acheter sa première crypto : guide débutant", "") == "crypto-beginner"

def test_extract_topic_from_description_when_title_is_vague():
    assert extract_topic("Ça change tout", "J'ai testé Solana et...") == "solana"

def test_extract_topic_unknown():
    assert extract_topic("Ma routine du matin", "Je me lève à 5h...") == "other"

def test_extract_topic_case_insensitive():
    assert extract_topic("ETHEREUM VA EXPLOSER", "") == "ethereum"

def test_extract_topic_halal_leverage_flagged():
    """Levier / futures / short : toujours étiqueté non-halal, même si Bitcoin est cité."""
    assert extract_topic("Bitcoin : gros SHORT SQUEEZE en approche", "") == "non-halal"
    assert extract_topic("Trader le Bitcoin avec effet de levier x50", "") == "non-halal"
    assert extract_topic("Crypto futures trading for beginners", "") == "non-halal"

def test_extract_topic_halal_gambling_lending_flagged():
    assert extract_topic("Polymarket : parier sur l'élection", "") == "non-halal"
    assert extract_topic("Crypto lending : 12 % d'intérêts sur tes USDC", "") == "non-halal"

def test_extract_topic_priority():
    """Non-halal passe avant tous les autres sujets."""
    assert TOPIC_KEYWORDS[0][0] == "non-halal"
    assert extract_topic("Memecoin Solana avec levier", "") == "non-halal"
