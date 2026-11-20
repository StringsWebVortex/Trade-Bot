"""PostToolUseFailure hook: adds compact error context without replacing the native failure."""
from __future__ import annotations

import json
import sys

_MAX_CONTEXT_LINES = 3
_MAX_CONTEXT_CHARS = 1200
_ERROR_KEYWORDS = ("ERROR", "FAIL", "Warning", "Exception", "Traceback", "Error", "Exit code")


def _extract_compact_context(error: str) -> str:
    lines = error.splitlines()
    # Find important lines first.
    important = [line for line in lines if any(kw in line for kw in _ERROR_KEYWORDS)]
    if important:
        kept = important[:_MAX_CONTEXT_LINES]
    else:
        kept = lines[:_MAX_CONTEXT_LINES]
    context = "\n".join(kept)
    if len(context) > _MAX_CONTEXT_CHARS:
        context = context[:_MAX_CONTEXT_CHARS]
    context += "\n[native failure record cannot be replaced — compact context only]"
    return context


def transform(payload: dict) -> dict:
    error = payload.get("error", "")
    context = _extract_compact_context(error)
    return {"hookSpecificOutput": {"additionalContext": context}}


if __name__ == "__main__":
    payload = json.loads(sys.stdin.read())
    result = transform(payload)
    print(json.dumps(result))
