---
name: youtube-vs-spotify
description: Use when someone wants to compare their YouTube watching with their Spotify listening (which app they use for what, when, where they find artists, which artists live on one app), or has both a Google Takeout YouTube export and a Spotify data export and asks what the difference says about them.
---

# YouTube vs Spotify

Lines up a YouTube watch history and a Spotify listening history over the years both cover, and turns the differences into one scrolling page: who does the work each year, the hour-of-day split, which app finds artists first, which app "owns" each shared artist, artists that live on one app only, songs played on both, and a short read of what it says.

The script does every count and chart. You do three judgment calls: link artists whose names differ between apps, mark Spotify focus/sleep audio, and write the story. Every number in the story must come from `facts.md`.

Stdlib Python 3.9+. `$SKILL` is this skill's base directory (shown when the skill loads; for a manual install, `~/.claude/skills/youtube-vs-spotify`). Run scripts with `python3 -I`.


## Talking to the person

Many people running this aren't technical. In conversation, never mention files, JSON, scripts, folders or Python unless they ask: say "your YouTube history", "a few channels I need to sort", "your page". Decide the timezone (the computer's) and the work folder yourself and mention each in one plain line. Before the first script, check `python3 --version` (3.9+); if it's missing, the `start` skill has plain-language install steps. If they don't have their export yet, the `start` skill has step-by-step download instructions.

## 1. Get both exports

- **YouTube:** a Google Takeout zip with YouTube history, JSON preferred (takeout.google.com → Deselect all → YouTube and YouTube Music → only "history" → JSON). Usually `~/Downloads/takeout-*.zip`. Make sure it's the account they actually watch on.
- **Spotify:** `my_spotify_data.zip` from spotify.com/account/privacy. "Extended streaming history" covers the account's lifetime; "Account data" only the last 12 months, which shrinks the comparison to one year.

If the `spotify-story` skill already ran, its `labels.json` (`functional`, `not_functional`) uses the same format: copy it into this work folder. `youtube_channels` is extra and optional.

## 2. First pass

Use the machine's timezone unless they lived elsewhere (IANA name). Pick a work folder they can keep, e.g. `~/Documents/mustory/youtube-vs-spotify/` (created if missing; reruns overwrite outputs). Use the same flags every run.

```bash
python3 -I "$SKILL/scripts/compare.py" --youtube ~/Downloads/takeout-XXXX.zip --spotify ~/Downloads/my_spotify_data.zip --work ~/Documents/mustory/youtube-vs-spotify --tz Europe/Berlin
```

## 3. Aliases and labels, then re-run

**aliases.json.** Read `artists.tsv`: the top 120 artists on each side and their plays on the other app. A big artist with 0 (or almost 0) on the other side may be a spelling mismatch. Link the ones that are the same act under different names: Cyrillic vs Latin spelling, a band vs its frontman, "X - Topic" leftovers. Only link what you're sure of. A frontman's solo work is a separate artist unless the plays are clearly the band's songs.

```json
{ "names": { "Кино": "Kino", "Земфира": "Zemfira", "Beyonce": "Beyoncé" } }
```

Keys are the spelling to replace, values the name to show.

**labels.json.** Focus, sleep, meditation and noise audio on Spotify isn't music taste. Artists are left out automatically when most of their tracks look like focus or sleep audio; facts.md lists every artist left out, so check that line. Add `functional` for ones it missed and `not_functional` for real bands it caught. Then read `youtube_channels.tsv` (top channels and the share counted as music) and fix channels that are clearly music but under-counted (covers, live sessions, non-Latin titles) or not music at all: `youtube_channels` maps a channel to "Music" or any other topic.

```json
{ "functional": ["Deep Focus Lab"], "not_functional": ["The Slumber Club"],
  "youtube_channels": { "Someone's Covers Channel": "Music", "A Podcast Clips Channel": "Other" } }
```

Run step 2 again.

## 4. Write story.json

Read `facts.md`, then `references/story.md`, and write `story.json` in the work folder.

## 5. Render and fact-check

```bash
python3 -I "$SKILL/scripts/render.py" --work ~/Documents/mustory/youtube-vs-spotify
```

Every number of 10 or more in the story must appear in facts.md (artist and song names are skipped). If one doesn't, it lists it, writes nothing and exits with code 2. Correct it, or add it to `"derived"` with how you computed it. Render again until it prints "Fact check passed". The check proves a number exists in facts.md, not that it belongs to your sentence: quote the right line. It may also print a PAIRING CHECK: a sentence that puts a number next to an artist or song with no facts.md line holding both. That catches a number that changed but still exists elsewhere in facts.md. Check each one; it is a warning, and a correct sentence can stay.

## 6. Deliver

Publish `compare.html` with an Artifact tool if there is one (starts private; say only they can see it until they share), otherwise `open` it or give the path.

## Common mistakes

| Mistake | Fix |
|---|---|
| Comparing raw totals as if the units matched | A YouTube play is a video start; a Spotify listen is 30 s+. Compare shares and patterns, and say so once |
| "Found on YouTube first" read as lifetime | It's first inside the compared window. Artists already playing in the first 30 days are left out of discovery, since they were known before |
| YouTube titles written "Song - Artist" | They create fake artists; alias them to the real artist if they're big enough to matter |
| Linking artists by guess | Alias only clear matches; leave the rest split |
| A real band left out as focus audio | Check the "Left out as focus/sleep audio" line in facts.md and put it in `not_functional` |
| Only one export, or exports that don't overlap | The script stops; ask for the missing or a newer export |
