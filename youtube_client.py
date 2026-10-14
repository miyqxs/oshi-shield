import logging
from dataclasses import dataclass

import httplib2
from google.auth.exceptions import GoogleAuthError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

log = logging.getLogger(__name__)


class YouTubeError(Exception):
    """Anything that went wrong talking to YouTube, with a human-readable message."""

    def __init__(self, message, retryable=False):
        super().__init__(message)
        self.retryable = retryable


class ChatEnded(YouTubeError):
    pass


@dataclass
class ChatMessage:
    id: str
    author: str
    text: str


@dataclass
class ChatPage:
    messages: list
    next_page_token: str | None
    poll_interval: float


class YouTubeClient:
    def __init__(self, api_key):
        if not api_key:
            raise YouTubeError("YOUTUBE_API_KEY is missing. Put it in your .env file.")
        try:
            self._yt = build("youtube", "v3", developerKey=api_key)
        except GoogleAuthError as e:  # includes MutualTLSChannelError
            raise YouTubeError(f"Google client setup failed: {e}") from e
        except (OSError, httplib2.HttpLib2Error) as e:
            raise YouTubeError("Can't reach Google. Check your internet.", retryable=True) from e

    # ---------- public ----------

    def get_live_chat_id(self, video_id):
        resp = self._execute(
            self._yt.videos().list(part="liveStreamingDetails", id=video_id)
        )
        items = resp.get("items")
        if not isinstance(items, list) or not items:
            raise YouTubeError("Video not found. Check the video ID.")

        item = items[0]
        details = item.get("liveStreamingDetails") if isinstance(item, dict) else None
        chat_id = details.get("activeLiveChatId") if isinstance(details, dict) else None
        if not chat_id:
            raise YouTubeError("No active live chat on this video (not live, or chat is off).")
        return chat_id

    def fetch_messages(self, chat_id, page_token=None):
        resp = self._execute(
            self._yt.liveChatMessages().list(
                liveChatId=chat_id,
                part="snippet,authorDetails",
                pageToken=page_token,
            )
        )

        messages = []
        for item in resp.get("items") or []:
            if not isinstance(item, dict) or not item.get("id"):
                continue
            messages.append(
                ChatMessage(
                    id=item["id"],
                    author=(item.get("authorDetails") or {}).get("displayName", "unknown"),
                    text=(item.get("snippet") or {}).get("displayMessage", ""),
                )
            )

        # YouTube tells us how long to wait; respecting it also saves API quota
        interval = max(resp.get("pollingIntervalMillis", 5000) / 1000, 2.0)
        return ChatPage(messages, resp.get("nextPageToken"), interval)

    # ---------- internal ----------

    def _execute(self, request):
        try:
            return request.execute(num_retries=3)  # retries 5xx / rate limits by itself
        except HttpError as e:
            raise self._convert_http_error(e) from e
        except (OSError, httplib2.HttpLib2Error) as e:
            raise YouTubeError("Network problem while talking to YouTube.", retryable=True) from e

    @staticmethod
    def _convert_http_error(e):
        status = e.resp.status
        body = e.content or b""

        if b"liveChatEnded" in body:
            return ChatEnded("The live chat has ended.")
        if b"ratelimitexceeded" in body.lower():
            return YouTubeError("YouTube asked us to slow down.", retryable=True)
        if status == 403 and b"quota" in body.lower():
            return YouTubeError("YouTube API quota is used up for today. Try again tomorrow.")
        if status in (400, 401, 403):
            return YouTubeError("YouTube rejected the request. Check your API key and its permissions.")
        if status == 404:
            return YouTubeError("Video or chat not found.")
        if status == 429 or status >= 500:
            return YouTubeError(f"YouTube is having problems (HTTP {status}).", retryable=True)
        return YouTubeError(f"YouTube error (HTTP {status}).")