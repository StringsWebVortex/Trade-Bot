#!/usr/bin/env python3
"""
PreCompact hook: checkpoint the active task before context compaction.

Delegates to src.agent_control.hooks.run_hook("precompact").
No active task → no-op (exit 0). Fails open on import error.
Registry: GOV-064.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(PROJECT_DIR))

try:
    from src.agent_control.hooks import run_hook

    result = run_hook("precompact", sys.stdin, sys.stdout, sys.stderr)
except Exception as exc:
    print(f"[precompact_checkpoint] unavailable: {exc!r}", file=sys.stderr)
    result = 0

sys.exit(result)
