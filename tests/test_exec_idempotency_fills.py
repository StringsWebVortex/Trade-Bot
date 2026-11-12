"""
Regression tests for EXR-001 (closed idempotency key blocked exit retries) and
EXR-002 (entry timeout / partial cancel left untracked exposure).

Decides:
  - REG-1030 — a venue-confirmed no-fill releases the key so a retried exit places an order
  - REG-1031 — timeout and partial-cancel outcomes are reconciled, booked or block entries
"""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import ccxt.async_support as ccxt
import pytest

from src.execution.live import LiveExecutor
from src.execution.order_manager import (
    AmbiguousExecutionError,
    OrderManager,
    OrderNotFilledError,
)

SYM = "BTC/USDT"


def _key() -> str:
    return f"tb{uuid.uuid4().hex[:30]}"


def _exchange(created: list[dict], fetched: list[dict]) -> MagicMock:
    ex = MagicMock()
    ex.id = "binance"
    ex.create_market_order = AsyncMock(side_effect=created)
    ex.fetch_order = AsyncMock(side_effect=fetched)
    ex.cancel_order = AsyncMock(return_value={})
    return ex


@pytest.mark.asyncio
async def test_cancelled_close_then_retry_places_new_order():
    mgr = OrderManager()
    key = _key()
    ex = _exchange(
        [{"id": "1"}, {"id": "2"}],
        [
            {"id": "1", "status": "canceled", "filled": 0.0},
            {"id": "2", "status": "closed", "filled": 1.0, "average": 100.0},
        ],
    )
    with pytest.raises(OrderNotFilledError):
        await mgr.place_order_with_fsm(ex, SYM, "sell", 1.0, key)
    _fsm, order = await mgr.place_order_with_fsm(ex, SYM, "sell", 1.0, key)
    assert order["id"] == "2"
    assert ex.create_market_order.await_count == 2
    ids = [c.kwargs["params"]["newClientOrderId"] for c in ex.create_market_order.await_args_list]
    assert ids[0] == key
    assert ids[1] != key
    assert len(ids[1]) == len(key)


@pytest.mark.asyncio
async def test_expired_with_partial_fill_is_returned_for_booking():
    mgr = OrderManager()
    ex = _exchange(
        [{"id": "1"}],
        [{"id": "1", "status": "expired", "filled": 0.4, "average": 50.0}],
    )
    _, order = await mgr.place_order_with_fsm(ex, SYM, "buy", 1.0, _key())
    assert order["filled"] == 0.4


@pytest.mark.asyncio
async def test_timeout_cancels_and_books_partial_fill():
    mgr = OrderManager()
    ex = _exchange(
        [{"id": "1"}],
        [{"id": "1", "status": "canceled", "filled": 0.3, "average": 50.0}],
    )
    with patch.object(mgr, "_confirm_order_fill", AsyncMock(side_effect=TimeoutError("t"))):
        _, order = await mgr.place_order_with_fsm(ex, SYM, "buy", 1.0, _key())
    ex.cancel_order.assert_awaited_once()
    assert order["filled"] == 0.3


@pytest.mark.asyncio
async def test_timeout_confirmed_no_fill_releases_key():
    mgr = OrderManager()
    key = _key()
    ex = _exchange([{"id": "1"}], [{"id": "1", "status": "canceled", "filled": 0.0}])
    with (
        patch.object(mgr, "_confirm_order_fill", AsyncMock(side_effect=TimeoutError("t"))),
        pytest.raises(TimeoutError),
    ):
        await mgr.place_order_with_fsm(ex, SYM, "sell", 1.0, key)
    assert not await mgr.idempotency.seen(key)


@pytest.mark.asyncio
async def test_timeout_unresolved_is_ambiguous_and_key_stays_claimed():
    mgr = OrderManager()
    key = _key()
    ex = _exchange([{"id": "1"}], [ccxt.NetworkError("down")])
    ex.cancel_order = AsyncMock(side_effect=ccxt.NetworkError("down"))
    with (
        patch.object(mgr, "_confirm_order_fill", AsyncMock(side_effect=TimeoutError("t"))),
        pytest.raises(AmbiguousExecutionError),
    ):
        await mgr.place_order_with_fsm(ex, SYM, "buy", 1.0, key)
    assert await mgr.idempotency.seen(key)


@pytest.mark.asyncio
async def test_placement_network_error_reconciles_by_client_order_id():
    mgr = OrderManager()
    ex = MagicMock()
    ex.id = "binance"
    ex.create_market_order = AsyncMock(side_effect=ccxt.RequestTimeout("lost response"))
    ex.fetch_order = AsyncMock(
        side_effect=[
            {"id": "9", "status": "closed", "filled": 1.0, "average": 10.0},  # by client id
            {"id": "9", "status": "closed", "filled": 1.0, "average": 10.0},  # confirm poll
        ]
    )
    _, order = await mgr.place_order_with_fsm(ex, SYM, "buy", 1.0, _key())
    assert order["id"] == "9"
    assert "newClientOrderId" in ex.fetch_order.await_args_list[0].args[2]


@pytest.mark.asyncio
async def test_placement_network_error_absent_order_releases_key():
    mgr = OrderManager()
    key = _key()
    ex = MagicMock()
    ex.id = "binance"
    ex.create_market_order = AsyncMock(side_effect=ccxt.RequestTimeout("lost"))
    ex.fetch_order = AsyncMock(side_effect=ccxt.OrderNotFound("none"))
    with pytest.raises(ccxt.NetworkError):
        await mgr.place_order_with_fsm(ex, SYM, "buy", 1.0, key)
    assert not await mgr.idempotency.seen(key)


def test_ambiguous_execution_blocks_new_entries():
    ex = LiveExecutor.__new__(LiveExecutor)
    ex._recovery_discrepancies = []
    ex._log = MagicMock()
    ex._block_entries_unreconciled(SYM, "test")
    assert ex.recovery_discrepancies
    assert ex.acknowledge_recovery("op") == 1
    assert not ex.recovery_discrepancies
