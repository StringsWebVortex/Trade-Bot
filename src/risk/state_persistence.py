"""
EXR-013 -- halts and kill switches survive a restart.

The capital-preservation floor and the strategy kill switch both promise that
only an explicit human action clears them, yet both held their state only in
memory, so a supervisor restart silently cleared the halt. This applies the
`src/execution/mode_persistence.py` pattern to them: atomic temp-file +
`os.replace` writes, a *missing* file meaning a first start, and an
*unreadable* file meaning "cannot rule out halted" (callers fail closed).
"""

from __future__ import annotations

import json
import os
import tempfile
from contextlib import suppress
from pathlib import Path
from typing import Any, Final

ENV_DIR_VAR: Final[str] = "RISK_STATE_DIR"
DEFAULT_STATE_DIR: Final[Path] = Path("data/risk_state")

_SCHEMA_VERSION: Final[int] = 1


class StateUnreadableError(Exception):
    """The state file exists but cannot be trusted; callers must fail closed."""


def state_dir() -> Path:
    override = os.environ.get(ENV_DIR_VAR, "").strip()
    return Path(override) if override else DEFAULT_STATE_DIR


def state_file(name: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in name)
    return state_dir() / f"{safe}.json"


def save_state(path: Path, state: dict[str, Any]) -> None:
    """Atomically persist *state* (temp file in the same directory + fsync + replace)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"version": _SCHEMA_VERSION, "state": state})
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=".risk_state-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        with suppress(OSError):
            os.unlink(tmp_name)
        raise


def load_state(path: Path) -> dict[str, Any] | None:
    """Return the saved state, None when no file exists; raise when unreadable."""
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or raw.get("version") != _SCHEMA_VERSION:
            raise StateUnreadableError(f"unexpected schema in {path}")
        state = raw["state"]
        if not isinstance(state, dict):
            raise StateUnreadableError(f"state is not an object in {path}")
        return state
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise StateUnreadableError(f"cannot read {path}: {exc}") from exc
