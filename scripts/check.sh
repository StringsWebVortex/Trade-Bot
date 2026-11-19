#!/usr/bin/env bash
# Quiet verification wrapper. Full logs go to audit/*.log; stdout is a SHORT summary.
# Usage:
#   scripts/check.sh                    # backend + frontend
#   scripts/check.sh backend            # lint + types + tests (backend)
#   scripts/check.sh backend tests/test_orders.py::test_create   # only that test
#   scripts/check.sh frontend           # eslint + build + npm test
# Exit code: 0 = all pass, 1 = something failed.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="$ROOT/."
FRONTEND="$ROOT/frontend"
LOGDIR="$ROOT/audit"; mkdir -p "$LOGDIR"
MAXFAIL="${MAXFAIL:-30}"   # max lines of failure detail shown
TARGET="${1:-all}"; [ $# -gt 0 ] && shift
EXTRA=("$@")
FAILED=0
have() { command -v "$1" >/dev/null 2>&1; }

# step <label> <logname> <dir> <cmd...>
step() {
  local label="$1" name="$2" dir="$3"; shift 3
  local log="$LOGDIR/$name.log"
  ( cd "$dir" && "$@" ) >"$log" 2>&1
  local rc=$?
  if [ $rc -eq 0 ]; then
    echo "PASS  $label"
  elif [ $rc -eq 5 ] && [ "$label" = "pytest" ]; then
    echo "NOTE  pytest collected no tests"
  else
    FAILED=1
    echo "FAIL  $label (exit $rc)  full log: audit/$name.log"
    # Show only the useful lines, capped.
    grep -E "^(FAILED|ERROR)|Error|error:|^E  |assert|:[0-9]+:[0-9]+:" "$log" | head -n "$MAXFAIL" | sed 's/^/      /'
    local total; total=$(wc -l <"$log")
    echo "      (+ full output: $total lines in audit/$name.log; read only a line range if needed)"
  fi
}

if [ "$TARGET" = "backend" ] || [ "$TARGET" = "all" ]; then
  have ruff   && step "ruff"   ruff_check   "$BACKEND" ruff check . --output-format=concise
  if have mypy; then step "mypy" mypy_check "$BACKEND" mypy . --ignore-missing-imports --no-error-summary; fi
  if have uv; then
    step "pytest" pytest_run "$BACKEND" env PYTHONASYNCIODEBUG=1 uv run --frozen pytest -q --tb=short -x -rf -W default::RuntimeWarning "${EXTRA[@]+"${EXTRA[@]}"}"
  elif have pytest; then
    step "pytest" pytest_run "$BACKEND" env PYTHONASYNCIODEBUG=1 pytest -q --tb=short -x -rf -W default::RuntimeWarning "${EXTRA[@]+"${EXTRA[@]}"}"
  else echo "SKIP  pytest not installed"; fi
fi

if [ "$TARGET" = "frontend" ] || [ "$TARGET" = "all" ]; then
  if [ -f "$FRONTEND/package.json" ] && [ -d "$FRONTEND/node_modules" ]; then
    step "eslint"   eslint_check "$FRONTEND" npx --no-install eslint . --quiet
    step "build"    build_check  "$FRONTEND" npm run build --silent
    step "npm test" npm_test     "$FRONTEND" npm test --if-present --silent
  else
    echo "SKIP  frontend (no package.json or node_modules missing)"
  fi
fi

[ $FAILED -eq 0 ] && echo "RESULT: ALL PASS" || echo "RESULT: FAILURES FOUND"
exit $FAILED
