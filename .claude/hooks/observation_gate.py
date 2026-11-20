"""PostToolUse observation gate: compacts tool outputs to stay within context budgets."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Limits (from config/observation_boundary.json when available)
# ---------------------------------------------------------------------------

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "observation_boundary.json"


def _load_limits() -> dict:
    try:
        return json.loads(_CONFIG_PATH.read_text(encoding="utf-8")).get("limits", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


_LIMITS = _load_limits()

_MAX_SOURCE_LINES: int = _LIMITS.get("max_source_lines", 80)
_MAX_SUCCESS_LINES: int = _LIMITS.get("max_success_lines", 80)
_MAX_SEARCH_ITEMS: int = _LIMITS.get("max_search_items", 40)
_MAX_LIST_ITEMS: int = _LIMITS.get("max_list_items", 40)
_MAX_ERROR_LINES = 3

# Pattern for the prfail report command.
_PRFAIL_RE = re.compile(r"^\s*\./scripts/prfail\s+--pr\s+[1-9][0-9]*\s*$")

_ERROR_KEYWORDS = ("ERROR", "FAIL", "Warning", "Exception", "Traceback", "Error")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_prfail_command(tool_input: dict | None) -> bool:
    if tool_input is None:
        return False
    return bool(_PRFAIL_RE.match(tool_input.get("command", "")))


def _extract_important_lines(lines: list[str]) -> list[str]:
    return [line for line in lines if any(kw in line for kw in _ERROR_KEYWORDS)]


def _compact_long_text(text: str, label: str = "observation compacted") -> str:
    """Compact text, prioritising error lines over head/tail."""
    lines = text.splitlines()
    if len(lines) <= _MAX_SUCCESS_LINES:
        return text

    error_lines = _extract_important_lines(lines)
    if error_lines:
        kept = error_lines[:_MAX_ERROR_LINES]
        note = f"[{label}: {len(lines)} lines; showing {len(kept)} error/warning lines]"
        return "\n".join(kept + [note])

    tail = next((line for line in reversed(lines) if line.strip()), "")
    suffix = f"[{label}: {len(lines)} lines]"
    return f"{tail}\n{suffix}" if tail else suffix


def _compact_bash_stdout(stdout: str, is_prfail: bool) -> str:
    if not stdout:
        return stdout

    if is_prfail:
        return stdout

    lines = stdout.splitlines()
    error_lines = _extract_important_lines(lines)

    # Compact when there are many error lines, even if total count is small.
    if len(error_lines) > _MAX_ERROR_LINES:
        kept = error_lines[:_MAX_ERROR_LINES]
        note = (
            f"[observation compacted: {len(lines)} lines, "
            f"{len(error_lines)} errors; showing first {_MAX_ERROR_LINES}]"
        )
        return "\n".join(kept + [note])

    if len(lines) <= _MAX_SUCCESS_LINES:
        return stdout

    # Total lines exceed budget.
    if error_lines:
        kept = error_lines[:_MAX_ERROR_LINES]
        note = f"[observation compacted: {len(lines)} lines total, showing {len(kept)} error lines]"
        return "\n".join(kept + [note])

    tail = next((line for line in reversed(lines) if line.strip()), "")
    suffix = f"[observation compacted: {len(lines)} lines total]"
    return f"{tail}\n{suffix}" if tail else suffix


def _compact_search_output(raw: str) -> str:
    lines = raw.splitlines()
    if len(lines) <= _MAX_SEARCH_ITEMS:
        return raw

    seen_files: dict[str, str] = {}
    for line in lines:
        m = re.match(r"^([^:]+\.py):", line)
        if m:
            fname = m.group(1)
            if fname not in seen_files:
                seen_files[fname] = line

    total = len(lines)
    kept = list(seen_files.values())[:_MAX_SEARCH_ITEMS]
    result = "\n".join(kept)
    if total > len(kept):
        result += (
            f"\n[search compacted: {total} matches across {len(seen_files)} files; "
            f"{total - len(kept)} lines omitted]"
        )
    return result


def _compact_glob_output(raw: str) -> str:
    lines = [line for line in raw.splitlines() if line.strip()]
    total = len(lines)
    if total <= _MAX_LIST_ITEMS:
        return raw

    dirs: dict[str, list[str]] = {}
    for line in lines:
        parts = line.split("/")
        top = parts[0] if len(parts) > 1 else "."
        dirs.setdefault(top, []).append(line)

    result_lines = [f"[{total} entries across {len(dirs)} directories]"]
    for d, files in sorted(dirs.items()):
        result_lines.append(f"{d}/ ({len(files)} files)")
        result_lines.extend(f"  {f}" for f in files[:2])
        if len(files) > 2:
            result_lines.append(f"  ... {len(files) - 2} more")
    result_lines.append("[Use a narrower search query to see specific files]")
    return "\n".join(result_lines)


def _compact_content_list(items: list) -> list:
    result = []
    for item in items:
        if isinstance(item, dict) and item.get("type") == "text":
            text = item.get("text", "")
            compacted = _compact_long_text(text)
            if compacted != text:
                item = {**item, "text": compacted}
        result.append(item)
    return result


def _compact_mcp_dict(response: dict) -> dict:
    result = dict(response)
    for key, val in response.items():
        if isinstance(val, str):
            compacted = _compact_long_text(val)
            if compacted != val:
                result[key] = compacted
        elif isinstance(val, list):
            result[key] = _compact_content_list(val)
    return result


# ---------------------------------------------------------------------------
# Main transform
# ---------------------------------------------------------------------------


def transform(event: dict) -> dict:
    """
    Transform a PostToolUse event, compacting the tool output if needed.
    Returns {"hookSpecificOutput": {"updatedToolOutput": <compacted>}}.
    """
    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input")
    response = event.get("tool_response")

    if tool_name == "Read" and isinstance(response, str):
        lines = response.splitlines()
        if len(lines) <= _MAX_SOURCE_LINES:
            return _wrap(response)
        kept = lines[:_MAX_SOURCE_LINES]
        omitted = len(lines) - _MAX_SOURCE_LINES
        kept.append(f"[source observation compacted: {omitted} lines omitted]")
        return _wrap("\n".join(kept))

    if tool_name == "Bash" and isinstance(response, dict):
        is_prfail = _is_prfail_command(tool_input)
        stdout = response.get("stdout", "")
        updated = {**response, "stdout": _compact_bash_stdout(stdout, is_prfail)}
        return _wrap(updated)

    if tool_name == "Grep" and isinstance(response, str):
        return _wrap(_compact_search_output(response))

    if tool_name == "Glob" and isinstance(response, str):
        return _wrap(_compact_glob_output(response))

    if tool_name.startswith("mcp__") and isinstance(response, dict):
        return _wrap(_compact_mcp_dict(response))

    return _wrap(response)


def _wrap(output) -> dict:
    return {"hookSpecificOutput": {"updatedToolOutput": output}}


if __name__ == "__main__":
    payload = json.loads(sys.stdin.read())
    result = transform(payload)
    print(json.dumps(result))
