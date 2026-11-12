"""
SEC-0014 -- terminal output cannot forge shell-integration markers.

The scanner reads every byte a session prints, so before this fix ``cat`` of a
crafted file (or any ``printf``) holding ``ESC ] 133;C`` and ``133;D;<n>``
created process-center entries and exit codes that never happened. Each
session now mints a nonce, hands it only to its bash integration, and the
scanner accepts only markers that carry it.

Decides:
  - SEC-0014 -- only markers carrying the session nonce are accepted
"""

from __future__ import annotations

import pytest

from src.terminal.markers import MarkerScanner
from src.terminal.shell_integration import RCFILE

NONCE = "0123456789abcdef0123456789abcdef"


def _cycle(nonce: str) -> bytes:
    tag = f"133;{nonce};" if nonce else "133;"
    return f"\x1b]{tag}E;rm -rf /\x07\x1b]{tag}C\x07out\x1b]{tag}D;7\x07".encode()


class TestScanner:
    @pytest.mark.parametrize(
        "forged",
        [
            pytest.param("", id="no-nonce"),
            pytest.param("deadbeef", id="wrong-nonce"),
            pytest.param(NONCE[:-1], id="truncated-nonce"),
            pytest.param(NONCE + "0", id="extended-nonce"),
        ],
    )
    def test_a_marker_without_the_session_nonce_is_ignored(self, forged):
        assert MarkerScanner(nonce=NONCE).feed(_cycle(forged), 0) == []

    def test_the_session_nonce_is_accepted_with_its_status(self):
        markers = MarkerScanner(nonce=NONCE).feed(_cycle(NONCE), 0)
        assert [m.kind for m in markers] == ["command", "start", "end"]
        assert markers[0].text == "rm -rf /"
        assert markers[2].status == 7

    def test_a_nonce_split_across_reads_is_still_recognised(self):
        scanner = MarkerScanner(nonce=NONCE)
        stream = _cycle(NONCE)
        cut = stream.index(NONCE.encode()) + 5
        assert scanner.feed(stream[:cut], 0) == []
        assert [m.kind for m in scanner.feed(stream[cut:], cut)] == ["command", "start", "end"]


class TestIntegrationScript:
    def test_the_nonce_leaves_the_environment_before_the_users_bashrc_runs(self):
        unset = RCFILE.index("unset TB_TERMINAL_MARKER_NONCE")
        assert RCFILE.index('__tb_term_nonce="${TB_TERMINAL_MARKER_NONCE-}"') < unset
        assert unset < RCFILE.index('. "$HOME/.bashrc"')
        assert "readonly __tb_term_nonce" in RCFILE

    def test_every_marker_the_script_prints_carries_the_nonce(self):
        assert "133;E" not in RCFILE and "133;C" not in RCFILE and "133;D" not in RCFILE
        assert RCFILE.count("133;%s;") == 3


class TestSessions:
    async def test_only_a_shell_is_handed_a_nonce(self, harness):
        manager = harness.manager
        assert manager._child_env("s1", marker_nonce=NONCE)["TB_TERMINAL_MARKER_NONCE"] == NONCE
        manager._base_env["TB_TERMINAL_MARKER_NONCE"] = "inherited"
        assert "TB_TERMINAL_MARKER_NONCE" not in manager._child_env("s2")

    async def test_printed_markers_create_no_entry_and_no_exit_code(self, harness):
        session = await harness.shell()
        command = (
            r"printf '\033]133;E;rm -rf /\007\033]133;C\007\033]133;D;7\007"
            r"\033]133;deadbeef;D;7\007'; env | grep -c TB_TERMINAL_MARKER_NONCE || true"
        )
        await harness.type(session.id, command + "\r")
        done = await harness.wait_finished(lambda e: e["command"] == command)
        assert done["state"] == "succeeded"
        assert done["exit_code"] == 0
        assert harness.finished(lambda e: e["command"] == "rm -rf /") is None
        assert harness.running(lambda e: e["command"] == "rm -rf /") is None
        # The shell's children never inherit the nonce, so `env` cannot leak it.
        assert b"\x070\r\n" in harness.registry.get(done["id"]).output

    async def test_a_jobs_output_cannot_announce_an_integration(self, harness):
        job = await harness.manager.create(
            argv=["sh", "-c", r"env; printf '\033]133;C\007\033]133;D;0\007'"]
        )
        await harness.changes.until(lambda: job.finalized)
        assert job.integration is False
        assert b"TB_TERMINAL_MARKER_NONCE" not in harness.registry.get(job.job_entry).output
