import os
import time
from dotenv import load_dotenv
from googleapiclient.discovery import build
from colorama import Fore, Style, init
from detector import analyze_message

init()  # Start colorama

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_live_chat_id(video_id):
    response = youtube.videos().list(
        part="liveStreamingDetails",
        id=video_id
    ).execute()
    if not response["items"]:
        print("Video not found or not a livestream")
        return None
    details = response["items"][0].get("liveStreamingDetails", {})
    return details.get("activeLiveChatId")

def get_chat_messages(live_chat_id):
    response = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part="snippet,authorDetails"
    ).execute()
    return response.get("items", [])

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
    video_id = input("Enter YouTube live video ID: ")
    print("Connecting to livestream...")
    
    chat_id = get_live_chat_id(video_id)
    if not chat_id:
        print("Could not find active live chat.")
        return

    print(f"Connected! Monitoring for harmful content...\n")
    seen_ids = set()

    while True:
        messages = get_chat_messages(chat_id)
        for msg in messages:
            msg_id = msg["id"]
            if msg_id not in seen_ids:
                seen_ids.add(msg_id)
                author = msg["authorDetails"]["displayName"]
                text = msg["snippet"]["displayMessage"]
                result = analyze_message(author, text)
                display_message(result)
        time.sleep(5)

if __name__ == "__main__":
    main()