"""MTH-010: shadow promotion needs a minimum sample and a significant paired
difference, takes required predictions and annualises with the configured factor.

Decides:
  - REG-1114 -- Shadow deployment promotes only on a significant paired improvement
"""

from __future__ import annotations

import sys
from unittest.mock import patch

import numpy as np
import pytest

from src.upgrade.shadow_deploy import ModelRecord, ShadowDeployer


def _deployer() -> ShadowDeployer:
    d = ShadowDeployer(lambda x: 0, lambda x: 0, shadow_hours=0.0)
    d.start()
    return d


def _evaluate(d: ShadowDeployer, inc: list[float], cha: list[float]):
    d._incumbent.returns = list(inc)
    d._challenger.returns = list(cha)
    with patch.dict(sys.modules, {"evidently": None}):
        return d.evaluate()


def test_too_few_paired_samples_never_promotes() -> None:
    """Would fail before the fix: 5 samples sufficed."""
    result = _evaluate(_deployer(), [0.001, -0.001] * 14 + [0.0], [0.02, 0.01] * 14 + [0.02])
    assert not result.promoted
    assert "insufficient" in result.reason


def test_sharpe_margin_without_significance_does_not_promote() -> None:
    inc = [0.01, -0.01] * 15
    cha = [0.06, -0.05] * 15
    result = _evaluate(_deployer(), inc, cha)
    assert not result.promoted
    assert "not significant" in result.reason


def test_significant_paired_improvement_promotes() -> None:
    result = _evaluate(_deployer(), [0.001, -0.001] * 20, [0.02, 0.01, 0.03, 0.02] * 10)
    assert result.promoted


def test_record_return_requires_predictions() -> None:
    with pytest.raises(TypeError):
        _deployer().record_return(0.01)  # type: ignore[call-arg]


def test_record_return_accepts_array_valued_predictions() -> None:
    d = _deployer()
    d.record_return(0.02, np.array([0.7]), np.array([-0.2]))
    assert d._incumbent.returns == [0.02]
    assert d._challenger.returns == [-0.02]


def test_sharpe_uses_configured_periods_per_year() -> None:
    returns = [0.01, -0.02, 0.03, 0.0, 0.01, -0.01]
    arr = np.array(returns)
    rec = ModelRecord(name="m", model=None, returns=returns, periods_per_year=365.0)
    assert rec.sharpe() == pytest.approx(float(arr.mean() / arr.std() * np.sqrt(365.0)))
