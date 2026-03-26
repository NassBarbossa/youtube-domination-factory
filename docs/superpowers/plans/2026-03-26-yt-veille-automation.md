# YouTube Veille Automation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatiser la veille YouTube avec deux scripts Python : monitoring quotidien des chaînes suivies + découverte de nouveaux créateurs, déployés sur VPS avec cron.

**Architecture:** Deux scripts indépendants sous `yt-veille/scripts/`. `daily_monitor.py` utilise YouTube Data API (`playlistItems.list` + `videos.list` batché) pour détecter les nouvelles vidéos et outliers, écrit dans `context/backlog.json`, commit+push. `discover_creators.py` utilise `search.list` pour trouver de nouveaux créateurs par mots-clés.

**Tech Stack:** Python 3.10+, google-api-python-client, python-dotenv

**Spec:** `docs/superpowers/specs/2026-03-26-yt-veille-automation-design.md`

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `yt-veille/scripts/youtube_api.py` | Create | Client YouTube API : fetch channel stats, uploads, video stats |
| `yt-veille/scripts/daily_monitor.py` | Create | Orchestrateur quotidien : collecte, outliers, backlog, git push |
| `yt-veille/scripts/discover_creators.py` | Create | Découverte de créateurs par mots-clés |
| `yt-veille/scripts/json_io.py` | Create | Lecture/écriture atomique de fichiers JSON |
| `yt-veille/scripts/config/channels.json` | Create | Liste des chaînes à surveiller |
| `yt-veille/scripts/config/keywords.json` | Create | Mots-clés pour la découverte |
| `yt-veille/scripts/data/last_check.json` | Create | État du dernier check (auto-généré) |
| `yt-veille/scripts/data/channel_stats.json` | Create | Historique des stats par chaîne (auto-généré) |
| `yt-veille/scripts/.env.example` | Create | Template des variables d'environnement |
| `yt-veille/scripts/.gitignore` | Create | Exclut .env |
| `yt-veille/scripts/requirements.txt` | Create | Dépendances Python |
| `context/backlog.json` | Create | Output principal de la veille |
| `yt-veille/scripts/tests/conftest.py` | Create | Ajoute le parent au sys.path pour les imports |
| `yt-veille/scripts/tests/test_youtube_api.py` | Create | Tests du client API |
| `yt-veille/scripts/tests/test_daily_monitor.py` | Create | Tests du monitoring |
| `yt-veille/scripts/tests/test_json_io.py` | Create | Tests lecture/écriture JSON |
| `yt-veille/scripts/tests/test_discover_creators.py` | Create | Tests de la découverte |

---

### Task 1: Project scaffolding — config, .env, requirements

**Files:**
- Create: `yt-veille/scripts/requirements.txt`
- Create: `yt-veille/scripts/.env.example`
- Create: `yt-veille/scripts/.gitignore`
- Create: `yt-veille/scripts/config/channels.json`
- Create: `yt-veille/scripts/config/keywords.json`
- Create: `context/backlog.json`

- [ ] **Step 1: Create requirements.txt**

```
google-api-python-client
python-dotenv
pytest
```

- [ ] **Step 2: Create .env.example**

```
YOUTUBE_API_KEY=your_youtube_api_key_here
GITHUB_TOKEN=your_github_token_here
```

- [ ] **Step 3: Create .gitignore**

```
.env
```

- [ ] **Step 4: Create channels.json**

```json
{
  "channels": [
    {
      "handle": "AlexFinnOfficial",
      "channel_id": "UCfQNB91qRP_5ILeu_S_bSkg",
      "niche": "claude-code-ai",
      "added_at": "2026-03-26"
    }
  ]
}
```

- [ ] **Step 5: Create keywords.json**

```json
{
  "keywords": [
    "Claude Code",
    "VibeCoding",
    "vibe coding",
    "AI tools tutorial",
    "build with AI",
    "Anthropic Claude",
    "AI automation business",
    "no code AI",
    "AI agent"
  ]
}
```

- [ ] **Step 6: Create empty backlog.json at project root**

```json
{
  "last_updated": null,
  "items": []
}
```

- [ ] **Step 7: Create tests/conftest.py for import resolution**

```python
# yt-veille/scripts/tests/conftest.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

- [ ] **Step 8: Create empty data directory files**

Create `yt-veille/scripts/data/last_check.json`:
```json
{
  "last_check_utc": null,
  "checked_video_ids": []
}
```

Create `yt-veille/scripts/data/channel_stats.json`:
```json
{}
```

- [ ] **Step 9: Commit**

```bash
git add yt-veille/scripts/requirements.txt yt-veille/scripts/.env.example yt-veille/scripts/.gitignore yt-veille/scripts/config/ yt-veille/scripts/data/ yt-veille/scripts/tests/conftest.py context/backlog.json
git commit -m "feat(veille): scaffold project config, env, and data files"
```

---

### Task 2: JSON I/O module — atomic reads and writes

**Files:**
- Create: `yt-veille/scripts/json_io.py`
- Create: `yt-veille/scripts/tests/test_json_io.py`

- [ ] **Step 1: Write failing tests**

```python
# yt-veille/scripts/tests/test_json_io.py
import json
import os
import tempfile
import pytest
from json_io import read_json, write_json

def test_read_json_valid_file(tmp_path):
    f = tmp_path / "test.json"
    f.write_text('{"key": "value"}')
    assert read_json(str(f)) == {"key": "value"}

def test_read_json_missing_file_returns_default(tmp_path):
    result = read_json(str(tmp_path / "missing.json"), default={"items": []})
    assert result == {"items": []}

def test_read_json_corrupted_file_returns_default(tmp_path):
    f = tmp_path / "bad.json"
    f.write_text("not json {{{")
    result = read_json(str(f), default={"items": []})
    assert result == {"items": []}

def test_write_json_creates_file(tmp_path):
    path = str(tmp_path / "out.json")
    write_json(path, {"key": "value"})
    with open(path) as f:
        assert json.load(f) == {"key": "value"}

def test_write_json_atomic_no_corruption_on_existing(tmp_path):
    path = str(tmp_path / "out.json")
    write_json(path, {"original": True})
    write_json(path, {"updated": True})
    with open(path) as f:
        assert json.load(f) == {"updated": True}

def test_write_json_creates_parent_dirs(tmp_path):
    path = str(tmp_path / "sub" / "dir" / "out.json")
    write_json(path, {"nested": True})
    with open(path) as f:
        assert json.load(f) == {"nested": True}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd yt-veille/scripts && python3 -m pytest tests/test_json_io.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'json_io'`

- [ ] **Step 3: Implement json_io.py**

```python
# yt-veille/scripts/json_io.py
import json
import logging
import os
import tempfile

logger = logging.getLogger(__name__)


def read_json(path: str, default=None):
    """Read a JSON file. Return default if missing or corrupted."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("File not found: %s — using default", path)
        return default if default is not None else {}
    except json.JSONDecodeError:
        logger.warning("Corrupted JSON: %s — using default", path)
        return default if default is not None else {}


def write_json(path: str, data):
    """Write JSON atomically: write to temp file then rename."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    dir_name = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp_path, path)
    except Exception:
        os.unlink(tmp_path)
        raise
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd yt-veille/scripts && python3 -m pytest tests/test_json_io.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add yt-veille/scripts/json_io.py yt-veille/scripts/tests/test_json_io.py
git commit -m "feat(veille): add atomic JSON read/write module with tests"
```

---

### Task 3: YouTube API client

**Files:**
- Create: `yt-veille/scripts/youtube_api.py`
- Create: `yt-veille/scripts/tests/test_youtube_api.py`

- [ ] **Step 1: Write failing tests**

```python
# yt-veille/scripts/tests/test_youtube_api.py
import pytest
from unittest.mock import MagicMock, patch
from youtube_api import YouTubeClient


@pytest.fixture
def mock_service():
    """Create a mock YouTube API service."""
    with patch("youtube_api.build") as mock_build:
        service = MagicMock()
        mock_build.return_value = service
        yield service


def test_get_channel_stats(mock_service):
    mock_service.channels().list().execute.return_value = {
        "items": [{
            "statistics": {
                "subscriberCount": "68000",
                "viewCount": "5000000",
                "videoCount": "171"
            }
        }]
    }
    client = YouTubeClient("fake_key")
    stats = client.get_channel_stats("UCfQNB91qRP_5ILeu_S_bSkg")
    assert stats["subscriber_count"] == 68000
    assert stats["view_count"] == 5000000
    assert stats["video_count"] == 171


def test_get_latest_uploads(mock_service):
    mock_service.playlistItems().list().execute.return_value = {
        "items": [
            {
                "contentDetails": {"videoId": "abc123"},
                "snippet": {
                    "title": "Test Video",
                    "publishedAt": "2026-03-25T20:00:00Z"
                }
            }
        ]
    }
    client = YouTubeClient("fake_key")
    videos = client.get_latest_uploads("UCfQNB91qRP_5ILeu_S_bSkg", max_results=5)
    assert len(videos) == 1
    assert videos[0]["video_id"] == "abc123"
    assert videos[0]["title"] == "Test Video"


def test_get_latest_uploads_fallback_to_search(mock_service):
    """If playlistItems fails, fallback to search."""
    mock_service.playlistItems().list().execute.side_effect = Exception("API error")
    mock_service.search().list().execute.return_value = {
        "items": [
            {
                "id": {"videoId": "xyz789"},
                "snippet": {
                    "title": "Fallback Video",
                    "publishedAt": "2026-03-24T10:00:00Z"
                }
            }
        ]
    }
    client = YouTubeClient("fake_key")
    videos = client.get_latest_uploads("UCfQNB91qRP_5ILeu_S_bSkg", max_results=5)
    assert len(videos) == 1
    assert videos[0]["video_id"] == "xyz789"


def test_get_video_stats_batched(mock_service):
    mock_service.videos().list().execute.return_value = {
        "items": [
            {
                "id": "abc123",
                "statistics": {
                    "viewCount": "15230",
                    "likeCount": "892",
                    "commentCount": "134"
                }
            },
            {
                "id": "def456",
                "statistics": {
                    "viewCount": "8000",
                    "likeCount": "400",
                    "commentCount": "50"
                }
            }
        ]
    }
    client = YouTubeClient("fake_key")
    stats = client.get_video_stats(["abc123", "def456"])
    assert stats["abc123"]["views"] == 15230
    assert stats["def456"]["views"] == 8000


def test_uploads_playlist_id():
    """UC -> UU conversion."""
    client = YouTubeClient.__new__(YouTubeClient)
    assert client._uploads_playlist_id("UCfQNB91qRP_5ILeu_S_bSkg") == "UUfQNB91qRP_5ILeu_S_bSkg"


def test_get_channel_stats_empty_response(mock_service):
    mock_service.channels().list().execute.return_value = {"items": []}
    client = YouTubeClient("fake_key")
    stats = client.get_channel_stats("UC_INVALID")
    assert stats is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd yt-veille/scripts && python3 -m pytest tests/test_youtube_api.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'youtube_api'`

- [ ] **Step 3: Implement youtube_api.py**

```python
# yt-veille/scripts/youtube_api.py
import logging
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class YouTubeClient:
    def __init__(self, api_key: str):
        self.service = build("youtube", "v3", developerKey=api_key)

    def _uploads_playlist_id(self, channel_id: str) -> str:
        """Convert channel ID (UC...) to uploads playlist ID (UU...)."""
        return "UU" + channel_id[2:]

    def get_channel_stats(self, channel_id: str, _retry: bool = True) -> dict | None:
        """Fetch subscriber count, view count, video count. Returns None if not found."""
        try:
            resp = self.service.channels().list(
                part="statistics",
                id=channel_id
            ).execute()
            if not resp.get("items"):
                logger.warning("Channel not found: %s", channel_id)
                return None
            stats = resp["items"][0]["statistics"]
            return {
                "subscriber_count": int(stats.get("subscriberCount", 0)),
                "view_count": int(stats.get("viewCount", 0)),
                "video_count": int(stats.get("videoCount", 0)),
            }
        except HttpError as e:
            logger.error("API error fetching channel %s: %s", channel_id, e)
            if e.resp.status in (403, 429):
                return None
            if e.resp.status >= 500 and _retry:
                time.sleep(5)
                return self.get_channel_stats(channel_id, _retry=False)
            return None

    def get_latest_uploads(self, channel_id: str, max_results: int = 10) -> list[dict]:
        """Fetch latest uploads via playlistItems. Fallback to search on failure."""
        try:
            playlist_id = self._uploads_playlist_id(channel_id)
            resp = self.service.playlistItems().list(
                part="contentDetails,snippet",
                playlistId=playlist_id,
                maxResults=max_results
            ).execute()
            return [
                {
                    "video_id": item["contentDetails"]["videoId"],
                    "title": item["snippet"]["title"],
                    "published_at": item["snippet"]["publishedAt"],
                }
                for item in resp.get("items", [])
            ]
        except Exception as e:
            logger.warning("playlistItems failed for %s, falling back to search: %s", channel_id, e)
            return self._search_latest_videos(channel_id, max_results)

    def _search_latest_videos(self, channel_id: str, max_results: int) -> list[dict]:
        """Fallback: use search.list (costs 100 units)."""
        try:
            resp = self.service.search().list(
                part="snippet",
                channelId=channel_id,
                order="date",
                type="video",
                maxResults=max_results
            ).execute()
            return [
                {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "published_at": item["snippet"]["publishedAt"],
                }
                for item in resp.get("items", [])
            ]
        except HttpError as e:
            logger.error("Search fallback also failed for %s: %s", channel_id, e)
            return []

    def get_video_stats(self, video_ids: list[str]) -> dict:
        """Fetch stats for multiple videos, batched by 50."""
        result = {}
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i + 50]
            try:
                resp = self.service.videos().list(
                    part="statistics",
                    id=",".join(batch)
                ).execute()
                for item in resp.get("items", []):
                    stats = item["statistics"]
                    result[item["id"]] = {
                        "views": int(stats.get("viewCount", 0)),
                        "likes": int(stats.get("likeCount", 0)),
                        "comments": int(stats.get("commentCount", 0)),
                    }
            except HttpError as e:
                logger.error("Error fetching video stats: %s", e)
        return result

    def search_channels(self, query: str, max_results: int = 10) -> list[dict]:
        """Search for channels by keyword. Used by discover_creators."""
        try:
            resp = self.service.search().list(
                part="snippet",
                q=query,
                type="channel",
                maxResults=max_results
            ).execute()
            return [
                {
                    "channel_id": item["id"]["channelId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                }
                for item in resp.get("items", [])
            ]
        except HttpError as e:
            logger.error("Error searching channels for '%s': %s", query, e)
            return []
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd yt-veille/scripts && python3 -m pytest tests/test_youtube_api.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add yt-veille/scripts/youtube_api.py yt-veille/scripts/tests/test_youtube_api.py
git commit -m "feat(veille): add YouTube API client with playlistItems + fallback + batching"
```

---

### Task 4: Daily monitor — core logic

**Files:**
- Create: `yt-veille/scripts/daily_monitor.py`
- Create: `yt-veille/scripts/tests/test_daily_monitor.py`

- [ ] **Step 1: Write failing tests**

```python
# yt-veille/scripts/tests/test_daily_monitor.py
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


def test_prune_backlog_archives_old_entries(tmp_path):
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd yt-veille/scripts && python3 -m pytest tests/test_daily_monitor.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement daily_monitor.py**

```python
# yt-veille/scripts/daily_monitor.py
"""Daily YouTube channel monitor — detects new videos and outliers."""
import logging
import os
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv

from json_io import read_json, write_json
from youtube_api import YouTubeClient

# Paths
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR / "config"
DATA_DIR = SCRIPT_DIR / "data"
PROJECT_ROOT = SCRIPT_DIR.parent.parent
BACKLOG_PATH = PROJECT_ROOT / "context" / "backlog.json"

logger = logging.getLogger("daily_monitor")


def setup_logging():
    handler = RotatingFileHandler(
        "/var/log/yt-veille.log", maxBytes=5 * 1024 * 1024, backupCount=3
    )
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)


def detect_new_videos(uploads: list[dict], checked_ids: set) -> list[dict]:
    """Return videos not in checked_ids."""
    return [v for v in uploads if v["video_id"] not in checked_ids]


def compute_outliers(video_views: dict, history: list[int]) -> dict:
    """Compute outlier status for each video. Requires >= 5 history entries."""
    result = {}
    if len(history) < 5:
        for vid, views in video_views.items():
            result[vid] = {"outlier": False, "median_views": None, "outlier_ratio": None}
        return result

    median = statistics.median(history)
    for vid, views in video_views.items():
        ratio = views / median if median > 0 else 0
        result[vid] = {
            "outlier": ratio > 3.0,
            "median_views": median,
            "outlier_ratio": ratio,
        }
    return result


def deduplicate_backlog(existing_items: list[dict], new_items: list[dict]) -> list[dict]:
    """Remove items from new_items that already exist in existing_items by id."""
    existing_ids = {item["id"] for item in existing_items}
    return [item for item in new_items if item["id"] not in existing_ids]


def build_backlog_entry(
    video_id: str, title: str, channel_name: str, channel_id: str,
    published_at: str, views: int, likes: int, comments: int,
    subscribers: int, outlier: bool, median_views, outlier_ratio,
) -> dict:
    return {
        "id": video_id,
        "title": title,
        "channel": channel_name,
        "channel_id": channel_id,
        "published": published_at,
        "views": views,
        "likes": likes,
        "comments": comments,
        "channel_subscribers": subscribers,
        "thumbnail": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "outlier": outlier,
        "median_views": median_views,
        "outlier_ratio": outlier_ratio,
        "detected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "daily_monitor",
    }


def prune_backlog(items: list[dict], max_age_days: int = 90) -> tuple[list[dict], list[dict]]:
    """Split items into kept (recent) and archived (older than max_age_days)."""
    cutoff = datetime.now(timezone.utc) - __import__("datetime").timedelta(days=max_age_days)
    kept, archived = [], []
    for item in items:
        detected = datetime.fromisoformat(item["detected_at"].replace("Z", "+00:00"))
        if detected >= cutoff:
            kept.append(item)
        else:
            archived.append(item)
    return kept, archived


def save_archive(archived: list[dict], project_root: Path):
    """Save archived items grouped by month into context/backlog-archive/."""
    if not archived:
        return
    archive_dir = project_root / "context" / "backlog-archive"
    by_month = {}
    for item in archived:
        month_key = item["detected_at"][:7]  # YYYY-MM
        by_month.setdefault(month_key, []).append(item)
    for month_key, items in by_month.items():
        path = str(archive_dir / f"{month_key}.json")
        existing = read_json(path, default={"items": []})
        existing_ids = {i["id"] for i in existing["items"]}
        new_items = [i for i in items if i["id"] not in existing_ids]
        existing["items"].extend(new_items)
        write_json(path, existing)
    logger.info("Archived %d items across %d month(s)", len(archived), len(by_month))


def git_push(project_root: Path):
    """Pull rebase, commit backlog changes, push."""
    try:
        subprocess.run(
            ["git", "pull", "--rebase"],
            cwd=project_root, check=True, capture_output=True, text=True
        )
        subprocess.run(
            ["git", "add", "context/backlog.json", "context/backlog-archive/", "yt-veille/scripts/data/"],
            cwd=project_root, check=True, capture_output=True, text=True
        )
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root, capture_output=True, text=True
        )
        if not result.stdout.strip():
            logger.info("No changes to commit")
            return
        subprocess.run(
            ["git", "commit", "-m", "chore(veille): daily monitor update"],
            cwd=project_root, check=True, capture_output=True, text=True
        )
        subprocess.run(
            ["git", "push"],
            cwd=project_root, check=True, capture_output=True, text=True
        )
        logger.info("Changes pushed to GitHub")
    except subprocess.CalledProcessError as e:
        logger.error("Git operation failed: %s\n%s", e, e.stderr)
        subprocess.run(["git", "rebase", "--abort"], cwd=project_root, capture_output=True)
        sys.exit(1)


def main():
    setup_logging()
    load_dotenv(SCRIPT_DIR / ".env")

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        logger.error("YOUTUBE_API_KEY not set")
        sys.exit(1)

    client = YouTubeClient(api_key)
    channels = read_json(str(CONFIG_DIR / "channels.json"), default={"channels": []})
    last_check = read_json(str(DATA_DIR / "last_check.json"), default={"last_check_utc": None, "checked_video_ids": []})
    channel_stats = read_json(str(DATA_DIR / "channel_stats.json"), default={})
    backlog = read_json(str(BACKLOG_PATH), default={"last_updated": None, "items": []})

    checked_ids = set(last_check.get("checked_video_ids", []))
    all_new_checked_ids = set()
    new_entries = []
    total_new = 0
    total_outliers = 0

    for ch in channels.get("channels", []):
        cid = ch["channel_id"]
        logger.info("Checking channel: %s (%s)", ch["handle"], cid)

        stats = client.get_channel_stats(cid)
        if stats is None:
            logger.warning("Skipping channel %s — could not fetch stats", ch["handle"])
            continue

        uploads = client.get_latest_uploads(cid, max_results=10)
        new_videos = detect_new_videos(uploads, checked_ids)

        if not new_videos:
            logger.info("  No new videos for %s", ch["handle"])
            all_new_checked_ids.update(v["video_id"] for v in uploads)
            continue

        video_ids = [v["video_id"] for v in new_videos]
        video_stats = client.get_video_stats(video_ids)
        all_new_checked_ids.update(v["video_id"] for v in uploads)

        # Update channel history
        history = channel_stats.get(cid, {"views_history": []})
        views_history = history.get("views_history", [])

        video_views = {vid: video_stats.get(vid, {}).get("views", 0) for vid in video_ids}
        outlier_info = compute_outliers(video_views, views_history)

        for v in new_videos:
            vid = v["video_id"]
            vs = video_stats.get(vid, {"views": 0, "likes": 0, "comments": 0})
            oi = outlier_info.get(vid, {"outlier": False, "median_views": None, "outlier_ratio": None})

            entry = build_backlog_entry(
                video_id=vid,
                title=v["title"],
                channel_name=ch["handle"],
                channel_id=cid,
                published_at=v["published_at"],
                views=vs["views"],
                likes=vs["likes"],
                comments=vs["comments"],
                subscribers=stats["subscriber_count"],
                outlier=oi["outlier"],
                median_views=oi["median_views"],
                outlier_ratio=oi["outlier_ratio"],
            )
            new_entries.append(entry)
            views_history.append(vs["views"])
            if oi["outlier"]:
                total_outliers += 1

        # Keep last 20 entries in history
        channel_stats[cid] = {
            "handle": ch["handle"],
            "subscriber_count": stats["subscriber_count"],
            "views_history": views_history[-20:],
            "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        total_new += len(new_videos)

    # Deduplicate and append to backlog
    deduped = deduplicate_backlog(backlog.get("items", []), new_entries)
    backlog["items"] = deduped + backlog.get("items", [])

    # Prune old entries (> 90 days) to archive
    kept, archived = prune_backlog(backlog["items"])
    backlog["items"] = kept
    save_archive(archived, PROJECT_ROOT)

    backlog["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Save files
    write_json(str(BACKLOG_PATH), backlog)
    write_json(str(DATA_DIR / "last_check.json"), {
        "last_check_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checked_video_ids": list(checked_ids | all_new_checked_ids),
    })
    write_json(str(DATA_DIR / "channel_stats.json"), channel_stats)

    logger.info("Checked %d channels, %d new videos, %d outliers", len(channels.get("channels", [])), total_new, total_outliers)

    git_push(PROJECT_ROOT)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd yt-veille/scripts && python3 -m pytest tests/test_daily_monitor.py -v`
Expected: All 8 tests PASS

- [ ] **Step 5: Commit**

```bash
git add yt-veille/scripts/daily_monitor.py yt-veille/scripts/tests/test_daily_monitor.py
git commit -m "feat(veille): add daily monitor with outlier detection and git push"
```

---

### Task 5: Discover creators script

**Files:**
- Create: `yt-veille/scripts/discover_creators.py`
- Create: `yt-veille/scripts/tests/test_discover_creators.py`

- [ ] **Step 1: Write failing tests**

```python
# yt-veille/scripts/tests/test_discover_creators.py
import pytest
from discover_creators import filter_known_channels, score_channel


def test_filter_known_channels():
    found = [
        {"channel_id": "UC_NEW", "title": "New Creator"},
        {"channel_id": "UCfQNB91qRP_5ILeu_S_bSkg", "title": "Alex Finn"},
    ]
    known_ids = {"UCfQNB91qRP_5ILeu_S_bSkg"}
    result = filter_known_channels(found, known_ids)
    assert len(result) == 1
    assert result[0]["channel_id"] == "UC_NEW"


def test_score_channel_high_relevance():
    channel = {
        "title": "Claude Code Tutorials",
        "description": "Learn vibe coding with AI tools",
        "subscriber_count": 5000,
        "video_count": 50,
    }
    keywords = ["Claude Code", "vibe coding", "AI tools"]
    score = score_channel(channel, keywords)
    assert score["relevance"] > 0
    assert score["total"] > 0


def test_score_channel_no_relevance():
    channel = {
        "title": "Cooking with Chef Mike",
        "description": "Best recipes for pasta lovers",
        "subscriber_count": 100000,
        "video_count": 200,
    }
    keywords = ["Claude Code", "vibe coding"]
    score = score_channel(channel, keywords)
    assert score["relevance"] == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd yt-veille/scripts && python3 -m pytest tests/test_discover_creators.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement discover_creators.py**

```python
# yt-veille/scripts/discover_creators.py
"""Discover new YouTube creators in the AI/Claude Code niche."""
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from json_io import read_json, write_json
from youtube_api import YouTubeClient

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR / "config"

logger = logging.getLogger("discover_creators")


def filter_known_channels(found: list[dict], known_ids: set) -> list[dict]:
    """Remove channels already in the monitoring list."""
    return [ch for ch in found if ch["channel_id"] not in known_ids]


def score_channel(channel: dict, keywords: list[str]) -> dict:
    """Score a channel on relevance, size, and activity."""
    text = (channel.get("title", "") + " " + channel.get("description", "")).lower()

    relevance = sum(1 for kw in keywords if kw.lower() in text)
    sub_count = channel.get("subscriber_count", 0)
    video_count = channel.get("video_count", 0)

    # Size score: 0-3 based on subscriber tiers
    if sub_count >= 100000:
        size = 3
    elif sub_count >= 10000:
        size = 2
    elif sub_count >= 1000:
        size = 1
    else:
        size = 0

    # Activity score: 0-2 based on video count
    if video_count >= 50:
        activity = 2
    elif video_count >= 10:
        activity = 1
    else:
        activity = 0

    return {
        "relevance": relevance,
        "size": size,
        "activity": activity,
        "total": relevance + size + activity,
    }


def main():
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
    load_dotenv(SCRIPT_DIR / ".env")

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        logger.error("YOUTUBE_API_KEY not set")
        sys.exit(1)

    client = YouTubeClient(api_key)
    channels_config = read_json(str(CONFIG_DIR / "channels.json"), default={"channels": []})
    keywords_config = read_json(str(CONFIG_DIR / "keywords.json"), default={"keywords": []})

    known_ids = {ch["channel_id"] for ch in channels_config.get("channels", [])}
    keywords = keywords_config.get("keywords", [])

    all_candidates = []

    for kw in keywords:
        logger.info("Searching for: %s", kw)
        found = client.search_channels(kw, max_results=10)
        new_channels = filter_known_channels(found, known_ids)

        for ch in new_channels:
            stats = client.get_channel_stats(ch["channel_id"])
            if stats is None:
                continue
            ch.update(stats)
            ch["scores"] = score_channel(ch, keywords)
            if ch["scores"]["relevance"] > 0:
                all_candidates.append(ch)
            known_ids.add(ch["channel_id"])  # Avoid duplicates across keywords

    # Sort by total score descending
    all_candidates.sort(key=lambda c: c["scores"]["total"], reverse=True)

    if not all_candidates:
        print("\nNo new relevant creators found.")
        return

    print(f"\n{'='*60}")
    print(f" Found {len(all_candidates)} new creator(s)")
    print(f"{'='*60}\n")

    for i, ch in enumerate(all_candidates, 1):
        s = ch["scores"]
        print(f"{i}. {ch['title']}")
        print(f"   Channel ID: {ch['channel_id']}")
        print(f"   Subscribers: {ch.get('subscriber_count', '?'):,}")
        print(f"   Videos: {ch.get('video_count', '?')}")
        print(f"   Score: relevance={s['relevance']} size={s['size']} activity={s['activity']} total={s['total']}")
        print(f"   Description: {ch.get('description', '')[:100]}")
        print()

    # Interactive: ask which to add
    print("Enter the numbers of channels to add (comma-separated), or 'q' to quit:")
    choice = input("> ").strip()
    if choice.lower() == "q":
        return

    indices = [int(x.strip()) - 1 for x in choice.split(",") if x.strip().isdigit()]
    added = 0
    for idx in indices:
        if 0 <= idx < len(all_candidates):
            ch = all_candidates[idx]
            channels_config["channels"].append({
                "handle": ch["title"],
                "channel_id": ch["channel_id"],
                "niche": "discovered",
                "added_at": __import__("datetime").date.today().isoformat(),
            })
            added += 1
            print(f"  Added: {ch['title']}")

    if added > 0:
        write_json(str(CONFIG_DIR / "channels.json"), channels_config)
        print(f"\n{added} channel(s) added to channels.json")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd yt-veille/scripts && python3 -m pytest tests/test_discover_creators.py -v`
Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add yt-veille/scripts/discover_creators.py yt-veille/scripts/tests/test_discover_creators.py
git commit -m "feat(veille): add creator discovery script with keyword search and scoring"
```

---

### Task 6: Integration test with real API

**Files:**
- None new — uses existing scripts

- [ ] **Step 1: Install dependencies**

```bash
cd yt-veille/scripts && pip install -r requirements.txt
```

- [ ] **Step 2: Create .env with real API key**

```bash
cd yt-veille/scripts && cp .env.example .env
# Edit .env and add real YOUTUBE_API_KEY
```

- [ ] **Step 3: Run daily_monitor.py locally**

```bash
cd yt-veille/scripts && python3 daily_monitor.py
```

Expected: Script runs, fetches AlexFinnOfficial videos, writes to `context/backlog.json`, logs output.

- [ ] **Step 4: Verify backlog.json has content**

```bash
cat ../../context/backlog.json | python3 -m json.tool | head -30
```

Expected: JSON with `items` array containing video entries.

- [ ] **Step 5: Run discover_creators.py locally**

```bash
cd yt-veille/scripts && python3 discover_creators.py
```

Expected: Script searches YouTube, shows candidate channels with scores, asks for input.

- [ ] **Step 6: Run all unit tests**

```bash
cd yt-veille/scripts && python3 -m pytest tests/ -v
```

Expected: All tests PASS.

- [ ] **Step 7: Commit any fixes**

```bash
git add -A && git commit -m "fix(veille): integration test fixes"
```

---

### Task 7: Deploy to VPS and setup cron

**Files:**
- None new — deployment steps

- [ ] **Step 1: Push code to GitHub**

```bash
git push origin master
```

- [ ] **Step 2: Clone/pull repo on VPS**

```bash
ssh root@72.62.253.227 "cd /root && git clone https://github.com/NassBarbossa/youtube-domination-factory.git || (cd youtube-domination-factory && git pull)"
```

- [ ] **Step 3: Install Python dependencies on VPS**

```bash
ssh root@72.62.253.227 "cd /root/youtube-domination-factory/yt-veille/scripts && pip3 install -r requirements.txt"
```

- [ ] **Step 4: Create .env on VPS with real API key**

```bash
ssh root@72.62.253.227 "cat > /root/youtube-domination-factory/yt-veille/scripts/.env << 'EOF'
YOUTUBE_API_KEY=<the_real_key>
EOF"
```

- [ ] **Step 5: Test run on VPS**

```bash
ssh root@72.62.253.227 "cd /root/youtube-domination-factory/yt-veille/scripts && python3 daily_monitor.py"
```

Expected: Script runs successfully, outputs log.

- [ ] **Step 6: Configure git credentials on VPS for push**

```bash
ssh root@72.62.253.227 "cd /root/youtube-domination-factory && git remote set-url origin https://<GITHUB_TOKEN>@github.com/NassBarbossa/youtube-domination-factory.git"
```

- [ ] **Step 7: Setup cron — 9h00 SGT = 01:00 UTC**

```bash
ssh root@72.62.253.227 "(crontab -l 2>/dev/null; echo '0 1 * * * cd /root/youtube-domination-factory/yt-veille/scripts && /usr/bin/python3 daily_monitor.py >> /var/log/yt-veille.log 2>&1') | crontab -"
```

- [ ] **Step 8: Verify cron is set**

```bash
ssh root@72.62.253.227 "crontab -l"
```

Expected: Shows the cron entry for 01:00 UTC.

- [ ] **Step 9: Commit deployment docs if needed**

```bash
git commit -m "chore(veille): deployment complete on VPS"
```
