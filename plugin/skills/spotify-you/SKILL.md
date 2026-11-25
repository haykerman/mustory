---
name: spotify-you
description: Use when someone wants a playful personality page from their Spotify listening ("what does my music say about me", "what kind of person am I based on my music", "make me a character from my Spotify", "my listening personality"), guesses about their real life from their taste, or a shareable "is this me?" card, and has a Spotify data export (my_spotify_data.zip) or can get one.
---

# Spotify You

Turns a Spotify personal-data export into a page about the person, not the music: an invented character with a drawn figurine, life guesses ("your friends probably think you're…", "at a party you're probably…"), five life reads, "this or that" picks, a day in the life, green and red flags, trait badges and a share card. Every guess shows a small hint of the music behind it. It is for fun, and the voice says "probably".

Scripts do every count, score every trait and draw every chart. You do what needs judgment: tag genres, write the character and the guesses. Every number you write must come from `facts.md` or `you_facts.md`.

All scripts are stdlib Python 3.9+. `$SKILL` is this skill's base directory (shown when the skill loads; for a manual install, `~/.claude/skills/spotify-you`). Run them with `python3 -I` from any folder.

## Talking to the person

Many people running this aren't technical. In conversation, never mention files, JSON, scripts, folders or Python unless they ask: say "your Spotify history", "a few artists I need to sort", "your page". Decide the timezone (the computer's) and the work folder yourself and mention each in one plain line. Before the first script, check `python3 --version` (3.9+); if it's missing, the `start` skill has plain-language install steps. If they don't have their export yet, the `start` skill has step-by-step download instructions.

## 1. Get the export

Look for `my_spotify_data.zip` in `~/Downloads`, or ask for the path. **Extended streaming history** is best (all years, skips, shuffle, devices, travel). **Account data** covers only 12 months and has no shuffle or picked-song data; the page still works, with fewer traits.

## 2. Timezone and work folder

Use the machine's timezone unless they say they lived elsewhere (pass an IANA name). Use `~/Documents/mustory/spotify-you/` as the work folder; outputs are overwritten. If they already made a `spotify-story` page, you can reuse its `labels.json` by copying it over. Keep everything local and don't web-search their artists.

## 3. First pass

```bash
python3 -I "$SKILL/scripts/analyze.py" --export ~/Downloads/my_spotify_data.zip --work ~/Documents/mustory/spotify-you --tz Europe/Berlin
```

## 4. Focus audio and genres

**labels.json** (optional). Read `artists.tsv`. Focus, sleep, white-noise and study-beats artists are left out of taste automatically when most of their titles look like it; facts.md lists who was left out. Fix misses with `{"functional": [...], "not_functional": [...]}` and run step 3 again.

**genres.json** (required). Tag the artists in `artists.tsv` from the top down with one genre each, from your own knowledge, until you've covered 80%+ of the hours. If you don't know an artist, use `"unsure"`; never guess from the name alone.

```json
{ "artists": { "Radiohead": "indie / alternative", "Rammstein": "metal", "Some Unknown Band": "unsure" } }
```

Genres (exactly these strings): pop, k-pop / j-pop, dance / edm, hip-hop / rap, r&b / soul, latin, reggae, country, folk / acoustic, singer-songwriter, indie / alternative, rock, metal, punk / hardcore, electronic, dream pop / shoegaze, ambient / new age, post-rock / experimental, jazz, blues, classical, soundtrack / score, world / traditional, holiday / novelty.

Then score:

```bash
python3 -I "$SKILL/scripts/you.py" --work ~/Documents/mustory/spotify-you
```

It prints the earned traits and warns if genres cover too little.

## 5. Write you.json

Read all of `you_facts.md`, the parts of `facts.md` you need (top artists, loops, travel, rituals, forgotten favorites, flings), then `references/you.md`, and write `you.json` in the work folder.

## 6. Render and fact-check

```bash
python3 -I "$SKILL/scripts/render.py" --work ~/Documents/mustory/spotify-you
```

It checks every number of 10 or more against facts.md and you_facts.md (song and artist names are skipped). If one is missing it lists it, writes nothing, and exits with code 2: fix it, or add it to `"derived"` with how you computed it. It may also print a PAIRING CHECK warning: a number next to an artist or song with no facts line holding both. Check each one.

## 7. Deliver

- With an Artifact/publish tool: publish `you.html` (starts private) and give the link; say only they can see it until they share it.
- Otherwise `open ~/Documents/mustory/spotify-you/you.html` or give the path.

Mention the share card at the bottom: it's sized for a phone screenshot.

## Common mistakes

| Mistake | Fix |
|---|---|
| A guess with no clue | Every guess needs a `because` with a real number or name, plus a chart or chips |
| Writing about the music instead of the person | Headlines and guesses are about life (friends, work, trips, parties, habits); the music is the evidence underneath |
| Guessing about health, relationship status, politics, religion, money or looks | Never. Keep it to habits, taste, social style and quirks |
| Mean jokes | Tease like a friend who likes them |
| Stating guesses as facts | "probably", "we'd bet", "the kind of person who" |
| Tagging genres from a name | Tag only artists you know; the rest are `unsure` |
| Contradicting the scores | If "Life of the party" is Low, don't write them as the party starter |
