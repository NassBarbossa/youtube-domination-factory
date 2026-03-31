"""Composite scoring for yt-veille videos."""
from datetime import datetime

OUTLIER_THRESHOLDS = [1.0, 2.0, 3.0, 10.0, 20.0]
VELOCITY_THRESHOLDS = [1.0, 2.0, 3.0, 8.0, 15.0]
VIEWS_SUBS_THRESHOLDS = [0.05, 0.15, 0.30, 1.0, 2.0]
ENGAGEMENT_THRESHOLDS = [0.5, 1.0, 2.0, 5.0, 8.0]

WEIGHTS = {
    "outlier": 0.40,
    "velocity": 0.25,
    "views_subs": 0.20,
    "engagement": 0.15,
}


def normalize(value: float, thresholds: list[float]) -> float:
    scores = [0, 25, 50, 75, 100]
    if value <= thresholds[0]:
        return 0
    if value >= thresholds[-1]:
        return 100
    for i in range(len(thresholds) - 1):
        if thresholds[i] <= value <= thresholds[i + 1]:
            ratio = (value - thresholds[i]) / (thresholds[i + 1] - thresholds[i])
            return scores[i] + ratio * (scores[i + 1] - scores[i])
    return 0


def composite_score(*, outlier: float, velocity_ratio: float,
                    views_subs: float, engagement: float) -> float:
    o = normalize(outlier, OUTLIER_THRESHOLDS)
    v = normalize(velocity_ratio, VELOCITY_THRESHOLDS)
    vs = normalize(views_subs, VIEWS_SUBS_THRESHOLDS)
    e = normalize(engagement, ENGAGEMENT_THRESHOLDS)
    return round(o * WEIGHTS["outlier"] + v * WEIGHTS["velocity"]
                 + vs * WEIGHTS["views_subs"] + e * WEIGHTS["engagement"], 2)


def compute_video_metrics(*, snapshots: list[dict], channel_median: float,
                          channel_avg_velocity: float,
                          channel_subscribers: int) -> dict:
    if not snapshots:
        return {"outlier_score": 0, "velocity_ratio": 0, "views_subs_ratio": 0,
                "engagement_rate": 0, "composite": 0}

    latest = snapshots[-1]
    views = latest["views"]
    likes = latest["likes"]
    comments = latest["comments"]

    outlier_score = views / channel_median if channel_median > 0 else 0

    if len(snapshots) >= 2:
        first, last = snapshots[0], snapshots[-1]
        t0 = datetime.fromisoformat(first["scraped_at"])
        t1 = datetime.fromisoformat(last["scraped_at"])
        hours = (t1 - t0).total_seconds() / 3600
        video_velocity = (last["views"] - first["views"]) / hours if hours > 0 else 0
        velocity_ratio = video_velocity / channel_avg_velocity if channel_avg_velocity > 0 else 0
    else:
        velocity_ratio = 0

    views_subs_ratio = views / channel_subscribers if channel_subscribers > 0 else 0
    engagement_rate = (likes + comments) / views if views > 0 else 0

    score = composite_score(
        outlier=outlier_score,
        velocity_ratio=velocity_ratio,
        views_subs=views_subs_ratio,
        engagement=engagement_rate * 100,
    )

    return {
        "outlier_score": round(outlier_score, 2),
        "velocity_ratio": round(velocity_ratio, 2),
        "views_subs_ratio": round(views_subs_ratio, 4),
        "engagement_rate": round(engagement_rate, 4),
        "composite": score,
    }
