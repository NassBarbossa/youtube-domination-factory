# tests/test_database.py
import sqlite3
import pytest
from database import init_db, get_connection

def test_init_db_creates_tables(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    assert "channels" in tables
    assert "videos" in tables
    assert "snapshots" in tables

def test_init_db_idempotent(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    init_db(db_path)  # should not raise


from database import upsert_channel, upsert_video, insert_snapshot

def test_upsert_channel(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    upsert_channel(db_path, channel_id="UC123", handle="TestChannel",
                   subscribers=50000, niche="ai-tools", added_at="2026-03-01")
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT * FROM channels WHERE channel_id='UC123'").fetchone()
    conn.close()
    assert row is not None
    assert row[1] == "TestChannel"
    assert row[2] == 50000

def test_upsert_channel_updates_existing(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    upsert_channel(db_path, channel_id="UC123", handle="TestChannel",
                   subscribers=50000, niche="ai-tools", added_at="2026-03-01")
    upsert_channel(db_path, channel_id="UC123", handle="TestChannel",
                   subscribers=60000, niche="ai-tools", added_at="2026-03-01")
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT subscribers FROM channels WHERE channel_id='UC123'").fetchone()
    conn.close()
    assert row[0] == 60000

def test_upsert_video(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    upsert_channel(db_path, channel_id="UC123", handle="Test",
                   subscribers=1000, niche="ai", added_at="2026-03-01")
    upsert_video(db_path, video_id="vid1", channel_id="UC123",
                 title="Test Video", description="A test", tags='["ai","test"]',
                 duration_seconds=600, published_at="2026-03-25T10:00:00Z",
                 thumbnail_url="https://img.youtube.com/vi/vid1/hq.jpg",
                 category_id="28", detected_at="2026-03-25T12:00:00Z")
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT * FROM videos WHERE video_id='vid1'").fetchone()
    conn.close()
    assert row is not None

def test_insert_snapshot(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    upsert_channel(db_path, channel_id="UC123", handle="Test",
                   subscribers=1000, niche="ai", added_at="2026-03-01")
    upsert_video(db_path, video_id="vid1", channel_id="UC123",
                 title="Test", description="", tags="[]",
                 duration_seconds=300, published_at="2026-03-25T10:00:00Z",
                 thumbnail_url="", category_id="28", detected_at="2026-03-25T12:00:00Z")
    insert_snapshot(db_path, video_id="vid1", scraped_at="2026-03-25",
                    views=1000, likes=50, comments=10)
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT * FROM snapshots WHERE video_id='vid1'").fetchone()
    conn.close()
    assert row is not None

def test_insert_snapshot_dedup(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    upsert_channel(db_path, channel_id="UC123", handle="Test",
                   subscribers=1000, niche="ai", added_at="2026-03-01")
    upsert_video(db_path, video_id="vid1", channel_id="UC123",
                 title="Test", description="", tags="[]",
                 duration_seconds=300, published_at="2026-03-25T10:00:00Z",
                 thumbnail_url="", category_id="28", detected_at="2026-03-25T12:00:00Z")
    insert_snapshot(db_path, video_id="vid1", scraped_at="2026-03-25",
                    views=1000, likes=50, comments=10)
    insert_snapshot(db_path, video_id="vid1", scraped_at="2026-03-25",
                    views=1200, likes=60, comments=12)
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT * FROM snapshots WHERE video_id='vid1'").fetchall()
    conn.close()
    assert len(rows) == 1
    assert rows[0][3] == 1200


from database import get_channel_median, get_channel_avg_velocity, get_video_snapshots, get_scored_videos

def _seed_db(tmp_path):
    """Helper: create a DB with 1 channel, 2 videos, multiple snapshots."""
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    upsert_channel(db_path, channel_id="UC123", handle="Test",
                   subscribers=50000, niche="ai", added_at="2026-03-01")
    upsert_video(db_path, video_id="vid1", channel_id="UC123",
                 title="Outlier Video", description="This is about Claude Code",
                 tags='["claude code"]', duration_seconds=600,
                 published_at="2026-03-20T10:00:00Z", thumbnail_url="",
                 category_id="28", detected_at="2026-03-20T12:00:00Z")
    insert_snapshot(db_path, video_id="vid1", scraped_at="2026-03-20", views=5000, likes=300, comments=50)
    insert_snapshot(db_path, video_id="vid1", scraped_at="2026-03-21", views=50000, likes=3000, comments=500)
    insert_snapshot(db_path, video_id="vid1", scraped_at="2026-03-22", views=80000, likes=4500, comments=700)
    upsert_video(db_path, video_id="vid2", channel_id="UC123",
                 title="Normal Video", description="Regular content",
                 tags='["ai"]', duration_seconds=400,
                 published_at="2026-03-18T10:00:00Z", thumbnail_url="",
                 category_id="28", detected_at="2026-03-18T12:00:00Z")
    insert_snapshot(db_path, video_id="vid2", scraped_at="2026-03-18", views=2000, likes=100, comments=20)
    insert_snapshot(db_path, video_id="vid2", scraped_at="2026-03-19", views=8000, likes=400, comments=60)
    insert_snapshot(db_path, video_id="vid2", scraped_at="2026-03-20", views=10000, likes=500, comments=80)
    return db_path

def test_get_channel_median(tmp_path):
    db_path = _seed_db(tmp_path)
    median = get_channel_median("UC123", db_path)
    assert median is not None
    assert median == 45000.0

def test_get_channel_avg_velocity(tmp_path):
    db_path = _seed_db(tmp_path)
    avg_vel = get_channel_avg_velocity("UC123", db_path)
    assert avg_vel is not None
    assert avg_vel > 0

def test_get_video_snapshots(tmp_path):
    db_path = _seed_db(tmp_path)
    snaps = get_video_snapshots("vid1", db_path)
    assert len(snaps) == 3
    assert snaps[0]["views"] == 5000
    assert snaps[-1]["views"] == 80000

def test_get_scored_videos(tmp_path):
    db_path = _seed_db(tmp_path)
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE videos SET composite_score=75.0 WHERE video_id='vid1'")
    conn.execute("UPDATE videos SET composite_score=30.0 WHERE video_id='vid2'")
    conn.commit()
    conn.close()
    results = get_scored_videos(db_path, min_score=50)
    assert len(results) == 1
    assert results[0]["video_id"] == "vid1"
