#!/usr/bin/env bash
# Check that the shared scripts are identical in every skill, then zip each skill into dist/.
set -euo pipefail
cd "$(dirname "$0")"
status=0
for f in takeout.py classify.py spotify.py; do
  copies=(plugin/skills/*/scripts/"$f")
  [ -e "${copies[0]}" ] || continue
  for c in "${copies[@]:1}"; do
    if ! cmp -s "${copies[0]}" "$c"; then
      echo "out of sync: ${copies[0]} vs $c"
      status=1
    fi
  done
done
# spotify-you runs spotify-story's analysis unchanged (youtube-story has its own analyze.py)
if ! cmp -s plugin/skills/spotify-story/scripts/analyze.py plugin/skills/spotify-you/scripts/analyze.py; then
  echo "out of sync: plugin/skills/spotify-story/scripts/analyze.py vs plugin/skills/spotify-you/scripts/analyze.py"
  status=1
fi
[ "$status" -eq 0 ] || { echo "Fix the copies above, then run ./build.sh again."; exit 1; }
rm -rf dist && mkdir dist
find plugin/skills -name __pycache__ -prune -exec rm -rf {} +
for skill in plugin/skills/*/; do
  name="$(basename "$skill")"
  (cd plugin/skills && zip -qr "../../dist/$name.zip" "$name" -x '*.DS_Store')
  echo "dist/$name.zip"
done
