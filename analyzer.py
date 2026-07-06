import json
from collections import Counter

def load_data():
    with open('data/chat_log.json', encoding='utf-8') as f:
        return json.load(f)

def analyze(data):
    total = len(data)
    flagged = [m for m in data if m['flagged']]
    
    # Messages per video
    videos = Counter(m['video_id'] for m in data)
    
    # Flag reasons
    all_reasons = []
    for m in flagged:
        all_reasons.extend(m['reasons'])
    reasons = Counter(all_reasons)
    
    print(f"Total messages: {total}")
    print(f"Flagged: {len(flagged)} ({len(flagged)/total*100:.1f}%)")
    print(f"Clean: {total - len(flagged)}")
    print(f"\nStreams monitored: {len(videos)}")
    for vid, count in videos.most_common():
        print(f"  {vid}: {count} messages")
    
    if reasons:
        print(f"\nFlag reasons:")
        for reason, count in reasons.most_common():
            print(f"  {reason}: {count}")
    else:
        print(f"\nNo flags triggered — community appears clean")

if __name__ == "__main__":
    data = load_data()
    analyze(data)