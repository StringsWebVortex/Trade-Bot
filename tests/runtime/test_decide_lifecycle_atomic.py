"""REG-1206: a failed shadow check ends the change instead of stranding it.

Decides: REG-1206"""

from __future__ import annotations

from dataclasses import replace

import pytest

from src.runtime.changes import ChangeRequest, ChangeStatus
from src.runtime.contracts import ComponentType, LifecycleAction, LifecycleState
from src.runtime.supervisor import ActionRefusedError

from ._support import HUMAN, REQUESTER, SYSTEM, build_platform, spec, version


class _RefusingLifecycle:
    def record_shadow_stage(self, component: object) -> str:
        raise ActionRefusedError("candidate paired evaluation is no longer current and passing")

    def complete_promotion(self, component: object) -> None:  # pragma: no cover
        return None


def _submit(platform):  # type: ignore[no-untyped-def]
    component_spec = replace(
        spec("horizon", ComponentType.MODEL), version=version("1", horizon_id=0)
    )
    platform.registry.register(component_spec, observed_state=LifecycleState.STANDBY)
    return platform.changes.submit(
        ChangeRequest(
            component_id="model:horizon",
            action=LifecycleAction.ACTIVATE,
            actor=REQUESTER,
            reason="promote evaluated horizon",
        )
    )


def test_refused_shadow_check_fails_the_change_and_frees_the_component() -> None:
    platform = build_platform()
    change = _submit(platform)
    platform.changes._horizon_models = _RefusingLifecycle()

    with pytest.raises(ActionRefusedError):
        platform.changes.decide_lifecycle(change.change_id, "approve", HUMAN, system_actor=SYSTEM)

    assert platform.changes.get(change.change_id).status is ChangeStatus.FAILED
    # Not stranded APPROVED: nothing is open, so a new request is accepted.
    assert platform.changes.open_change("model:horizon") is None
