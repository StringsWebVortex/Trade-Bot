#!/usr/bin/env python3
"""GOV-069 — hold a push made by ChatGPT until the pull request's CI answers.

ChatGPT works on this repository through Desktop Commander, which runs its
commands in a terminal on the owner's machine. Git's ``reference-transaction``
hook runs after a push has succeeded and ``git push`` does not return until the
hook does, so this script keeps ChatGPT's push command open until
``./scripts/prfail`` has an answer for the pushed commit:

  - no lines: CI is green and no review conversation is open; ChatGPT is free;
  - lines: the exact failure lines, which ChatGPT fixes and pushes again, and
    that push is held the same way;
  - nothing after HOLD_SECONDS: CI is stuck, and ChatGPT is told to stop.

Only a push whose process ancestry contains Desktop Commander is held. Pushes
from anyone else return at once. TB_PUSH_WAIT=1 holds any push and
TB_PUSH_WAIT=0 holds none.

.githooks/reference-transaction calls this; scripts/install_push_wait_hook.sh
installs that hook.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import time
import urllib.parse
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path

try:
    from scripts import ci_diagnostics
except ImportError:  # run as `python3 scripts/push_wait.py` by the hook
    import ci_diagnostics

HOLD_SECONDS = 12 * 60
POLL_SECONDS = 20
AGENT_MARKER = "desktop-commander"
# Desktop Commander runs as `node .../desktop-commander/dist/index.js` or
# `npx @wonderwhy-er/desktop-commander`: the name is a path segment. A shell
# whose command text merely mentions the name does not match.
AGENT_PATH = re.compile(r"[/\\]" + AGENT_MARKER + r"(?:[/\\@]|$)", re.IGNORECASE)
FORCE_ENV = "TB_PUSH_WAIT"
REMOTE_PREFIX = "refs/remotes/origin/"
DELETED = "0" * 40
MAX_ANCESTORS = 64

Answer = Callable[[int], tuple[str, list[str]]]


def pushed_refs(
    lines: Iterable[str], local_sha: Callable[[str], str | None]
) -> list[tuple[str, str]]:
    """(branch, sha) for each origin branch moved to the commit its local branch holds.

    A push moves origin/<branch> to the local branch's commit. A fetch moves it
    to a commit the local branch does not hold yet, so it is not a push.
    """
    found: list[tuple[str, str]] = []
    for line in lines:
        parts = line.split()
        if len(parts) != 3:
            continue
        _old, new, ref = parts
        branch = ref[len(REMOTE_PREFIX) :] if ref.startswith(REMOTE_PREFIX) else ""
        if not branch or branch == "HEAD" or new == DELETED:
            continue
        if local_sha(branch) == new:
            found.append((branch, new))
    return found


def is_agent_push(env: Mapping[str, str], ancestors: Iterable[str]) -> bool:
    forced = env.get(FORCE_ENV, "").strip()
    if forced in {"0", "1"}:
        return forced == "1"
    return any(AGENT_PATH.search(token) for command in ancestors for token in command.split())


def proc_ancestry(pid: int, root: Path = Path("/proc")) -> list[str]:
    """Command lines of pid's ancestors, read from a Linux /proc tree."""
    commands: list[str] = []
    for _ in range(MAX_ANCESTORS):
        try:
            stat = (root / str(pid) / "stat").read_text(encoding="utf-8")
            # The command name in field 2 may hold spaces; the parent pid is
            # the second field after its closing parenthesis.
            ppid = int(stat.rsplit(")", 1)[1].split()[1])
            raw = (root / str(ppid) / "cmdline").read_bytes()
        except (OSError, IndexError, ValueError):
            break
        commands.append(raw.replace(b"\0", b" ").decode("utf-8", "replace").strip())
        if ppid <= 1:
            break
        pid = ppid
    return commands


def ps_ancestry(pid: int, run: Callable[[list[str]], str]) -> list[str]:
    """Command lines of pid's ancestors from `ps` (macOS, BSD)."""
    commands: list[str] = []
    for _ in range(MAX_ANCESTORS):
        fields = run(["ps", "-o", "ppid=", "-p", str(pid)]).split()
        if not fields or not fields[0].isdigit():
            break
        ppid = int(fields[0])
        commands.append(run(["ps", "-o", "command=", "-p", str(ppid)]).strip())
        if ppid <= 1:
            break
        pid = ppid
    return commands


def windows_ancestry(pid: int, run: Callable[[list[str]], str]) -> list[str]:
    """Command lines of pid's ancestors from Win32_Process (Windows, Git Bash)."""
    script = (
        f"$p = {pid}; for ($i = 0; $i -lt {MAX_ANCESTORS}; $i++) {{"
        ' $x = Get-CimInstance Win32_Process -Filter "ProcessId=$p";'
        " if (-not $x) { break }; $p = $x.ParentProcessId;"
        ' $y = Get-CimInstance Win32_Process -Filter "ProcessId=$p";'
        " if (-not $y) { break }; Write-Output $y.CommandLine }"
    )
    output = run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script])
    return [line.strip() for line in output.splitlines() if line.strip()]


def _run(command: list[str]) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout if result.returncode == 0 else ""


def ancestry() -> list[str]:
    pid = os.getpid()
    if Path("/proc/self/stat").exists():
        return proc_ancestry(pid)
    if os.name == "nt" or sys.platform in {"cygwin", "msys"} or os.environ.get("MSYSTEM"):
        return windows_ancestry(os.getppid(), _run) + ps_ancestry(pid, _run)
    return ps_ancestry(pid, _run)


def find_pr(branch: str) -> int | None:
    slug = ci_diagnostics._repo_slug()
    owner = slug.split("/", 1)[0]
    query = urllib.parse.urlencode({"state": "open", "head": f"{owner}:{branch}", "per_page": 10})
    pulls = ci_diagnostics._json(f"repos/{slug}/pulls?{query}")
    numbers = [p["number"] for p in pulls if isinstance(p, dict)] if isinstance(pulls, list) else []
    return numbers[0] if len(numbers) == 1 else None


def hold(
    pr: int,
    sha: str,
    answer: Answer,
    say: Callable[[str], None],
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    """Wait for prfail's answer on exactly this commit; return how it ended."""
    short = sha[:7]
    deadline = clock() + HOLD_SECONDS
    say(f"PRFAIL: holding this push until CI answers for PR #{pr} at {short} (up to 12 min).")
    while True:
        try:
            head, lines = answer(pr)
        except ci_diagnostics.ReportPending:
            head, lines = "", []
        except (ci_diagnostics.DiagnosticError, OSError, ValueError, TypeError, KeyError) as exc:
            say(f"PRFAIL: error: {exc}. Stop and tell the owner.")
            return "error"
        # A report for another commit is the PR before GitHub saw this push.
        if head == sha:
            if not lines:
                say(
                    f"PRFAIL: no failures on {short}. CI is green and no review conversation is open."
                )
                return "green"
            say(
                f"PRFAIL: {len(lines)} line(s) to fix on {short}. Fix them, commit and push "
                "again; that push waits for CI the same way."
            )
            for line in lines:
                say(line)
            return "failed"
        if clock() >= deadline:
            say(
                f"PRFAIL: CI did not finish within 12 min on {short}; a workflow is stuck. "
                "Stop and tell the owner."
            )
            return "timeout"
        say("PRFAIL: wait")
        sleep(min(POLL_SECONDS, max(deadline - clock(), 0)))


def _local_sha(branch: str) -> str | None:
    sha = _run(["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"]).strip()
    return sha or None


def _say(text: str) -> None:
    sys.stderr.write(text + "\n")
    sys.stderr.flush()


def main(
    argv: list[str],
    stdin: Iterable[str],
    env: Mapping[str, str],
    *,
    ancestors: Callable[[], list[str]] = ancestry,
    local_sha: Callable[[str], str | None] = _local_sha,
    pr_for: Callable[[str], int | None] = find_pr,
    answer: Answer = ci_diagnostics.prfail_answer,
    say: Callable[[str], None] = _say,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    # Git ignores this hook's exit status once the transaction is committed;
    # what ChatGPT reads is the text.
    if argv[:1] != ["committed"]:
        return 0
    pushes = pushed_refs(stdin, local_sha)
    if not pushes or not is_agent_push(env, ancestors()):
        return 0
    for branch, sha in pushes:
        try:
            pr = pr_for(branch)
        except (ci_diagnostics.DiagnosticError, OSError, ValueError) as exc:
            say(f"PRFAIL: error: could not find the pull request for {branch}: {exc}")
            continue
        if pr is None:
            say(f"PRFAIL: no single open pull request for {branch}; nothing to wait for.")
            continue
        hold(pr, sha, answer, say, clock, sleep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:], sys.stdin, os.environ))
