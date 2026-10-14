import json
import os
import threading
from datetime import datetime

from utils import DATA_FILE, load_data

# the monitor thread writes while the dashboard reads
_lock = threading.Lock()


def save_message(result, video_id):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "video_id": video_id,
        "author": result["author"],
        "text": result["text"],
        "flagged": result["flagged"],
        "reasons": result["reasons"],
    }

    with _lock:
        data = load_data()
        data.append(entry)

        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = DATA_FILE.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, DATA_FILE)  # atomic: a reader never sees a half-written file