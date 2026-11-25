---
name: start
description: Use when someone wants a Wrapped-style story or stats of their YouTube or Spotify history but hasn't said which, doesn't have their data yet, or asks how mustory works, what it needs, or how to download their YouTube or Spotify data.
---

# mustory: getting started

mustory turns someone's own YouTube and Spotify history into a story page, the way Spotify Wrapped does, for any span of years. This skill is the front door for people who aren't technical: find out what they want, get their data, then hand over to the right skill.

## How to talk

Write like a helpful friend, not a developer. Never mention file names, JSON, scripts, folders, Python or terminals unless they ask. Say "your YouTube history" and "your Spotify data", not "the Takeout zip". Ask one question at a time, and only when you can't decide yourself. Pick sensible defaults and say them in one line.

## 1. What do they want?

| They want | Data needed | Then use skill |
|---|---|---|
| A story of their YouTube watching | YouTube history from Google Takeout | `youtube-wrapped` |
| A story of their Spotify listening | Spotify data download | `spotify-wrapped` |
| How their YouTube and Spotify habits differ | Both | `youtube-vs-spotify` |

If they're unsure, offer the one whose data they already have.

## 2. Do they have the data?

Look in their Downloads folder for `takeout-*.zip` (YouTube) and `my_spotify_data.zip` (Spotify) before asking. If you find it, say what you found ("I found your Spotify download from 24 November") and continue.

If not, give the steps below as a short numbered list, and tell them to come back when the email arrives. Waiting is normal: Google usually takes minutes to hours, Spotify a few days.

**YouTube (Google Takeout):**
1. Go to takeout.google.com, signed in to the Google account you watch YouTube on.
2. Click **Deselect all** near the top.
3. Scroll to **YouTube and YouTube Music** and tick it.
4. Click **All YouTube data included**, click **Deselect all** in that window, tick only **history**, then **OK**.
5. Click **Multiple formats**, set **history** to **JSON**, then **OK**.
6. Scroll down, click **Next step**, then **Create export**.
7. When the email arrives, download the file. Leave it in Downloads.

**Spotify:**
1. Go to spotify.com/account/privacy and log in.
2. Under "Download your data", tick **Extended streaming history** (this one has every song since the account began). Untick the others unless they want them.
3. Click **Request data**, then confirm in the email Spotify sends.
4. When the "your data is ready" email arrives (often a few days), download `my_spotify_data.zip`. Leave it in Downloads.

If they only want something quick, the "Account data" package works too, but covers only the last 12 months.

## 3. Check the computer can run it

Run `python3 --version`. Anything 3.9 or newer is fine. If it's missing or older, say it plainly: "Your computer needs a free tool called Python before I can build this." On a Mac or Windows, send them to python.org/downloads, tell them to click the big yellow download button and run the installer with the default options (on Windows, tick "Add python.exe to PATH" first), then come back. Don't suggest Homebrew, conda or a terminal.

## 4. Hand over

Load the matching skill and follow it. Keep its technical steps to yourself, and only surface choices that are really theirs. The other skills use the same tone.
