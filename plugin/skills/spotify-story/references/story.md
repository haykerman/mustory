# Writing story.json

`story.json` holds every sentence on the page. The scripts draw all charts and lists from `data.json`; you write the words around them. A chapter whose data is empty hides itself, so skip its keys.

## The one rule for numbers

Every number you write must come from `facts.md`. If you computed one from facts.md numbers (a sum, a difference, a ratio), list it in `"derived"` with how. `render.py` refuses to write the page while any number of 10 or more is unaccounted for. Write such numbers as digits. Before a claim like "your biggest year" or "X came first", find the facts.md line that says so.

Words to keep straight, because facts.md uses them precisely:
- **hours**: listening time with overlaps removed. Use it for "how much".
- **listens**: song streams of 30 s or more. Use it for "how often".
- **streams**: every start, including instant skips.
- **quick skip**: next button within 30 s.

## Voice

Second person, warm, specific, a little playful, like a friend who noticed things. Short sentences. Name real songs, artists and dates. No filler, no em-dash asides, no "not X, but Y". Headlines are claims, not labels: "Taylor Swift, by a distance." beats "Your top artists".

`**bold**` works in any text field. In `hero.h`, `\n` makes a line break.

## Privacy

- Never mention what was played in private sessions; the count is enough (the footer already says it).
- Don't name cities or guess why someone travelled. Countries and dates from facts.md are fine.
- A journey marked "maybe a VPN or layover" is hidden from the travel list; don't write about it as a trip.
- Podcast show names are fine to mention; they're in facts.md for that.

## Shape (the `//` notes explain fields; story.json itself is plain JSON with no comments)

```json
{
  "title": "Five Years of Skipping",
  "hero": { "eyebrow": "Your Spotify, Jan 2021 – Oct 2025", "h": "2,140 hours.\nFive years.\nOne very busy skip button.", "lede": "First and last stream, total days of music." },
  "shape":     { "h": "...", "lede": "Busiest month and year, the quietest stretch." },
  "artists":   { "h": "...", "lede": "Top by hours vs top by listens, if they differ.",
                 "callout": { "eyebrow": "...", "name": "...", "body": "Something surprising: focus audio beating every band, a huge lead, a lifer." } },
  "tracks":    { "h": "...", "lede": "..." },
  "loops":     { "h": "...", "lede": "The longest back-to-back run and how many loops in total." },
  "eras":      { "h": "...", "lede": "Define an era (≥N listens of one artist, gaps ≤10 days); name the biggest, the longest-lasting and the newest (facts.md lists all three)." },
  "dedications": { "h": "...", "lede": "Say what the dots mean (one per year)." },
  "forgotten": { "h": "...", "lede": "..." },
  "skips":     { "h": "...", "lede": "Skip rate over the years, the median seconds before a skip, a most-skipped song." },
  "autopilot": { "h": "...", "lede": "How rarely songs were picked on purpose; shuffle over the years." },
  "focus":     { "h": "...", "lede": "Hours of focus/sleep audio, its share, its hour of day." },
  "seasons":   { "h": "...", "lede": "Explain the tile: big name = top artist by hours, small line = best new find, edge brightness = skip rate." },
  "soundtrack": { "h": "..." },
  "mood":      { "h": "...", "lede": "How many artists you tagged and what the quarters show." },
  "night":     { "h": "...", "lede": "Busiest hour, weekday vs weekend, after-midnight share." },
  "devices":   { "h": "...", "lede": "The device story year by year." },
  "travel":    { "h": "...", "lede": "Countries and the song that opened a trip." },
  "discovery": { "h": "...", "lede": "New artists per year and how much of each year went to them." },
  "drift":     { "h": "...", "lede": "Most-alike and least-alike years, lifers." },
  "flings":    { "h": "Flings and lifers." },
  "gateways":  { "h": "...", "lede": "..." },
  "marathons": { "h": "...", "lede": "...", "notes": ["one line per marathon, same order as facts.md"] },
  "rituals":   { "h": "...", "lede": "About the charted ritual.", "chart_index": 0, "cards": [{ "tag": "...", "title": "...", "body": "..." }] },
  "otd":       { "h": "3 June, through the years." },   // the date facts.md shows under "On this day"
  "odd":       { "h": "...", "lede": "...", "items": [{ "date": "3 May 2018", "title": "Artist – Track", "note": "one dry line" }],
                 "feature": { "tag": "...", "title": "...", "body": "optional wide card" } },
  "you": {
    "h": "A one-line portrait.",
    "essay": [{ "h": "You're a rewatcher, not a browser", "p": "2–3 sentences with evidence." }],
    "change": [{ "when": "2019–2020", "title": "...", "body": "What defined it, with numbers." }]
  },
  "method_extra": ["Optional extra footnotes."],
  "derived": { "200": "artist A 120 + the same artist under another spelling 80" }
}
```

## Chapter notes

- **callout / focus**: if focus or sleep audio tops the artist list, say so plainly and kindly. It's a tool, not a taste.
- **marathons**: one artist for 20+ hours is almost always a loop left running (asleep, out of the house). Say that rather than "you listened for 63 hours".
- **skips**: the most-skipped list is songs shuffle kept serving. Have fun with it.
- **odd**: pick 6–9 rows from `odd_candidates.tsv` (artists heard exactly once): funny, unexpected genres, strange titles. Skip anything sexual or tragic. Title format "Artist – Track", copied exactly.
- **you.essay**: 4–5 traits with numbers (how they use music: focus tool, comfort loops, shuffle-and-skip, discovery, devices, travel).
- **you.change**: 4–6 periods from "By year", "Top artists per year" and "Devices".
