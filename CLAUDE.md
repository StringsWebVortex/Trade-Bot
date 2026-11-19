# Project guide for Claude

Stack: async Python (FastAPI) backend + React (Vite) JavaScript frontend. Large codebase.

## Layout
- Backend: `./`
- Frontend: `frontend/`
- API boundary: FastAPI routers/schemas  <->  the React API client. Most cross-language bugs live here; check both sides together.

## How to run
- Backend dev:   `uv run uvicorn src.api.main:app --reload`
- Backend tests: `uv run pytest -q --tb=short -x`
- Backend lint:  `ruff check .`  |  types: `mypy .` (or `pyright`)
- Frontend dev:  `npm run dev`   (inside `frontend/`)
- Frontend lint/build: `npx eslint . --quiet` | `npm run build`
- Full free audit: `bash scripts/audit.sh`  (writes `audit/*.txt`)

## Working rules (token-efficient)
- Trust a successful Edit/Write result. Do NOT re-read a file after editing it.
- Find code with Grep/Glob first, then Read only the needed line range, not whole files.
- Review the diff (`git diff main...HEAD`), not the whole repo. One module per session.
- Run tests/lint/types ONCE at the end of an edit batch, not after every small change.
- Keep tool output small: use `-q`, `--tb=short`, `--quiet`, `git diff --stat` first.
- Do not rewrite or refactor beyond the task. Refactors go in separate commits.
- One logical change per commit.

## Async rules (backend)
- No blocking calls inside `async def` (requests, time.sleep, sync DB drivers, heavy CPU). Use httpx.AsyncClient, asyncio.to_thread, async drivers.
- Every coroutine must be awaited. Keep a reference to tasks from `asyncio.create_task`.
- Always close DB sessions/connections on error paths; set timeouts on outbound calls.
- Background tasks must handle exceptions and cancellation.

## Frontend rules
- `useEffect` needs cleanup / AbortController for fetches; guard against stale responses.
- Every request path needs loading + error states.
- API response shapes must match the FastAPI schemas.

## Review output format
Report: `file:line | severity (high/med/low) | issue | one-line fix`. Do not edit unless asked.

## Agents (see .claude/agents/)
- explorer (read-only map/summary), auditor (read-only review), fixer (applies approved fixes),
  async-security-reviewer (auth, DB, background tasks, API boundary).
- test-runner (runs scripts/check.sh, returns ≤15-line verdict, never edits).
- debugger (fixes failures with max-3-attempt loop, minimal edits).

## Environment & known state (updated 2026-11-19)
- Python requirement: `>=3.11,<3.12`. Use `uv run` for all backend commands; direct `python` is 3.13 in CI containers and will fail.
- `pytest-cov` must be installed for pytest to run (pyproject.toml addopts inject `--cov`). CI installs it; local: `pip install pytest-cov`.
- `audit/` is gitignored; `scripts/audit.sh` writes there, safe to run any time.
- Frontend `node_modules` not present in cloud containers — frontend check/eslint will SKIP; run `npm ci` in `frontend/` first if needed.

## Pre-existing failures on main (do not fix without a dedicated task)
- mypy: "Duplicate module named 'agent_control'" — `tests/agent_control/__init__.py` vs `scripts/agent_control.py`. Pre-existing.
- pytest collection: tests referencing `.claude/hooks/pre_tool_use.py` and `_gh_contract.py` fail to import. Files don't exist on main. Pre-existing.
- frontend npm test: `Workspace.grid.test.jsx` assertion failures. Pre-existing on main.
- CI gates: pyre, Pyre gate, Security/SUP gates, CodeQL gate all fail on main. Pre-existing.

## PostToolUse hook
- Wired in `.claude/settings.json` → `.claude/hooks/post_edit_check.sh`.
- Lints only the edited file (ruff for .py, eslint for .js/.jsx/.ts/.tsx). Silent when clean, exits 2 on failure so Claude sees lint errors immediately.
- Gracefully exits 0 when file_path is empty or file doesn't exist.

## Tests & failures (keep raw output out of context)
- NEVER run `pytest`, `npm test`, `npm run build` or `eslint` directly. Run `bash scripts/check.sh [backend|frontend|all] [test path]`; it prints a short summary and stores full logs in `audit/*.log`.
- After a batch of edits, delegate verification to the `test-runner` subagent; it returns a short verdict.
- On failure, delegate to the `debugger` subagent with the failure summary. Max 3 attempts per failure, then stop and report.
- Never delete/skip/weaken tests or add lint-disable comments to get green without asking.
- Read a log file only by line range (offset/limit), never whole.
