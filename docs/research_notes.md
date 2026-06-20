# Research Notes

## June 2026

**Why I started this project:**
Honestly this started from just translating streams. You end up reading live chat for hours and after a while you start noticing the same stuff over and over — people asking for personal info, guessing who someone "really" is. Made me uncomfortable. Also made me wonder if that pattern could actually be caught automatically instead of just scrolled past.

**First technical challenge:**
YouTube Data API v3 docs. Took longer than expected to figure out live chat IDs specifically.

**June 6 — first time it actually worked:**
Connected to a live Japanese stream and the bot pulled real-time chat messages successfully. Handles Japanese characters fine, which I was kind of worried about. Next thing to build is actual detection — right now it just reads, doesn't flag anything yet.

**June 10 — Phase 2, detection engine:**
Got doxxing + hate speech detection working across three languages today (EN/RU/JP). Tested live and it correctly left normal messages alone — green checkmarks across the board. No false positives in this first run, which honestly surprised me a bit. Probably won't stay that clean once I test more streams.

**June 15 — Phase 3, coordination detection:**
Now flags when 3+ different accounts post the same message within 60 seconds. Spent way too long debugging this because of an indentation mistake — turns out Python really does care about every single space. Lesson learned. No coordinated spam showed up in testing, which is a good sign — means it's not just flagging normal repeated chat stuff like "www" or "がんばれー".

**Found a false positive — ナイス incident:**
Bot flagged "ナイス" (nice) as a coordinated attack because three people happened to type it within a minute of each other. Which, obviously, is just normal stream reaction behavior, not harassment.

Good catch though because it proves the obvious thing: matching identical text isn't enough on its own. Stuff to think about —
- positive vs negative context matters a lot
- some words are just common reactions and shouldn't count the same way
- is 3 accounts actually a meaningful threshold, or too sensitive?

Maybe a whitelist for common reaction words. Or only flag coordination when the message is negative/harmful to begin with, not just repeated.


**Fixed it — combined coordination with content analysis:**
Changed the logic so coordination only matters if the message 
is already flagged as harmful on its own. So "ナイス" x3 = ignored, 
but a doxxing attempt x3 = flagged hard. Feels like a more honest 
signal — coordination should amplify a real threat, not just 
catch any repeated phrase. Simple fix but makes the whole system 
noticeably less annoying.

**Hit a network error mid-run:**
Bot crashed with SSLEOFError after running fine for a while — 
basically just internet hiccup, not a real bug. But it made me 
realize the bot needs to survive small failures instead of dying 
completely, especially if it's meant to monitor a stream for 
hours. Added a try/except so it retries instead of crashing. 
Small fix but feels like the kind of thing that matters more in 
practice than in theory.

**Started actually logging data:**
Added a logger so every message — flagged or not — gets saved to a json file instead of just printing and disappearing. Sounds small but it's the difference between "I made a bot" and "I have something to actually analyze later."

Important — I'm NOT pushing the real data to GitHub. It's still other people's messages, even if the chat is technically public, and publishing it in a structured dataset feels like a different thing than someone scrolling past it live. Kind of funny/ironic considering the whole project is about protecting people's privacy online lol. Code stays public, the actual logged data stays local only.

**What's next:**
Want to run this across a bunch of different streams over the next couple weeks — Japanese for sure, English and Russian if I can find live ones with active chat. Trying to get enough real data that I can say something actually meaningful instead of just "it worked on one test stream once."