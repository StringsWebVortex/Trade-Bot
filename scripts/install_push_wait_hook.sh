#!/bin/sh
# GOV-069: install the hook that holds ChatGPT's pushes until CI answers.
# Run once per clone: sh scripts/install_push_wait_hook.sh
set -eu
root=$(git rev-parse --show-toplevel)
source="$root/.githooks/reference-transaction"
hooks=$(git rev-parse --git-path hooks)
target="$hooks/reference-transaction"
mkdir -p "$hooks"
if [ -e "$target" ] && ! cmp -s "$source" "$target"; then
  echo "refusing: $target already exists and is not this repository's hook" >&2
  exit 1
fi
cp "$source" "$target"
chmod +x "$target"
echo "installed $target"
