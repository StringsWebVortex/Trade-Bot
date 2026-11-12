"""Regression tests for the phase-4 CI / infrastructure audit findings.

Decides:
  - REG-1260 — A placeholder deployment cannot report success (OPS-003)
  - SEC-1261 — main requires an approving code-owner review (OPS-004)
  - SEC-1262 — Compose services are hardened and ship no default DB password (OPS-005, OPS-006)
  - REG-1263 — Risk limits agree between risk.yaml and .env.example (OPS-007)
  - SEC-1264 — The supply-chain gate analyses secrets and permissions per job (OPS-016, SCR-002)
  - SEC-1265 — Diagnostics reports must come from the collector workflow run (OPS-017)
  - REG-1266 — Horizon-gated ordering defaults to off (OPS-019)
  - SEC-1267 — Every credentialed venue needs a key-posture declaration (SCR-004)
  - REG-1268 — Mutation scores are read from the pinned mutmut cache (SCR-003)
  - REG-1269 — math_registry consumer rows are real imports (SCR-005)
  - SEC-1270 — command_policy has no dead sections and guards all .env readers (SCR-006)
  - REG-1271 — Execution/risk arch-baseline findings are tracked in the registry (OPS-018)
"""

from __future__ import annotations

import json
import re
import sqlite3
import textwrap
from pathlib import Path

import pytest
import yaml

from scripts import check_mutation_score, ci_diagnostics
from scripts.check_supply_chain import check_fork_secret_isolation, check_permissions
from src.security.exchange_key_posture import PostureViolation, assert_all_safe

ROOT = Path(__file__).resolve().parents[1]


def _text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _yaml(rel: str) -> dict:
    return yaml.safe_load(_text(rel))


# --- OPS-003 ---------------------------------------------------------------


def test_deploy_canary_fails_closed_while_steps_are_placeholders():
    steps = _yaml(".github/workflows/deploy.yml")["jobs"]["canary"]["steps"]
    guard = [s for s in steps if "placeholder" in str(s.get("name", "")).lower()]
    assert guard and "exit 1" in guard[0]["run"]


# --- OPS-004 ---------------------------------------------------------------


def test_ruleset_requires_code_owner_approval():
    rules = json.loads(_text(".github/rulesets/main-protection.json"))["rules"]
    params = next(r for r in rules if r["type"] == "pull_request")["parameters"]
    assert params["required_approving_review_count"] >= 1
    assert params["require_code_owner_review"] is True


# --- OPS-005 / OPS-006 -----------------------------------------------------


@pytest.mark.parametrize("service", ["api", "worker"])
def test_compose_services_are_hardened(service):
    svc = _yaml("docker-compose.yml")["services"][service]
    assert svc["read_only"] is True
    assert svc["cap_drop"] == ["ALL"]
    assert "no-new-privileges:true" in svc["security_opt"]
    assert "/tmp" in svc["tmpfs"]


def test_compose_has_no_default_db_password():
    text = _text("docker-compose.yml")
    assert "tradebot-local" not in text
    assert "${POSTGRES_PASSWORD:?" in text
    assert "POSTGRES_PASSWORD=" in _text(".env.example")


# --- OPS-007 ---------------------------------------------------------------


def _env_example() -> dict[str, str]:
    out = {}
    for line in _text(".env.example").splitlines():
        m = re.match(r"^([A-Z][A-Z0-9_]*)=(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def test_risk_limits_agree_across_config_layers():
    env = _env_example()
    risk = _yaml("config/risk.yaml")
    assert int(env["RISK_CONSECUTIVE_LOSS_HALT"]) == risk["circuit_breaker"]["consecutive_losses"]
    floor = risk["drawdown_floor"]
    assert float(env["RISK_CAPITAL_PRESERVATION_MAX_DRAWDOWN_PCT"]) <= floor
    assert float(env["RISK_MAX_DRAWDOWN_THRESHOLD"]) / 100.0 <= floor


# --- OPS-016 / SCR-002 -----------------------------------------------------


def _wf(root: Path, name: str, body: str) -> None:
    d = root / ".github" / "workflows"
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(textwrap.dedent(body).lstrip(), encoding="utf-8")


def test_fork_guard_is_per_job_not_per_file(tmp_path):
    _wf(
        tmp_path,
        "w.yml",
        """
        on: [pull_request]
        permissions:
          contents: read
        jobs:
          safe:
            if: github.event.pull_request.head.repo.fork == false
            runs-on: ubuntu-latest
            steps:
              - run: a
                env:
                  T: ${{ secrets.A }}
          unsafe:
            runs-on: ubuntu-latest
            steps:
              - run: b
                env:
                  T: ${{ secrets.B }}
        """,
    )
    found = check_fork_secret_isolation(tmp_path)
    assert len(found) == 1 and "secrets.B" in found[0].detail


def test_push_workflow_persisting_a_pat_on_an_untrusted_ref_is_flagged(tmp_path):
    _wf(
        tmp_path,
        "w.yml",
        """
        on: [push]
        permissions:
          contents: read
        jobs:
          j:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
                with:
                  ref: ${{ needs.pick.outputs.resolve_ref }}
                  token: ${{ secrets.PAT }}
        """,
    )
    assert check_fork_secret_isolation(tmp_path)


def test_job_level_write_all_and_bare_comment_are_flagged(tmp_path):
    _wf(
        tmp_path,
        "a.yml",
        """
        on: [push]
        permissions:
          contents: read
        jobs:
          j:
            permissions: write-all
            runs-on: ubuntu-latest
            steps:
              - run: a
        """,
    )
    _wf(
        tmp_path,
        "b.yml",
        """
        on: [push]
        permissions:
          checks: write  #
        jobs:
          j:
            runs-on: ubuntu-latest
            steps:
              - run: a
        """,
    )
    names = {f.where for f in check_permissions(tmp_path)}
    assert names == {"a.yml", "b.yml"}


# --- OPS-017 ---------------------------------------------------------------


def _run_payload(path: str, event: str, repo: str = "o/r") -> dict:
    return {"path": path, "event": event, "repository": {"full_name": repo}}


def test_report_must_come_from_the_collector_workflow(monkeypatch):
    runs = {
        1: _run_payload(ci_diagnostics.COLLECTOR_WORKFLOW_PATH, "workflow_run"),
        2: _run_payload(".github/workflows/evil.yml", "pull_request"),
        3: _run_payload(ci_diagnostics.COLLECTOR_WORKFLOW_PATH, "pull_request"),
    }
    monkeypatch.setattr(
        ci_diagnostics, "_json", lambda path, **kw: runs.get(int(path.rsplit("/", 1)[1]))
    )
    cache: dict[int, bool] = {}

    def ok(run_id: int, url: str | None = None) -> bool:
        cr = {"details_url": url or f"https://github.com/o/r/actions/runs/{run_id}"}
        return ci_diagnostics._from_collector_run("o/r", cr, cache)

    assert ok(1)
    assert not ok(2)
    assert not ok(3)
    assert not ok(1, "https://github.com/other/r/actions/runs/1")
    assert not ok(1, "https://example.com/o/r/actions/runs/1")
    assert not ci_diagnostics._from_collector_run("o/r", {}, cache)


def test_retrieved_report_is_labelled_untrusted(monkeypatch, capsys):
    sha = "a" * 40
    monkeypatch.setattr(ci_diagnostics, "_answer", lambda pr: (sha, ["untrusted diagnostic"]))
    assert ci_diagnostics._retrieve(7) == 0
    captured = capsys.readouterr()
    assert "UNTRUSTED DATA" in captured.err
    assert "untrusted diagnostic" in captured.out


# --- OPS-019 ---------------------------------------------------------------


def test_intelligence_gated_ordering_defaults_off():
    for rel in ("src/engine/orchestrator.py", "src/api/main.py"):
        defaults = re.findall(r'environ\.get\("INTEL_ENABLED",\s*"([^"]*)"', _text(rel))
        assert defaults, rel
        assert all(d.lower() == "false" for d in defaults), rel
    assert _env_example()["INTEL_ENABLED"] == "false"
    assert "INTEL_ENABLED" not in _text("docker-compose.yml")


# --- SCR-004 ---------------------------------------------------------------

_SAFE = {
    "capabilities": ["read", "trade"],
    "ip_allowlisted": True,
    "withdrawal_whitelist_only": True,
    "declared_by": "operator",
    "declared_on": "2026-09-12",
}


def test_a_credentialed_venue_without_a_declaration_is_refused():
    with pytest.raises(PostureViolation):
        assert_all_safe({"binance": _SAFE}, required=("binance", "okx"))
    assert_all_safe({"binance": _SAFE, "okx": _SAFE}, required=("binance", "okx"))


# --- SCR-003 ---------------------------------------------------------------


def test_mutation_counts_come_from_the_cache(tmp_path):
    db = tmp_path / "cache"
    with sqlite3.connect(db) as con:
        con.execute("CREATE TABLE mutant (status TEXT)")
        con.executemany(
            "INSERT INTO mutant VALUES (?)",
            [("ok_killed",)] * 3 + [("bad_survived",), ("bad_timeout",), ("untested",)],
        )
    con.close()
    assert check_mutation_score.read_cache_counts(db) == {
        "killed": 3,
        "survived": 1,
        "timeout": 1,
    }
    assert check_mutation_score.read_cache_counts(tmp_path / "absent")["killed"] == 0


def test_mutmut_is_pinned_to_the_version_the_script_drives():
    wf = _text(".github/workflows/nightly-quality.yml")
    assert f"mutmut=={check_mutation_score.MUTMUT_VERSION}" in wf
    assert not re.search(r"mutmut\s*$", wf, re.MULTILINE)


# --- SCR-005 ---------------------------------------------------------------


def test_math_registry_consumers_reference_their_owner():
    entries = json.loads(_text("config/math_registry.json"))["entries"]
    bad = []
    for e in entries:
        wiring = e.get("wiring", [])
        owners = [w["module"] for w in wiring if w["kind"] in ("owner", "component")]
        tails = {
            ".".join(o.removesuffix("/__init__.py").removesuffix(".py").split("/")[-2:])
            for o in owners
        }
        for w in wiring:
            if w["kind"] != "consumer":
                continue
            target = ROOT / w["module"]
            files = list(target.rglob("*.py")) if target.is_dir() else [target]
            src = "".join(f.read_text(encoding="utf-8") for f in files)
            if not any(t.replace("/", ".") in src for t in tails):
                bad.append((e["id"], w["module"]))
    assert not bad, f"consumer rows that never import their owner: {bad}"


# --- SCR-006 ---------------------------------------------------------------


def test_command_policy_has_no_dead_sections_and_guards_env_readers():
    policy = json.loads(_text("config/command_policy.json"))
    for dead in ("bounded_output", "observation_boundary", "ci_observability"):
        assert dead not in policy
    patterns = policy["secret_echo"]["patterns"]

    def blocked(cmd: str) -> bool:
        return any(re.search(p, cmd, re.IGNORECASE) for p in patterns)

    for cmd in (
        "head -n 30 .env",
        "sed -n 1,30p .env",
        "grep . .env",
        "python3 -c \"print(open('.env').read())\"",
    ):
        assert blocked(cmd), cmd
    assert not blocked("grep -n RISK_ .env.example")


# --- OPS-018 ---------------------------------------------------------------

_TRACKED_LAWS = {"LAW1", "LAW2", "LAW9", "LAW10", "LAW13"}


def test_execution_and_risk_baseline_findings_are_tracked_in_the_registry():
    baseline = json.loads(_text("config/arch_baseline.json"))["fingerprints"]
    entries = json.loads(_text("config/quality_registry.json"))["entries"]
    tracked = {
        m for e in entries if e["id"].startswith("ARCH-") for m in e.get("owning_modules", [])
    }
    for e in entries:
        if e["id"].startswith("ARCH-"):
            assert e["status"] == "accepted_gap" and e["waiver"]["review_by"]
    missing = []
    for fp in baseline:
        law, _, rest = fp.partition("|")
        path = rest.rsplit("|", 1)[1]
        if law in _TRACKED_LAWS and path not in tracked:
            missing.append(fp)
    assert not missing, missing
