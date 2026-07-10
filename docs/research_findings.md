# OshiShield — Research Findings
*June–July 2026*

---

## 1. What I was trying to figure out

Anonymous content creators — VTubers, utaite, indie artists — 
choose to hide their identity for a reason. Their talent should 
speak for itself, not their face or their name. But online 
communities don't always respect that choice. People leak real 
names, post addresses, try to "unmask" creators who explicitly 
asked not to be found.

I wanted to know two things: can a bot actually catch this kind 
of harassment automatically, in real time, across multiple 
languages? And more importantly — what does it get wrong?

This document covers what I found after monitoring 6,473 messages 
across 16 YouTube livestreams in June–July 2026.

---

## 2. How the bot works

OshiShield connects to YouTube's Live Chat API and reads messages 
as they appear in real time. Every message goes through three 
checks:

**Doxxing detection** — looks for patterns associated with leaking 
personal information: phone numbers, email addresses, physical 
addresses, and phrases like "real name is" or "found their address." 
Also checks for Japanese terms specifically used in deanonymization 
attempts (本名, 住所, 特定した).

**Hate speech detection** — keyword matching across three languages. 
English, Russian, and Japanese lists were built separately because 
harassment culture differs between communities — what counts as 
an attack in one language might be a normal expression in another.

**Coordination detection** — tracks when 3+ different accounts 
post the same message within 60 seconds. Real harassment campaigns 
rarely come from one person; they come from pile-ons.

Everything gets logged locally to a JSON file for analysis. 
Raw message data stays off GitHub for privacy reasons — only 
the code and findings are public.

---

## 3. What I collected

| Metric | Number |
|--------|--------|
| Total messages | 6,473 |
| Streams monitored | 16 |
| Flagged messages | 5 (0.077%) |
| Genuine harassment detected | 0 |
| False positives | 5 |

Streams were mostly Japanese — VTubers (NIJISANJI), utaite, 
music livestreams. One large stream (Lauren Iroas, NIJISANJI) 
accounted for 2,645 messages alone, roughly 40% of the dataset.

---

## 4. What actually happened

Short answer: nothing. In 6,473 messages, the bot found zero 
genuine harassment attempts.

All 5 false positives were triggered by "Doxxing pattern 
detected" — not hate speech as initially assumed. The actual 
culprits were 嫌い (dislike) and 下手くそ (roughly "you suck") 
which had been incorrectly placed in the doxxing pattern list 
rather than hate speech keywords. Neither word has anything 
to do with leaking personal information.

This revealed a classification error in the initial keyword 
categorization — words were assigned to wrong categories 
without enough consideration of what doxxing actually means 
in Japanese context.

---

## 5. What this actually means

The zero genuine detections could mean a few things:

One — these communities are genuinely well-moderated. Japanese 
VTuber and music fandoms tend to have strong community norms 
around respecting creators. Harassment might happen but not in 
the open live chat.

Two — real harassment is more subtle than keyword matching can 
catch. Actual deanonymization attempts probably use coded 
language, inside references, or get deleted before the API 
even returns them.

Three — the bot needs smarter detection. Pattern matching works 
for obvious cases, but the false positives show it breaks badly 
on nuance — especially in Japanese where context changes meaning 
completely.

The most important finding isn't "harassment exists" or "it 
doesn't." It's that **protecting anonymity requires understanding 
intent, not just surface patterns.** A system that flags 
"ローレン" as doxxing doesn't understand what anonymity actually 
means — the difference between a public persona and a private 
identity.

---

## 6. What the bot gets wrong (and why it matters)

Both false positive types point to the same root problem: 
context blindness.

The doxxing detector doesn't know the difference between:
- A creator's public streaming name (ローレン = Lauren Iroas, VTuber)
- Someone's real private name being leaked

The hate speech detector doesn't know the difference between:
- 嫌い as genuine hatred directed at someone
- 嫌い as part of a compound word meaning something unrelated

Fixing this properly would require the bot to understand who 
is being talked about, in what context, with what intent. 
That's a much harder problem than pattern matching — it's 
closer to natural language understanding.

---

## 7. What I'd build next

A whitelist of known VTuber/utaite public names so the bot 
doesn't flag creators' own communities for mentioning them.

Context-aware Japanese processing — checking what comes before 
and after 嫌い instead of just flagging the word alone.

Sentiment analysis layer — only flag coordination when the 
repeated message is negative, not just any repeated phrase 
(this would have prevented the ナイス false positive from 
earlier testing).

Longer-term: training a proper classifier on labeled data 
instead of keyword lists. But that needs way more data than 
6,473 messages.

---

## 8. Honest limitations

- Dataset is small and not diverse enough — 16 streams, mostly 
  Japanese music/VTuber content
- No ground truth — I can't verify whether genuine harassment 
  happened and just wasn't caught
- Keyword lists were built by one person (me) and reflect my 
  knowledge of these communities — definitely incomplete
- The bot only sees messages the API returns, which may already 
  be filtered by YouTube's own moderation

---

*Full development notes in [`docs/research_notes.md`](research_notes.md)*
*Code: [`github.com/miyqxs/oshi-shield`](https://github.com/miyqxs/oshi-shield)*