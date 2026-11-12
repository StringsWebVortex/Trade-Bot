"""REG-1712: an arch-ignore comment silences only the rule it names, with a reason.

The crypto-architect validator used to skip every FORBIDDEN pattern on any
line containing ``# arch-ignore``. One comment written for a LAW12 false
positive therefore also hid a LAW6 secret or a LAW5 TLS bypass on the same
line, with no reason recorded and nothing counted in the report.

The scoped form ``# arch-ignore[LAWn]: reason`` is now the only one that
suppresses, and only for the listed laws. A bare or reasonless marker
suppresses nothing and is reported; LAW6 cannot be silenced inline at all.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
VALIDATOR = REPO / ".claude" / "skills" / "crypto-architect" / "scripts" / "validate_arch.py"
SCAN_DIR = REPO / "src"

# Scoped markers in src/ today: engine_backtest LAW9 (offline holdout metric)
# and nutms LAW12 (two constant-table names). A ratchet: lower it when one is
# removed, and justify any increase in the diff that adds the marker.
EXPECTED_SRC_MARKERS = 3

SECRET = 'key = os.environ["API_KEY"]'
WEAK_HASH = 'algo = "md5"'


@pytest.fixture(scope="module")
def va():
    spec = importlib.util.spec_from_file_location("validate_arch", VALIDATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_arch"] = module
    spec.loader.exec_module(module)
    return module


def _scan(va, tmp_path: Path, line: str):
    path = tmp_path / "mod.py"
    path.write_text(line + "\n", encoding="utf-8")
    return va.check_patterns(path)


def _open(findings, law: str):
    return [f for f in findings if f.law == law and not f.passed]


def test_marker_for_another_law_does_not_hide_a_secret(va, tmp_path: Path) -> None:
    line = 'key = os.environ["API_KEY"] + "md5"  # arch-ignore[LAW12]: table name'
    findings = _scan(va, tmp_path, line)
    assert _open(findings, "LAW6"), "a LAW12 marker must not silence LAW6"
    assert not _open(findings, "LAW12")
    assert not _open(findings, "ARCH")


@pytest.mark.parametrize(
    "marker",
    [
        "# arch-ignore",
        "# arch-ignore LAW12: no brackets",
        "# arch-ignore[LAW12]:",
        "#arch-ignore[]",
    ],
)
def test_bare_or_reasonless_marker_suppresses_nothing_and_is_reported(
    va, tmp_path: Path, marker: str
) -> None:
    findings = _scan(va, tmp_path, f"{WEAK_HASH}  {marker}")
    assert _open(findings, "LAW12"), "the original finding must still fire"
    (problem,) = _open(findings, "ARCH")
    assert problem.check == va.ARCH_IGNORE_INVALID
    assert problem.severity == va.Severity.MEDIUM
    assert problem.line == 1


def test_scoped_marker_suppresses_only_its_law_and_is_counted(va, tmp_path: Path) -> None:
    findings = _scan(va, tmp_path, f"{WEAK_HASH}  # arch-ignore[LAW5, LAW12]: table name")
    assert not _open(findings, "LAW12") and not _open(findings, "ARCH")
    (silenced,) = [f for f in findings if f.arch_ignore_reason is not None]
    assert silenced.law == "LAW12" and silenced.arch_ignore_reason == "table name"

    report = va.ValidationReport(component="t", findings=findings)
    assert report.stats()["suppressed_by_arch_ignore"] == 1
    assert report.to_sarif()["runs"][0]["properties"]["suppressedByArchIgnore"] == 1
    assert report.fingerprints() == [], "an inline suppression must not reach a baseline"


def test_law6_cannot_be_suppressed_inline(va, tmp_path: Path) -> None:
    findings = _scan(va, tmp_path, f"{SECRET}  # arch-ignore[LAW6]: test key")
    assert _open(findings, "LAW6")
    (problem,) = _open(findings, "ARCH")
    assert problem.check == va.ARCH_IGNORE_REFUSED


def test_every_src_marker_is_scoped_and_silences_a_real_hit(va) -> None:
    marked: dict[Path, list[int]] = {}
    for path in sorted(SCAN_DIR.rglob("*")):
        if path.suffix not in va.SCAN_EXTENSIONS or va.SKIP_DIRS & set(path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "arch-ignore" not in text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            laws, _, problem = va._arch_ignore_scope(line)
            assert problem is None, f"{path}:{i}: {problem}"
            if laws:
                marked.setdefault(path, []).append(i)

    assert sum(len(lines) for lines in marked.values()) == EXPECTED_SRC_MARKERS
    for path, lines in marked.items():
        silenced = {f.line for f in va.check_patterns(path) if f.arch_ignore_reason}
        dead = sorted(set(lines) - silenced)
        assert not dead, f"{path}: arch-ignore on lines {dead} suppresses nothing; remove it"
