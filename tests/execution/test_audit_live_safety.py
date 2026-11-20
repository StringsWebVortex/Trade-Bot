"""
Audit fixes for two live-path safety defects.

1. An exchange reporting an order filled without usable fill details used to
   raise a bare ValueError out of submit_signal, leaving possibly-real
   exposure untracked. It must now fail closed: a rejected outcome, a
   recovery discrepancy that blocks new entries, and no further orders.
2. An approved intent is executed on a later tick (EXR-018 queue-and-return),
   so the state checked when it was queued may no longer hold. The executor's
   own pre-trade conditions (initialised, no unresolved recovery discrepancy)
   must be re-evaluated on that later tick and refuse without touching the
   exchange.
"""

from __future__ import annotations

import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.config import ExecutionMode
from src.diagnostics.disaster_recovery import Discrepancy, DiscrepancyType
from src.execution import order_manager as order_manager_module
from src.execution.base import ApprovalRequest
from src.execution.order_manager import UnverifiableFillError
from tests.test_live_executor_coverage import _filled_order, _kelly, _make_executor

_SYMBOL = "BTC/USDT"


def _exchange(fetch_result: dict) -> MagicMock:
    exchange = MagicMock(id="binance")
    exchange.create_market_order = AsyncMock(return_value={"id": "ord-1"})
    exchange.fetch_order = AsyncMock(return_value=fetch_result)
    return exchange


async def _submit(ex, mode: ExecutionMode, notional: float = 5000.0):
    with patch("src.execution.live.runtime_config") as mock_rc:
        mock_rc.get_execution_mode = AsyncMock(return_value=mode)
        return await ex.submit_signal(
            symbol=_SYMBOL,
            timeframe="1h",
            direction=1,
            kelly_result=_kelly(notional=notional),
            regime_state=0,
            meta_label_prob=0.7,
            raw_signal=0.5,
            current_price=50000.0,
        )


@pytest.fixture(autouse=True)
def _fast_polling(monkeypatch):
    monkeypatch.setattr(order_manager_module, "_ORDER_CONFIRM_INTERVAL", 0.0)


# ───────────────────────── Defect 1: filled without fill details


class TestUnverifiableFill:
    @pytest.mark.asyncio
    async def test_fails_closed_and_blocks_further_entries(self):
        ex = _make_executor(cash=100_000.0)
        exchange = _exchange({"id": "ord-1", "status": "closed", "filled": 0.1})  # no price
        ex._fetcher.get_order_exchange = MagicMock(return_value=exchange)

        trade_id, outcome = await _submit(ex, ExecutionMode.AUTOMATIC)

        assert (trade_id, outcome) == (None, "rejected")
        assert ex._positions == {}
        assert len(ex.recovery_discrepancies) == 1
        d = ex.recovery_discrepancies[0]
        assert d.symbol == _SYMBOL
        assert d.discrepancy_type is DiscrepancyType.MISSING_LOCALLY
        assert d.reference_quantity == pytest.approx(0.1)
        # Reservation is held, not released: the venue says the cash was spent.
        assert ex._cash < 100_000.0
        assert exchange.create_market_order.await_count == 1

        trade_id, outcome = await _submit(ex, ExecutionMode.AUTOMATIC)
        assert (trade_id, outcome) == (None, "rejected")
        assert exchange.create_market_order.await_count == 1

    @pytest.mark.asyncio
    async def test_exception_is_a_value_error_subclass_for_existing_callers(self):
        assert issubclass(UnverifiableFillError, ValueError)

    @pytest.mark.asyncio
    async def test_unrelated_value_error_still_propagates(self):
        ex = _make_executor()
        ex._fetcher.get_order_exchange = MagicMock(return_value=MagicMock(id="binance"))
        ex._order_manager.place_order_with_fsm = AsyncMock(side_effect=ValueError("bug"))

        with pytest.raises(ValueError, match="bug"):
            await _submit(ex, ExecutionMode.AUTOMATIC)
        assert ex.recovery_discrepancies == []


# ───────────────────────── Defect 2: re-check on the tick that executes an approval


def _queue_approved_intent(ex, *, notional: float = 5000.0) -> None:
    """An operator-approved intent waiting for the next tick to execute it."""
    req = ApprovalRequest(
        request_id="req-1",
        symbol=_SYMBOL,
        timeframe="1h",
        direction=1,
        notional_usd=notional,
        entry_price=50000.0,
        quantity=notional / 50000.0,
        kelly_fraction=0.02,
        regime_state=0,
        meta_label_prob=0.7,
        raw_signal=0.5,
        created_at=time.monotonic(),
    )
    req.resolved = True
    req.approved = True
    req.operator = "operator-1"
    req.resolved_at = time.monotonic()
    ex._approval_queue["req-1"] = req


class TestApprovalRecheck:
    @pytest.mark.asyncio
    async def test_discrepancy_after_approval_rejects_without_ordering(self):
        ex = _make_executor()
        ex._order_manager.place_order_with_fsm = AsyncMock()
        _queue_approved_intent(ex)
        ex._recovery_discrepancies.append(
            Discrepancy(
                symbol=_SYMBOL,
                discrepancy_type=DiscrepancyType.MISSING_LOCALLY,
                local_quantity=0.0,
                reference_quantity=0.1,
            )
        )

        result = await _submit(ex, ExecutionMode.MANUAL)

        assert result == (None, "rejected")
        ex._order_manager.place_order_with_fsm.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_uninitialized_after_approval_rejects_without_ordering(self):
        ex = _make_executor()
        ex._order_manager.place_order_with_fsm = AsyncMock()
        _queue_approved_intent(ex, notional=50_000.0)
        ex._initialized = False

        with pytest.raises(RuntimeError):
            await _submit(ex, ExecutionMode.RESTRICTED, notional=50_000.0)
        ex._order_manager.place_order_with_fsm.assert_not_awaited()

    def test_precondition_helper_names_the_stage(self):
        ex = _make_executor()
        assert ex._entry_preconditions_ok(_SYMBOL, stage="submit") is True
        ex._recovery_discrepancies.append(
            Discrepancy(
                symbol=_SYMBOL,
                discrepancy_type=DiscrepancyType.MISSING_LOCALLY,
                local_quantity=0.0,
                reference_quantity=0.1,
            )
        )
        assert ex._entry_preconditions_ok(_SYMBOL, stage="submit") is False

    @pytest.mark.asyncio
    async def test_all_clear_approved_intent_places_order(self):
        ex = _make_executor()
        ex._fetcher.get_order_exchange = MagicMock(return_value=MagicMock(id="binance"))
        fsm = MagicMock()
        fsm.state.order_id = "ord-1"
        fsm.state.filled_qty = 0.1
        fsm.state.average_fill_price = 50000.0
        fsm.state.retry_count = 0
        ex._order_manager.place_order_with_fsm = AsyncMock(return_value=(fsm, _filled_order()))
        ex._register_order_fsm = MagicMock()
        ex._risk_cfg.approval_max_price_drift_bps = 50.0
        _queue_approved_intent(ex)

        trade_id, outcome = await _submit(ex, ExecutionMode.MANUAL)

        assert outcome == "opened"
        assert trade_id is not None
        ex._order_manager.place_order_with_fsm.assert_awaited_once()
