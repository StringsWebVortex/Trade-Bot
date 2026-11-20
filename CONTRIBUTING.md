# Contributing

## Mandatory workflow

### 1. Run the free audit first
Before touching any module, run the full audit so you have a baseline:

```bash
bash scripts/audit.sh
```

Output lands in `audit/*.txt` (git-ignored). Give those files to the auditor agent along with the specific module you plan to change.

### 2. Use agents in order

| Agent | Model | When |
|---|---|---|
| `explorer` | Haiku | Map a feature or flow; locate files before any change |
| `auditor` | Sonnet | Review the diff or one module; produces a findings table |
| `fixer` | Sonnet | Apply only the approved findings from the auditor |
| `async-security-reviewer` | Sonnet | Auth routes, DB access, background tasks, API boundary |

Invoke via Claude Code: `/agents` lists them. Run `explorer` before you start, `auditor` before you finish, `fixer` for the patch, and `async-security-reviewer` on any route that touches auth or the DB.

### 3. The PostToolUse hook runs automatically
Every `Edit`, `Write`, or `MultiEdit` call triggers `.claude/hooks/post_edit_check.sh`, which lints the saved file with `ruff` (Python) or `eslint` (JS/TS). It is silent on success and returns a short error on failure. Never skip or disable it.

### 4. All changes go through a PR; CI must pass before merge
- No direct commits to `main`.
- Open a pull request for every change, however small.
- The CI workflow (`.github/workflows/ci.yml`) runs ruff, mypy, pytest, bandit (backend) and eslint + build (frontend) on every PR. All jobs must be green before merging.

### 5. Install the required tools once
```bash
pip install ruff mypy pytest pytest-asyncio bandit vulture
(cd frontend && npm ci)
```
