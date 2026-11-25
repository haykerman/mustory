# Writing you.json

`you.json` holds every sentence on the page. The scripts score the traits and draw every chart from `you_data.json`; you write the person around them.

## The idea

Life first, music as the evidence. Each line is a playful guess about who they are away from the headphones (friends, work, trips, parties, mornings, decisions), and each guess shows the clue it came from. Music-psychology research loosely links taste to personality, and this page plays with that:

- **Intense** (metal, punk, rock): curious, questions the default, calm on the outside.
- **Sophisticated** (jazz, classical, experimental, ambient): likes complexity, open to new ideas, a bit of a nerd.
- **Mellow** (singer-songwriter, soul, dream pop): feels things deeply, good listener, romantic.
- **Contemporary** (pop, dance, hip-hop, latin): social, upbeat, likes being where things happen.
- **Unpretentious** (country, folk, singalongs): warm, loyal, values tradition and their people.

Habits say as much as genres: loops (comfort seekers), skips (impatient, knows what they want), shuffle (goes with the flow), picking songs by hand (decisive), late nights, focus music at work (deep worker), trips, yearly rituals, forgotten favorites (moves on completely), lifers (loyal).

## Rules

- Every number must come from `facts.md` or `you_facts.md`; write numbers as digits. Computed ones go in `"derived"`.
- Agree with the scores. Read `## Traits` and `## Life reads` in you_facts.md first; a guess may stretch a trait but never contradict it.
- Second person, warm, specific, funny like a friend who noticed things. Short sentences. No em-dash asides.
- Hedge with "probably", "we'd bet", "the kind of person who", but not in every sentence.
- Never guess about health, relationship status, sexuality, politics, religion, money, looks or family. Never mean.
- Name real artists and songs as evidence, copied exactly.
- Don't name cities or guess why they travelled; countries are fine.

## Shape (the `//` notes explain fields; you.json itself is plain JSON with no comments)

```json
{
  "title": "The Gentle Contrarian",
  "eyebrow": "Who your music says you are · probably",
  "character": {
    "name": "The Gentle Contrarian",          // 2-4 words, a one-off name that sums up the earned traits. Not a trait name.
    "lede": "2-3 sentences: who this person is, in life terms.",
    "made_of": ["free_thinker", "creature_of_habit", "night_owl"],  // optional: 3-5 trait keys from you_data.json; default is the top earned
    "portrait": [                              // 5-6 rows, life details, playful and specific
      { "k": "Job", "v": "Something with a long attention span…" },
      { "k": "Weekend", "v": "…" },
      { "k": "Coffee", "v": "…" },
      { "k": "Theme song", "v": "“Harbor Lights”, Paper Lanterns. Never skipped it once." },
      { "k": "Group chat", "v": "…" }
    ],
    "look": {                                  // optional; draws the figurine. Omit any field to let the traits decide.
      "card": "lilac",          // share card color: amber, lilac, aqua, sage, rust. Default: from the lead trait (first in made_of): social traits amber, night and feeling traits lilac, curious traits aqua, loyal traits sage, intense traits rust
      "animal": "fox",          // owl, fox, wolf, dog, cat, bear, rabbit, otter, deer, squirrel, panda, raccoon, beaver, bird. Default: picked from the strongest traits
      "outfit": "hoodie",       // tee, hoodie, sweater, jacket
      "outfit_color": "violet", // navy, amber, lilac, aqua, blue, rose, ochre, green, violet, rust, black
      "eyes": "dots",           // dots, sleepy, glasses, sunglasses
      "props": ["moon", "repeat", "plane"]  // up to 3: moon, coffee, plane, laptop, repeat, compass, sun, heart, bolt, star, sparkle, book, pencil, gamepad, film, note
    }
  },
  "taste": { "h": "Your taste, in five directions.", "lede": "Which directions lead and what that combination says about a person." },
  "reads": {
    "h": "The person behind the playlist.",
    "lede": "optional",
    "items": {                                 // one or two sentences each, matching the level in you_facts.md
      "open": "…", "habit": "…", "party": "…", "plans": "…", "deep": "…"
    }
  },
  "guesses": {
    "h": "Things we'd bet on.",
    "lede": "optional",
    "items": [                                 // 6-10. Cover friends, a party, work, holidays, "you'd probably never…", karaoke, a breakup playlist, 2 a.m. self, and more of your own
      { "q": "Your friends probably think you're…",
        "a": "calm, until someone says something wrong about a thing you love.",
        "because": "Because your taste is **41%** contemporary but you still played Iron Meridian all winter.",
        "chart": "dims",                       // optional, one of the menu below
        "chips": ["Iron Meridian", "Juno Park"] }  // optional, 1-4 artists or songs
    ]
  },
  "spectrum": { "h": "You'd probably rather…" },
  "day": {
    "h": "The Gentle Contrarian's Tuesday.",
    "items": [ { "time": "08:40", "what": "One line of their day.", "song": "Okapi" } ]   // 5-6, shaped by the real 24-hour clock
  },
  "flags": {
    "h": "Green flags, red flags.",
    "green": [ { "t": "Loyal for years, not months", "e": "Paper Lanterns: 5 years and counting" } ],   // 3 each; e = the music evidence
    "red":   [ { "t": "“One more episode” means six", "e": "a playlist left running 18 hours" } ]
  },
  "share": { "h": "Send it. Make them guess.", "line": "One quotable line about them for the share card." },
  "method_extra": ["optional footnotes"],
  "derived": { "120": "how you computed it" }
}
```

## Chart menu for guesses

| chart | shows |
|---|---|
| `clock` | listening by hour, busiest hour lit |
| `night` / `morning` | the same, with 21:00–03:00 or 05:00–10:00 lit |
| `taste` | top 5 genres as one bar |
| `dims` | the five taste directions as one bar |
| `skip_years`, `shuffle_years`, `night_years`, `discovery_years`, `focus_years`, `hours_years` | one small bar per year |
| `loop` | one tick per play of the longest loop |
| `top10` | share of time on the top 10 artists |
| `picked`, `shuffle`, `weekend` | a two-part split |
| `countries` | a dot per country listened from |

Use each chart once at most, and pick the one that proves the guess.

## The animal

The figurine is an animal in headphones, picked from the strongest traits (night owl → owl, explorer → fox, loyalist → dog, comfort seeker → bear, party starter → otter, romantic → deer, globetrotter → bird, and so on). The page names it under the figure. Override it with `look.animal` only when another animal clearly fits the character better, and let the portrait play along with it if you like.

## Character name

Combine the 2-3 strongest traits with a personal detail into something a friend would laugh at and agree with: "The Midnight Archivist", "The Gentle Contrarian", "The Weekend Romantic", "The Shuffle Philosopher". Avoid trait names themselves and avoid anything that sounds like a diagnosis.
