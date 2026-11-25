---
name: youtube-you
description: Use when someone wants a playful personality page from their YouTube history ("what does my YouTube say about me", "what kind of person am I based on what I watch", "make me a character from my YouTube", "my spirit animal from my history"), guesses about their real life from what they watch and listen to, or a shareable "is this me?" card, and has a Google Takeout YouTube export (takeout-*.zip) or can get one.
---

# YouTube You

Turns a Google Takeout YouTube history into a page about the person, not the videos: an invented character drawn as an animal in headphones, life guesses ("your friends probably think you're…"), five life reads, "this or that" picks, a day in the life, green and red flags, trait badges and a share card. Every guess shows a small hint of what they watched behind it. It is for fun, and the voice says "probably".

Scripts do every count, score every trait and draw every chart. You do what needs judgment: label channels, tag music genres, place watch topics in parts of life, and write the character and the guesses. Every number you write must come from `facts.md` or `you_facts.md`.

All scripts are stdlib Python 3.9+. `$SKILL` is this skill's base directory (shown when the skill loads; for a manual install, `~/.claude/skills/youtube-you`). Run them with `python3 -I` from any folder.

## Talking to the person

Many people running this aren't technical. In conversation, never mention files, JSON, scripts, folders or Python unless they ask: say "your YouTube history", "a few channels I need to sort", "your page". Decide the timezone (the computer's) and the work folder yourself and mention each in one plain line. Before the first script, check `python3 --version` (3.9+); if it's missing, the `start` skill has plain-language install steps. If they don't have their export yet, the `start` skill has step-by-step download instructions.

## 1. Get the export

Look for the newest `takeout-*.zip` in `~/Downloads`, or ask for the path. It must be from the account they actually watch on, with YouTube history in JSON (the `start` skill has the steps).

## 2. Timezone and work folder

Use the machine's timezone unless they say they lived elsewhere (pass an IANA name). Use `~/Documents/mustory/youtube-you/` as the work folder; outputs are overwritten. If they already made a `youtube-story` page, copy its `labels.json` and `moods.json` over to save work. Keep everything local and don't web-search their titles or searches.

## 3. First pass

```bash
python3 -I "$SKILL/scripts/analyze.py" --export ~/Downloads/takeout-XXXX.zip --work ~/Documents/mustory/youtube-you --tz Europe/Berlin
```

## 4. Label, tag, place

**labels.json.** Read `to_label.tsv` (top channels with sample titles) and give the big unlabeled ones a topic, plus how-to `quests` regexes for hobbies you spot, exactly as the `youtube-story` skill describes:

```json
{ "channels": { "Kurzgesagt": "Science & learning", "Binging with Babish": "Food" },
  "quests": { "3D & rendering": "blender|render|sketchup" } }
```

Run step 3 again.

**genres.json.** Tag the music artists in `artists.tsv` from the top down with one genre each from your own knowledge, until 80%+ of the plays are covered; unknown artists are `"unsure"`. Use exactly these genres: pop, k-pop / j-pop, dance / edm, hip-hop / rap, r&b / soul, latin, reggae, country, folk / acoustic, singer-songwriter, indie / alternative, rock, metal, punk / hardcore, electronic, dream pop / shoegaze, ambient / new age, post-rock / experimental, jazz, blues, classical, soundtrack / score, world / traditional, holiday / novelty.

**topics.json.** Place every watch topic in facts.md's "Topics (all time)" list (except Music and the "Other" ones), and every quest, in one part of life: learning, making, stories, news, comedy, gaming, lifestyle, tech, self, calm.

```json
{ "topics": { "Movie recaps": "stories", "Tech reviews": "tech", "Psychology & self": "self" },
  "quests": { "3D & rendering": "making", "Driving test": "learning", "Climbing in League": "gaming" } }
```

Then score:

```bash
python3 -I "$SKILL/scripts/you.py" --work ~/Documents/mustory/youtube-you
```

## 5. Write you.json

Read all of `you_facts.md`, the parts of `facts.md` you need (top artists, obsessions, rabbit holes, quests, rituals, forgotten favorites, searches), then `references/you.md`, and write `you.json` in the work folder.

## 6. Render and fact-check

```bash
python3 -I "$SKILL/scripts/render.py" --work ~/Documents/mustory/youtube-you
```

It checks every number of 10 or more against facts.md and you_facts.md. If one is missing it lists it, writes nothing, and exits with code 2: fix it, or add it to `"derived"` with how you computed it. Check every PAIRING CHECK warning too.

## 7. Deliver

- With an Artifact/publish tool: publish `you.html` (starts private) and give the link; say only they can see it until they share it.
- Otherwise `open ~/Documents/mustory/youtube-you/you.html` or give the path.

Mention their animal and the share card at the bottom: it's sized for a phone screenshot.
## Common mistakes

| Mistake | Fix |
|---|---|
| A guess with no clue | Every guess needs a `because` with a real number or name, plus a chart or chips |
| Writing about the music instead of the person | Headlines and guesses are about life (friends, work, trips, parties, habits); the music is the evidence underneath |
| Guessing about health, relationship status, politics, religion, money or looks | Never. Keep it to habits, taste, social style and quirks |
| Mean jokes | Tease like a friend who likes them |
| Stating guesses as facts | "probably", "we'd bet", "the kind of person who" |
| Tagging genres from a name | Tag only artists you know; the rest are `unsure` |
| Quoting a personal search | Only harmless searches (a hobby, a band), never health, relationships or money |
| Contradicting the scores | If "Life of the party" is Low, don't write them as the party starter |
