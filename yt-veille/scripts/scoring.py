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

WEIGHTS_EARLY = {
    "outlier": 0.35,
    "velocity": 0.25,
    "views_subs": 0.15,
    "engagement": 0.25,
}

TIER_MULTIPLIER = {
    "Tier 1": 1.5,
    "Tier 2": 1.2,
    "Tier 3": 1.0,
    "Non classé": 1.0,
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
                    views_subs: float, engagement: float,
                    early: bool = False) -> float:
    w = WEIGHTS_EARLY if early else WEIGHTS
    o = normalize(outlier, OUTLIER_THRESHOLDS)
    v = normalize(velocity_ratio, VELOCITY_THRESHOLDS)
    vs = normalize(views_subs, VIEWS_SUBS_THRESHOLDS)
    e = normalize(engagement, ENGAGEMENT_THRESHOLDS)
    return round(o * w["outlier"] + v * w["velocity"]
                 + vs * w["views_subs"] + e * w["engagement"], 2)


def apply_tier_boost(score: float, tier: str) -> float:
    """Apply tier multiplier to composite score, capped at 100."""
    multiplier = TIER_MULTIPLIER.get(tier, 1.0)
    return min(round(score * multiplier, 2), 100.0)


def compute_video_metrics(*, snapshots: list[dict], channel_median: float,
                          channel_avg_velocity: float,
                          channel_subscribers: int,
                          published_at: str | None = None,
                          tier: str = "Non classé") -> dict:
    if not snapshots:
        return {"outlier_score": 0, "velocity_ratio": 0, "views_subs_ratio": 0,
                "engagement_rate": 0, "composite": 0, "composite_raw": 0, "early": False}

    latest = snapshots[-1]
    views = latest["views"]
    likes = latest["likes"]
    comments = latest["comments"]

    outlier_score = views / channel_median if channel_median > 0 else 0

    # Determine if video is < 24h old
    early = False
    if published_at:
        pub_time = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        now = datetime.now(pub_time.tzinfo) if pub_time.tzinfo else datetime.utcnow()
        age_hours = (now - pub_time).total_seconds() / 3600
        early = age_hours < 24

    # Velocity calculation
    if len(snapshots) >= 2:
        first, last = snapshots[0], snapshots[-1]
        t0 = datetime.fromisoformat(first["scraped_at"])
        t1 = datetime.fromisoformat(last["scraped_at"])
        hours = (t1 - t0).total_seconds() / 3600
        video_velocity = (last["views"] - first["views"]) / hours if hours > 0 else 0
        velocity_ratio = video_velocity / channel_avg_velocity if channel_avg_velocity > 0 else 0
    elif early and published_at:
        # Early velocity: views / hours since publication
        pub_time = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        now = datetime.now(pub_time.tzinfo) if pub_time.tzinfo else datetime.utcnow()
        hours_since_pub = (now - pub_time).total_seconds() / 3600
        if hours_since_pub > 0:
            early_vel = views / hours_since_pub
            velocity_ratio = early_vel / channel_avg_velocity if channel_avg_velocity > 0 else 0
        else:
            velocity_ratio = 0
    else:
        velocity_ratio = 0

    views_subs_ratio = views / channel_subscribers if channel_subscribers > 0 else 0
    engagement_rate = (likes + comments) / views if views > 0 else 0

    raw_score = composite_score(
        outlier=outlier_score,
        velocity_ratio=velocity_ratio,
        views_subs=views_subs_ratio,
        engagement=engagement_rate * 100,
        early=early,
    )
    boosted_score = apply_tier_boost(raw_score, tier)

    return {
        "outlier_score": round(outlier_score, 2),
        "velocity_ratio": round(velocity_ratio, 2),
        "views_subs_ratio": round(views_subs_ratio, 4),
        "engagement_rate": round(engagement_rate, 4),
        "composite_raw": raw_score,
        "composite": boosted_score,
        "early": early,
    }
