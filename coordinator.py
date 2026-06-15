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
    
    def add_and_check(self, author, text):
        now = datetime.now()
        
        # Add new message
        self.messages.append({
            "author": author,
            "text": text.lower().strip(),
            "time": now
        })
        
        # Clean messages outside time window
        cutoff = now - self.time_window
        self.messages = [m for m in self.messages if m["time"] > cutoff]
        
        # Count unique authors sending same message
        text_clean = text.lower().strip()
        matching_authors = set(
            m["author"] for m in self.messages 
            if m["text"] == text_clean
        )
        
        if len(matching_authors) >= self.threshold:
            return True, len(matching_authors)
        return False, 0