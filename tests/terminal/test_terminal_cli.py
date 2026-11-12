"""
TERM-007, TERM-008 -- the host CLI and the daemon lifecycle commands.

`tradebot-term` is a second client of the same daemon the dashboard uses, so
these tests run the real CLI functions against a real daemon (in a thread,
because the CLI's client blocks) and check the two directions of sharing: a
session made here is the daemon's session, and a job run here reports the
exit status the job really had -- including 128+N for a signal, as a shell
would. Attaching never stops a session; the terminal is restored however the
attach ends.

Decides:
  - SEC-1224 -- see config/quality_registry.json
  - TERM-007 -- the host CLI lists, creates, attaches to, inspects and detaches
  - TERM-008 -- install, start and stop never clobber and never orphan
  - REG-0025 -- attach closes only after the daemon has applied what it sent

Decides:
  - REG-1494 — Terminal CLI stop/pid/tail are safe

Decides: SEC-1231
"""

from __future__ import annotations

import base64
import io
import json
import os
import pty
import re
import runpy
import signal
import socket
import termios
import time
from pathlib import Path

import pytest

from src.terminal import cli, install
from src.terminal.client import TerminalClient, TerminalClientError

from ._support import WAIT_S, ThreadedDaemon


def run_cli(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    code = cli.main(list(argv), out=out)
    return code, out.getvalue()


def wait_for_output(socket_path: Path, sid: str, needle: bytes) -> bytes:
    with TerminalClient(socket_path, timeout=WAIT_S).connect() as client:
        client.request("session.attach", sid=sid)
        seen = b""
        deadline = time.monotonic() + WAIT_S
        while needle not in seen:
            frame = client.recv(max(0.1, deadline - time.monotonic()))
            assert frame is not None, "connection closed"
            if frame["t"] == "output" and frame["sid"] == sid:
                seen += base64.b64decode(frame["data"])
        return seen


class TestDaemonStatus:
    def test_status_of_a_running_daemon(self, threaded_daemon):
        code, out = run_cli("status")
        assert code == 0
        assert f"running pid={os.getpid()}" in out and "sessions=0" in out
        _, out = run_cli("status", "--json")
        status = json.loads(out)
        assert status["running"] is True and status["outdated"] is False

    def test_status_when_nothing_runs(self, monkeypatch, short_tmp):
        monkeypatch.setenv("TB_TERMINAL_RUNTIME_DIR", str(short_tmp))
        assert run_cli("status") == (cli.EXIT_NOT_RUNNING, "terminal service is not running\n")
        _, out = run_cli("status", "--json")
        assert json.loads(out) == {"running": False}
        code, _ = run_cli("ls")
        assert code == cli.EXIT_NOT_RUNNING

    def test_start_reports_the_running_daemon(self, threaded_daemon):
        code, out = run_cli("start", "--json")
        info = json.loads(out)
        assert code == 0
        assert info["socket"] == str(threaded_daemon.config.socket_path)
        assert info["pid"] == os.getpid() and info["ws_url"] is None
        assert run_cli("start", "--quiet") == (0, "")
        assert "terminal service running" in run_cli("start")[1]

    def test_a_reported_older_version_is_flagged(self, threaded_daemon, monkeypatch):
        monkeypatch.setattr(cli, "SERVICE_VERSION", "9.9.9")
        _, out = run_cli("status")
        assert "tradebot-term restart" in out


class TestSessionsFromTheCli:
    def test_a_cli_session_is_the_daemons_session(self, threaded_daemon, short_tmp):
        code, out = run_cli("new", "--name", "cli-one", "--cwd", str(short_tmp))
        sid = out.strip()
        assert code == 0 and re.fullmatch(r"s-[0-9a-f]{8}", sid)
        described = threaded_daemon.server.manager.describe(sid)
        assert (described["name"], described["cwd"]) == ("cli-one", str(short_tmp))

        _, listing = run_cli("ls")
        assert sid in listing and "cli-one" in listing
        assert json.loads(run_cli("ls", "--json")[1])[0]["id"] == sid

        assert run_cli("send", "cli-one", "echo", "via-cli-$((3*3))")[0] == 0
        wait_for_output(threaded_daemon.config.socket_path, sid, b"via-cli-9")
        _, text = run_cli("output", "cli-one", "--plain")
        assert "via-cli-9" in text and "\x1b]133" not in text
        _, tail = run_cli("output", sid, "--tail", "5")
        assert len(tail) <= 5

        assert run_cli("rename", sid, "renamed")[0] == 0
        assert "renamed" in run_cli("ls")[1]
        code, out = run_cli("kill", "renamed", "--signal", "INT")
        assert code == 0 and out.startswith("signalled process group")
        assert run_cli("close", "renamed") == (0, f"closed {sid}\n")
        assert sid not in run_cli("ls")[1]

    def test_names_must_be_unambiguous(self, threaded_daemon, capsys):
        run_cli("new", "--name", "twin")
        run_cli("new", "--name", "twin")
        code, _ = run_cli("send", "twin", "x")
        assert code == 1
        assert "no unique session named 'twin'" in capsys.readouterr().err


class TestJobsFromTheCli:
    def test_run_wait_returns_the_jobs_own_status(self, threaded_daemon, short_tmp, monkeypatch):
        monkeypatch.chdir(short_tmp)
        argv = ["sh", "-c", "echo job-out; pwd; exit 5"]
        code, out = run_cli("run", "--wait", "--name", "five", "--", *argv)
        assert code == 5
        assert "job-out" in out and str(short_tmp) in out
        status = run_cli("run", "--wait", "--", "sh", "-c", "kill -TERM $$")[0]
        assert status == 128 + signal.SIGTERM

    def test_ps_and_output_show_the_recorded_result(self, threaded_daemon):
        run_cli("run", "--wait", "--", "sh", "-c", "echo recorded; exit 7")
        processes = json.loads(run_cli("ps", "--json")[1])
        (entry,) = [p for p in processes["history"] if "exit 7" in p["title"]]
        assert entry["exit_code"] == 7
        assert "exit 7" not in run_cli("ps")[1]
        assert "failed" in run_cli("ps", "--all")[1]
        _, detail = run_cli("output", entry["id"])
        assert detail.startswith(f"[{entry['id']} failed exit=7")
        assert "recorded" in detail
        assert not run_cli("output", entry["id"], "--plain")[1].startswith("[")

    def test_run_without_wait_returns_immediately_and_kill_stops_it(self, threaded_daemon):
        code, out = run_cli("run", "--", "sleep", "30")
        sid, job_id = out.split()
        assert code == 0 and job_id.startswith("p-")
        assert "sleep 30" in run_cli("ps")[1]
        with TerminalClient(threaded_daemon.config.socket_path).connect() as watcher:
            assert run_cli("kill", job_id)[0] == 0
            while True:
                frame = watcher.recv(WAIT_S)
                assert frame is not None
                if frame["t"] == "process_done" and frame["process"]["id"] == job_id:
                    assert frame["process"]["signal"] == "SIGTERM"
                    break
        assert threaded_daemon.server.manager.describe(sid)["signal"] == "SIGTERM"

    def test_run_needs_a_command(self, threaded_daemon, capsys):
        assert run_cli("run")[0] == 1
        assert "nothing to run" in capsys.readouterr().err


class TestAttach:
    def _session(self, socket_path: Path, **fields) -> str:
        with TerminalClient(socket_path).connect() as client:
            return client.request("session.create", **fields)["session"]["id"]

    def test_piped_input_runs_then_detaches(self, threaded_daemon, tmp_path):
        sid = self._session(threaded_daemon.config.socket_path)
        read_end, write_end = os.pipe()
        os.write(write_end, b"echo piped-$((5*5))\n")
        os.close(write_end)
        out_path = tmp_path / "out"
        out_fd = os.open(out_path, os.O_WRONLY | os.O_CREAT, 0o600)
        try:
            with TerminalClient(threaded_daemon.config.socket_path).connect() as client:
                assert cli.attach(client, sid, stdin_fd=read_end, stdout_fd=out_fd) == 0
        finally:
            os.close(read_end)
            os.close(out_fd)
        text = out_path.read_text(encoding="utf-8", errors="replace")
        assert f"[detached from {sid}; it keeps running]" in text
        wait_for_output(threaded_daemon.config.socket_path, sid, b"piped-25")
        assert threaded_daemon.server.manager.describe(sid)["state"] == "running"

    def test_attach_closes_only_after_its_detach_is_answered(self, tmp_path):
        # REG-0025: attach sent its keystrokes and detach without waiting and
        # closed. With frames still unread on its side, Linux reset the
        # daemon's end and asyncio dropped the requests it had not read yet:
        # the typed line never reached the shell. A detach that is answered
        # proves everything sent before it was applied.
        calls: list[tuple[str, str]] = []
        sock, peer = socket.socketpair()

        class Recorder:
            def __init__(self) -> None:
                self.sock = sock

            def request(self, kind: str, **_fields: object) -> dict:
                calls.append(("request", kind))
                return {"t": "ok"}

            def send(self, frame: dict) -> None:
                calls.append(("send", frame["t"]))

            def pop_events(self) -> list:
                return []

            def has_buffered_frame(self) -> bool:
                return False

        read_end, write_end = os.pipe()
        os.write(write_end, b"echo typed\n" + cli.DETACH_BYTE)
        os.close(write_end)
        out_fd = os.open(tmp_path / "out", os.O_WRONLY | os.O_CREAT, 0o600)
        try:
            assert cli.attach(Recorder(), "s-00000000", stdin_fd=read_end, stdout_fd=out_fd) == 0
        finally:
            for closable in (sock, peer):
                closable.close()
            for fd in (read_end, out_fd):
                os.close(fd)
        assert calls == [
            ("request", "session.attach"),
            ("send", "session.input"),
            ("request", "session.detach"),
        ]

    def test_a_tty_is_put_back_exactly_as_it_was(self, threaded_daemon, tmp_path):
        sid = self._session(threaded_daemon.config.socket_path)
        master, slave = pty.openpty()
        before = termios.tcgetattr(slave)
        handler = signal.getsignal(signal.SIGWINCH)
        out_fd = os.open(tmp_path / "out", os.O_WRONLY | os.O_CREAT, 0o600)
        try:
            os.write(master, b"echo tty-attach\r" + cli.DETACH_BYTE)
            with TerminalClient(threaded_daemon.config.socket_path).connect() as client:
                assert cli.attach(client, sid, stdin_fd=slave, stdout_fd=out_fd) == 0
            assert termios.tcgetattr(slave) == before
            assert signal.getsignal(signal.SIGWINCH) == handler
        finally:
            for fd in (master, slave, out_fd):
                os.close(fd)
        wait_for_output(threaded_daemon.config.socket_path, sid, b"tty-attach\r\n")

    def test_attach_ends_when_the_session_does(self, threaded_daemon, tmp_path):
        argv = ["sh", "-c", "read x; echo bye-$x"]
        sid = self._session(threaded_daemon.config.socket_path, argv=argv)
        read_end, write_end = os.pipe()
        os.write(write_end, b"now\n")
        out_path = tmp_path / "out"
        out_fd = os.open(out_path, os.O_WRONLY | os.O_CREAT, 0o600)
        try:
            with TerminalClient(threaded_daemon.config.socket_path).connect() as client:
                assert cli.attach(client, sid, stdin_fd=read_end, stdout_fd=out_fd) == 0
        finally:
            for fd in (read_end, write_end, out_fd):
                os.close(fd)
        text = out_path.read_text(encoding="utf-8", errors="replace")
        assert "bye-now" in text and "[session ended]" in text

    def test_a_session_cannot_be_attached_to_itself(self, threaded_daemon, monkeypatch):
        sid = self._session(threaded_daemon.config.socket_path)
        monkeypatch.setenv("TB_TERMINAL_SESSION_ID", sid)
        client = TerminalClient(threaded_daemon.config.socket_path).connect()
        with client, pytest.raises(cli.CliError):
            cli.attach(client, sid, stdin_fd=0, stdout_fd=1)

    def test_a_vanished_service_ends_the_attach(self, tmp_path):
        ours, theirs = socket.socketpair(socket.AF_UNIX)

        class GoneClient:
            sock = ours

            def request(self, *_args, **_kwargs):
                return {}

            def send(self, frame):
                raise TerminalClientError("gone")

            def pop_events(self):
                return iter(())

            def has_buffered_frame(self):
                return False

            def recv(self, _timeout):
                return None

        theirs.close()
        read_end, write_end = os.pipe()
        out_fd = os.open(tmp_path / "out", os.O_WRONLY | os.O_CREAT, 0o600)
        try:
            assert cli.attach(GoneClient(), "s-00000001", stdin_fd=read_end, stdout_fd=out_fd) == 1
        finally:
            for fd in (read_end, write_end, out_fd):
                os.close(fd)
            ours.close()
        assert "closed the connection" in (tmp_path / "out").read_text(encoding="utf-8")

    def test_the_attach_commands_resolve_their_session(self, threaded_daemon, monkeypatch):
        calls = []
        monkeypatch.setattr(cli, "attach", lambda client, sid, **_: calls.append(sid) or 0)
        code, out = run_cli("new", "--name", "attach-me", "--attach")
        sid = out.strip()
        assert code == 0 and calls == [sid]
        assert run_cli("attach", "attach-me")[0] == 0
        assert calls == [sid, sid]


class TestSetupCommands:
    def test_token_and_paths(self, monkeypatch, short_tmp):
        monkeypatch.setenv("TB_TERMINAL_RUNTIME_DIR", str(short_tmp / "rt"))
        monkeypatch.setenv("TB_TERMINAL_STATE_DIR", str(short_tmp / "st"))
        first = run_cli("token")[1].strip()
        assert len(first) == 64
        assert run_cli("token")[1].strip() == first
        assert run_cli("token", "--rotate")[1].strip() != first
        paths = json.loads(run_cli("paths", "--json")[1])
        assert paths["socket"] == str(short_tmp / "rt" / "termd.sock")
        assert "token: " in run_cli("paths")[1]

    def test_install_and_uninstall_touch_only_their_own_files(self, monkeypatch, short_tmp):
        home = short_tmp / "home"
        home.mkdir()
        monkeypatch.setenv("HOME", str(home))
        monkeypatch.setenv("XDG_CONFIG_HOME", str(home / ".config"))
        monkeypatch.setenv("TB_TERMINAL_RUNTIME_DIR", str(short_tmp / "rt"))
        monkeypatch.setenv("TB_TERMINAL_STATE_DIR", str(short_tmp / "st"))
        code, out = run_cli("install", "--no-systemd")
        wrapper = home / ".local" / "bin" / "tradebot-term"
        assert code == 0 and f"wrote {wrapper}" in out
        assert "note: systemd unit skipped" in out
        assert "up to date" in run_cli("install", "--no-systemd")[1]
        code, out = run_cli("uninstall", "--purge")
        assert code == 0 and f"removed {wrapper}" in out
        assert not wrapper.exists()

    def test_a_conflicting_file_fails_the_install(self, monkeypatch, short_tmp, capsys):
        home = short_tmp / "home"
        (home / ".local" / "bin").mkdir(parents=True)
        wrapper = home / ".local" / "bin" / "tradebot-term"
        wrapper.write_text("#!/bin/sh\necho mine\n", encoding="utf-8")
        monkeypatch.setenv("HOME", str(home))
        assert run_cli("install", "--no-systemd")[0] == 1
        assert "conflict:" in capsys.readouterr().err


class TestLifecycleHelpers:
    def test_ensure_running_starts_a_missing_daemon(self, config, short_tmp):
        started: list[ThreadedDaemon] = []
        try:
            welcome = cli.ensure_running(
                config,
                spawn=lambda cfg: started.append(ThreadedDaemon(cfg, short_tmp).start()),
                env={"HOME": str(short_tmp)},
            )
            assert welcome["server_pid"] == os.getpid() and len(started) == 1
            # Already running: nothing is spawned again.
            cli.ensure_running(config, spawn=lambda cfg: pytest.fail("spawned twice"))
        finally:
            for d in started:
                d.shutdown()

    def test_ensure_running_prefers_the_installed_user_unit(self, config, short_tmp, monkeypatch):
        home = short_tmp / "home"
        unit = home / ".config" / "systemd" / "user" / install.UNIT_NAME
        unit.parent.mkdir(parents=True)
        unit.write_text(f"# {install.MARKER}\n", encoding="utf-8")
        monkeypatch.setattr(install.shutil, "which", lambda name: "/usr/bin/systemctl")
        started: list[ThreadedDaemon] = []
        commands: list[list[str]] = []

        def run(argv):
            commands.append(argv)
            if argv[-2:] == ["start", install.UNIT_NAME]:
                started.append(ThreadedDaemon(config, short_tmp).start())
            return 0

        try:
            cli.ensure_running(
                config,
                run=run,
                spawn=lambda cfg: pytest.fail("not via systemd"),
                env={"HOME": str(home)},
            )
            assert ["systemctl", "--user", "start", install.UNIT_NAME] in commands
        finally:
            for d in started:
                d.shutdown()

    def test_ensure_running_gives_up_with_a_pointer_to_the_log(self, config):
        with pytest.raises(cli.CliError, match="did not come up"):
            cli.ensure_running(
                config, spawn=lambda cfg: None, timeout_s=0.05, env={"HOME": str(config.state_dir)}
            )

    def test_stop_signals_only_our_own_daemon(self, config, short_tmp, tmp_path):
        assert cli.stop_daemon(config) is False
        d = ThreadedDaemon(config, short_tmp).start()
        proc = tmp_path / "proc"
        (proc / str(os.getpid())).mkdir(parents=True)
        (proc / str(os.getpid()) / "cmdline").write_bytes(b"python\x00-m\x00pytest\x00")
        try:
            with pytest.raises(cli.CliError, match="pid file"):
                cli.stop_daemon(config, run=lambda argv: 3, proc=proc)
            cmdline = proc / str(os.getpid()) / "cmdline"
            cmdline.write_bytes(b"python\x00-m\x00src.terminal\x00daemon\x00")
            signalled = []

            def kill(pid, signum):
                signalled.append((pid, signum))
                # The fake /proc entry models the daemon process exiting.
                cmdline.unlink()
                d.loop.call_soon_threadsafe(d.stop.set)

            assert cli.stop_daemon(config, run=lambda argv: 3, kill=kill, proc=proc) is True
            assert signalled == [(os.getpid(), signal.SIGTERM)]
            assert not config.socket_path.exists()
        finally:
            d.shutdown()

    def test_stop_goes_through_systemd_when_the_unit_is_active(self, config, short_tmp):
        d = ThreadedDaemon(config, short_tmp).start()
        commands = []
        unit_active = True

        def run(argv):
            nonlocal unit_active
            commands.append(argv)
            if argv[-1] == install.UNIT_NAME and argv[2] == "stop":
                unit_active = False
                d.loop.call_soon_threadsafe(d.stop.set)
                return 0
            if argv[-1] == install.UNIT_NAME and argv[2] == "is-active":
                return 0 if unit_active else 3
            return 0

        try:
            assert cli.stop_daemon(config, run=run) is True
            assert ["systemctl", "--user", "stop", install.UNIT_NAME] in commands
        finally:
            d.shutdown()

    def test_stop_restart_and_daemon_commands(self, monkeypatch, short_tmp, capsys):
        monkeypatch.setenv("TB_TERMINAL_RUNTIME_DIR", str(short_tmp))
        monkeypatch.setattr(cli, "stop_daemon", lambda cfg: True)
        monkeypatch.setattr(cli, "ensure_running", lambda cfg: {"server_pid": 4242})
        assert run_cli("stop") == (0, "terminal service stopped\n")
        assert run_cli("restart") == (0, "terminal service restarted (pid 4242)\n")
        monkeypatch.setattr(cli, "stop_daemon", lambda cfg: False)
        assert run_cli("stop") == (0, "terminal service was not running\n")

        import src.terminal.server as server_module

        monkeypatch.setattr(cli, "_configure_daemon_logging", lambda: None)
        seen = []

        async def fake_daemon(config, *, allow_root):
            seen.append(allow_root)

        monkeypatch.setattr(server_module, "run_daemon", fake_daemon)
        assert run_cli("daemon", "--allow-root") == (0, "")
        assert seen == [True]

        async def refusing(config, *, allow_root):
            raise server_module.DaemonError("already running")

        monkeypatch.setattr(server_module, "run_daemon", refusing)
        assert run_cli("daemon")[0] == 1
        assert "already running" in capsys.readouterr().err

    def test_daemon_logging_redacts(self, monkeypatch):
        import structlog

        from src.logging_setup import redact_event

        captured = {}
        monkeypatch.setattr(structlog, "configure", lambda **kwargs: captured.update(kwargs))
        cli._configure_daemon_logging()
        assert redact_event in captured["processors"]

    def test_spawn_detached_starts_a_new_session_and_rotates_the_log(self, config, monkeypatch):
        config.log_path.write_bytes(b"x" * 10)
        monkeypatch.setattr(cli, "LOG_ROTATE_BYTES", 5)
        monkeypatch.setenv("PYTHONPATH", "/elsewhere")
        launched = {}

        def fake_popen(argv, **kwargs):
            launched.update(argv=argv, **kwargs)

        monkeypatch.setattr(cli.subprocess, "Popen", fake_popen)
        cli._spawn_detached(config)
        assert launched["argv"][1:] == ["-m", "src.terminal", "daemon"]
        assert launched["start_new_session"] is True
        assert launched["env"]["PYTHONPATH"].endswith(os.pathsep + "/elsewhere")
        assert config.log_path.stat().st_size == 0

    def test_spawn_detached_does_not_pass_secrets_to_the_daemon(self, config, monkeypatch):
        """AGT-023: the daemon used to inherit the caller's whole environment."""
        monkeypatch.setenv("BINANCE_API_SECRET", "s3cret")
        monkeypatch.setenv("OPERATOR_SECRET", "op")
        monkeypatch.setenv("TB_TERMINAL_API_TOKEN", "tok")
        monkeypatch.setenv("UNRELATED_VAR", "x")
        monkeypatch.setenv("PATH", "/usr/bin")
        launched = {}
        monkeypatch.setattr(cli.subprocess, "Popen", lambda argv, **kw: launched.update(kw))
        cli._spawn_detached(config)
        env = launched["env"]
        assert env["PATH"] == "/usr/bin"
        leaked = {"BINANCE_API_SECRET", "OPERATOR_SECRET", "TB_TERMINAL_API_TOKEN", "UNRELATED_VAR"}
        assert not leaked & set(env)

    def test_session_manager_default_environment_is_scrubbed(self, monkeypatch):
        from src.terminal.config import scrubbed_environment

        monkeypatch.setenv("EXCHANGE_API_KEY", "k")
        monkeypatch.setenv("LANG", "C.UTF-8")
        env = scrubbed_environment()
        assert "EXCHANGE_API_KEY" not in env
        assert env["LANG"] == "C.UTF-8"

    def test_session_manager_scrubs_explicit_environment(self, tmp_path):
        from src.terminal.config import TerminalConfig
        from src.terminal.registry import ProcessRegistry
        from src.terminal.sessions import SessionManager

        manager = SessionManager(
            TerminalConfig.from_env({}),
            ProcessRegistry(history_limit=10, output_limit=1024),
            base_env={
                "PATH": "/usr/bin",
                "HOME": str(tmp_path),
                "LANG": "C.UTF-8",
                "BINANCE_API_SECRET": "must-not-reach-pty",
                "OPERATOR_SECRET": "must-not-reach-pty",
                "UNRELATED_VAR": "must-not-reach-pty",
            },
        )
        child_env = manager._child_env("s-12345678")
        assert child_env["PATH"] == "/usr/bin"
        assert child_env["HOME"] == str(tmp_path)
        assert "BINANCE_API_SECRET" not in child_env
        assert "OPERATOR_SECRET" not in child_env
        assert "UNRELATED_VAR" not in child_env


class TestHelpers:
    @pytest.mark.parametrize(
        ("seconds", "text"), [(None, "-"), (5.9, "0:05"), (125, "2:05"), (3725, "1:02:05")]
    )
    def test_elapsed(self, seconds, text):
        assert cli._elapsed(seconds) == text

    @pytest.mark.parametrize(
        ("count", "text"),
        [(None, "-"), (512, "512B"), (2048, "2.0K"), (3 << 20, "3.0M"), (5 << 40, "5120.0G")],
    )
    def test_bytes(self, count, text):
        assert cli._bytes(count) == text

    @pytest.mark.parametrize(("name", "number"), [("SIGKILL", 9), ("SIG77", 77), ("SIGWHAT", 0)])
    def test_signal_number(self, name, number):
        assert cli.signal_number(name) == number

    def test_a_bad_environment_is_reported_not_raised(self, monkeypatch, capsys):
        monkeypatch.setenv("TB_TERMINAL_WS_HOST", "0.0.0.0")
        assert run_cli("paths")[0] == 1
        assert "non-loopback" in capsys.readouterr().err

    def test_python_m_runs_the_cli_and_exits_with_its_code(self, monkeypatch):
        # runpy re-executes __main__, which binds whatever src.terminal.cli
        # exposes as main at that moment, so the patch is what it calls.
        calls = []

        def fake_main(*args, **kwargs):
            calls.append((args, kwargs))
            return 3

        monkeypatch.setattr(cli, "main", fake_main)
        with pytest.raises(SystemExit) as exc_info:
            runpy.run_module("src.terminal", run_name="__main__")
        assert exc_info.value.code == 3
        assert calls == [((), {})]


class TestClient:
    def test_an_absent_service_is_a_clear_error(self, short_tmp):
        with pytest.raises(TerminalClientError) as exc_info:
            TerminalClient(short_tmp / "absent.sock").connect()
        assert exc_info.value.code == "unavailable"

    def test_a_refused_request_raises_with_its_code(self, threaded_daemon):
        with TerminalClient(threaded_daemon.config.socket_path).connect() as client:
            with pytest.raises(TerminalClientError) as exc_info:
                client.request("session.close", sid="s-00000000")
            assert exc_info.value.code == "not_found"
            client.sock.sendall(b"{not json\n")  # answered by an id-less error
            with pytest.raises(TerminalClientError):
                client.request("ping")
        client.close()

    def test_an_unconnected_client_refuses_to_send_or_receive(self, short_tmp):
        client = TerminalClient(short_tmp / "x.sock")
        with pytest.raises(TerminalClientError):
            client.send({"t": "ping"})
        with pytest.raises(TerminalClientError):
            client.recv(0.1)


class TestPhase6Lows:
    """AGT-026/027/028: pid-file targeting, stop timeout and --tail validation."""

    def test_daemon_pid_rejects_another_cli_invocation(self, config, tmp_path):
        config.pid_path.parent.mkdir(parents=True, exist_ok=True)
        config.pid_path.write_text(f"{os.getpid()}\n")
        proc = tmp_path / "proc"
        (proc / str(os.getpid())).mkdir(parents=True)
        (proc / str(os.getpid()) / "cmdline").write_bytes(b"python\x00-m\x00src.terminal\x00ls\x00")
        assert cli._daemon_pid(config, proc) is None

    def test_stop_reports_a_daemon_that_never_exits(self, config, short_tmp, tmp_path):
        d = ThreadedDaemon(config, short_tmp).start()
        proc = tmp_path / "proc"
        (proc / str(os.getpid())).mkdir(parents=True)
        (proc / str(os.getpid()) / "cmdline").write_bytes(
            b"python\x00-m\x00src.terminal\x00daemon\x00"
        )
        try:
            with pytest.raises(cli.CliError, match="did not stop"):
                cli.stop_daemon(
                    config,
                    run=lambda argv: 3,
                    # Simulate the socket disappearing before the daemon exits.
                    kill=lambda p, s: config.socket_path.unlink(),
                    proc=proc,
                    timeout_s=0.2,
                )
        finally:
            d.shutdown()

    @pytest.mark.parametrize("tail", [0, -3])
    def test_non_positive_tail_is_rejected(self, config, tail):
        import argparse
        import io

        with pytest.raises(cli.CliError, match="--tail"):
            cli.cmd_output(
                config, argparse.Namespace(target="x", tail=tail, plain=False), io.StringIO()
            )


def test_daemon_pid_rejects_a_non_integer_pid_file(config):
    config.pid_path.parent.mkdir(parents=True, exist_ok=True)
    config.pid_path.write_text("not-a-pid", encoding="utf-8")
    assert cli._daemon_pid(config) is None


def test_collect_session_output_uses_matching_buffered_frames():
    import base64

    class Client:
        timeout = 0.01

        def __init__(self):
            self.requests = []

        def request(self, name, **_fields):
            self.requests.append(name)
            return {"offset": 0, "end": 3} if name == "session.attach" else {}

        def pop_events(self):
            return [
                {
                    "t": "output",
                    "sid": "sid",
                    "offset": 0,
                    "data": base64.b64encode(b"abc").decode(),
                }
            ]

        def recv(self, *_args):
            return None

    client = Client()
    assert cli._collect_session_output(client, "sid") == b"abc"
    assert client.requests == ["session.attach", "session.detach"]


def test_collect_session_output_stops_when_the_connection_closes():
    class Client:
        timeout = 0.01

        def __init__(self):
            self.requests = []

        def request(self, name, **_fields):
            self.requests.append(name)
            return {"offset": 0, "end": 1} if name == "session.attach" else {}

        def pop_events(self):
            return []

        def recv(self, *_args):
            return None

    client = Client()
    assert cli._collect_session_output(client, "sid") == b""
    assert client.requests == ["session.attach", "session.detach"]


def test_terminal_size_clamps_zero_dimensions(monkeypatch):
    monkeypatch.setattr(cli.os, "get_terminal_size", lambda _fd: cli.os.terminal_size((0, 0)))
    assert cli._terminal_size(1) == (1, 1)


def test_new_omits_optional_name_and_cwd_fields(config, monkeypatch):
    import argparse
    import io

    class Client:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def request(self, name, **fields):
            self.requested = (name, fields)
            return {"session": {"id": "sid"}}

    client = Client()
    monkeypatch.setattr(cli, "_client", lambda _config: client)
    monkeypatch.setattr(cli, "_terminal_size", lambda _fd: (24, 80))

    result = cli.cmd_new(
        config,
        argparse.Namespace(name=None, cwd=None, attach=False),
        io.StringIO(),
    )

    assert result == 0
    assert client.requested == ("session.create", {"rows": 24, "cols": 80})


def test_attach_exits_when_the_daemon_removes_the_session(monkeypatch, tmp_path):
    import os
    import socket

    sock, peer = socket.socketpair()
    stdin_fd, stdin_write = os.pipe()
    os.close(stdin_write)
    output_fd = os.open(tmp_path / "output", os.O_WRONLY | os.O_CREAT, 0o600)

    class Client:
        def __init__(self):
            self.sock = sock
            self.requests = []

        def request(self, name, **_fields):
            self.requests.append(name)
            return {}

        def pop_events(self):
            return [{"t": "session_removed", "id": "sid"}]

        def has_buffered_frame(self):
            return False

        def recv(self, *_args):
            return None

        def send(self, _frame):
            raise AssertionError("no input should be sent after session removal")

    client = Client()
    monkeypatch.setattr(cli, "_drain", lambda *_args, **_kwargs: None)
    monkeypatch.delenv("TB_TERMINAL_SESSION_ID", raising=False)
    try:
        assert cli.attach(client, "sid", stdin_fd=stdin_fd, stdout_fd=output_fd) == 0
        assert client.requests == ["session.attach", "session.detach"]
    finally:
        os.close(stdin_fd)
        os.close(output_fd)
        sock.close()
        peer.close()


def test_attach_detach_key_without_preceding_input_sends_no_empty_frame(
    monkeypatch, tmp_path
):
    import os
    import socket

    stdin_fd, stdin_write = os.pipe()
    os.write(stdin_write, cli.DETACH_BYTE)
    os.close(stdin_write)
    output_fd = os.open(tmp_path / "output", os.O_WRONLY | os.O_CREAT, 0o600)
    sock, peer = socket.socketpair()

    class Client:
        def __init__(self):
            self.sock = sock
            self.requests = []
            self.sent = []

        def request(self, name, **_fields):
            self.requests.append(name)
            return {}

        def pop_events(self):
            return []

        def has_buffered_frame(self):
            return False

        def recv(self, *_args):
            return None

        def send(self, frame):
            self.sent.append(frame)

    client = Client()
    monkeypatch.setattr(cli.select, "select", lambda *_args: ([stdin_fd], [], []))
    monkeypatch.delenv("TB_TERMINAL_SESSION_ID", raising=False)
    try:
        assert cli.attach(client, "sid", stdin_fd=stdin_fd, stdout_fd=output_fd) == 0
        assert client.sent == []
        assert client.requests == ["session.attach", "session.detach"]
    finally:
        os.close(stdin_fd)
        os.close(output_fd)
        sock.close()
        peer.close()


def test_drain_returns_when_the_socket_closes(monkeypatch):
    sock = object()

    class Client:
        def __init__(self):
            self.sock = sock

        def has_buffered_frame(self):
            return False

        def recv(self, *_args):
            return None

    monkeypatch.setattr(cli.select, "select", lambda *_args: ([sock], [], []))
    cli._drain(Client(), "sid", 1, quiet_s=0.0)


def test_run_returns_an_exit_status_already_in_the_event_queue(config, monkeypatch):
    import argparse
    import io

    class Client:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def request(self, _name, **_fields):
            return {"session": {"id": "sid", "job_entry": "job"}}

        def pop_events(self):
            return [
                {
                    "t": "process_done",
                    "process": {"id": "job", "signal": None, "exit_code": 7},
                }
            ]

        def recv(self, *_args):
            raise AssertionError("the buffered completion should be consumed first")

    monkeypatch.setattr(cli, "_client", lambda _config: Client())
    monkeypatch.setattr(cli, "_terminal_size", lambda _fd: (24, 80))
    result = cli.cmd_run(
        config,
        argparse.Namespace(command=["true"], cwd=None, name=None, wait=True),
        io.StringIO(),
    )
    assert result == 7


def test_run_raises_when_the_service_closes_before_process_completion(config, monkeypatch):
    import argparse
    import io

    class Client:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def request(self, _name, **_fields):
            return {"session": {"id": "sid", "job_entry": "job"}}

        def pop_events(self):
            return []

        def recv(self, *_args):
            return None

    monkeypatch.setattr(cli, "_client", lambda _config: Client())
    monkeypatch.setattr(cli, "_terminal_size", lambda _fd: (24, 80))
    with pytest.raises(cli.CliError, match="closed the connection"):
        cli.cmd_run(
            config,
            argparse.Namespace(command=["true"], cwd=None, name=None, wait=True),
            io.StringIO(),
        )
