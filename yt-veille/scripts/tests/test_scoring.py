import pytest
from scoring import normalize, composite_score, compute_video_metrics, apply_tier_boost

def test_normalize_at_zero():
    thresholds = [1.0, 2.0, 3.0, 10.0, 20.0]
    assert normalize(0.5, thresholds) == 0
    assert normalize(1.0, thresholds) == 0

def test_normalize_between_thresholds():
    thresholds = [1.0, 2.0, 3.0, 10.0, 20.0]
    assert normalize(2.0, thresholds) == 25
    assert normalize(3.0, thresholds) == 50
    assert normalize(10.0, thresholds) == 75

def test_normalize_interpolation():
    thresholds = [1.0, 2.0, 3.0, 10.0, 20.0]
    result = normalize(1.5, thresholds)
    assert result == pytest.approx(12.5)

def test_normalize_capped_at_100():
    thresholds = [1.0, 2.0, 3.0, 10.0, 20.0]
    assert normalize(50.0, thresholds) == 100

def test_composite_score_all_max():
    result = composite_score(outlier=20.0, velocity_ratio=15.0,
                             views_subs=2.0, engagement=8.0)
    assert result == 100.0

def test_composite_score_all_zero():
    result = composite_score(outlier=0.5, velocity_ratio=0.5,
                             views_subs=0.02, engagement=0.3)
    assert result == 0.0

def test_composite_score_mixed():
    result = composite_score(outlier=10.0, velocity_ratio=3.0,
                             views_subs=0.30, engagement=5.0)
    # outlier=75*0.4=30, velocity=50*0.25=12.5, views_subs=50*0.2=10, engagement=75*0.15=11.25
    assert result == pytest.approx(63.75)

def test_compute_video_metrics():
    snapshots = [
        {"scraped_at": "2026-03-20", "views": 5000, "likes": 300, "comments": 50},
        {"scraped_at": "2026-03-21", "views": 50000, "likes": 3000, "comments": 500},
    ]
    metrics = compute_video_metrics(
        snapshots=snapshots,
        channel_median=10000,
        channel_avg_velocity=500.0,
        channel_subscribers=50000,
    )
    assert metrics["outlier_score"] == pytest.approx(5.0)
    assert metrics["velocity_ratio"] > 0
    assert metrics["views_subs_ratio"] == pytest.approx(1.0)
    assert metrics["engagement_rate"] > 0
    assert 0 <= metrics["composite"] <= 100

def test_compute_video_metrics_single_snapshot():
    snapshots = [
        {"scraped_at": "2026-03-20", "views": 50000, "likes": 3000, "comments": 500},
    ]
    metrics = compute_video_metrics(
        snapshots=snapshots,
        channel_median=10000,
        channel_avg_velocity=500.0,
        channel_subscribers=50000,
    )
    assert metrics["velocity_ratio"] == 0
    assert metrics["composite"] >= 0
    assert metrics["early"] is False


def test_composite_score_early_weights():
    """Early mode should give more weight to engagement."""
    result_normal = composite_score(outlier=5.0, velocity_ratio=3.0,
                                     views_subs=0.30, engagement=7.0)
    result_early = composite_score(outlier=5.0, velocity_ratio=3.0,
                                    views_subs=0.30, engagement=7.0, early=True)
    # With high engagement, early mode should score higher
    assert result_early > result_normal


def test_compute_video_metrics_early_velocity():
    """Video < 24h old with 1 snapshot should use early velocity from published_at."""
    from datetime import datetime, timezone, timedelta
    # Published 6 hours ago
    pub_time = (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat()
    snapshots = [
        {"scraped_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
         "views": 30000, "likes": 2000, "comments": 300},
    ]
    metrics = compute_video_metrics(
        snapshots=snapshots,
        channel_median=10000,
        channel_avg_velocity=500.0,
        channel_subscribers=50000,
        published_at=pub_time,
    )
    assert metrics["early"] is True
    # 30000 views / 6 hours = 5000 views/h, channel avg = 500 → ratio = 10
    assert metrics["velocity_ratio"] > 5
    assert metrics["composite"] > 0


def test_compute_video_metrics_old_video_not_early():
    """Video > 24h old should NOT use early mode."""
    from datetime import datetime, timezone, timedelta
    pub_time = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
    snapshots = [
        {"scraped_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
         "views": 30000, "likes": 2000, "comments": 300},
    ]
    metrics = compute_video_metrics(
        snapshots=snapshots,
        channel_median=10000,
        channel_avg_velocity=500.0,
        channel_subscribers=50000,
        published_at=pub_time,
    )
    assert metrics["early"] is False
    # No 2nd snapshot + not early → velocity = 0
    assert metrics["velocity_ratio"] == 0


def test_apply_tier_boost():
    assert apply_tier_boost(50.0, "Tier 1") == 75.0   # ×1.5
    assert apply_tier_boost(50.0, "Tier 2") == 60.0   # ×1.2
    assert apply_tier_boost(50.0, "Tier 3") == 50.0   # ×1.0
    assert apply_tier_boost(50.0, "Non classé") == 50.0

def test_apply_tier_boost_capped():
    assert apply_tier_boost(80.0, "Tier 1") == 100.0  # 80×1.5=120 → capé à 100

def test_compute_video_metrics_with_tier():
    snapshots = [
        {"scraped_at": "2026-03-20", "views": 5000, "likes": 300, "comments": 50},
        {"scraped_at": "2026-03-21", "views": 50000, "likes": 3000, "comments": 500},
    ]
    raw = compute_video_metrics(
        snapshots=snapshots, channel_median=10000,
        channel_avg_velocity=500.0, channel_subscribers=50000,
        tier="Non classé",
    )
    boosted = compute_video_metrics(
        snapshots=snapshots, channel_median=10000,
        channel_avg_velocity=500.0, channel_subscribers=50000,
        tier="Tier 1",
    )
    assert boosted["composite"] > raw["composite"]
    assert boosted["composite_raw"] == raw["composite_raw"]
    assert boosted["composite"] <= 100
