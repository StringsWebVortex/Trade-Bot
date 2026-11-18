# Trade-Bot

Python 3.11 trading backend (`src/`, FastAPI in `src/api/`) + React/Vite dashboard (`frontend/`).

## Tests
- Python: `pytest -q` (full suite; addopts enforce `--cov-fail-under=99`). For a subset:
  `pytest -q --no-cov tests/path/test_x.py`. Lint: `ruff check .` and `ruff format --check .`
- JS: `npm --prefix frontend test` (vitest; run `npm --prefix frontend ci` first if `node_modules` is missing).
- New tests: no real sleeps, network, real DB, or files outside `tmp_path`; prefer `parametrize`.

## Python <-> JS boundary
- Backend HTTP/WebSocket API: `src/api/main.py` (auth in `auth.py`, `access_control.py`, `ws_guard.py`).
- Dashboard client: `frontend/src/hooks/useApi.js` (base URL `VITE_API_URL`, keys `VITE_API_KEY*`).
- Change both sides plus their tests together when an endpoint or payload shape changes.

## Conventions
- Architecture layering in `config/architecture_layers.json`: a package imports only its own or lower
  layers (foundation < crypto < io < analytics < decision < orchestration < edge/api).
- `src/engines/` engine order is positional (E-01..E-18); never reorder without updating the seam test.
- Trading, risk and execution paths fail closed; never degrade silently.
- `config/math_registry.json` and `config/quality_registry.json` + `config/quality_registry.d/` are the
  sources of truth; a new quality entry is its own file `config/quality_registry.d/<ID>.json`.
- Never weaken, skip or quarantine a test or CI gate to get green. Never use `--no-verify`.
- Do not reset, stash, overwrite or delete the user's uncommitted work.

## Working rules
- Trust successful Edit/Write results; do not re-read a file after editing it.
- Verify with the post-edit hook output, then `git diff --stat`, then run tests once per batch.
- Read line ranges or use `rg`, not whole files, when only a part is needed.
- Review tasks: review the diff only; report `file:line`, severity, one-line fix; do not rewrite code
  unless asked.
