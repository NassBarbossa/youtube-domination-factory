import pytest
from unittest.mock import MagicMock, patch
from daily_monitor import (
    detect_new_videos,
    compute_outliers,
    deduplicate_backlog,
    build_backlog_entry,
    prune_backlog,
)


def test_detect_new_videos():
    uploads = [
        {"video_id": "aaa", "title": "New", "published_at": "2026-03-25T00:00:00Z"},
        {"video_id": "bbb", "title": "Old", "published_at": "2026-03-20T00:00:00Z"},
    ]
    checked_ids = {"bbb"}
    new = detect_new_videos(uploads, checked_ids)
    assert len(new) == 1
    assert new[0]["video_id"] == "aaa"


def test_detect_new_videos_first_run():
    uploads = [
        {"video_id": "aaa", "title": "V1", "published_at": "2026-03-25T00:00:00Z"},
        {"video_id": "bbb", "title": "V2", "published_at": "2026-03-24T00:00:00Z"},
    ]
    new = detect_new_videos(uploads, set())
    assert len(new) == 2


def test_compute_outliers_enough_history():
    history = [100, 200, 150, 300, 120]  # median = 150
    video_views = {"vid1": 500, "vid2": 100}
    outliers = compute_outliers(video_views, history)
    assert outliers["vid1"]["outlier"] is True
    assert outliers["vid1"]["outlier_ratio"] == pytest.approx(500 / 150, rel=0.01)
    assert outliers["vid2"]["outlier"] is False


def test_compute_outliers_not_enough_history():
    history = [100, 200]  # < 5 videos
    video_views = {"vid1": 9999}
    outliers = compute_outliers(video_views, history)
    assert outliers["vid1"]["outlier"] is False
    assert outliers["vid1"]["outlier_ratio"] is None


def test_deduplicate_backlog():
    existing_items = [
        {"id": "aaa", "title": "Existing"},
    ]
    new_items = [
        {"id": "aaa", "title": "Existing duplicate"},
        {"id": "bbb", "title": "Actually new"},
    ]
    result = deduplicate_backlog(existing_items, new_items)
    assert len(result) == 1
    assert result[0]["id"] == "bbb"


def test_prune_backlog_archives_old_entries():
    items = [
        {"id": "new", "detected_at": "2026-03-20T00:00:00Z"},
        {"id": "old", "detected_at": "2025-12-01T00:00:00Z"},
    ]
    kept, archived = prune_backlog(items, max_age_days=90)
    assert len(kept) == 1
    assert kept[0]["id"] == "new"
    assert len(archived) == 1
    assert archived[0]["id"] == "old"


def test_prune_backlog_keeps_all_if_recent():
    items = [
        {"id": "a", "detected_at": "2026-03-25T00:00:00Z"},
        {"id": "b", "detected_at": "2026-03-24T00:00:00Z"},
    ]
    kept, archived = prune_backlog(items, max_age_days=90)
    assert len(kept) == 2
    assert len(archived) == 0


def test_build_backlog_entry():
    entry = build_backlog_entry(
        video_id="abc123",
        title="Test Video",
        channel_name="Alex Finn",
        channel_id="UCfQNB91qRP_5ILeu_S_bSkg",
        published_at="2026-03-25T20:00:00Z",
        views=15230,
        likes=892,
        comments=134,
        subscribers=68000,
        outlier=True,
        median_views=4500,
        outlier_ratio=3.38,
    )
    assert entry["id"] == "abc123"
    assert entry["url"] == "https://www.youtube.com/watch?v=abc123"
    assert entry["outlier"] is True
    assert entry["source"] == "daily_monitor"
    assert "detected_at" in entry
