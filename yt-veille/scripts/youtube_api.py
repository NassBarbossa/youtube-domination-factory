import logging
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class YouTubeClient:
    def __init__(self, api_key: str):
        self.service = build("youtube", "v3", developerKey=api_key)

    def _uploads_playlist_id(self, channel_id: str) -> str:
        return "UU" + channel_id[2:]

    def get_channel_stats(self, channel_id: str, _retry: bool = True) -> dict | None:
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
