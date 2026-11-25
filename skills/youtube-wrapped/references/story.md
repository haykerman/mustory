# Writing story.json

`story.json` holds every sentence on the page. The scripts draw all charts and lists from `data.json`; you write the words around them. A chapter whose data is empty hides itself, so skip its keys.

## The one rule for numbers

Every number you write must come from `facts.md`. If you computed one from facts.md numbers (a sum, a difference), list it in `"derived"`. `render.py` refuses to write the page while any number of 10 or more is unaccounted for. Write such numbers as digits. Before writing a claim like "X and Y overlap most" or "Z came first", find the exact line in facts.md that says so. Claims written from a quick skim are often wrong.

## Voice

Second person, warm, specific, a little playful, like a friend who noticed things. Short sentences. Name real songs, channels and dates. No filler ("it's worth noting"), no em-dash asides, no "not X, but Y". Headlines are claims, not labels: "Taylor Swift, by a distance." beats "Your top artists".

`**bold**` works in any text field. In `hero.h`, `\n` makes a line break.

## Shape (the `//` notes explain fields; story.json itself is plain JSON, no comments)

```json
{
  "title": "Six Years of Late Nights",
  "hero": {
    "eyebrow": "Your YouTube, Mar 2019 – Jun 2025",
    "h": "21,400 plays.\nSix years.\nMostly after midnight.",
    "lede": "One paragraph: first and last play, the once-vs-repeat split from Totals."
  },
  "shape":    { "h": "...", "lede": "...", "notes": [{ "month": "2021-02", "text": "the quiet month" }] },   // month: YYYY-MM inside the data range
  "artists":  { "h": "...", "lede": "...",
                "callout": { "eyebrow": "The mystery at #3", "name": "Artist", "body": "Something surprising about one top artist." } },
  "eras":     { "h": "...", "lede": "Define an era (≥N plays of one artist, gaps ≤10 days) and name the longest and the most recent big one." },
  "dedications": { "h": "...", "lede": "Say what the dots mean (one per year)." },
  "forgotten": { "h": "...", "lede": "..." },
  "seasons":  { "h": "...", "lede": "Explain the tile: big name = top artist, small line = topic watched far more than usual, edge brightness = music share." },
  "soundtrack": { "h": "..." },
  "mood":     { "h": "...", "lede": "Say how many artists you tagged and what the quarters show." },
  "night":    { "h": "...", "lede": "..." },
  "comfort":  { "h": "...", "lede": "..." },
  "drift":    { "h": "...", "lede": "Most-alike and least-alike pairs, lifers." },
  "flings":   { "h": "Flings and lifers." },
  "gateways": { "h": "...", "lede": "..." },
  "rabbit":   { "h": "...", "lede": "...", "notes": ["one line per session listed under Rabbit holes, same order"] },
  "quests":   { "h": "...", "lede": "..." },
  "rituals":  { "h": "...", "lede": "About the charted ritual.", "chart_index": 0,
                "cards": [{ "tag": "September 2025", "title": "...", "body": "..." }] },
  "otd":      { "h": "3 June, through the years." },   // the date facts.md shows under "On this day"
  "odd":      { "h": "...", "lede": "...",
                "items": [{ "date": "3 May 2018", "title": "exact video title", "note": "one dry line" }],
                "feature": { "tag": "Right now", "title": "...", "body": "optional wide card" } },
  "search":   { "h": "...", "lede": "..." },
  "you": {
    "h": "A one-line portrait.",
    "essay": [{ "h": "You're a rewatcher, not a browser", "p": "2–3 sentences with evidence." }],
    "change": [{ "when": "2017–2018", "title": "The night shift", "body": "What defined it, with numbers." }]
  },
  "method_extra": ["Optional extra footnotes."],
  "derived": { "312": "Nov+Dec Christmas-song plays from the rituals line" }
}
```

## Chapter by chapter

- **hero**: the total plays and span. The lede uses the first-play and last-play lines and the once/10+ split.
- **shape**: the busiest year and the quietest year from "By year". `notes` label at most two months on the chart.
- **artists.callout**: one surprising thing about a top artist: an artist that might be the user themself (a covers channel), a huge lead, an artist from an unexpected language. Leave it out if nothing stands out.
- **rituals**: pick `chart_index` from the numbered "Yearly rituals" list (prefer a theme or a festival over a single channel). Use the cards for other rhythms, such as Christmas songs or a 7-day burst. Only link a burst to an event (an anniversary, a release, a tour) if you're sure of the date; otherwise describe the burst without explaining it.
- **odd**: choose 6–9 rows from `odd_candidates.tsv`: funny, strange, oddly specific. Skip anything sexual, medical, tragic or about private people. Copy titles exactly. Each note is one dry line. `feature` can hold a strange repeat-watch (look at the 2026 soundtrack or the obsessions).
- **you.essay**: 4–5 traits, each backed by numbers (rewatching, a dominant mood, things they make, languages, a curiosity).
- **you.change**: 4–6 periods from "By year" and "Top artists per year": what was playing, what else they watched, night share.
