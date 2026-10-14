import logging
import threading

from coordinator import CoordinationDetector
from detector import analyze_message
from storage import save_message
from youtube_client import ChatEnded, YouTubeClient, YouTubeError

log = logging.getLogger(__name__)

RETRY_DELAY = 5


class Monitor:
    def __init__(self, client: YouTubeClient, video_id, on_result=None):
        self.client = client
        self.video_id = video_id
        self.on_result = on_result  # optional callback, e.g. the terminal printer
        self.seen_ids = set()
        self.coordinator = CoordinationDetector(time_window_seconds=60, threshold=3)

    def analyze(self, msg):
        result = analyze_message(msg.author, msg.text)
        coordinated, count = self.coordinator.add_and_check(
            msg.author, msg.text, is_harmful=result["flagged"]
        )
        if coordinated:
            result["flagged"] = True
            result["reasons"].append(f"Coordinated attack: {count} accounts same message")
        return result

    def handle_message(self, msg):
        if msg.id in self.seen_ids:
            return
        self.seen_ids.add(msg.id)

        result = self.analyze(msg)
        save_message(result, self.video_id)
        if self.on_result:
            self.on_result(result)

    def run(self, stop: threading.Event):
        """Blocks until stop is set or the chat ends. Raises YouTubeError on fatal problems."""
        chat_id = self.client.get_live_chat_id(self.video_id)
        log.info("Connected to live chat for video %s", self.video_id)

        page_token = None
        while not stop.is_set():
            try:
                page = self.client.fetch_messages(chat_id, page_token)
            except ChatEnded:
                log.info("Live chat ended, stopping.")
                return
            except YouTubeError as e:
                if not e.retryable:
                    raise
                log.warning("%s Retrying in %ss...", e, RETRY_DELAY)
                stop.wait(RETRY_DELAY)
                continue

            page_token = page.next_page_token
            for msg in page.messages:
                self.handle_message(msg)
            stop.wait(page.poll_interval)