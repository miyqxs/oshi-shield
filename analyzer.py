from collections import Counter

from utils import load_data


def compute_stats(data):
    flagged = [m for m in data if m.get("flagged")]
    videos = Counter(m.get("video_id", "unknown") for m in data)
    reasons = Counter(r for m in flagged for r in m.get("reasons", []))

    return {
        "total": len(data),
        "flagged": len(flagged),
        "clean": len(data) - len(flagged),
        "streams": len(videos),
        "videos": dict(videos.most_common()),
        "reasons": dict(reasons.most_common()),
    }


def print_report(stats):
    total = stats["total"]
    flagged = stats["flagged"]
    clean = stats["clean"]
    percent = flagged / total * 100 if total else 0.0

    print(f"Total messages: {total}")
    print(f"Flagged: {flagged} ({percent:.1f}%)")
    print(f"Clean: {clean}")

    print(f"\nStreams monitored: {stats['streams']}")
    for video_id, count in stats["videos"].items():
        print(f"  {video_id}: {count} messages")

    if stats["reasons"]:
        print("\nFlag reasons:")
        for reason, count in stats["reasons"].items():
            print(f"  {reason}: {count}")
    else:
        print("\nNo flags triggered — community appears clean")


if __name__ == "__main__":
    print_report(compute_stats(load_data()))