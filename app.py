import logging
import os
import threading
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from analyzer import compute_stats
from monitor import Monitor
from utils import BASE_DIR, load_data, setup_logging
from youtube_client import YouTubeClient, YouTubeError

log = logging.getLogger(__name__)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
stop_event = threading.Event()


def run_monitor(video_id):
    try:
        client = YouTubeClient(os.getenv("YOUTUBE_API_KEY"))
        Monitor(client, video_id).run(stop_event)
    except YouTubeError as e:
        log.error("Monitor stopped: %s", e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    load_dotenv()

    thread = None
    video_id = os.getenv("VIDEO_ID")  # optional: set it in .env to monitor from the dashboard
    if video_id:
        # googleapiclient is blocking, so it gets its own thread and never blocks FastAPI
        thread = threading.Thread(target=run_monitor, args=(video_id,), daemon=True)
        thread.start()
    else:
        log.info("VIDEO_ID not set: dashboard only (no live monitoring)")

    yield

    stop_event.set()
    if thread:
        thread.join(timeout=10)


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/api/messages")
def messages():
    # last 100, newest first
    return load_data()[-100:][::-1]


@app.get("/api/stats")
def stats():
    return compute_stats(load_data())