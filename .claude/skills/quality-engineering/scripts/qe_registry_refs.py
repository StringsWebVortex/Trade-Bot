"""Git ref helpers for the quality-engineering registry scaffolder."""
from __future__ import annotations

import subprocess


class GitUnavailable(RuntimeError):
    """Raised when git is unavailable or the repo root cannot be determined."""


def _git(repo: str, *args: str, stdin: str | None = None) -> str:
    """Run a git command and return its stdout as a string."""
    cmd = ["git", "-C", repo, *args]
    try:
        result = subprocess.run(
            cmd,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if result.returncode != 0:
            raise GitUnavailable(result.stderr.strip() or f"git {args[0]} failed")
        return result.stdout
    except FileNotFoundError:
        raise GitUnavailable("git is not installed") from None
    except subprocess.TimeoutExpired:
        raise GitUnavailable("git timed out") from None
