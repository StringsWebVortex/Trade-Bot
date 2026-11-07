"""
EXR-006/007/008/012 -- execution accounting regressions.

006: crypto-box Kelly scaling must change the order quantity/notional.
007: a partial live close settles only the filled share; residual stays open.
008: a spot account must refuse short (non-long) entries.
012: base-asset fees reduce the tracked quantity so a close never oversells.

Decides:
  - REG-1040 — Crypto-box Kelly reduction reaches the order size
  - REG-1041 — Partial live close settles only the filled share
  - REG-1042 — Spot live executor refuses short entries
  - REG-1043 — Base-asset entry fees reduce tracked position quantity
"""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import AsyncMock

import pytest

from src.engine.orchestrator import _DEFAULT_SYMBOL_PRECISION, _apply_crypto_box_scale
from src.risk.kelly import KellyResult
from tests.test_live_executor_coverage import (
    _filled_order,
    _kelly,
    _make_executor,
    _make_position,
)


@dataclass(frozen=True)
class _Res:
    kelly_result: KellyResult | None
    tradeable: bool = True
    skip_reason: str = ""


def test_crypto_box_scale_reduces_quantity_and_notional() -> None:
    k = _kelly(notional=5000.0, qty=0.1, price=50000.0)
    out = _apply_crypto_box_scale(_Res(k), 0.5, 50000.0, _DEFAULT_SYMBOL_PRECISION)
    assert out.tradeable
    assert out.kelly_result.quantity == pytest.approx(0.05)
    assert out.kelly_result.notional_usd == pytest.approx(2500.0)


def test_crypto_box_scale_skips_when_below_minimum() -> None:
    k = _kelly(notional=5000.0, qty=0.1, price=50000.0)
    prec = {**_DEFAULT_SYMBOL_PRECISION, "min_cost": 4000.0}
    out = _apply_crypto_box_scale(_Res(k), 0.5, 50000.0, prec)
    assert out.tradeable is False


@pytest.mark.asyncio
async def test_partial_close_credits_only_filled_share_and_keeps_residual() -> None:
    ex = _make_executor(cash=95_000.0)
    ex._positions["t"] = _make_position(
        trade_id="t", entry_price=50_000.0, quantity=0.1, notional_usd=5_000.0
    )
    ex._place_market_order = AsyncMock(
        return_value=_filled_order(price=50_000.0, qty=0.04, fee_usd=0)
    )
    ex._storage.update_trade_exit = AsyncMock()
    ex._storage.record_trade_partial_exit = AsyncMock()
    ex._storage.insert_equity = AsyncMock()
    await ex.close_position("t", exit_price=50_000.0, exit_reason="x")
    assert "t" in ex._positions
    assert ex._positions["t"].quantity == pytest.approx(0.06)
    assert ex._positions["t"].notional_usd == pytest.approx(3_000.0)
    # zero pnl: cash rises by the 40% of notional sold, minus the fallback fee
    assert ex._cash < 95_000.0 + 2_000.0 + 1e-6
    assert ex._cash > 95_000.0 + 1_900.0
    ex._storage.update_trade_exit.assert_not_awaited()
    ex._storage.record_trade_partial_exit.assert_awaited_once()


@pytest.mark.asyncio
async def test_multiple_partial_fills_persist_then_final_close_accumulates() -> None:
    ex = _make_executor(cash=95_000.0)
    ex._positions["t"] = _make_position(
        trade_id="t", entry_price=50_000.0, quantity=0.1, notional_usd=5_000.0
    )
    ex._place_market_order = AsyncMock(
        side_effect=[
            _filled_order(price=51_000.0, qty=0.04, fee_usd=1.0),
            _filled_order(price=52_000.0, qty=0.03, fee_usd=1.0),
            _filled_order(price=53_000.0, qty=0.03, fee_usd=1.0),
        ]
    )
    ex._storage.record_trade_partial_exit = AsyncMock()
    ex._storage.update_trade_exit = AsyncMock()
    ex._storage.insert_equity = AsyncMock()

    await ex.close_position("t", exit_price=51_000.0, exit_reason="scale_out")
    assert ex._positions["t"].quantity == pytest.approx(0.06)
    await ex.close_position("t", exit_price=52_000.0, exit_reason="scale_out")
    assert ex._positions["t"].quantity == pytest.approx(0.03)
    await ex.close_position("t", exit_price=53_000.0, exit_reason="final")

    assert "t" not in ex._positions
    assert ex._storage.record_trade_partial_exit.await_count == 2
    assert ex._storage.update_trade_exit.await_count == 1
    assert ex._storage.update_trade_exit.await_args.kwargs["fee_usd"] == pytest.approx(1.0)


@pytest.mark.asyncio
async def test_base_asset_exit_fee_reduces_residual_and_is_not_double_charged_to_cash() -> None:
    ex = _make_executor(cash=95_000.0)
    ex._positions["t"] = _make_position(
        trade_id="t", entry_price=50_000.0, quantity=0.1, notional_usd=5_000.0
    )
    ex._place_market_order = AsyncMock(
        return_value={
            "id": "sell-1",
            "filled": 0.04,
            "average": 51_000.0,
            "fees": [{"currency": "BTC", "cost": 0.0001}],
        }
    )
    ex._storage.record_trade_partial_exit = AsyncMock()
    ex._storage.update_trade_exit = AsyncMock()
    ex._storage.insert_equity = AsyncMock()

    await ex.close_position("t", exit_price=51_000.0, exit_reason="scale_out")

    assert ex._positions["t"].quantity == pytest.approx(0.0599)
    assert ex._storage.record_trade_partial_exit.await_args.kwargs["fee_usd"] == pytest.approx(5.1)
    # 0.04 BTC was sold; 0.0001 BTC was consumed as fee, not quote cash.
    assert ex._cash == pytest.approx(95_000.0 + 0.04 * 51_000.0)


@pytest.mark.asyncio
async def test_near_full_fill_keeps_the_unfilled_residual_open() -> None:
    ex = _make_executor(cash=95_000.0)
    ex._positions["t"] = _make_position(
        trade_id="t", entry_price=50_000.0, quantity=0.1, notional_usd=5_000.0
    )
    ex._place_market_order = AsyncMock(
        return_value=_filled_order(price=50_000.0, qty=0.09995, fee_usd=1.0)
    )
    ex._storage.record_trade_partial_exit = AsyncMock()
    ex._storage.update_trade_exit = AsyncMock()
    ex._storage.insert_equity = AsyncMock()

    await ex.close_position("t", exit_price=50_000.0, exit_reason="near_full")

    assert "t" in ex._positions
    assert ex._positions["t"].quantity == pytest.approx(0.00005)
    ex._storage.record_trade_partial_exit.assert_awaited_once()
    ex._storage.update_trade_exit.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize("direction", [0, -1])
async def test_spot_account_rejects_short_entry(direction: int) -> None:
    ex = _make_executor()
    ex._place_market_order = AsyncMock()
    res = await ex._place_and_record(
        symbol="BTC/USDT",
        timeframe="1h",
        direction=direction,
        kelly_result=_kelly(),
        regime_state=0,
        meta_label_prob=0.6,
        raw_signal=-1.0,
        approved_by="auto",
    )
    assert res is None
    ex._place_market_order.assert_not_awaited()
    assert ex._cash == pytest.approx(100_000.0)


@pytest.mark.asyncio
async def test_base_asset_fee_reduces_tracked_quantity() -> None:
    ex = _make_executor()
    ex._place_market_order = AsyncMock(
        return_value={
            "id": "o",
            "filled": 0.1,
            "average": 50_000.0,
            "fees": [{"currency": "BTC", "cost": 0.0001}],
        }
    )
    ex._storage.insert_trade = AsyncMock()
    ex._storage.insert_equity = AsyncMock()
    ex._cfg.execution_mode.value = "automatic"
    tid = await ex._place_and_record(
        symbol="BTC/USDT",
        timeframe="1h",
        direction=1,
        kelly_result=_kelly(),
        regime_state=0,
        meta_label_prob=0.6,
        raw_signal=1.0,
        approved_by="auto",
    )
    pos = ex._positions[tid]
    assert pos.quantity == pytest.approx(0.0999)
    assert pos.fee_usd == pytest.approx(5.0)  # 0.0001 BTC at 50k
