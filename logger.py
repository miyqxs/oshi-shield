import json
import os
from datetime import datetime

LOG_FILE = "data/chat_log.json"

def ensure_data_folder():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def log_message(result, video_id):
    ensure_data_folder()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "video_id": video_id,
        "author": result["author"],
        "text": result["text"],
        "flagged": result["flagged"],
        "reasons": result["reasons"]
    }
    
    # Read existing data safely
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []
    
    data.append(entry)
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)