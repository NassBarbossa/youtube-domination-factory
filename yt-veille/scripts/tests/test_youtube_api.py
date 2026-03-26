import pytest
from unittest.mock import MagicMock, patch
from youtube_api import YouTubeClient


@pytest.fixture
def mock_service():
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
    client = YouTubeClient.__new__(YouTubeClient)
    assert client._uploads_playlist_id("UCfQNB91qRP_5ILeu_S_bSkg") == "UUfQNB91qRP_5ILeu_S_bSkg"


def test_get_channel_stats_empty_response(mock_service):
    mock_service.channels().list().execute.return_value = {"items": []}
    client = YouTubeClient("fake_key")
    stats = client.get_channel_stats("UC_INVALID")
    assert stats is None
