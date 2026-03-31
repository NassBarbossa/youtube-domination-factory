import pytest
from scoring import normalize, composite_score, compute_video_metrics

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
