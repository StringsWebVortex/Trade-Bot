"""REG-1611: a missing dependency fails a test in CI instead of skipping it (TSA-07).

The registry-schema, QE-skill, ID-allocation and API-signer tests used
``pytest.importorskip`` for jsonschema and cryptography. In CI a broken install
then skipped security and quality tests and the job still went green.
``required_import.require`` skips only outside CI.

Decides: REG-1611"""

from __future__ import annotations

from pathlib import Path

import pytest
from required_import import require

_MISSING = "tradebot_reg1611_no_such_module"
_TESTS = Path(__file__).resolve().parent


def test_a_missing_module_fails_in_ci(monkeypatch) -> None:
    monkeypatch.setenv("CI", "true")
    with pytest.raises(ModuleNotFoundError):
        require(_MISSING)


def test_a_missing_module_skips_outside_ci(monkeypatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    with pytest.raises(pytest.skip.Exception):
        require(_MISSING)


def test_an_installed_module_is_returned(monkeypatch) -> None:
    monkeypatch.setenv("CI", "true")
    assert require("json").__name__ == "json"


@pytest.mark.parametrize(
    "relative",
    [
        "quality/test_quality_registry_schema.py",
        "quality/test_qe_skill.py",
        "quality/test_qe_id_allocation.py",
        "test_api_signer_audit.py",
    ],
)
def test_the_guarded_tests_no_longer_skip_on_a_missing_dependency(relative: str) -> None:
    source = (_TESTS / relative).read_text(encoding="utf-8")
    assert "importorskip(" not in source
    assert "require(" in source
