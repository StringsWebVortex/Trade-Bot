"""Regressions for the Phase 6 execution/risk/API/security Low findings.

Decides:
  - REG-1400 — Execution and risk helpers fail safe on null, NaN and out-of-range inputs
  - REG-1401 — Control-plane tables and settings reject malformed or mutable definitions
  - SEC-1400 — Security helpers fail closed on unknown or ambiguous inputs
"""

from __future__ import annotations

import asyncio
import ipaddress
import math

import pytest
from pydantic import BaseModel, Field, ValidationError

from src.api.control_surface import _field_bounds
from src.api.middleware import validate_cors_config
from src.config import StrategySettings
from src.execution.idempotency import IdempotencyRegistry
from src.execution.paper import ApprovalRequest, PaperExecutor
from src.execution.router import SmartOrderRouter
from src.risk.gate import RiskGate
from src.risk.portfolio_correlation import PortfolioCorrelationTracker
from src.risk.vol_target_sizer import vol_target_size
from src.runtime.changes import INVERSE, STAGE_FOR
from src.runtime.contracts import TRANSITIONS
from src.runtime.supervisor import SUPERVISOR_TYPES
from src.security.api_signer import ApiSigner
from src.security.credential_vault import CredentialVault
from src.security.exchange_key_posture import (
    Capability,
    KeyPosture,
    PostureViolation,
    assert_safe,
)
from src.security.ssrf import inspect_url


def test_router_order_with_null_filled_does_not_raise() -> None:  # EXR-022
    router = SmartOrderRouter.__new__(SmartOrderRouter)
    res = router._order_to_result(
        "binance", "market", {"id": "1", "filled": None, "average": None}, 100.0, 10.0
    )
    assert res.filled_qty == 0.0 and res.success is False and res.avg_price == 100.0


def test_push_return_does_not_record_a_meaningless_covariance() -> None:  # EXR-023
    t = PortfolioCorrelationTracker()
    for i in range(60):
        t.push_return("A", 0.01 * ((-1) ** i))
        t.push_return("B", 0.01 * ((-1) ** i))
    assert not t._covs


def test_capacity_eviction_keeps_completed_keys_within_ttl() -> None:  # EXR-025
    async def run() -> bool:
        reg = IdempotencyRegistry(max_entries=2)
        for i in range(5):
            await reg.reserve(f"k{i}")
            await reg.complete(f"k{i}", f"o{i}")
        return await reg.seen("k0")

    assert asyncio.run(run())


def test_vol_target_uses_daily_target_and_rejects_nan() -> None:  # EXR-027
    r = vol_target_size(
        100_000.0,
        100_000.0,
        100_000.0,
        realized_vol_pct=50.0,
        target_vol_pct=1.0,
        kelly_fraction=1.0,
        max_notional_pct=10.0,
        periods_per_year=365,
    )
    # daily vol = 50 / sqrt(365); scalar = 1 / that; ratio times capital, times Kelly 1.0
    expected = 100_000.0 * 1.0 / (50.0 / math.sqrt(365))
    assert r.vol_target_notional == pytest.approx(expected)
    bad = vol_target_size(1e5, 1e5, 1e5, realized_vol_pct=math.nan)
    assert bad.notional_usd == 0.0 and bad.reject_reason == "non_finite_input"


def test_risk_gate_rejects_nan_and_out_of_range_horizon() -> None:  # EXR-028
    gate = RiskGate(n_horizons=3)
    sig = {"confidence": math.nan, "sharpe_est": 5.0, "edge": 0.01, "odds": 1.0}
    res = gate.size(sig, vol=0.01, cvar=0.01, horizon_idx=0)
    assert res.suppressed and res.size_pct == 0.0
    assert gate.check_drift(99, 0.1) is True
    assert gate.check_drift(0, math.nan) is False


def test_pending_approvals_does_not_prune() -> None:  # EXR-030
    ex = PaperExecutor.__new__(PaperExecutor)
    req = ApprovalRequest(
        request_id="r1",
        symbol="BTC/USDT",
        timeframe="15m",
        direction=1,
        notional_usd=1.0,
        entry_price=1.0,
        quantity=1.0,
        kelly_fraction=0.1,
        regime_state=1,
        meta_label_prob=0.6,
        raw_signal=0.5,
        created_at=-1e9,
    )
    req.resolved = True
    ex._approval_queue = {"r1": req}
    assert ex.pending_approvals() == []
    assert "r1" in ex._approval_queue


@pytest.mark.parametrize("cap", [Capability.MARGIN, Capability.FUTURES])
def test_margin_and_futures_keys_are_refused(cap: Capability) -> None:  # API-016
    posture = KeyPosture(
        "binance", frozenset({Capability.READ, cap}), True, True, "op", "2026-01-01"
    )
    with pytest.raises(PostureViolation):
        assert_safe(posture)


def test_signer_canonicalisation_is_unambiguous() -> None:  # API-017
    s = ApiSigner()
    assert s.sign_request("GET", "/a", "b", 1) != s.sign_request("GET", "/ab", "", 1)


def test_vault_rejects_unknown_exchange_and_oversize_index() -> None:  # API-018
    v = CredentialVault(b"x" * 32)
    with pytest.raises(ValueError):
        v.derive("kucoin")
    with pytest.raises(ValueError):
        v.derive("binance", key_index=2**31)


def test_ssrf_blocks_cgnat() -> None:  # API-020
    assert ipaddress.ip_address("100.64.0.1").is_global is False
    verdict = inspect_url("https://example.test/", resolver=lambda host: ("100.64.0.1",))
    assert verdict.allowed is False


def test_cors_requires_https_off_loopback() -> None:  # API-024
    with pytest.raises(RuntimeError):
        validate_cors_config(["http://example.com"], allow_credentials=False)
    validate_cors_config(["http://localhost:3000"], allow_credentials=False)


def test_field_bounds_keeps_zero_bound() -> None:  # API-026
    class M(BaseModel):
        x: float = Field(default=0.0, ge=0.0, le=0.0)

    assert _field_bounds(M.model_fields["x"]) == (0.0, 0.0)


def test_lookup_tables_are_read_only() -> None:  # API-027
    for table in (TRANSITIONS, INVERSE, STAGE_FOR, SUPERVISOR_TYPES):
        with pytest.raises(TypeError):
            table[object()] = object()  # type: ignore[index]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"mr_min_half_life": 50, "mr_max_half_life": 10},
        {"mr_exit_z": 3.0, "mr_entry_z": 2.0},
        {"bo_exit_period": 30, "bo_entry_period": 20},
        {"bo_min_atr_pct": 20.0, "bo_max_atr_pct": 10.0},
    ],
)
def test_strategy_settings_reject_inverted_pairs(kwargs: dict) -> None:  # API-031
    with pytest.raises(ValidationError):
        StrategySettings(**kwargs)
