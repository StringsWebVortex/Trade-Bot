"""
Locks on the two CI behaviours that made fixed failures look like new ones.

Decides:
  - REG-1706 — One failing test shard never hides the failures of the others
  - REG-1707 — A test that leaks an async resource fails instead of passing with 'Event loop is closed'
"""

from __future__ import annotations

import gc
import tomllib
from pathlib import Path

import yaml

from tests.regression.unraisable import collect_unraisable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CI_YML = PROJECT_ROOT / ".github" / "workflows" / "ci.yml"
CI = yaml.safe_load(CI_YML.read_text(encoding="utf-8"))
PYPROJECT = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
PYTEST_INI = PYPROJECT["tool"]["pytest"]["ini_options"]


def test_a_failing_shard_does_not_cancel_the_others() -> None:
    """
    REG-1706. With fail-fast the first failing shard cancelled the other five,
    so a run reported one shard's failures and the rest appeared one push
    later, reading as new failures each time.
    """
    strategy = CI["jobs"]["python-tests"]["strategy"]
    assert strategy["fail-fast"] is False
    assert len(strategy["matrix"]["shard"]) > 1


def test_an_unraisable_exception_fails_the_test_that_raised_it() -> None:
    """
    REG-1707. "Event loop is closed" from a transport finalised after its loop
    closed was only a warning, so the leaking test passed on every run.
    """
    assert "error::pytest.PytestUnraisableExceptionWarning" in PYTEST_INI["filterwarnings"]


def test_the_existing_deprecation_filter_is_kept() -> None:
    assert "error::DeprecationWarning:src.*" in PYTEST_INI["filterwarnings"]


class _RaisesOnFinalize:
    def __del__(self) -> None:
        raise RuntimeError("Event loop is closed")


def test_session_end_guard_names_a_finalizer_that_raises() -> None:
    """REG-1707: a leak that outlives every test is still caught and named."""
    gc.disable()  # an automatic collection would run the finalizer under pytest's own hook
    try:
        leaked = _RaisesOnFinalize()
        leaked.cycle = leaked  # only the collector can free it
        del leaked
        caught = collect_unraisable()
    finally:
        gc.enable()

    assert len(caught) == 1
    assert isinstance(caught[0].exc_value, RuntimeError)
    assert "_RaisesOnFinalize" in repr(caught[0].object)
