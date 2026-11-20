"""Quality gate hook."""
import json
import os
import sys
from pathlib import Path


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        print("quality_gate: degraded — could not parse hook input", file=sys.stderr)
        return 0

    file_path = payload.get("tool_input", {}).get("file_path", "")
    if not file_path:
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_dir and not Path(file_path).is_relative_to(Path(project_dir)):
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
