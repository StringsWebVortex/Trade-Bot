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
