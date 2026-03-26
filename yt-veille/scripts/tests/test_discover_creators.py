import pytest
from discover_creators import filter_known_channels, score_channel


def test_filter_known_channels():
    found = [
        {"channel_id": "UC_NEW", "title": "New Creator"},
        {"channel_id": "UCfQNB91qRP_5ILeu_S_bSkg", "title": "Alex Finn"},
    ]
    known_ids = {"UCfQNB91qRP_5ILeu_S_bSkg"}
    result = filter_known_channels(found, known_ids)
    assert len(result) == 1
    assert result[0]["channel_id"] == "UC_NEW"


def test_score_channel_high_relevance():
    channel = {
        "title": "Claude Code Tutorials",
        "description": "Learn vibe coding with AI tools",
        "subscriber_count": 5000,
        "video_count": 50,
    }
    keywords = ["Claude Code", "vibe coding", "AI tools"]
    score = score_channel(channel, keywords)
    assert score["relevance"] > 0
    assert score["total"] > 0


def test_score_channel_no_relevance():
    channel = {
        "title": "Cooking with Chef Mike",
        "description": "Best recipes for pasta lovers",
        "subscriber_count": 100000,
        "video_count": 200,
    }
    keywords = ["Claude Code", "vibe coding"]
    score = score_channel(channel, keywords)
    assert score["relevance"] == 0
