"""Stable input/output contract for Claude Code hook adapters.

Hook handlers stay in :mod:`src.agent_control.hooks`; this module owns only
payload validation, dispatch metadata, and serialization at the process edge.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal


class HookProtocolError(ValueError):
    """Raised when a hook name, event payload, or handler result violates the contract."""


@dataclass(frozen=True, slots=True)
class HookSpec:
    """Wire-level contract for one supported hook entry point."""

    name: str
    handler: str
    output: Literal["json", "text", "none"]


HOOK_SPECS: dict[str, HookSpec] = {
    "stop": HookSpec("stop", "stop", "json"),
    "precompact": HookSpec("precompact", "precompact", "json"),
    "session-start": HookSpec("session-start", "session_start", "text"),
    "post-bash": HookSpec("post-bash", "post_bash", "none"),
}


def get_hook_spec(name: str) -> HookSpec:
    """Return a registered hook contract or raise a stable protocol error."""
    try:
        return HOOK_SPECS[name]
    except KeyError:
        raise HookProtocolError(f"unknown hook {name!r}") from None


def parse_event(raw: str) -> dict:
    """Parse Claude's stdin payload; an empty stream is the documented empty event."""
    if not raw.strip():
        return {}
    try:
        event = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HookProtocolError(
            f"invalid JSON payload at line {exc.lineno}, column {exc.colno}"
        ) from exc
    if not isinstance(event, dict):
        raise HookProtocolError("payload is not a JSON object")
    return event


def format_result(spec: HookSpec, result: object) -> str | None:
    """Serialize a handler result according to its registered wire format."""
    if spec.output == "none":
        if result is not None:
            raise HookProtocolError(f"{spec.name} hook must not return output")
        return None
    if result is None:
        return None
    if spec.output == "json":
        if not isinstance(result, dict):
            raise HookProtocolError(f"{spec.name} hook must return an object or None")
        return json.dumps(result) + "\n"
    if not isinstance(result, str):
        raise HookProtocolError(f"{spec.name} hook must return text or None")
    return result + "\n" if result else None
