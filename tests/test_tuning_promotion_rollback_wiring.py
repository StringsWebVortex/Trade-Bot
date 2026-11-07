"""STR-04: the post-promotion watchdog is started by the runner, and a
rollback reaches the live parameter registry (not only the version store).

Decides:
  - REG-1110 -- Watchdog rollback restores the live registry value and the runner starts probation
"""

from __future__ import annotations

import random
from pathlib import Path

from src.config import SelfTuningSettings
from src.risk.performance_drift import PerformanceBaseline, PerformanceDriftDetector
from src.tuning.audit import TuningAuditLog
from src.tuning.evaluator import MetricComparison
from src.tuning.gate import PromotionGate
from src.tuning.proposer import TuningProposer
from src.tuning.registry import ParameterRegistry, TunableParameter
from src.tuning.runner import TuningRunner
from src.tuning.store import VersionedConfigStore
from src.tuning.watchdog import PostPromotionWatchdog, WatchdogOutcome

NAME = "hmm.entropy_threshold"


def _detector() -> PerformanceDriftDetector:
    return PerformanceDriftDetector(
        PerformanceBaseline(
            train_sharpe=2.0,
            oos_sharpe=1.8,
            train_accuracy=0.60,
            oos_accuracy=0.58,
            train_win_rate=0.55,
            max_drawdown_pct=0.05,
            trades_in_backtest=1000,
        )
    )


def _improving(_param: TunableParameter, _proposal: object) -> list[MetricComparison]:
    return [
        MetricComparison(
            metric_name="oos_sharpe",
            champion_mean=0.01,
            challenger_mean=0.05,
            delta=0.04,
            p_value=0.001,
            significant_improvement=True,
            significant_regression=False,
        )
    ]


def _build(tmp_path: Path) -> tuple[TuningRunner, PostPromotionWatchdog, ParameterRegistry]:
    registry = ParameterRegistry()
    registry.register(
        TunableParameter(
            name=NAME,
            description="t",
            floor=0.3,
            ceiling=0.7,
            current=0.5,
            eval_strategy="cpcv_oos_sharpe",
        )
    )
    store = VersionedConfigStore(tmp_path / "v.jsonl")
    store.promote(NAME, 0.5, {"note": "seed champion"})
    audit = TuningAuditLog(tmp_path / "a.jsonl")
    settings = SelfTuningSettings(
        enabled=True, min_hours_between_attempts=24.0, probation_trades=100, probation_hours=999.0
    )
    watchdog = PostPromotionWatchdog(store, audit, settings, registry=registry)
    runner = TuningRunner(
        registry,
        store,
        audit,
        settings,
        TuningProposer(step_pct=0.2, rng=random.Random(1)),
        PromotionGate(),
        shadow_mode=False,
        watchdog=watchdog,
        probation_detector_factory=_detector,
    )
    return runner, watchdog, registry


def _losing_trades(watchdog: PostPromotionWatchdog) -> WatchdogOutcome:
    outcome = WatchdogOutcome.IN_PROBATION
    for i in range(40):
        outcome = watchdog.record_trade_outcome(
            NAME,
            pnl_usd=-50.0,
            predicted_prob=0.6,
            actual_direction=1,
            current_equity=1000.0 - i * 50,
            starting_equity=1000.0,
        )
        if outcome == WatchdogOutcome.ROLLED_BACK:
            break
    return outcome


def test_promotion_starts_probation_and_rollback_restores_live_registry(tmp_path: Path) -> None:
    """Would fail before the fix: nothing called start_probation, and a rollback
    left registry.current (what live_overrides reads) at the bad promoted value."""
    runner, watchdog, registry = _build(tmp_path)

    result = runner.attempt(NAME, _improving, primary_metric="oos_sharpe")
    assert result.promoted
    promoted_value = registry.get(NAME).current
    assert promoted_value != 0.5
    assert watchdog.probation_status(NAME) == WatchdogOutcome.IN_PROBATION

    assert _losing_trades(watchdog) == WatchdogOutcome.ROLLED_BACK
    assert registry.get(NAME).current == 0.5


def test_runner_refuses_attempt_while_watchdog_lock_active(tmp_path: Path) -> None:
    """A rolled-back parameter is locked out; the runner must honour it."""
    runner, watchdog, registry = _build(tmp_path)
    runner.attempt(NAME, _improving, primary_metric="oos_sharpe")
    _losing_trades(watchdog)
    assert watchdog.is_locked(NAME)

    again = runner.attempt(NAME, _improving, primary_metric="oos_sharpe")
    assert not again.attempted
    assert again.reasons == ("watchdog_locked",)
    assert registry.get(NAME).current == 0.5


def test_no_probation_without_a_detector_factory(tmp_path: Path) -> None:
    """Negative case: with no factory there is nothing to watch with, and the
    promotion must still succeed rather than fail."""
    runner, watchdog, _ = _build(tmp_path)
    runner.set_probation_detector_factory(None)
    assert runner.attempt(NAME, _improving, primary_metric="oos_sharpe").promoted
    assert watchdog.probation_params() == []
