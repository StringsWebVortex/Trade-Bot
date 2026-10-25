"""Regression tests for the engine/signal audit fixes.

Decides:
  - REG-1080 (STR-01) E-10 emits spot, not the S2F level, as predicted_price
  - REG-1081 (STR-02) meta-engines receive the other engines' outputs
  - REG-1082 (STR-03) TTL hysteresis holds state inside the mid band
  - REG-1083 (INT-006) a member that errors is excluded, not counted as 0.0
  - REG-1084 (INT-008) the adapter persists an ABSTAIN decision
  - REG-1085 (MTH-001) the nonce scanner finds sigs followed by a 0x21 push
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import numpy as np
import pandas as pd
import pytest

from src.ecc.ecdsa_scan import extract_ecdsa_signatures
from src.engines.consensus import TtlManager
from src.engines.e10_supply import E10Supply
from src.engines.orchestrator import EngineOrchestrator
from src.engines.schema import EngineOutput
from src.intelligence.ensemble_predictor import (
    EnsemblePredictor,
    XGBoostPredictor,
)
from src.intelligence.intelligence_adapter import IntelligenceAdapter

_G = bytes.fromhex("0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798")


def test_e10_predicted_price_is_spot_not_the_s2f_level() -> None:
    async def go() -> EngineOutput:
        e = E10Supply()
        out = None
        for spot in np.linspace(60_000.0, 60_100.0, 40):
            out = await e.run("BTC/USDT", {"spot": float(spot), "block_height": 900_000})
        assert out is not None
        return out

    out = asyncio.run(go())
    assert out.confidence >= 0.0 and "protocol_fair_value" in out.metadata
    assert out.metadata["protocol_fair_value"] > 5 * 60_100.0  # the level is huge
    assert out.predicted_price == pytest.approx(60_100.0)


class _Stub:
    def __init__(self, eid: str, direction: int = 0) -> None:
        self.eid, self.direction, self.seen = eid, direction, None

    async def run(self, symbol: str, data: dict) -> EngineOutput:
        self.seen = dict(data)
        return EngineOutput(
            engine_id=self.eid,
            symbol=symbol,
            timestamp_utc=datetime.now(UTC),
            predicted_price=100.0,
            confidence=0.5,
            direction=self.direction,
            horizon_hours=4,
        )


def test_meta_engines_receive_prior_engine_outputs_and_e07_direction() -> None:
    orch = EngineOrchestrator()
    stubs = [_Stub(f"E-{i:02d}", direction=1 if i == 7 else 0) for i in range(1, 19)]
    orch._engines = stubs
    asyncio.run(orch.run("BTC/USDT", {"spot": 100.0}))
    for idx in (7, 8, 14):  # E-08, E-09, E-15
        seen = stubs[idx].seen
        assert "E-01" in seen["engine_outputs"] and "E-07" in seen["engine_outputs"]
        assert seen["e07_direction"] == 1
    assert "engine_outputs" not in stubs[0].seen or not stubs[0].seen["engine_outputs"]


def test_ttl_does_not_flip_inside_the_mid_band() -> None:
    mgr = TtlManager()
    assert {mgr.compute(0.5) for _ in range(6)} == {24}
    mgr.compute(0.9)  # go high
    assert {mgr.compute(0.5) for _ in range(6)} == {1}
    assert mgr.compute(0.1) == 24


class _Raises(XGBoostPredictor):
    def __init__(self) -> None:
        super().__init__()
        self.model = MagicMock()
        self.model.predict.side_effect = RuntimeError("boom")


class _Ok:
    model = object()
    rmse = 0.1
    is_fitted = True

    def predict_with_uncertainty(self, f):
        return 0.6, 0.1


def test_a_member_that_errors_raises_and_is_excluded_from_the_vote() -> None:
    with pytest.raises(RuntimeError):
        _Raises().predict(pd.DataFrame({"x": [1.0]}))
    ens = object.__new__(EnsemblePredictor)
    ens.models = {"bad": _Raises(), "ok": _Ok()}
    ens.weights = {"bad": 0.5, "ok": 0.5}
    ens._update_weights = lambda: None  # type: ignore[method-assign]
    res = ens.predict(pd.DataFrame({"x": [1.0]}))
    assert res.point_estimate == pytest.approx(0.6)
    assert res.failed_models == ("bad",)


def test_adapter_persists_an_abstain_decision_when_no_signal_is_sized() -> None:
    intel = MagicMock()
    intel.on_bar = AsyncMock(return_value=None)
    intel.last_decision = {
        "action": "ABSTAIN",
        "direction": 0,
        "expected_return": 0.001,
        "uncertainty": 0.01,
        "conflict": False,
        "contributions": {1: 0.5},
        "model_versions": {1: "v1"},
        "freshness_seconds": {1: 2.0},
        "abstain_reason": "validated portfolio risk context unavailable",
        "regime_id": 2,
    }
    storage = MagicMock()
    storage.store_intelligence_features = AsyncMock()
    asyncio.run(IntelligenceAdapter(intel, storage).on_bar("BTC/USDT", "1m", 1000, {"close": 1.0}))
    storage.store_intelligence_features.assert_awaited_once()
    f = storage.store_intelligence_features.await_args.kwargs["features"]
    assert f["direction_v6"] == 0.0 and f["size_pct_v6"] == 0.0
    assert f["algo_v6"] == "ABSTAIN" and f["regime_id_v6"] == 2.0


def _der(r: int, s: int) -> bytes:
    rb, sb = r.to_bytes(32, "big"), s.to_bytes(32, "big")
    body = b"\x02\x20" + rb + b"\x02\x20" + sb
    return b"\x30" + bytes([len(body)]) + body


@pytest.mark.parametrize("push", [b"\x21", b""])
def test_signature_followed_by_push_opcode_and_pubkey_is_found(push: bytes) -> None:
    sig = _der(0x11 << 200, 0x22 << 200)
    raw = b"\x01\x00\x00\x00" + sig + b"\x01" + push + _G + b"\x00" * 8
    found = extract_ecdsa_signatures(raw.hex())
    assert len(found) == 1 and found[0][2] == _G
