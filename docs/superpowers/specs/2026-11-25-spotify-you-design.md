# spotify-you: a "who your music says you are" page

## Why

The story pages are about the music. This page is about the person: playful guesses about real life ("your friends probably think…", "at a party you're probably…") drawn from taste and listening habits, plus an invented character who sums them up. It is for the listener to recognize themselves, and to send to friends with "is this me?". Not science; the voice says "probably".

## Goals

- Life first, music as the evidence: every guess shows a small hint of the music behind it (artist chips, a mini chart, one clue number).
- A fixed set of 24 traits, scored the same way for everyone so friends can compare; a person can match several.
- A one-off character written by Claude from the matched traits and personal details.
- Same look as the other mustory pages; heavy on charts; works on a phone; share card sized for a screenshot.

## Non-goals and anti-goals

- No real psychology claims, no diagnosis, nothing about health, relationships status, politics, religion or other sensitive guesses. Teasing is fine, mean is not.
- Not a horoscope: a guess with no clue is not allowed.
- No web lookups of the person's artists; genres come from Claude's own knowledge, and unknown artists are marked unsure and left out.

## Approach (chosen)

A new skill, `spotify-you`, next to `spotify-story`. Considered:

1. **New skill with a synced copy of spotify-story's `analyze.py`** (chosen). All the tested metrics (hours, loops, skips, eras, focus audio, travel, rituals) are reused unchanged; `build.sh` checks the copy stays identical. A new `you.py` turns them plus `genres.json` into traits and clues.
2. A second page inside `spotify-story`. Less code, but the skill would do two jobs and its trigger description would blur.
3. Rewriting the metrics for this page. Duplicates tested logic for no gain.

## How it works

1. `analyze.py` (copy) → `data.json`, `facts.md`, `artists.tsv`.
2. Claude writes `labels.json` (focus/sleep audio, as in spotify-story) and `genres.json`: each top artist mapped to one genre from a fixed list of about 20, or `unsure`.
3. `you.py` → `you_data.json` and `you_facts.md`:
   - genre shares (taste hours, focus audio excluded) and five taste directions (Mellow, Unpretentious, Sophisticated, Intense, Contemporary, after Rentfrow and Gosling's music-preference research);
   - 24 traits, each scored 0–100 from fixed thresholds with its clue numbers and evidence artists; ≥60 earned, 35–59 "almost";
   - five life reads (open to new ideas, creature of habit, life of the party, plans ahead, feels things deeply) with levels;
   - "this or that" positions and the 24-hour clock.
4. Claude writes `you.json`: the character (name, lede, portrait), read prose, 6–10 guesses (each with a clue, artist chips and a chart from a fixed menu), a day in the life with a song per moment, green and red flags, and the share-card line.
5. `render.py` fact-checks every number against `facts.md` + `you_facts.md` (same rules and pairing check as spotify-story) and writes `you.html`.

## Left to the builder

Trait thresholds, exact genre list and its direction weights, chart menu details, and copy for the method note.
