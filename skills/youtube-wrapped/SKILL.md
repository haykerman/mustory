---
name: youtube-wrapped
description: Use when someone wants a Spotify Wrapped–style story, recap, year-in-review or personality read of their YouTube watch history, or has a Google Takeout YouTube export (takeout-*.zip, watch-history.json or watch-history.html) and wants to explore what they watched, their obsessions, forgotten favorites or how their taste changed.
---

# YouTube Wrapped

Turns a Google Takeout YouTube history export into a long, scrolling, Wrapped-style page: eras, dedications, forgotten favorites, seasons, night-owl hours, rabbit holes, rituals, odd watches and a personality read, all built from the person's own data.

Scripts do every count and draw every chart. You do the three things that need judgment: label their channels, tag their artists' moods, and write the story. Every number in the story must come from `facts.md`.

All scripts are stdlib Python 3.9+. In the commands below, `$SKILL` is this skill's base directory (shown when the skill loads; for a manual install, `~/.claude/skills/youtube-wrapped`). Run them with `python3 -I` from any folder.


## Talking to the person

Many people running this aren't technical. In conversation, never mention files, JSON, scripts, folders or Python unless they ask: say "your YouTube history", "a few channels I need to sort", "your page". Decide the timezone (the computer's) and the work folder yourself and mention each in one plain line. Before the first script, check `python3 --version` (3.9+); if it's missing, the `start` skill has plain-language install steps. If they don't have their export yet, the `start` skill has step-by-step download instructions.

## 1. Get the export

Look for the newest `takeout-*.zip` in `~/Downloads`, or ask for the path. If there is none, give these steps:

1. Open takeout.google.com while signed in to **the account they actually watch on** (a common mistake is exporting a second account with a few hundred plays).
2. **Deselect all**, tick **YouTube and YouTube Music**.
3. **All YouTube data included** → keep only **history**. **Multiple formats** → history: **JSON**.
4. Export, wait for the email, download the zip.

HTML exports work only in English. If `analyze.py` says it can't read dates, ask for a JSON export.

## 2. Choose the timezone and a work folder

Times are shown in one zone. Use the machine's zone unless they say they lived somewhere else; ask "Which city were you in for most of these years?" if unsure, and pass an IANA name (`Europe/Berlin`). Add `--southern` for southern-hemisphere seasons.

Pick a work folder they can keep, e.g. `~/Documents/mustory/youtube-wrapped/` (the script creates it). Their history is private: keep everything local, and don't paste titles into web searches.

"Today" defaults to now in that zone. It sets "On this day" and what counts as forgotten (no plays in 18 months); pass `--today YYYY-MM-DD` only to reproduce an earlier run.

## 3. First pass

```bash
python3 -I "$SKILL/scripts/analyze.py" --export ~/Downloads/takeout-XXXX.zip --work ~/Documents/mustory/youtube-wrapped --tz Europe/Berlin
```

It prints the play count and the unclassified share ("Other" plus "…-language other").

## 4. Label channels and moods, then re-run

**labels.json.** Read `to_label.tsv` (top 300 channels, sample titles, current guess). Give a topic to every channel whose guess is wrong or vague ("Other", "…-language other", a news channel guessed as Music).

Built-in topics, applied by keyword to every channel you don't label: Music, Gaming, Programming, Tech, News & politics, Comedy & entertainment, Science & learning, Playing music, Sports, Food, Fitness & health, "<script>-language other", Other. Reuse these names where they fit, so labeled and unlabeled channels land in the same bucket. Add a new topic only for a real cluster in *this* person's history ("Armenian news & politics", "League of Legends"). To rename a built-in everywhere, use `rename`. Aim for 10–16 topics in total.

`quests` are hobbies they learn, as a case-insensitive regex matched against **video titles only**. Defaults: Guitar, Piano, Singing, Drawing, Languages, Cooking, Fitness, Driving test, Coding tutorials, Home & DIY, Chess. A quest with a default's name replaces that default.

```json
{ "channels": { "Marques Brownlee": "Tech", "City Evening News": "Local news & politics" },
  "rename": { "Tech": "Tech reviews" },
  "quests": { "Ukulele": "ukulele", "Pottery": "pottery|wheel throwing" } }
```

**moods.json.** Read `artists.tsv` (top 150 artists). Pick up to four moods that describe *their* music (the defaults "Melancholy", "Heavy", "Pop & R&B", "Night drive" fit many people; swap them if their taste is K-pop, classical, hip-hop…), then tag the artists you can place, ideally 100+.

```json
{ "moods": ["Melancholy", "Heavy", "Pop & R&B", "Night drive"],
  "artists": { "Radiohead": "Melancholy", "Rammstein": "Heavy" } }
```

Run step 3 again. The unclassified share should drop by several points. What's left is the long tail of channels watched once or twice, which is fine.

## 5. Write story.json

Read all of `facts.md` and `odd_candidates.tsv`, then read `references/story.md` and write `story.json` in the work folder. It describes every key, the voice, and what each chapter needs.

## 6. Render and fact-check

```bash
python3 -I "$SKILL/scripts/render.py" --work ~/Documents/mustory/youtube-wrapped
```

It checks every number of 10 or more in the story against facts.md. Video titles and clock times are skipped. If a number is missing, it lists it, writes nothing, and exits with code 2. Correct the number from facts.md. If you computed it from facts.md numbers (a sum, a difference), add it to `"derived": {"745": "Feb+Mar+Apr+May Eurovision plays"}` in story.json. Render again until it prints "Fact check passed". Write numbers of 10 or more as digits, not words, so they get checked. It may also print a PAIRING CHECK: a sentence that puts a number next to an artist or song with no facts.md line holding both. That catches a number that changed but still exists elsewhere in facts.md. Check each one; it is a warning, and a correct sentence can stay.

## 7. Deliver

- If you have an Artifact/publish tool, publish `wrapped.html` (it starts private) and give them the link. Tell them only they can see it until they share it.
- Otherwise run `open ~/Documents/mustory/youtube-wrapped/wrapped.html` (macOS) or give them the path.

Offer the optional database for follow-up questions ("what was I watching the week I moved?"):

```bash
python3 -I "$SKILL/scripts/build_db.py" --export <zip> --work ~/Documents/mustory/youtube-wrapped --tz Europe/Berlin
```

Then answer questions with `sqlite3 ~/Documents/mustory/youtube-wrapped/history.db` (tables `watches`, `searches`, view `videos`, full-text `titles_fts`).

## Common mistakes

| Mistake | Fix |
|---|---|
| A few hundred plays, years missing | Wrong Google account; export again from the one they watch on |
| Writing claims from memory of the data ("2017 and 2018 overlap most") | Quote the exact facts.md line; render.py flags stray numbers |
| Mixing totals with and without deleted videos | Year totals in facts.md include deleted videos; topic shares don't. Say which you mean |
| Skipping labels.json | Topics stay generic and "Other" swallows a fifth of the history |
| Picking sexual, medical or tragic videos as "odd" | Pick funny, strange, specific; when unsure, leave it out |
| Calling a loop-heavy song "only played 3 times" | YouTube logs a play per start; loops may count once. Counts are a floor |
