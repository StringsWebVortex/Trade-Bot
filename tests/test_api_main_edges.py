"""Coverage for the small uncovered branches in src/api/main.py.

Targets the pieces reachable without standing up the full app lifespan:
the shared operator validator behind several request models, the
CryptoBoxSignalAdapter singleton cache, and the /crypto-box/status
response shaping.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

import src.api.main as api_main
from src.api.main import (
    RecoveryAcknowledgeRequest,
    StrategyReEnableRequest,
    _get_crypto_box_adapter,
    crypto_box_status,
)


def test_reenable_request_accepts_valid_operator():
    req = StrategyReEnableRequest(operator="alice", operator_secret="s3cret")
    assert req.operator == "alice"
    assert req.force is False


def test_reenable_request_force_defaults_false_and_is_settable():
    req = StrategyReEnableRequest(operator="alice", operator_secret="s", force=True)
    assert req.force is True


def test_reenable_request_rejects_invalid_operator():
    with pytest.raises(ValueError):
        StrategyReEnableRequest(operator="bad operator!!", operator_secret="s")


def test_recovery_ack_request_validates_operator():
    req = RecoveryAcknowledgeRequest(operator="bob", operator_secret="s")
    assert req.operator == "bob"


def test_recovery_ack_request_rejects_invalid_operator():
    with pytest.raises(ValueError):
        RecoveryAcknowledgeRequest(operator="!!!", operator_secret="s")


def test_get_crypto_box_adapter_is_cached():
    _get_crypto_box_adapter.cache_clear()
    fake_adapter = MagicMock()
    try:
        with patch(
            "src.engine.crypto_box_adapter.CryptoBoxSignalAdapter", return_value=fake_adapter
        ) as mock_cls:
            first = _get_crypto_box_adapter()
            second = _get_crypto_box_adapter()
        assert first is second is fake_adapter
        mock_cls.assert_called_once()  # constructed once, reused after
    finally:
        _get_crypto_box_adapter.cache_clear()


async def test_crypto_box_status_shapes_response():
    fake_cache = MagicMock()
    fake_cache.get_sentiment.return_value = {"score": 0.5}
    fake_cache.get_macro.return_value = {"dxy": 103.456789, "label": "risk_on"}
    fake_cache._data = {
        "orderbook_BTCUSDT": {},
        "options_BTC": {},
        "unrelated_key": {},
    }

    fake_adapter = MagicMock(enabled=True)

    with (
        patch("src.data.provider_cache.get_provider_cache", return_value=fake_cache),
        patch.object(api_main, "_get_crypto_box_adapter", return_value=fake_adapter),
    ):
        result = await crypto_box_status()

    assert result["enabled"] is True
    assert result["sentiment"] == {"score": 0.5}
    assert result["macro"]["dxy"] == 103.4568  # floats rounded to 4dp
    assert result["macro"]["label"] == "risk_on"  # non-floats passed through
    assert result["orderbook_symbols"] == ["BTCUSDT"]
    assert result["options_symbols"] == ["BTC"]


async def test_crypto_box_status_handles_empty_macro():
    fake_cache = MagicMock()
    fake_cache.get_sentiment.return_value = None
    fake_cache.get_macro.return_value = None
    fake_cache._data = {}

    fake_adapter = MagicMock(enabled=False)

    with (
        patch("src.data.provider_cache.get_provider_cache", return_value=fake_cache),
        patch.object(api_main, "_get_crypto_box_adapter", return_value=fake_adapter),
    ):
        result = await crypto_box_status()

    assert result["enabled"] is False
    assert result["macro"] == {}
    assert result["orderbook_symbols"] == []


def test_security_control_gate_fails_closed_then_allows_healthy_controls():
    from fastapi import HTTPException

    api_main.CONTROL_HEALTH.reset()
    try:
        with pytest.raises(HTTPException) as exc:
            api_main.require_healthy_security_controls()
        assert exc.value.status_code == 503
        api_main.mark_all_healthy()
        api_main.require_healthy_security_controls()
    finally:
        api_main.CONTROL_HEALTH.reset()


async def test_audit_event_marks_control_healthy_after_success():
    storage = MagicMock()
    storage.insert_audit_event = __import__("unittest.mock", fromlist=["AsyncMock"]).AsyncMock(
        return_value="audit-id"
    )
    api_main.CONTROL_HEALTH.reset()
    try:
        result = await api_main._audit_event(storage, event_type="test")
        assert result == "audit-id"
        assert api_main.CONTROL_HEALTH.status(api_main.SecurityControl.AUDIT_LOGGING).healthy
    finally:
        api_main.CONTROL_HEALTH.reset()


async def test_audit_event_marks_control_degraded_and_propagates_failure():
    storage = MagicMock()
    storage.insert_audit_event = __import__("unittest.mock", fromlist=["AsyncMock"]).AsyncMock(
        side_effect=OSError("disk full")
    )
    api_main.CONTROL_HEALTH.reset()
    try:
        with pytest.raises(OSError, match="disk full"):
            await api_main._audit_event(storage, event_type="test")
        status = api_main.CONTROL_HEALTH.status(api_main.SecurityControl.AUDIT_LOGGING)
        assert not status.healthy
        assert status.reason == "OSError"
    finally:
        api_main.CONTROL_HEALTH.reset()


def test_require_ready_and_orchestrator_return_503_during_startup(monkeypatch):
    from fastapi import HTTPException

    monkeypatch.setattr(api_main._state, "ready", False)
    monkeypatch.setattr(api_main._state, "orchestrator", None)
    with pytest.raises(HTTPException) as ready:
        api_main.require_ready()
    assert ready.value.status_code == 503
    with pytest.raises(HTTPException) as orchestrator:
        api_main.require_orchestrator()
    assert orchestrator.value.status_code == 503


def test_require_orchestrator_returns_assigned_instance(monkeypatch):
    expected = object()
    monkeypatch.setattr(api_main._state, "orchestrator", expected)
    assert api_main.require_orchestrator() is expected


async def test_order_status_rejects_bad_id_and_reports_unavailable_executor(monkeypatch):
    monkeypatch.setattr(api_main._state, "orchestrator", None)
    assert await api_main.get_order_status("../bad") == api_main.not_found_response()
    assert await api_main.get_order_status("order-123") == {
        "error": "Orchestrator not initialised."
    }
    monkeypatch.setattr(api_main._state, "orchestrator", MagicMock(_executor=object()))
    result = await api_main.get_order_status("order-123")
    assert "only available in live trading mode" in result["error"]


async def test_order_status_hides_executor_exception_and_missing_state(monkeypatch):
    from unittest.mock import AsyncMock

    executor = MagicMock()
    executor.get_order_fsm_state = AsyncMock(side_effect=RuntimeError("private exchange detail"))
    monkeypatch.setattr(api_main._state, "orchestrator", MagicMock(_executor=executor))
    failed = await api_main.get_order_status("order-123")
    assert failed == {"error": "Failed to look up order status."}
    executor.get_order_fsm_state.side_effect = None
    executor.get_order_fsm_state.return_value = None
    assert await api_main.get_order_status("order-123") == api_main.not_found_response()


async def test_order_status_serializes_existing_fsm_state(monkeypatch):
    from unittest.mock import AsyncMock

    state = MagicMock()
    state.to_dict.return_value = {"status": "FILLED"}
    executor = MagicMock()
    executor.get_order_fsm_state = AsyncMock(return_value=state)
    monkeypatch.setattr(api_main._state, "orchestrator", MagicMock(_executor=executor))
    assert await api_main.get_order_status("order-123") == {"status": "FILLED"}


async def test_horizons_reports_config_when_intel_is_disabled(monkeypatch):
    monkeypatch.setattr(api_main._state, "intel_adapter", None)
    result = await api_main.horizons()
    assert result["enabled"] is False
    assert result["horizons"]
    assert all(item["status"] == "DISABLED" for item in result["horizons"])


async def test_horizons_reports_live_intel_snapshot(monkeypatch):
    intel = MagicMock(
        last_horizon_symbol="BTC/USDT",
        last_horizon_ts=123,
        last_decision={"side": "long"},
        learning_status={"ready": True},
    )
    intel.horizon_status.return_value = [{"horizon": "1h"}]
    intel.worker_pool.health_snapshot.return_value = {"workers": 2}
    monkeypatch.setattr(api_main._state, "intel_adapter", MagicMock(_intel=intel))
    result = await api_main.horizons()
    assert result["enabled"] is True
    assert result["symbol"] == "BTC/USDT"
    assert result["scheduler"] == {"workers": 2}


async def test_models_status_counts_artifacts_and_handles_missing_directory(monkeypatch, tmp_path):
    from unittest.mock import MagicMock

    from src.config import Settings

    monkeypatch.setattr(
        api_main,
        "require_orchestrator",
        lambda: MagicMock(retrain_status=lambda: {"1h": {"state": "idle"}}),
    )
    settings = Settings()
    settings.storage.model_dir = tmp_path / "absent"
    monkeypatch.setattr(api_main, "get_settings", lambda: settings)
    result = await api_main.models_status()
    assert result["timeframes"]["1h"]["artifact_count"] == 0
    model_dir = tmp_path / "models"
    model_dir.mkdir()
    (model_dir / "model_1h.bin").write_bytes(b"model")
    settings.storage.model_dir = model_dir
    result = await api_main.models_status()
    assert result["timeframes"]["1h"]["artifact_count"] == 1
