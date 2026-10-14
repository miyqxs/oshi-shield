import logging
import os
import sys
import threading

from colorama import Fore, Style, init
from dotenv import load_dotenv

from monitor import Monitor
from utils import setup_logging
from youtube_client import YouTubeClient, YouTubeError


def display_message(result):
    if result["flagged"]:
        print(f"{Fore.RED}🚨 FLAGGED{Style.RESET_ALL}")
        print(f"   {Fore.YELLOW}Author:{Style.RESET_ALL} {result['author']}")
        print(f"   {Fore.YELLOW}Message:{Style.RESET_ALL} {result['text']}")
        print(f"   {Fore.YELLOW}Reason:{Style.RESET_ALL} {', '.join(result['reasons'])}")
        print()
    else:
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} {result['author']}: {result['text']}")


def main():
    init()  # colorama
    load_dotenv()
    setup_logging(logging.WARNING)  # keep the terminal clean; full log goes to logs/

    video_id = input("Enter YouTube live video ID: ").strip()
    if not video_id:
        print("No video ID given.")
        return

    try:
        client = YouTubeClient(os.getenv("YOUTUBE_API_KEY"))
        monitor = Monitor(client, video_id, on_result=display_message)
        print("Connecting to livestream...")
        monitor.run(threading.Event())
    except YouTubeError as e:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()