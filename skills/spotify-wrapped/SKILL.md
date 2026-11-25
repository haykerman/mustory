---
name: spotify-wrapped
description: Use when someone wants a Spotify Wrapped–style story, recap, personality read or deep stats of their own Spotify listening history, or has a Spotify data export (my_spotify_data.zip, Streaming_History_Audio_*.json, StreamingHistory_music_*.json) and wants to explore it, including outside Spotify's own Wrapped season.
---

# Spotify Wrapped

Turns a Spotify personal-data export into a long, scrolling, Wrapped-style page that goes past Spotify's own: real lifetime totals, eras, loops, the skip button, autopilot vs songs picked on purpose, focus and sleep audio, devices, travel, discovery, taste drift, marathons, rituals and a personality read.

Scripts do every count and draw every chart. You do what needs judgment: mark focus and sleep audio, tag moods, and write the story. Every number in the story must come from `facts.md`.

All scripts are stdlib Python 3.9+. `$SKILL` below is the folder this SKILL.md is in (usually `~/.claude/skills/spotify-wrapped`). Run them with `python3 -I` from any folder.

## 1. Get the export

Look for `my_spotify_data.zip` in `~/Downloads`, or ask for the path. The zip can be either package:

| Package | What it has | Chapters |
|---|---|---|
| **Extended streaming history** (best) | Every stream for the account's lifetime: end time, ms played, why it started/ended, shuffle, skip, offline, private session, device, country | All |
| **Account data** | Only the last 12 months: end time, artist, track, ms played | Skips are estimated (under 30 s); autopilot, shuffle, devices and travel hide themselves |

If there is no export, give these steps: open spotify.com/account/privacy while signed in → tick **Extended streaming history** (untick the others unless they want them) → **Request data** → confirm the email. Spotify says it can take up to 30 days; it is often a few days. Then download `my_spotify_data.zip`.

## 2. Timezone and work folder

Spotify stores UTC. Use the machine's zone unless they say they lived elsewhere; ask "Which city were you in for most of these years?" if unsure, and pass an IANA name. Streams abroad are still shown in that zone (the footer says so). `--southern` flips seasons.

Pick a work folder they can keep, e.g. `~/spotify-wrapped/` (the script creates it; an existing one is fine, outputs are overwritten). Use the same flags on every run. The export holds IP addresses and private-session plays: the scripts never keep IPs, and the page never lists private-session tracks. Keep everything local and don't web-search their tracks.

"Today" defaults to now; pass `--today YYYY-MM-DD` only to reproduce a run.

## 3. First pass

```bash
python3 -I "$SKILL/scripts/analyze.py" --export ~/Downloads/my_spotify_data.zip --work ~/spotify-wrapped --tz Europe/Berlin
```

## 4. Mark focus audio and moods, then re-run

**labels.json.** Read `artists.tsv` (top 200 artists by hours, with an automatic focus/sleep guess from track names). Focus, sleep, meditation, white-noise and study-beats artists distort "favorite artist" lists, so mark them:

```json
{ "functional": ["Deep Focus Lab", "Rain Sounds for Sleep"],
  "not_functional": ["Sleep Token"] }
```

Artists are left out automatically when most of their tracks, from 2+ different titles, look like focus or sleep audio. facts.md lists everyone left out ("Left out of taste sections"): check it, add `functional` for misses and `not_functional` for real bands it caught.

**moods.json.** Pick up to four moods that describe *their* music and tag the artists you can place, ideally 100+ (moods are weighted by hours):

```json
{ "moods": ["Melancholy", "Heavy", "Pop & R&B", "Night drive"],
  "artists": { "Radiohead": "Melancholy", "Rammstein": "Heavy" } }
```

Run step 3 again.

## 5. Write story.json

Read all of `facts.md` and `odd_candidates.tsv`, then `references/story.md`, and write `story.json` in the work folder.

## 6. Render and fact-check

```bash
python3 -I "$SKILL/scripts/render.py" --work ~/spotify-wrapped
```

It checks every number of 10 or more in the story against facts.md (song, artist and album names are skipped). If one is missing it lists it, writes nothing, and exits with code 2. Correct it from facts.md, or, if you computed it from facts.md numbers, add it to `"derived"` in story.json with how. Render again until it prints "Fact check passed". It may also print a PAIRING CHECK: a sentence that puts a number next to an artist or song with no facts.md line holding both. That catches a number that changed but still exists elsewhere in facts.md. Check each one; it is a warning, and a correct sentence can stay.

## 7. Deliver

- With an Artifact/publish tool: publish `wrapped.html` (starts private) and give the link; say only they can see it until they share it.
- Otherwise `open ~/spotify-wrapped/wrapped.html` or give the path.

## Common mistakes

| Mistake | Fix |
|---|---|
| Summing `ms_played` for hours | Use facts.md hours: overlaps between devices and runaway streams are already removed |
| Calling a 60-hour session a listening marathon | One artist for 20+ hours is a loop left running; say so |
| Focus/sleep audio as the "favorite artist" | Mark it `functional`. Songs, albums, loops, eras, seasons, flings, gateways, rituals, drift and the soundtrack then leave it out; totals, hours and the top-artist list keep it (say so in the callout) |
| Listing private-session tracks or guessing trip purposes | Count only; countries and dates only |
| Writing "you skipped 48%" without saying of what | Say "of streams" (every start) vs "of listens" (30 s+) |
| Trusting the fact check for meaning | It proves a number exists in facts.md, not that it belongs to your sentence. Quote the line the claim comes from |
| A loop vs a playlist on repeat | "Loops" are one song back to back. A few songs cycling for hours (all "previous song ended") is a playlist left running; it shows up in Marathons |
| An Account-data export with "lifetime" claims | It covers 12 months; say so in the hero |
