# Writing story.json

`story.json` holds every sentence; `data.json` draws every chart and list. A chapter with no data hides itself (discovery, exclusives, songs).

## Numbers

Every number must come from `facts.md`. A number you computed from facts.md (a sum, a difference) goes in `"derived"` with how. Write numbers of 10 or more as digits so the checker sees them.

Keep the units straight: "YouTube music plays" (video starts) vs "Spotify listens" (30 s+). Compare shares, peaks and leans; don't claim one app has "more" of an artist from raw counts. The lean percentages in facts.md already correct for the size difference.

## Voice

Second person, warm and specific, a little playful. Short sentences. Headlines are claims ("Spotify works the day shift. YouTube takes the night."), not labels. No filler, no em-dash asides, no "not X, but Y". `**bold**` works; in `hero.h`, `\n` breaks the line.

## Shape (`//` notes are for you; story.json is plain JSON)

```json
{
  "title": "Two Apps, One Taste",
  "hero":  { "h": "Spotify at work.\nYouTube at night.", "lede": "The window, both totals, the one-line thesis." },
  "split": { "h": "...", "lede": "Spotify's share per year; the most lopsided and the most even year." },
  "clock": { "h": "...", "lede": "Peak hours, after-midnight and weekend shares." },
  "discovery": { "h": "...", "lede": "How many artists each app found first, the median lag." },
  "lean":  { "h": "...", "lede": "Which artists lean which way. Mention once that units differ, so the split is the point." },
  "only":  { "h": "...", "lede": "Why some artists live on one app (not on Spotify, discovered via a video, etc.) only if the reason is evident." },
  "songs": { "h": "...", "lede": "The songs played on both." },
  "days":  { "h": "...", "lede": "Days with both apps vs one, the top-50 overlap." },
  "you":   { "h": "Two habits, one taste.", "cards": [ { "h": "Spotify is the soundtrack", "p": "2–3 sentences." }, { "h": "...", "p": "..." }, { "h": "...", "p": "..." } ] },   // exactly three cards read best
  "method_extra": ["Optional footnotes, e.g. aliases you made."],
  "derived": {}
}
```

## What makes it interesting

- A year that looks quiet on one app is often loud on the other. Check "By year" for it.
- Hour-of-day differences usually tell a work-vs-leisure story. Say what the data shows, not more.
- Discovery lag is the headline when one app finds most artists first.
- One-app artists often have a reason in the data (covers channels and live sessions only on YouTube; long synth or focus albums only on Spotify). Don't invent reasons.
