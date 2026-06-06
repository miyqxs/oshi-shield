# OshiShield 🛡️

> Real-time livestream moderation system to detect doxxing, coordinated harassment,
> and hate speech targeting anonymous content creators.

---

## The Problem

Anonymous content creators — artists, streamers, and performers who deliberately
choose to hide their identity — face a unique and growing threat online.

On platforms like YouTube Live, coordinated harassment campaigns can appear within
seconds. Fans attempt to leak personal information (doxxing), post real names,
share addresses, or flood chats with hate speech. Existing platform moderation
tools react slowly and were not designed with anonymous creators in mind.

I became aware of this problem through my own experience running a YouTube channel
translating Japanese livestreams for Russian and English-speaking audiences. 
Watching harassment unfold in real time — and seeing platforms fail to stop it —
made me want to build something better.

---

## What OshiShield Does

- **Connects** to YouTube Live Chat API and reads messages in real time
- **Detects** doxxing attempts using pattern recognition (phone numbers, addresses,
  personal identifiers)
- **Flags** hate speech using multilingual keyword detection (English, Russian, Japanese)
- **Identifies** coordinated harassment by tracking repeated messages across
  multiple accounts within a time window
- **Alerts** the streamer or moderator before harmful content spreads

---

## Project Status

🚧 **In active development** — started June 2025

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | YouTube API connection + message logging | 🔄 In progress |
| 2 | Doxxing pattern detection | ⏳ Planned |
| 2 | Hate speech detection (EN/RU/JP) | ⏳ Planned |
| 3 | Coordination detection | ⏳ Planned |
| 4 | Web dashboard | ⏳ Planned |

---

## Research Motivation

This project sits at the intersection of **information systems**, **online community
behavior**, and **digital privacy**. The core research question driving it:

> *Can we design automated systems that protect chosen anonymity at scale —
> detecting not just harmful content, but harmful patterns of behavior?*

Development notes and research thinking are documented in [`docs/research_notes.md`](docs/research_notes.md).

---

## Tech Stack

- Python 3.11+
- YouTube Data API v3
- `google-api-python-client`
- `colorama` (terminal display)
- Flask (web dashboard — Phase 4)

---

## Setup

```bash
git clone https://github.com/miyqxs/oshi-shield.git
cd oshi-shield
pip install -r requirements.txt
```

Add your YouTube Data API key to a `.env` file:
```
YOUTUBE_API_KEY=your_key_here
```

Then run:
```bash
python main.py --video-id YOUR_LIVE_VIDEO_ID
```

---

## About

Built by a multilingual developer and Japanese music community translator from
Kazakhstan, currently studying information technology.

Questions or collaboration: open an issue or reach out via GitHub.
