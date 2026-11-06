"""
REG-1708 (STR-22): E-17 reads depth from the orderbook snapshot and scores
liquidity without a unit-dependent constant.

E-17 read ``data["bids"]``, a key the provider-cache snapshot never has, so its
depth was always 0, the stress flag never fired and the cascade level was
always the spot * 0.98 fallback. Its score was ``1 - amihud * 1e6``, which
changes with whether volume is quoted in base or quote units. It now decodes
the snapshot's ``orderbook`` field as E-02 does and ranks the Amihud ratio
against the symbol's own history.
"""

from __future__ import annotations

import json
import math
from collections import deque

import numpy as np
import pandas as pd
import pytest

from src.engines.e17_liquidity import (
    E17Liquidity,
    amihud_liquidity_score,
    bids_from_orderbook,
)

_SPOT = 50_000.0


def _ohlcv(n: int = 140, seed: int = 7, volume_scale: float = 1.0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    closes = np.cumprod(1 + rng.normal(0.0, 0.01, n)) * _SPOT
    return pd.DataFrame(
        {
            "close": closes,
            "volume": rng.uniform(1000, 5000, n) * volume_scale,
        }
    )


def _book(levels: int = 20, size: float = 5.0) -> pd.DataFrame:
    bids = [[_SPOT - i * 10.0, size] for i in range(levels)]
    return pd.DataFrame({"bids_json": [json.dumps(bids)]})


def test_bids_are_decoded_from_the_snapshot_pairs() -> None:
    bids = bids_from_orderbook(_book(levels=2))
    assert bids == [{"price": _SPOT, "size": 5.0}, {"price": _SPOT - 10.0, "size": 5.0}]


@pytest.mark.parametrize(
    "book",
    [
        None,
        pd.DataFrame({"bids_json": []}),
        pd.DataFrame({"bids_json": ["not json"]}),
        pd.DataFrame({"bids_json": [json.dumps([[1.0]])]}),
        pd.DataFrame({"asks_json": ["[]"]}),
    ],
)
def test_a_missing_or_malformed_snapshot_has_no_levels(book: pd.DataFrame | None) -> None:
    assert bids_from_orderbook(book) == []


@pytest.mark.asyncio
async def test_depth_comes_from_the_orderbook_snapshot() -> None:
    df = _ohlcv()
    out = await E17Liquidity().run("BTC/USDT", {"ohlcv": df, "spot": _SPOT, "orderbook": _book()})
    # 50 bps of 50_000 is 250: all 20 levels (10 apart) are inside the band.
    assert out.metadata["depth_score"] == pytest.approx(20 * 5.0)


@pytest.mark.asyncio
async def test_without_a_snapshot_depth_is_unknown_and_the_engine_still_answers() -> None:
    out = await E17Liquidity().run("BTC/USDT", {"ohlcv": _ohlcv(), "spot": _SPOT})
    assert out.metadata["depth_score"] == 0.0
    assert not out.metadata["stress_flag"]
    assert out.metadata["cascade_price_level"] == pytest.approx(_SPOT * 0.98)
    # Cold start: no Amihud history to rank against, so the score is neutral.
    assert out.confidence == 1.0


async def _scores(volume_scale: float) -> list[float]:
    df = _ohlcv(volume_scale=volume_scale)
    engine = E17Liquidity()
    scores = []
    for start in range(40):
        window = df.iloc[start : start + 100].reset_index(drop=True)
        out = await engine.run("BTC/USDT", {"ohlcv": window, "spot": _SPOT})
        scores.append(out.metadata["liquidity_score"])
    return scores


@pytest.mark.asyncio
async def test_the_score_does_not_depend_on_the_volume_unit() -> None:
    base = await _scores(1.0)
    quote = await _scores(1_000.0)
    assert base == pytest.approx(quote)
    # Neutral until 20 readings exist, then it ranks and moves.
    assert base[:20] == [1.0] * 20
    assert len(set(base[20:])) > 1
    assert all(0.0 <= s <= 1.0 for s in base)


def test_a_less_liquid_reading_scores_lower() -> None:
    history = deque(float(i) for i in range(1, 21))
    assert amihud_liquidity_score(0.5, history) == 1.0
    assert amihud_liquidity_score(25.0, history) == 0.0
    assert amihud_liquidity_score(10.0, history) == pytest.approx(1.0 - 9.5 / 20)


def test_a_short_history_or_non_finite_reading_is_neutral() -> None:
    assert amihud_liquidity_score(5.0, deque([1.0] * 19)) == 1.0
    assert amihud_liquidity_score(math.nan, deque([1.0] * 20)) == 1.0
