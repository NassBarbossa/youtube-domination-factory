"""Composite scoring for yt-veille videos."""
from datetime import datetime
import statistics

OUTLIER_THRESHOLDS = [1.0, 2.0, 3.0, 10.0, 20.0]
VIEWS_ABS_THRESHOLDS = [1000, 5000, 20000, 40000, 100000]
VELOCITY_THRESHOLDS = [1.0, 2.0, 3.0, 8.0, 15.0]
VIEWS_SUBS_THRESHOLDS = [0.05, 0.15, 0.30, 1.0, 2.0]
ENGAGEMENT_THRESHOLDS = [0.5, 1.0, 2.0, 5.0, 8.0]

WEIGHTS = {
    "outlier": 0.15,
    "views_abs": 0.30,
    "velocity": 0.25,
    "views_subs": 0.15,
    "engagement": 0.15,
}

WEIGHTS_EARLY = {
    "outlier": 0.10,
    "views_abs": 0.30,
    "velocity": 0.25,
    "views_subs": 0.10,
    "engagement": 0.25,
}

TIER_MULTIPLIER = {
    "Tier 1": 1.5,
    "Tier 2": 1.2,
    "Tier 3": 1.0,
    "Non classé": 1.0,
}

AGE_DECAY = [
    (24, 1.0),
    (72, 0.85),
    (144, 0.65),
    (168, 0.0),
]

ANOMALY_THRESHOLD = 80


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


def compute_channel_stats(video_snapshots: dict[str, list[dict]]) -> dict:
    """Compute median views and avg velocity for a channel from its video snapshots.
    video_snapshots: {video_id: [{"scraped_at":..., "views":..., ...}, ...]}
    """
    latest_views = []
    all_velocities = []

    for vid_id, snaps in video_snapshots.items():
        if not snaps:
            continue
        latest_views.append(snaps[-1]["views"])

        for i in range(1, len(snaps)):
            t0 = datetime.fromisoformat(snaps[i-1]["scraped_at"])
            t1 = datetime.fromisoformat(snaps[i]["scraped_at"])
            hours = (t1 - t0).total_seconds() / 3600
            if hours > 0:
                vel = (snaps[i]["views"] - snaps[i-1]["views"]) / hours
                all_velocities.append(vel)

    median = statistics.median(latest_views) if latest_views else 0
    avg_vel = sum(all_velocities) / len(all_velocities) if all_velocities else 0

    return {"median_views": median, "avg_velocity": avg_vel}


def compute_score(*, views: int, likes: int, comments: int,
                  channel_median: float, channel_avg_velocity: float,
                  channel_subscribers: int, snapshots: list[dict],
                  published_at: str | None = None) -> dict:
    """Compute raw composite score for a video. No tier boost, no decay."""

    # Outlier
    outlier = views / channel_median if channel_median > 0 else 0

    # Views absolute
    views_abs = views

    # Early detection
    early = False
    if published_at:
        pub_time = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        now = datetime.now(pub_time.tzinfo) if pub_time.tzinfo else datetime.utcnow()
        early = (now - pub_time).total_seconds() / 3600 < 24

    # Velocity
    if len(snapshots) >= 2:
        t0 = datetime.fromisoformat(snapshots[0]["scraped_at"])
        t1 = datetime.fromisoformat(snapshots[-1]["scraped_at"])
        hours = (t1 - t0).total_seconds() / 3600
        video_vel = (snapshots[-1]["views"] - snapshots[0]["views"]) / hours if hours > 0 else 0
        velocity_ratio = video_vel / channel_avg_velocity if channel_avg_velocity > 0 else 0
    elif early and published_at:
        pub_time = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        now = datetime.now(pub_time.tzinfo) if pub_time.tzinfo else datetime.utcnow()
        hours_since = (now - pub_time).total_seconds() / 3600
        if hours_since > 0:
            early_vel = views / hours_since
            velocity_ratio = early_vel / channel_avg_velocity if channel_avg_velocity > 0 else 0
        else:
            velocity_ratio = 0
    else:
        velocity_ratio = 0

    # Views/subs
    views_subs = views / channel_subscribers if channel_subscribers > 0 else 0

    # Engagement
    engagement = (likes + comments) / views if views > 0 else 0

    # Normalize all
    w = WEIGHTS_EARLY if early else WEIGHTS
    composite = round(
        normalize(outlier, OUTLIER_THRESHOLDS) * w["outlier"]
        + normalize(views_abs, VIEWS_ABS_THRESHOLDS) * w["views_abs"]
        + normalize(velocity_ratio, VELOCITY_THRESHOLDS) * w["velocity"]
        + normalize(views_subs, VIEWS_SUBS_THRESHOLDS) * w["views_subs"]
        + normalize(engagement * 100, ENGAGEMENT_THRESHOLDS) * w["engagement"],
        2
    )

    return {
        "composite": composite,
        "outlier": round(outlier, 2),
        "views_abs": views_abs,
        "velocity_ratio": round(velocity_ratio, 2),
        "views_subs": round(views_subs, 4),
        "engagement": round(engagement, 4),
        "early": early,
    }


def apply_tier_boost(score: float, tier: str) -> float:
    multiplier = TIER_MULTIPLIER.get(tier, 1.0)
    return min(round(score * multiplier, 2), 100.0)


def apply_decay(score: float, published_at: str | None) -> tuple[float, bool]:
    """Returns (decayed_score, is_anomaly)."""
    if not published_at:
        return score, False
    pub_time = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    now = datetime.now(pub_time.tzinfo) if pub_time.tzinfo else datetime.utcnow()
    age_hours = (now - pub_time).total_seconds() / 3600

    for threshold, multiplier in AGE_DECAY:
        if age_hours < threshold:
            return min(round(score * multiplier, 2), 100.0), False

    if score >= ANOMALY_THRESHOLD:
        return min(round(score * 0.3, 2), 100.0), True
    return 0.0, False
