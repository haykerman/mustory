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
# pairs that must stay identical: the "you" skills reuse the story skills' analysis and share one page
for pair in spotify-story/scripts/analyze.py:spotify-you/scripts/analyze.py \
            youtube-story/scripts/analyze.py:youtube-you/scripts/analyze.py \
            spotify-you/scripts/page_template.py:youtube-you/scripts/page_template.py \
            spotify-you/scripts/render.py:youtube-you/scripts/render.py; do
  a="plugin/skills/${pair%%:*}"; b="plugin/skills/${pair##*:}"
  if ! cmp -s "$a" "$b"; then echo "out of sync: $a vs $b"; status=1; fi
done
[ "$status" -eq 0 ] || { echo "Fix the copies above, then run ./build.sh again."; exit 1; }
rm -rf dist && mkdir dist
find plugin/skills -name __pycache__ -prune -exec rm -rf {} +
for skill in plugin/skills/*/; do
  name="$(basename "$skill")"
  (cd plugin/skills && zip -qr "../../dist/$name.zip" "$name" -x '*.DS_Store')
  echo "dist/$name.zip"
done
