# mustory

Your music and video history, told back to you. mustory is a set of three [Claude Code](https://claude.com/claude-code) skills that turn your own data exports into Spotify Wrapped–style pages, any time of year, for any span of years:

| Skill | Needs | Makes |
|---|---|---|
| `youtube-wrapped` | Google Takeout export of YouTube history | Eras, obsessions, forgotten favorites, seasons, night-owl hours, rabbit holes, rituals, odd watches, a personality read |
| `spotify-wrapped` | Spotify data export (Extended streaming history is best) | Lifetime hours, loops, the skip button, autopilot vs songs you picked, focus music, devices, travel, discovery, marathons |
| `youtube-vs-spotify` | Both of the above | Which app does what, when you use each, where artists are found first, artists that live on one app, songs you play everywhere |

Scripts do every count and draw every chart. Claude does the parts that need judgment (labeling channels, tagging moods, writing the story), and a fact checker makes sure every number in the story comes from your data. Everything stays on your computer.

## Install

Requires Claude Code and Python 3.9+ (stdlib only, nothing to pip install).

```bash
git clone <this repo> mustory && cd mustory
./install.sh
```

`install.sh` links the three skills into `~/.claude/skills/`, so edits in this repo apply right away. To share a single skill as a zip, run `./build.sh` and send the file from `dist/`.

## Get your data

- **YouTube:** takeout.google.com → **Deselect all** → **YouTube and YouTube Music** → "All YouTube data included": keep only **history** → "Multiple formats": history as **JSON** → export. Use the Google account you actually watch on.
- **Spotify:** spotify.com/account/privacy → tick **Extended streaming history** → request. Spotify emails you when it's ready (often a few days, up to 30). The quicker "Account data" package works too, but covers only the last 12 months.

## Run

Open Claude Code anywhere and say one of:

- "Make my YouTube Wrapped."
- "Make my Spotify Wrapped."
- "Compare my YouTube and Spotify."

Claude finds the export in `~/Downloads` (or asks), picks a work folder such as `~/spotify-wrapped/`, and walks you through the rest. You get a single HTML page; in Claude apps that can publish, it becomes a private link you can share.

## Repo layout

```
skills/
  youtube-wrapped/      SKILL.md, scripts/, assets/template.html, references/story.md
  spotify-wrapped/      same shape
  youtube-vs-spotify/   same shape
docs/ideas.md           the question catalog the pages answer, plus ideas not built yet
install.sh              link the skills into ~/.claude/skills
build.sh                check shared code is in sync, zip each skill into dist/
```

Each skill is self-contained so it can be shared on its own. That means `takeout.py`, `classify.py` and `spotify.py` exist in more than one skill. Edit one copy, then let `./build.sh` tell you which others to update.

## Privacy

Exports contain everything you've watched and played, plus IP addresses on Spotify. The scripts never keep IP addresses, never list private-session tracks, unzip into a temporary folder that's deleted when they finish, and write only to the work folder you choose. Keep exports and work folders out of this repo (`.gitignore` already does).
