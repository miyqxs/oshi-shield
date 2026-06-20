from collections import defaultdict
from datetime import datetime, timedelta

class CoordinationDetector:
    """
    Detects when multiple different accounts send the same
    or very similar messages within a short time window.
    """
    
    def __init__(self, time_window_seconds=60, threshold=3):
        self.messages = []
        self.time_window = timedelta(seconds=time_window_seconds)
        self.threshold = threshold  # how many accounts = coordinated
    
    def add_and_check(self, author, text, is_harmful=False):
        now = datetime.now()
        
        self.messages.append({
            "author": author,
            "text": text.lower().strip(),
            "time": now,
            "harmful": is_harmful
        })
        
        cutoff = now - self.time_window
        self.messages = [m for m in self.messages if m["time"] > cutoff]
        
        text_clean = text.lower().strip()
        matching = [m for m in self.messages if m["text"] == text_clean]
        matching_authors = set(m["author"] for m in matching)
        
        # Only flag if it's coordinated AND the content itself is harmful
        if len(matching_authors) >= self.threshold and is_harmful:
            return True, len(matching_authors)
        return False, 0