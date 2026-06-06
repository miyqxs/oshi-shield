import os
import time
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
print(f"API Key loaded: {API_KEY[:10] if API_KEY else 'NOT FOUND'}")

# Connect to YouTube
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_live_chat_id(video_id):
    """Get the live chat ID from a YouTube video ID"""
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
    """Fetch messages from live chat"""
    response = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part="snippet,authorDetails"
    ).execute()
    return response.get("items", [])

def main():
    video_id = input("Enter YouTube live video ID: ")
    
    print(f"Connecting to livestream...")
    chat_id = get_live_chat_id(video_id)
    
    if not chat_id:
        print("Could not find active live chat.")
        return
    
    print(f"Connected! Reading messages...\n")
    
    while True:
        messages = get_chat_messages(chat_id)
        for msg in messages:
            author = msg["authorDetails"]["displayName"]
            text = msg["snippet"]["displayMessage"]
            print(f"{author}: {text}")
        
        time.sleep(5)  # Wait 5 seconds before fetching again

if __name__ == "__main__":
    main()