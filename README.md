# OshiShield 🛡️

A real-time bot that monitors YouTube live chats and tries to catch doxxing 
attempts, harassment, and hate speech before they spread — built specifically 
with anonymous content creators in mind.

---

## Why I'm building this

Artists and streamers who choose to stay anonymous — utaite, vtubers, indie 
musicians — deal with a weird kind of harassment that most moderation tools 
just weren't built for. People try to leak their real names, find their 
addresses, post personal info in chat, sometimes within seconds of a stream 
starting. And it's often not even one person doing it — it's a bunch of 
accounts piling on at once.

I noticed this firsthand running a YouTube channel where I translate Japanese 
livestreams for Russian and English-speaking fans. Spending hours in live 
chats, you start seeing the same harassment patterns over and over. Platforms 
mostly just don't catch it fast enough, or at all. So I started building 
something that could.

---

## What it actually does right now

- Connects to YouTube Live Chat and reads messages as they come in
- Flags doxxing attempts (phone numbers, addresses, "found their real name" type stuff)
- Catches hate speech in English, Russian, and Japanese
- Detects when multiple accounts post the same harmful message at once — basically catching coordinated pile-ons, not just one rude comment
- Logs everything locally so I can actually go back and study what gets flagged

---

## Where it's at

🚧 still actively building this, started June 2026

| Phase | What | Status |
|-------|------|--------|
| 1 | Connect to YouTube API, read live chat | ✅ done |
| 2 | Doxxing detection | ✅ done |
| 3 | Hate speech detection (EN/RU/JP) | ✅ done |
| 4 | Coordination detection | ✅ done |
| 5 | Logging data for research | ✅ done |
| 6 | Web dashboard | ⏳ working on it |

---

## The bigger question I'm actually trying to answer

This isn't just "make a moderation bot." What I actually care about is:

> can you build something that protects people's chosen anonymity, by catching 
> *patterns* of bad behavior, not just bad words?

I'm keeping track of what I learn (and what breaks, and what I get wrong) in 
[`docs/research_notes.md`](docs/research_notes.md) — it's pretty unfiltered, 
basically my actual thought process as I build this.

---

## Built with

- Python 3.11+
- YouTube Data API v3
- `google-api-python-client`
- `colorama` for the terminal output
- Flask (coming soon, for the dashboard)

---

## Running it yourself

```bash
git clone https://github.com/miyqxs/oshi-shield.git
cd oshi-shield
pip install -r requirements.txt
```

Make a `.env` file and drop your YouTube API key in:
```bash
YOUTUBE_API_KEY=your_key_here
```
Then:
```bash
python main.py
```

It'll ask for a live video ID and start monitoring.

---

## About me

Kazakh student, speak 5 languages, run a YouTube channel translating Japanese 
livestreams (mostly Ado content, mostly). Got into coding because I wanted 
to actually solve this problem, not just watch it happen.

Feel free to open an issue if you find bugs or have ideas.