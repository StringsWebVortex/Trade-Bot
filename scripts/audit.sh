#!/usr/bin/env bash
# Free audit: runs linters/type checkers/tests and saves SHORT output to audit/*.txt
# Missing tools are skipped (noted in the file), never fatal.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="$ROOT/."
FRONTEND="$ROOT/frontend"
OUT="$ROOT/audit"
mkdir -p "$OUT"
MAXLINES="${MAXLINES:-200}"

have() { command -v "$1" >/dev/null 2>&1; }

# run <outfile> <dir> <command...>  : saves trimmed output, records exit code
run() {
  local name="$1" dir="$2"; shift 2
  local f="$OUT/$name.txt"
  {
    echo "# $name"
    echo "# cmd: $*"
    echo "# dir: $dir"
    echo
  } >"$f"
  ( cd "$dir" && "$@" ) >"$f.tmp" 2>&1
  local rc=$?
  tail -n "$MAXLINES" "$f.tmp" >>"$f"
  rm -f "$f.tmp"
  echo "" >>"$f"
  echo "# exit code: $rc" >>"$f"
  echo "done: $name (exit $rc)"
}

skip() { echo "# SKIPPED: $2" >"$OUT/$1.txt"; echo "skip: $1 ($2)"; }

echo "== Backend =="
if have ruff; then
  run ruff_general "$BACKEND" ruff check . --output-format=concise
  # Async + bugbear + pyflakes + syntax errors
  run ruff_async  "$BACKEND" ruff check . --select E9,F,B,ASYNC --output-format=concise
else skip ruff_general "ruff not installed (pip install ruff)"; fi

if have mypy; then run mypy "$BACKEND" mypy . --ignore-missing-imports --no-error-summary
elif have pyright; then run pyright "$BACKEND" pyright
else skip mypy "mypy/pyright not installed"; fi

if have pytest; then
  # asyncio debug + show RuntimeWarning (never-awaited coroutines)
  run pytest "$BACKEND" env PYTHONASYNCIODEBUG=1 pytest -q --tb=short -W default::RuntimeWarning
else skip pytest "pytest not installed"; fi

if have bandit; then run bandit "$BACKEND" bandit -r . -q -x ./tests,./.venv,./venv
else skip bandit "bandit not installed (pip install bandit)"; fi

if have vulture; then run vulture "$BACKEND" vulture . --min-confidence 80 --exclude .venv,venv,tests
else skip vulture "vulture not installed (pip install vulture)"; fi

echo "== Frontend =="
if [ -f "$FRONTEND/package.json" ]; then
  if [ -d "$FRONTEND/node_modules" ]; then
    run eslint "$FRONTEND" npx --no-install eslint . --quiet
    run build  "$FRONTEND" npm run build --silent
    run knip   "$FRONTEND" npx --yes knip --no-progress
    run npm_audit "$FRONTEND" npm audit --omit=dev
  else
    skip eslint "node_modules missing (run npm ci in frontend)"
  fi
else
  skip eslint "no package.json in frontend"
fi

echo "== Open items (TODO/FIXME/...) =="
{
  echo "# open_items"
  if have rg; then
    rg -n --no-heading -g '!node_modules' -g '!.venv' -g '!venv' -g '!audit' -g '!dist' -g '!.git' \
      'TODO|FIXME|HACK|XXX|NotImplemented' "$ROOT" | head -n "$MAXLINES"
  else
    grep -rnE 'TODO|FIXME|HACK|XXX|NotImplemented' "$ROOT" \
      --exclude-dir=node_modules --exclude-dir=.venv --exclude-dir=venv \
      --exclude-dir=audit --exclude-dir=dist --exclude-dir=.git | head -n "$MAXLINES"
  fi
} >"$OUT/open_items.txt" 2>&1
echo "done: open_items"

echo "== Async smells (grep) =="
{
  echo "# async_smells (heuristic; verify before fixing)"
  echo "## blocking calls (requests / time.sleep) in python files"
  grep -rnE '(^|[^a-zA-Z_])requests\.(get|post|put|delete|patch)\(|time\.sleep\(' "$BACKEND" \
    --include='*.py' --exclude-dir=.venv --exclude-dir=venv --exclude-dir=tests | head -n 80
  echo
  echo "## create_task not assigned (possible lost task)"
  grep -rnE '^[[:space:]]*(asyncio\.)?(create_task|ensure_future)\(' "$BACKEND" \
    --include='*.py' --exclude-dir=.venv --exclude-dir=venv | head -n 80
  echo
  echo "## useEffect with fetch but no AbortController (manual review)"
  grep -rlE 'useEffect' "$FRONTEND" --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' \
    --exclude-dir=node_modules --exclude-dir=dist 2>/dev/null \
    | xargs -r grep -lE 'fetch\(|axios' 2>/dev/null \
    | xargs -r grep -L 'AbortController' 2>/dev/null | head -n 80
} >"$OUT/async_smells.txt" 2>&1
echo "done: async_smells"

echo
echo "Audit saved in: $OUT"
echo "Next: give the auditor agent audit/*.txt + ONE module at a time."
