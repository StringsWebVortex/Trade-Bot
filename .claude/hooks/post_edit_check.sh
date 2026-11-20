#!/usr/bin/env bash
# PostToolUse hook: lint only the edited file. Silent when clean.
# Exit 2 + stderr => the failure is shown to Claude so it can fix it.
set -u
PROJECT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
FRONTEND="$PROJECT/frontend"

input="$(cat)"
file="$(printf '%s' "$input" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    print((d.get("tool_input") or {}).get("file_path", "") or "")
except Exception:
    print("")
' 2>/dev/null)"

[ -n "$file" ] && [ -f "$file" ] || exit 0

out=""
rc=0
case "$file" in
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      out="$(ruff check --quiet --output-format=concise "$file" 2>&1)" || rc=$?
    fi
    ;;
  *.js|*.jsx|*.ts|*.tsx)
    if [ -d "$FRONTEND/node_modules" ]; then
      out="$(cd "$FRONTEND" && npx --no-install eslint --quiet "$file" 2>&1)" || rc=$?
    fi
    ;;
esac

if [ "$rc" -ne 0 ] && [ -n "$out" ]; then
  printf 'Lint failed for %s:\n%s\n' "$file" "$(printf '%s' "$out" | head -n 20)" >&2
  exit 2
fi
exit 0
