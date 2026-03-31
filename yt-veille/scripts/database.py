"""SQLite database layer for yt-veille."""
import sqlite3
import statistics
from pathlib import Path
from datetime import datetime


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: str):
    conn = get_connection(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY,
            handle TEXT NOT NULL,
            subscribers INTEGER DEFAULT 0,
            median_views REAL,
            avg_velocity REAL,
            niche TEXT,
            added_at TEXT,
            last_updated TEXT
        );

        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            channel_id TEXT NOT NULL REFERENCES channels(channel_id),
            title TEXT,
            description TEXT,
            tags TEXT,
            duration_seconds INTEGER,
            published_at TEXT,
            thumbnail_url TEXT,
            category_id TEXT,
            detected_at TEXT,
            topic TEXT,
            composite_score REAL
        );

        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL REFERENCES videos(video_id),
            scraped_at TEXT NOT NULL,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            UNIQUE(video_id, scraped_at)
        );

        CREATE INDEX IF NOT EXISTS idx_snapshots_video ON snapshots(video_id);
        CREATE INDEX IF NOT EXISTS idx_videos_channel ON videos(channel_id);
        CREATE INDEX IF NOT EXISTS idx_videos_composite ON videos(composite_score);
    """)
    conn.commit()
    conn.close()


def upsert_channel(db_path: str, *, channel_id: str, handle: str,
                   subscribers: int, niche: str, added_at: str):
    conn = get_connection(db_path)
    conn.execute("""
        INSERT INTO channels (channel_id, handle, subscribers, niche, added_at, last_updated)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(channel_id) DO UPDATE SET
            handle=excluded.handle,
            subscribers=excluded.subscribers,
            last_updated=datetime('now')
    """, (channel_id, handle, subscribers, niche, added_at))
    conn.commit()
    conn.close()


def upsert_video(db_path: str, *, video_id: str, channel_id: str,
                 title: str, description: str, tags: str,
                 duration_seconds: int, published_at: str,
                 thumbnail_url: str, category_id: str, detected_at: str):
    conn = get_connection(db_path)
    conn.execute("""
        INSERT INTO videos (video_id, channel_id, title, description, tags,
                           duration_seconds, published_at, thumbnail_url,
                           category_id, detected_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(video_id) DO UPDATE SET
            title=excluded.title,
            description=excluded.description,
            tags=excluded.tags
    """, (video_id, channel_id, title, description, tags,
          duration_seconds, published_at, thumbnail_url,
          category_id, detected_at))
    conn.commit()
    conn.close()


def insert_snapshot(db_path: str, *, video_id: str, scraped_at: str,
                    views: int, likes: int, comments: int):
    conn = get_connection(db_path)
    conn.execute("""
        INSERT INTO snapshots (video_id, scraped_at, views, likes, comments)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(video_id, scraped_at) DO UPDATE SET
            views=excluded.views,
            likes=excluded.likes,
            comments=excluded.comments
    """, (video_id, scraped_at, views, likes, comments))
    conn.commit()
    conn.close()


def get_channel_median(channel_id: str, db_path: str) -> float | None:
    conn = get_connection(db_path)
    rows = conn.execute("""
        SELECT s.views FROM snapshots s
        JOIN videos v ON s.video_id = v.video_id
        WHERE v.channel_id = ?
        AND s.scraped_at = (
            SELECT MAX(s2.scraped_at) FROM snapshots s2
            WHERE s2.video_id = s.video_id
        )
    """, (channel_id,)).fetchall()
    conn.close()
    if not rows:
        return None
    views = [r[0] for r in rows]
    return statistics.median(views)


def get_channel_avg_velocity(channel_id: str, db_path: str) -> float | None:
    conn = get_connection(db_path)
    videos = conn.execute(
        "SELECT video_id FROM videos WHERE channel_id = ?", (channel_id,)
    ).fetchall()
    all_velocities = []
    for vid_row in videos:
        vid_id = vid_row[0]
        snaps = conn.execute(
            "SELECT scraped_at, views FROM snapshots WHERE video_id = ? ORDER BY scraped_at",
            (vid_id,)
        ).fetchall()
        for i in range(1, len(snaps)):
            t0 = datetime.fromisoformat(snaps[i-1][0])
            t1 = datetime.fromisoformat(snaps[i][0])
            hours = (t1 - t0).total_seconds() / 3600
            if hours > 0:
                vel = (snaps[i][1] - snaps[i-1][1]) / hours
                all_velocities.append(vel)
    conn.close()
    if not all_velocities:
        return None
    return sum(all_velocities) / len(all_velocities)


def get_video_snapshots(video_id: str, db_path: str) -> list[dict]:
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT scraped_at, views, likes, comments FROM snapshots WHERE video_id = ? ORDER BY scraped_at",
        (video_id,)
    ).fetchall()
    conn.close()
    return [{"scraped_at": r[0], "views": r[1], "likes": r[2], "comments": r[3]} for r in rows]


def get_scored_videos(db_path: str, min_score: float = 50, days: int = 30) -> list[dict]:
    conn = get_connection(db_path)
    rows = conn.execute("""
        SELECT v.video_id, v.channel_id, v.title, v.description, v.tags,
               v.published_at, v.thumbnail_url, v.topic, v.composite_score,
               c.handle, c.subscribers
        FROM videos v
        JOIN channels c ON v.channel_id = c.channel_id
        WHERE v.composite_score >= ?
        AND v.detected_at >= date('now', ?)
        ORDER BY v.composite_score DESC
    """, (min_score, f"-{days} days")).fetchall()
    conn.close()
    return [
        {
            "video_id": r[0], "channel_id": r[1], "title": r[2],
            "description": r[3], "tags": r[4], "published_at": r[5],
            "thumbnail_url": r[6], "topic": r[7], "composite_score": r[8],
            "channel_handle": r[9], "channel_subscribers": r[10],
        }
        for r in rows
    ]


def update_video_score(db_path: str, video_id: str, composite_score: float, topic: str | None = None):
    conn = get_connection(db_path)
    if topic:
        conn.execute(
            "UPDATE videos SET composite_score=?, topic=? WHERE video_id=?",
            (composite_score, topic, video_id)
        )
    else:
        conn.execute(
            "UPDATE videos SET composite_score=? WHERE video_id=?",
            (composite_score, video_id)
        )
    conn.commit()
    conn.close()


def update_channel_stats(db_path: str, channel_id: str, median_views: float, avg_velocity: float):
    conn = get_connection(db_path)
    conn.execute(
        "UPDATE channels SET median_views=?, avg_velocity=?, last_updated=datetime('now') WHERE channel_id=?",
        (median_views, avg_velocity, channel_id)
    )
    conn.commit()
    conn.close()
