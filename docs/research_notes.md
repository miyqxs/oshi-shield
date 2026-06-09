# Research Notes

## June 2026
**Why I started this project:**
Translating streams meant spending hours reading live chats. Even in relatively calm communities, I noticed recurring patterns — users asking for personal details, speculative 
comments about creators' real identities. It made me uncomfortable and curious about whether this could be detected automatically.

**First technical challenge:**
Getting familiar with the YouTube Data API v3 documentation.

**June 6, 2026 — First successful test:**
Connected to a live Japanese YouTube stream and successfully 
read real-time chat messages. Bot correctly handles Japanese 
characters. Next step: add detection engine to flag harmful 
content patterns.

**June 9, 2026 — Phase 2 done:**
Built the actual detection engine today. It now flags doxxing 
patterns and hate speech in real time across three languages — 
English, Russian, and Japanese. Tested it on a live Japanese 
stream and it correctly showed green checkmarks for normal 
messages. No false positives yet which is honestly surprising.

