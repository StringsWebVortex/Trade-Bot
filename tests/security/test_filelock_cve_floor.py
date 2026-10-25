"""SEC-0012: the runtime manifest can never resolve a vulnerable filelock.

filelock 3.32.3 carries CVE-2026-112940 (arbitrary file overwrite through
insecure lock-file reopening, fixed in 4.2.1). It is only transitive -- torch
and huggingface-hub require it unbounded -- so pip kept whatever 3.x it found
and the container scan failed. Declaring it directly is what holds the floor.

The floor alone did not clear the image. The Dockerfile installs torch from
the CPU index into ``--prefix=/install`` first, and pip does not look inside a
prefix for what is installed: the requirements pass installed filelock 4.x
beside the pre-pass's 3.32.3 instead of replacing it, and the old dist-info
stayed for the scan to read. Every later install into the prefix must see it.
"""

from __future__ import annotations

import re
from pathlib import Path

from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parents[2]
REQUIREMENTS = ROOT / "requirements.txt"


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


def test_every_later_install_into_the_prefix_sees_what_is_already_there() -> None:
    text = (ROOT / "Dockerfile").read_text(encoding="utf-8").replace("\\\n", " ")
    commands = [" ".join(c.split()) for c in re.split(r"&&|\n", text)]
    installs = [c for c in commands if "pip install" in c and "--prefix=/install" in c]
    assert len(installs) >= 2, "expected the CPU torch pre-pass and the requirements pass"
    for command in installs[1:]:
        assert command.startswith("PYTHONPATH=/install/lib/python3.11/site-packages "), command
