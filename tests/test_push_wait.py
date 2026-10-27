"""
A push ChatGPT makes through Desktop Commander waits for the pull request's CI.

Git's reference-transaction hook runs after a successful push and `git push`
does not return until it does, so scripts/push_wait.py holds ChatGPT there
until ./scripts/prfail answers for the pushed commit: green releases it,
failure lines are handed back to fix, and twelve minutes means CI is stuck.

Decides:
  - GOV-069 — A ChatGPT push waits up to 12 minutes for prfail's answer on that commit
"""

from __future__ import annotations

import os
import stat
import threading
from pathlib import Path

import pytest

from scripts import ci_diagnostics, push_wait

ROOT = Path(__file__).resolve().parents[1]
SHA = "a" * 40
OLD = "b" * 40
AGENT = ["node /usr/lib/node_modules/@wonderwhy-er/desktop-commander/dist/index.js"]


def _line(new: str, ref: str, old: str = OLD) -> str:
    return f"{old} {new} {ref}\n"


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        (_line(SHA, "refs/remotes/origin/feature"), [("feature", SHA)]),
        (_line(OLD, "refs/remotes/origin/feature", old=SHA), []),  # a fetch of another commit
        (_line("0" * 40, "refs/remotes/origin/feature"), []),  # a deleted branch
        (_line(SHA, "refs/heads/feature"), []),  # a local branch update
        (_line(SHA, "refs/remotes/upstream/feature"), []),
        (_line(SHA, "refs/remotes/origin/HEAD"), []),
        ("garbage\n", []),
    ],
    ids=["push", "fetch", "delete", "local", "other-remote", "origin-head", "garbage"],
)
def test_only_a_push_of_the_local_commit_counts(line: str, expected) -> None:
    local = {"feature": SHA}
    assert push_wait.pushed_refs([line], local.get) == expected


@pytest.mark.parametrize(
    ("env", "ancestors", "held"),
    [
        ({}, AGENT, True),
        ({}, ["node C:\\npm\\npx-cli.js -y @wonderwhy-er/desktop-commander@latest"], True),
        ({}, ["/bin/bash", "sshd: owner"], False),
        ({}, ["/bin/bash -c echo desktop-commander; git push"], False),
        ({"TB_PUSH_WAIT": "0"}, AGENT, False),
        ({"TB_PUSH_WAIT": "1"}, ["/bin/bash"], True),
    ],
    ids=[
        "desktop-commander",
        "npx-windows",
        "a-person",
        "named-in-a-shell",
        "forced-off",
        "forced-on",
    ],
)
def test_only_chatgpt_pushes_are_held(env, ancestors, held) -> None:
    assert push_wait.is_agent_push(env, ancestors) is held


@pytest.mark.parametrize(
    ("ancestors", "push"),
    [
        (["git push"], True),
        (["/usr/bin/git -c push.negotiate=false push -q", "bash"], True),
        (['"C:\\Program Files\\Git\\mingw64\\bin\\git.exe" push origin x'], True),
        (["git fetch origin"], False),
        (["git -c push.default=simple fetch"], False),
        (["git pull", "git push"], False),  # the nearest git decides
        (["/bin/bash -c cd /repo && /usr/bin/git push"], False),
        (["node desktop-commander"], False),
    ],
    ids=[
        "push",
        "push-with-options",
        "windows",
        "fetch",
        "fetch-push-option",
        "pull",
        "shell",
        "no-git",
    ],
)
def test_only_a_git_push_is_a_push(ancestors, push) -> None:
    assert push_wait.is_git_push(ancestors) is push


def test_proc_ancestry_walks_up_to_init(tmp_path: Path) -> None:
    for pid, ppid in [(30, 20), (20, 10), (10, 1)]:
        (tmp_path / str(pid)).mkdir(exist_ok=True)
        (tmp_path / str(pid) / "stat").write_text(f"{pid} (name with) spaces) S {ppid} 0")
        (tmp_path / str(ppid)).mkdir(exist_ok=True)
    (tmp_path / "20" / "cmdline").write_bytes(b"node\0desktop-commander\0")
    (tmp_path / "10" / "cmdline").write_bytes(b"bash\0")
    (tmp_path / "1" / "cmdline").write_bytes(b"init\0")
    assert push_wait.proc_ancestry(30, tmp_path) == ["node desktop-commander", "bash", "init"]


def test_ps_ancestry_walks_up_to_init() -> None:
    table = {"30": ("20", ""), "20": ("1", "node desktop-commander"), "1": ("0", "launchd")}

    def run(command: list[str]) -> str:
        pid = command[-1]
        return table[pid][0] if command[2] == "ppid=" else table[pid][1]

    assert push_wait.ps_ancestry(30, run) == ["node desktop-commander", "launchd"]


class _Clock:
    def __init__(self) -> None:
        self.now = 0.0
        self.slept: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.now += seconds


def _direct(answer, pr: int, seconds: float):
    assert seconds > 0
    return answer(pr)


def _hold(answers: list) -> tuple[str, list[str], _Clock]:
    said: list[str] = []
    clock = _Clock()
    queue = list(answers)

    def answer(pr: int) -> tuple[str, list[str]]:
        assert pr == 7
        item = queue.pop(0) if len(queue) > 1 else queue[0]
        if isinstance(item, Exception):
            raise item
        return item

    result = push_wait.hold(7, SHA, answer, said.append, clock, clock.sleep, _direct)
    return result, said, clock


def test_green_releases_after_ci_finishes() -> None:
    pending = ci_diagnostics.ReportPending("not yet")
    result, said, clock = _hold([pending, pending, (SHA, [])])
    assert result == "green"
    assert said[-1].startswith("PRFAIL: no failures on aaaaaaa")
    assert said.count("PRFAIL: wait") == 2
    assert clock.slept == [push_wait.POLL_SECONDS] * 2


def test_failure_lines_are_handed_back_exactly() -> None:
    lines = ["##[error]Process completed with exit code 1.", "README.md:3: Typo"]
    result, said, _ = _hold([(SHA, lines)])
    assert result == "failed"
    assert said[1].startswith("PRFAIL: 2 line(s) to fix on aaaaaaa")
    assert said[2:] == lines


def test_a_report_for_the_previous_commit_is_not_the_answer() -> None:
    result, said, _ = _hold([(OLD, ["old failure"]), (SHA, [])])
    assert result == "green"
    assert "old failure" not in said


def test_twelve_minutes_without_an_answer_means_ci_is_stuck() -> None:
    result, said, clock = _hold([ci_diagnostics.ReportPending("never")])
    assert result == "timeout"
    assert push_wait.HOLD_SECONDS == 12 * 60
    assert clock.now == push_wait.HOLD_SECONDS
    assert "did not finish within 12 min" in said[-1]


def test_a_lookup_that_outlives_the_deadline_is_stuck() -> None:
    said: list[str] = []
    clock = _Clock()

    def never(answer, pr: int, seconds: float):
        assert seconds == push_wait.HOLD_SECONDS
        raise push_wait.AnswerTimeout("hung")

    result = push_wait.hold(7, SHA, None, said.append, clock, clock.sleep, never)
    assert result == "timeout"
    assert "did not finish within 12 min" in said[-1]


def test_within_stops_waiting_for_a_hung_lookup() -> None:
    release = threading.Event()

    def hung(pr: int):
        release.wait()
        return SHA, []

    try:
        with pytest.raises(push_wait.AnswerTimeout):
            push_wait.within(hung, 7, 0)
    finally:
        release.set()


def test_within_returns_or_raises_what_the_lookup_did() -> None:
    assert push_wait.within(lambda pr: (SHA, [str(pr)]), 7, 5) == (SHA, ["7"])
    with pytest.raises(ci_diagnostics.ReportPending):
        push_wait.within(_raise_pending, 7, 5)


def _raise_pending(pr: int):
    raise ci_diagnostics.ReportPending("not yet")


def test_an_error_releases_and_says_so() -> None:
    result, said, _ = _hold([ci_diagnostics.DiagnosticError("report digest mismatch")])
    assert result == "error"
    assert said[-1] == "PRFAIL: error: report digest mismatch. Stop and tell the owner."


GIT_PUSH = ["git push -u origin feature"]


def _main(argv, *, ancestors=GIT_PUSH + AGENT, pr=7, answer=None):
    said: list[str] = []
    clock = _Clock()
    calls: list[str] = []

    def pr_for(branch: str) -> int | None:
        calls.append(branch)
        return pr

    code = push_wait.main(
        argv,
        [_line(SHA, "refs/remotes/origin/feature")],
        {},
        ancestors=lambda: ancestors,
        local_sha={"feature": SHA}.get,
        pr_for=pr_for,
        answer=answer or (lambda n: (SHA, [])),
        say=said.append,
        clock=clock,
        sleep=clock.sleep,
    )
    return code, said, calls


def test_a_chatgpt_push_is_held_until_green() -> None:
    code, said, calls = _main(["committed"])
    assert (code, calls) == (0, ["feature"])
    assert said[-1].startswith("PRFAIL: no failures")


@pytest.mark.parametrize(
    ("argv", "ancestors"),
    [
        (["prepared"], GIT_PUSH + AGENT),
        (["committed"], [*GIT_PUSH, "/bin/bash"]),
        (["committed"], ["git fetch origin", *AGENT]),
    ],
    ids=["not-committed-yet", "a-person-pushed", "chatgpt-fetched"],
)
def test_other_pushes_return_at_once_without_asking_github(argv, ancestors) -> None:
    code, said, calls = _main(argv, ancestors=ancestors)
    assert (code, said, calls) == (0, [], [])


def test_a_branch_without_a_pull_request_is_not_held() -> None:
    code, said, _ = _main(["committed"], pr=None)
    assert code == 0
    assert said == ["PRFAIL: no single open pull request for feature; nothing to wait for."]


def test_the_hook_runs_push_wait_only_after_the_push_committed() -> None:
    hook = ROOT / ".githooks" / "reference-transaction"
    text = hook.read_text(encoding="utf-8")
    assert '[ "$1" = committed ] || exit 0' in text
    assert 'scripts/push_wait.py" "$@"' in text
    assert hook.stat().st_mode & stat.S_IXUSR
    installer = (ROOT / "scripts" / "install_push_wait_hook.sh").read_text(encoding="utf-8")
    assert "refusing:" in installer and "git rev-parse --git-path hooks" in installer


def test_a_second_prfail_answer_while_one_runs_is_wait(tmp_path, monkeypatch) -> None:
    import tempfile

    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))
    # The same lock prfail takes, so this holds on POSIX (fcntl) and Windows (msvcrt).
    with ci_diagnostics._single_flight(7):
        with pytest.raises(ci_diagnostics.PrfailBusy):
            ci_diagnostics.prfail_answer(7)
    assert os.path.exists(tmp_path / "tradebot-prfail-7.lock")
