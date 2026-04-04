"""SQLite database layer for yt-veille."""
import sqlite3


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
            subscribers INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            channel_id TEXT NOT NULL REFERENCES channels(channel_id),
            title TEXT,
            description TEXT,
            duration_seconds INTEGER,
            published_at TEXT
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
    """)
    conn.commit()
    conn.close()


def upsert_channel(db_path: str, *, channel_id: str, handle: str,
                   subscribers: int):
    conn = get_connection(db_path)
    conn.execute("""
        INSERT INTO channels (channel_id, handle, subscribers)
        VALUES (?, ?, ?)
        ON CONFLICT(channel_id) DO UPDATE SET
            handle=excluded.handle,
            subscribers=excluded.subscribers
    """, (channel_id, handle, subscribers))
    conn.commit()
    conn.close()


def upsert_video(db_path: str, *, video_id: str, channel_id: str,
                 title: str, description: str,
                 duration_seconds: int, published_at: str):
    conn = get_connection(db_path)
    conn.execute("""
        INSERT INTO videos (video_id, channel_id, title, description,
                           duration_seconds, published_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(video_id) DO UPDATE SET
            title=excluded.title,
            description=excluded.description
    """, (video_id, channel_id, title, description,
          duration_seconds, published_at))
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


def get_video_snapshots(video_id: str, db_path: str) -> list[dict]:
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT scraped_at, views, likes, comments FROM snapshots WHERE video_id = ? ORDER BY scraped_at",
        (video_id,)
    ).fetchall()
    conn.close()
    return [{"scraped_at": r[0], "views": r[1], "likes": r[2], "comments": r[3]} for r in rows]


def get_all_videos(db_path: str) -> list[dict]:
    """Get all videos with their channel info."""
    conn = get_connection(db_path)
    rows = conn.execute("""
        SELECT v.video_id, v.channel_id, v.title, v.description,
               v.duration_seconds, v.published_at,
               c.handle, c.subscribers
        FROM videos v
        JOIN channels c ON v.channel_id = c.channel_id
    """).fetchall()
    conn.close()
    return [
        {
            "video_id": r[0], "channel_id": r[1], "title": r[2],
            "description": r[3], "duration_seconds": r[4],
            "published_at": r[5], "channel_handle": r[6],
            "channel_subscribers": r[7],
        }
        for r in rows
    ]
