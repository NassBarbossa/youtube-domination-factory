import pytest
from datetime import datetime, timezone, timedelta
from scoring import (
    normalize, compute_score, compute_channel_stats,
    apply_tier_boost, apply_decay,
)


# --- normalize ---

def test_normalize_at_zero():
    assert normalize(0.5, [1.0, 2.0, 3.0, 10.0, 20.0]) == 0
    assert normalize(1.0, [1.0, 2.0, 3.0, 10.0, 20.0]) == 0

def test_normalize_between_thresholds():
    t = [1.0, 2.0, 3.0, 10.0, 20.0]
    assert normalize(2.0, t) == 25
    assert normalize(3.0, t) == 50
    assert normalize(10.0, t) == 75

def test_normalize_interpolation():
    assert normalize(1.5, [1.0, 2.0, 3.0, 10.0, 20.0]) == pytest.approx(12.5)

def test_normalize_capped_at_100():
    assert normalize(50.0, [1.0, 2.0, 3.0, 10.0, 20.0]) == 100

def test_normalize_views_abs():
    t = [1000, 5000, 20000, 40000, 100000]
    assert normalize(500, t) == 0
    assert normalize(5000, t) == 25
    assert normalize(20000, t) == 50
    assert normalize(40000, t) == 75
    assert normalize(100000, t) == 100
    assert normalize(200000, t) == 100


# --- compute_channel_stats ---

def test_compute_channel_stats():
    video_snapshots = {
        "vid1": [
            {"scraped_at": "2026-04-01", "views": 5000},
            {"scraped_at": "2026-04-02", "views": 15000},
        ],
        "vid2": [
            {"scraped_at": "2026-04-01", "views": 2000},
            {"scraped_at": "2026-04-02", "views": 4000},
        ],
    }
    stats = compute_channel_stats(video_snapshots)
    assert stats["median_views"] == 9500.0  # median of [15000, 4000]
    assert stats["avg_velocity"] > 0

def test_compute_channel_stats_single_snapshot():
    video_snapshots = {
        "vid1": [{"scraped_at": "2026-04-01", "views": 5000}],
    }
    stats = compute_channel_stats(video_snapshots)
    assert stats["median_views"] == 5000
    assert stats["avg_velocity"] == 0


# --- compute_score ---

def test_compute_score_basic():
    snaps = [
        {"scraped_at": "2026-04-01", "views": 5000, "likes": 300, "comments": 50},
        {"scraped_at": "2026-04-02", "views": 50000, "likes": 3000, "comments": 500},
    ]
    result = compute_score(
        views=50000, likes=3000, comments=500,
        channel_median=10000, channel_avg_velocity=500.0,
        channel_subscribers=50000, snapshots=snaps,
    )
    assert 0 <= result["composite"] <= 100
    assert result["outlier"] == 5.0
    assert result["views_abs"] == 50000
    assert result["velocity_ratio"] > 0
    assert result["early"] is False

def test_compute_score_views_abs_matters():
    """Video with high absolute views should score higher than low views with high outlier."""
    snaps_low = [{"scraped_at": "2026-04-01", "views": 3000, "likes": 200, "comments": 30}]
    snaps_high = [{"scraped_at": "2026-04-01", "views": 60000, "likes": 2000, "comments": 200}]

    low_views = compute_score(
        views=3000, likes=200, comments=30,
        channel_median=300, channel_avg_velocity=0,
        channel_subscribers=5000, snapshots=snaps_low,
    )
    high_views = compute_score(
        views=60000, likes=2000, comments=200,
        channel_median=30000, channel_avg_velocity=0,
        channel_subscribers=200000, snapshots=snaps_high,
    )
    # 60k views should beat 3k views even though 3k has 10x outlier
    assert high_views["composite"] > low_views["composite"]

def test_compute_score_early():
    now = datetime.now(timezone.utc)
    pub = (now - timedelta(hours=6)).isoformat()
    snaps = [{"scraped_at": now.strftime("%Y-%m-%d"), "views": 30000, "likes": 2000, "comments": 300}]
    result = compute_score(
        views=30000, likes=2000, comments=300,
        channel_median=10000, channel_avg_velocity=500.0,
        channel_subscribers=50000, snapshots=snaps,
        published_at=pub,
    )
    assert result["early"] is True
    assert result["velocity_ratio"] > 0

def test_compute_score_no_snapshots():
    result = compute_score(
        views=0, likes=0, comments=0,
        channel_median=10000, channel_avg_velocity=500,
        channel_subscribers=50000, snapshots=[],
    )
    assert result["composite"] == 0


# --- apply_tier_boost ---

def test_tier_boost():
    assert apply_tier_boost(50.0, "Tier 1") == 75.0
    assert apply_tier_boost(50.0, "Tier 2") == 60.0
    assert apply_tier_boost(50.0, "Tier 3") == 50.0
    assert apply_tier_boost(50.0, "Non classé") == 50.0

def test_tier_boost_capped():
    assert apply_tier_boost(80.0, "Tier 1") == 100.0


# --- apply_decay ---

def test_decay_fresh():
    pub = (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat()
    score, anomaly = apply_decay(75.0, pub)
    assert score == 75.0
    assert anomaly is False

def test_decay_2_days():
    pub = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
    score, _ = apply_decay(80.0, pub)
    assert score == 68.0  # ×0.85

def test_decay_5_days():
    pub = (datetime.now(timezone.utc) - timedelta(hours=120)).isoformat()
    score, _ = apply_decay(80.0, pub)
    assert score == 52.0  # ×0.65

def test_decay_old_excluded():
    pub = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
    score, anomaly = apply_decay(50.0, pub)
    assert score == 0.0
    assert anomaly is False

def test_decay_old_anomaly():
    pub = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
    score, anomaly = apply_decay(90.0, pub)
    assert score == 27.0
    assert anomaly is True
