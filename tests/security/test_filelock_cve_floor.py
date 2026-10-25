"""SEC-0012: the runtime manifest can never resolve a vulnerable filelock.

filelock 3.32.3 carries CVE-2026-112940 (arbitrary file overwrite through
insecure lock-file reopening, fixed in 4.2.1). It is only transitive -- torch
and huggingface-hub require it unbounded -- so pip kept whatever 3.x it found
and the container scan failed. Declaring it directly is what holds the floor.
"""

from __future__ import annotations

from pathlib import Path

from packaging.requirements import Requirement

REQUIREMENTS = Path(__file__).resolve().parents[2] / "requirements.txt"


def _filelock() -> Requirement:
    for raw in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line and not line.startswith("-"):
            req = Requirement(line)
            if req.name.lower() == "filelock":
                return req
    raise AssertionError("requirements.txt does not declare filelock")


def test_filelock_is_declared_with_the_fixed_floor() -> None:
    spec = _filelock().specifier
    assert not spec.contains("3.32.3"), "filelock 3.32.3 (CVE-2026-112940) is still allowed"
    assert spec.contains("4.2.1"), "the fixed filelock 4.2.1 must stay installable"
