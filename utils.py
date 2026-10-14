import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "chat_log.json"

log = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    """Call once at startup (main.py / app.py)."""
    (BASE_DIR / "logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                BASE_DIR / "logs" / "oshishield.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
            ),
        ],
    )


def load_data():
    """Read the chat log. Always returns a list, never raises."""
    try:
        with DATA_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        log.warning("%s is corrupted, treating it as empty", DATA_FILE)
        return []
    return data if isinstance(data, list) else []