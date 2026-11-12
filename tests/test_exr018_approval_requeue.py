"""REG-1718 (audit EXR-018): an approval never blocks the tick, and an approved
trade never fills on a stale price or skips the gates.

submit_signal() in RESTRICTED (above the limit) and MANUAL queues the trade
and returns "queued" at once. The approved intent is executed only by the
next tick whose own signal is still tradeable -- that tick re-ran the gate
stack and Kelly on fresh data -- and only in the approved direction, within
approval_max_price_drift_bps of the price the request showed, and at no more
than the approved notional. An intent its next tick does not execute lapses.
"""

from __future__ import annotations

import asyncio
import inspect
import math
import time

import pytest

from src.config import ExecutionMode, runtime_config
from src.data.storage import StorageBackend
from src.engine.orchestrator import Orchestrator
from src.execution.base import (
    ApprovalRequest,
    lapse_approved_intents,
    revalidate_approved_intent,
)
from src.execution.paper import PaperExecutor
from src.risk.kelly import KellyResult

SYMBOL = "BTC/USDT"
TF = "15m"


def _kelly(notional: float = 500.0, price: float = 100.0) -> KellyResult:
    return KellyResult(
        kelly_fraction=0.2,
        adjusted_fraction=0.1,
        capital_usd=10_000.0,
        entry_price=price,
        quantity=notional / price,
        notional_usd=notional,
        is_capped=False,
    )


def _approval_request(
    request_id: str,
    *,
    symbol: str = SYMBOL,
    timeframe: str = TF,
    notional: float = 500.0,
    entry_price: float = 100.0,
    resolved: bool = False,
    approved: bool = False,
) -> ApprovalRequest:
    return ApprovalRequest(
        request_id=request_id,
        symbol=symbol,
        timeframe=timeframe,
        direction=1,
        notional_usd=notional,
        entry_price=entry_price,
        quantity=notional / entry_price if entry_price > 0 else 0.0,
        kelly_fraction=0.1,
        regime_state=1,
        meta_label_prob=0.6,
        raw_signal=0.5,
        created_at=0.0,
        resolved=resolved,
        approved=approved,
    )


@pytest.fixture
async def manual_executor(tmp_path):
    storage = StorageBackend(db_path=str(tmp_path / "exr018.db"))
    await storage.initialize()
    ex = PaperExecutor(storage, starting_capital=10_000.0)
    await ex.initialize()
    await runtime_config.set_execution_mode(ExecutionMode.MANUAL)
    yield ex
    await runtime_config.set_execution_mode(ExecutionMode.AUTOMATIC)
    await storage.close()


async def _submit(ex: PaperExecutor, *, direction=1, notional=500.0, price=100.0):
    # wait_for only turns a regression (a blocking submit) into a failure
    # instead of a hung test; nothing here resolves the approval concurrently.
    return await asyncio.wait_for(
        ex.submit_signal(SYMBOL, TF, direction, _kelly(notional, price), 1, 0.6, 0.5, price),
        timeout=5.0,
    )


async def _queue_and_approve(ex: PaperExecutor, *, price=100.0, notional=500.0) -> str:
    assert await _submit(ex, price=price, notional=notional) == (None, "queued")
    (req_id,) = ex._approval_queue
    assert await ex.resolve_approval(req_id, approved=True, operator="alice")
    return req_id


async def test_submit_returns_queued_without_waiting_for_the_operator(manual_executor):
    assert await _submit(manual_executor) == (None, "queued")
    assert await _submit(manual_executor) == (None, "queued")
    assert len(manual_executor.pending_approvals()) == 1  # no duplicate per key


async def test_approved_trade_fills_at_the_fresh_price_not_the_queued_one(manual_executor):
    await _queue_and_approve(manual_executor, price=100.0)

    trade_id, outcome = await _submit(manual_executor, price=100.3)  # 30 bps < 50

    assert outcome == "opened"
    pos = manual_executor._positions[trade_id]
    assert pos.entry_price == pytest.approx(100.3, abs=0.05)
    assert pos.approved_by == "alice"


@pytest.mark.parametrize(
    ("direction", "price"),
    [(1, 101.0), (1, 99.0), (0, 100.0)],
    ids=["drift-up", "drift-down", "direction-changed"],
)
async def test_approved_trade_that_no_longer_matches_is_rejected(manual_executor, direction, price):
    await _queue_and_approve(manual_executor, price=100.0)

    outcome = await _submit(manual_executor, direction=direction, price=price)

    assert outcome == (None, "rejected")
    assert manual_executor.open_positions() == []
    assert manual_executor._approval_queue == {}  # consumed, never retried


async def test_fresh_size_never_exceeds_the_approved_notional(manual_executor):
    await _queue_and_approve(manual_executor, notional=500.0)

    trade_id, outcome = await _submit(manual_executor, notional=800.0)

    assert outcome == "opened"
    assert manual_executor._positions[trade_id].notional_usd == pytest.approx(500.0, rel=1e-6)


async def test_an_approval_its_next_tick_does_not_use_lapses(manual_executor):
    req_id = await _queue_and_approve(manual_executor)

    manual_executor.close_approval_window(SYMBOL, TF)  # next tick: not tradeable
    assert req_id in manual_executor._approval_queue
    manual_executor.close_approval_window(SYMBOL, TF)  # the tick after
    assert req_id not in manual_executor._approval_queue

    assert await _submit(manual_executor) == (None, "queued")
    assert manual_executor.open_positions() == []


async def test_restricted_approval_after_the_timeout_is_refused(manual_executor):
    await runtime_config.set_execution_mode(ExecutionMode.RESTRICTED)
    assert await _submit(manual_executor) == (None, "queued")  # 500 > 100 limit
    (req,) = manual_executor._approval_queue.values()
    req.created_at = time.monotonic() - req.timeout_s - 1.0

    assert await manual_executor.resolve_approval(req.request_id, True, "alice") is False
    assert req.operator == "auto_timeout"
    assert await _submit(manual_executor) == (None, "queued")  # asks again
    assert manual_executor.open_positions() == []


@pytest.mark.parametrize(
    ("approved_price", "fresh_price"),
    [(0.0, 100.0), (math.nan, 100.0), (100.0, math.nan), (100.0, 0.0), (100.0, math.inf)],
)
def test_unknown_prices_fail_closed(approved_price, fresh_price):
    req = ApprovalRequest(
        request_id="r",
        symbol=SYMBOL,
        timeframe=TF,
        direction=1,
        notional_usd=500.0,
        entry_price=approved_price,
        quantity=5.0,
        kelly_fraction=0.1,
        regime_state=1,
        meta_label_prob=0.6,
        raw_signal=0.5,
        created_at=0.0,
    )
    fill, reason = revalidate_approved_intent(
        req,
        direction=1,
        kelly_result=_kelly(),
        current_price=fresh_price,
        max_price_drift_bps=50.0,
    )
    assert fill is None
    assert reason in {"approval_price_unknown", "approval_price_drift"}


def test_approved_intents_lapse_after_one_matching_tick():
    approved = _approval_request("approved", resolved=True, approved=True)
    queue = {
        "other-symbol": _approval_request(
            "other-symbol", symbol="ETH/USDT", resolved=True, approved=True
        ),
        "other-timeframe": _approval_request(
            "other-timeframe", timeframe="1h", resolved=True, approved=True
        ),
        "pending": _approval_request("pending", resolved=False, approved=True),
        "rejected": _approval_request("rejected", resolved=True, approved=False),
        "approved": approved,
    }

    assert lapse_approved_intents(queue, SYMBOL, TF) == []
    assert approved.window_seen is True
    assert "approved" in queue
    assert lapse_approved_intents(queue, SYMBOL, TF) == [approved]
    assert "approved" not in queue
    assert set(queue) == {"other-symbol", "other-timeframe", "pending", "rejected"}


def test_revalidate_rejects_invalid_or_unfillable_approved_sizes():
    request = _approval_request("size-check", resolved=True, approved=True)
    fill, reason = revalidate_approved_intent(
        request,
        direction=1,
        kelly_result=_kelly(notional=0.0),
        current_price=100.0,
        max_price_drift_bps=50.0,
    )
    assert fill is None
    assert reason == "approval_size_invalid"

    request.notional_usd = 1e-12
    fill, reason = revalidate_approved_intent(
        request,
        direction=1,
        kelly_result=_kelly(notional=500.0),
        current_price=100.0,
        max_price_drift_bps=50.0,
    )
    assert fill is None
    assert reason == "approval_size_below_minimum"


def test_the_tick_opens_the_approval_window_and_does_not_log_queued_as_missed():
    source = inspect.getsource(Orchestrator._tick_traced)
    assert "executor.close_approval_window(self._symbol, tf.value)" in source
    assert 'if outcome not in ("opened", "queued"):' in source
