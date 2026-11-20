"""INT-024: ModelRegistry promotes only a paired, materially better shadow and
promote_shadow re-checks.

Decides:
  - REG-1115 -- ModelRegistry shadow promotion needs paired windows and a minimum improvement
"""

from __future__ import annotations

import pytest

from src.models.model_registry import ModelRegistry


def _feed(reg: ModelRegistry, shadow_correct: int, live_correct: int, n: int) -> None:
    for i in range(n):
        reg.record_shadow_prediction("v2", 0.9 if i < shadow_correct else 0.1, 1)
        reg.record_live_prediction_for_comparison("v2", 0.9 if i < live_correct else 0.1, 1)


def _reg(min_evaluations: int = 100) -> ModelRegistry:
    reg = ModelRegistry(min_evaluations=min_evaluations)
    reg.set_live_model("v1")
    reg.register_shadow("v2")
    return reg


def test_one_percent_edge_is_not_enough() -> None:
    """Would fail before the fix: any accuracy difference promoted."""
    reg = _reg()
    _feed(reg, 51, 50, 100)
    ready, reason = reg.evaluate_shadow("v2")
    assert not ready
    assert "does not beat" in reason


def test_unpaired_empty_live_window_is_not_ready() -> None:
    """Would fail before the fix: empty live list scored 0.0 so any shadow won."""
    reg = _reg(min_evaluations=10)
    for _ in range(10):
        reg.record_shadow_prediction("v2", 0.9, 1)
    ready, reason = reg.evaluate_shadow("v2")
    assert not ready
    assert "unpaired" in reason


def test_promote_shadow_rechecks_and_refuses() -> None:
    reg = _reg()
    with pytest.raises(ValueError, match="not ready"):
        reg.promote_shadow("v2")
    assert reg.live_model_id == "v1"
    assert "v2" in reg.shadow_ids()


def test_clear_improvement_promotes() -> None:
    reg = _reg()
    _feed(reg, 70, 50, 100)
    assert reg.evaluate_shadow("v2")[0]
    reg.promote_shadow("v2")
    assert reg.live_model_id == "v2"
