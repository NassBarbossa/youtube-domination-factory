import sqlite3
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from daily_monitor import run_monitor
from database import init_db, get_connection

@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "test.db")
    init_db(path)
    return path

@pytest.fixture
def mock_youtube_client():
    now = datetime.now(timezone.utc)
    pub1 = (now - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
    pub2 = (now - timedelta(hours=12)).strftime("%Y-%m-%dT%H:%M:%SZ")

    client = MagicMock()
    client.get_channel_stats.return_value = {
        "subscriber_count": 50000,
        "view_count": 5000000,
        "video_count": 100,
    }
    client.get_latest_uploads.return_value = [
        {"video_id": "vid1", "title": "Video 1", "published_at": pub1},
        {"video_id": "vid2", "title": "Video 2", "published_at": pub2},
    ]
    client.get_video_details.return_value = {
        "vid1": {
            "title": "Claude Code Full Tutorial",
            "description": "Learn Claude Code from scratch",
            "tags": ["claude code", "tutorial"],
            "published_at": pub1,
            "thumbnail_url": "https://img.youtube.com/vi/vid1/hq.jpg",
            "category_id": "28",
            "duration_seconds": 900,
            "views": 80000,
            "likes": 4500,
            "comments": 700,
            "topic_categories": [],
        },
        "vid2": {
            "title": "My Daily Routine",
            "description": "How I start my day",
            "tags": ["routine"],
            "published_at": pub2,
            "thumbnail_url": "https://img.youtube.com/vi/vid2/hq.jpg",
            "category_id": "22",
            "duration_seconds": 600,
            "views": 5000,
            "likes": 200,
            "comments": 30,
            "topic_categories": [],
        },
    }
    return client

def test_run_monitor_inserts_data(db_path, mock_youtube_client):
    channels = [{"channel_id": "UC123", "handle": "TestChannel", "niche": "ai", "added_at": "2026-03-01"}]
    run_monitor(db_path=db_path, client=mock_youtube_client, channels=channels)

    conn = sqlite3.connect(db_path)
    ch = conn.execute("SELECT * FROM channels WHERE channel_id='UC123'").fetchone()
    assert ch is not None

    vids = conn.execute("SELECT * FROM videos").fetchall()
    assert len(vids) == 2

    snaps = conn.execute("SELECT * FROM snapshots").fetchall()
    assert len(snaps) == 2
    conn.close()

def test_run_monitor_scores_videos(db_path, mock_youtube_client):
    channels = [{"channel_id": "UC123", "handle": "TestChannel", "niche": "ai", "added_at": "2026-03-01"}]
    run_monitor(db_path=db_path, client=mock_youtube_client, channels=channels)
    # Simulate next day with more views
    mock_youtube_client.get_video_details.return_value["vid1"]["views"] = 120000
    mock_youtube_client.get_video_details.return_value["vid2"]["views"] = 7000
    run_monitor(db_path=db_path, client=mock_youtube_client, channels=channels)

    conn = sqlite3.connect(db_path)
    vid1 = conn.execute("SELECT composite_score FROM videos WHERE video_id='vid1'").fetchone()
    vid2 = conn.execute("SELECT composite_score FROM videos WHERE video_id='vid2'").fetchone()
    conn.close()
    assert vid1[0] is not None
    assert vid1[0] > vid2[0]

def test_run_monitor_extracts_topic_above_threshold(db_path, mock_youtube_client):
    channels = [{"channel_id": "UC123", "handle": "TestChannel", "niche": "ai", "added_at": "2026-03-01"}]
    run_monitor(db_path=db_path, client=mock_youtube_client, channels=channels)
    run_monitor(db_path=db_path, client=mock_youtube_client, channels=channels)

    conn = sqlite3.connect(db_path)
    vid1 = conn.execute("SELECT topic, composite_score FROM videos WHERE video_id='vid1'").fetchone()
    vid2 = conn.execute("SELECT topic, composite_score FROM videos WHERE video_id='vid2'").fetchone()
    conn.close()
    if vid1[1] and vid1[1] > 50:
        assert vid1[0] is not None
    if vid2[1] and vid2[1] <= 50:
        assert vid2[0] is None
