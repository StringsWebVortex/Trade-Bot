"""Coordinator: plans big, exactly once. The cheap worker model never sees
this prompt, and this prompt never sees any worker's raw output."""

from __future__ import annotations

import json

from common.claude_cli import run_claude

from .config import COORDINATOR_MODEL, MAX_SUBTASKS

_SCHEMA_HINT = (
    "Break the goal into up to {n} short, independent, self-contained subtask "
    "instructions (strings) that together accomplish it."
)

_PLAN_SCHEMA = {
    "type": "object",
    "properties": {"subtasks": {"type": "array", "items": {"type": "string"}}},
    "required": ["subtasks"],
}


def _parse_text(text: str) -> object:
    """Lenient fallback: tolerate code fences and prose around a JSON array."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("["), text.rfind("]")
        if start == -1 or end <= start:
            raise
        return json.loads(text[start : end + 1])


def plan(task: str) -> list[str]:
    prompt = f"{_SCHEMA_HINT.format(n=MAX_SUBTASKS)}\n\nGOAL: {task}"
    out = run_claude(prompt, model=COORDINATOR_MODEL, max_turns=1, json_schema=_PLAN_SCHEMA)
    structured = out.get("structured_output")
    if isinstance(structured, dict) and isinstance(structured.get("subtasks"), list):
        subtasks = structured["subtasks"]
    else:
        text = out["result"].strip()
        subtasks = _parse_text(text)
        if not isinstance(subtasks, list):
            raise ValueError(f"Planner did not return a JSON list: {text[:200]}")
    return [str(s) for s in subtasks[:MAX_SUBTASKS]]
