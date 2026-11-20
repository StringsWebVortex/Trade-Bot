"""
_StartupGuard owns lifespan resources only until startup yields.

After the hand-off the normal shutdown path releases everything; an error
raised during that shutdown must not make the guard run _cleanup again
(orchestrator shut down twice, storage closed twice, original error buried).
Before the hand-off the guard is the only owner and must still clean up.
"""

from __future__ import annotations

import pytest

from src.api import main as api_main


class _Boom(RuntimeError):
    pass


@pytest.fixture
def guard(monkeypatch: pytest.MonkeyPatch) -> api_main._StartupGuard:
    instance = api_main._StartupGuard(storage=object())  # type: ignore[arg-type]
    instance.cleanup_calls = 0  # type: ignore[attr-defined]

    async def _counting_cleanup() -> None:
        instance.cleanup_calls += 1  # type: ignore[attr-defined]

    monkeypatch.setattr(instance, "_cleanup", _counting_cleanup)
    return instance


async def test_exception_before_hand_off_triggers_cleanup_once(guard) -> None:
    with pytest.raises(_Boom):
        async with guard:
            raise _Boom("startup failed")

    assert guard.cleanup_calls == 1


async def test_exception_after_hand_off_does_not_trigger_cleanup(guard) -> None:
    with pytest.raises(_Boom, match="shutdown failed") as excinfo:
        async with guard:
            guard.mark_started()
            raise _Boom("shutdown failed")

    assert guard.cleanup_calls == 0
    assert excinfo.value.__context__ is None


async def test_clean_exit_never_triggers_cleanup(guard) -> None:
    async with guard:
        pass
    async with guard:
        guard.mark_started()

    assert guard.cleanup_calls == 0


def test_guard_starts_un_handed_off() -> None:
    assert api_main._StartupGuard(storage=object()).started is False  # type: ignore[arg-type]
