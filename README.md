# mustory

Your music and video history, told back to you. mustory is a [Claude Code](https://claude.com/claude-code) plugin that turns your own data exports into year-in-review story pages, any time of year, for any span of years:

| Skill | Needs | Makes |
|---|---|---|
| `youtube-story` | Google Takeout export of YouTube history | Eras, obsessions, forgotten favorites, seasons, night-owl hours, rabbit holes, rituals, odd watches, a personality read |
| `spotify-story` | Spotify data export (Extended streaming history is best) | Lifetime hours, loops, the skip button, autopilot vs songs you picked, focus music, devices, travel, discovery, marathons |
| `youtube-vs-spotify` | Both of the above | Which app does what, when you use each, where artists are found first, artists that live on one app, songs you play everywhere |

Scripts do every count and draw every chart. Claude does the parts that need judgment (labeling channels, tagging moods, writing the story), and a fact checker makes sure every number in the story comes from your data. Everything stays on your computer.

## Install

You need Claude Code (the Claude desktop app's Code tab, the terminal app, or an IDE extension) and Python 3.9 or newer. If Python is missing, Claude tells you how to get it.

In a Claude Code chat, type:

```
/plugin install mustory --marketplace haykerman/mustory
```

That's it. To update later: `/plugin update mustory`.

**For developers working on mustory:** clone the repo and run `./install.sh` instead. It links the skills into `~/.claude/skills/`, so edits apply right away (don't also install the plugin, or every skill shows up twice). `./build.sh` checks the shared scripts are in sync and zips each skill into `dist/` for sharing one on its own.

## Get your data

Not sure what you need? Say "help me get started with mustory" and Claude walks you through it, step by step.

- **YouTube:** takeout.google.com → **Deselect all** → **YouTube and YouTube Music** → "All YouTube data included": keep only **history** → "Multiple formats": history as **JSON** → export. Use the Google account you actually watch on.
- **Spotify:** spotify.com/account/privacy → tick **Extended streaming history** → request. Spotify emails you when it's ready (often a few days, up to 30). The quicker "Account data" package works too, but covers only the last 12 months.

## Run

Open a Claude Code chat anywhere and say one of:

- "Tell the story of my YouTube history."
- "Make my Spotify story."
- "Compare my YouTube and Spotify."
- Not sure? "Help me get started with mustory."

Claude finds your download in Downloads (or asks), keeps its working files in `Documents/mustory/`, and walks you through the rest. You get a single HTML page; in Claude apps that can publish, it becomes a private link you can share.

## Repo layout

```
.claude-plugin/marketplace.json   lists the plugin, so /plugin install finds it
plugin/                           the plugin itself (only this folder is shipped)
  .claude-plugin/                 plugin.json and icon.png
  skills/
    start/                        front door: what you need, how to download it, plain-language setup
    youtube-story/                SKILL.md, scripts/ (incl. page_template.py), references/story.md
    spotify-story/                same shape
    youtube-vs-spotify/           same shape
  README.md, LICENSE
docs/ideas.md                     the question catalog the pages answer, plus ideas not built yet
install.sh                        link the skills into ~/.claude/skills (for development)
build.sh                          check shared code is in sync, zip each skill into dist/
```

The plugin lives in its own folder because the plugin directory accepts only Markdown, text, JSON, YAML and images from individual developers, so the shell scripts stay outside it.

Each skill is self-contained so it can be shared on its own. That means `takeout.py`, `classify.py` and `spotify.py` exist in more than one skill. Edit one copy, then let `./build.sh` tell you which others to update.

## Privacy

Exports contain everything you've watched and played, plus IP addresses on Spotify. The scripts never keep IP addresses, never list private-session tracks, unzip into a temporary folder that's deleted when they finish, and write only to the work folder you choose. Keep exports and work folders out of this repo (`.gitignore` already does).

## License

MIT. See [LICENSE](LICENSE).
