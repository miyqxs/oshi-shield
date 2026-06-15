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

**June 10, 2026 — Phase 2:**
Built the actual detection engine today. It now flags doxxing 
patterns and hate speech in real time across three languages — 
English, Russian, and Japanese. Tested it on a live Japanese 
stream and it correctly showed green checkmarks for normal 
messages. No false positives yet which is honestly surprising.

**June 15, 2026 — Phase 3: Coordination detection running:**
Bot now detects coordinated attacks — when 3+ different 
accounts send the same message within 60 seconds it gets 
flagged. Hardest part was getting the indentation right in 
Python (tabs matter a lot). No coordinated attacks in the 
test stream which is actually good — means the detector isn't 
producing false positives on normal chat repetition like 
"www" or "がんばれー". 

**False positive discovered — June 2026:**
Bot flagged "ナイス" (nice) as a coordinated attack because 
3 accounts sent it within 60 seconds. This is completely 
normal fan reaction behavior — someone does something cool 
and everyone reacts simultaneously.

This shows that identical-message detection alone isn't 
smart enough. Real coordination detection needs to consider:
- Is the word positive or negative in context?
- Is this a common reaction word?
- How many accounts is "too many"? 3 might be too low.

Possible solution: whitelist common reaction words, or raise 
threshold to 5+ accounts. Or combine with sentiment — only 
flag coordinated NEGATIVE messages.
