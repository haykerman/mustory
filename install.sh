#!/usr/bin/env bash
# Link mustory's skills into ~/.claude/skills so Claude Code finds them.
# Existing folders with the same name are moved aside (never deleted).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$dest"
for skill in "$here"/skills/*/; do
  name="$(basename "$skill")"
  target="$dest/$name"
  if [ -L "$target" ]; then
    rm "$target"
  elif [ -e "$target" ]; then
    backup="$target.backup-$(date +%Y%m%d%H%M%S)"
    mv "$target" "$backup"
    echo "moved existing $name to $backup"
  fi
  ln -s "${skill%/}" "$target"
  echo "linked $name"
done
command -v python3 >/dev/null || echo "warning: python3 not found; the skills need Python 3.9+"
