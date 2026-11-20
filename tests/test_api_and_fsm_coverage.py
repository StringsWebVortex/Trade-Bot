"""
Coverage for small zero-coverage modules — Debt-005.

Covers:
  - src/api/auth.py (verify_websocket_key)
"""

from __future__ import annotations

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

# ---------------------------------------------------------------------------
# auth.py — verify_websocket_key
#
# validate_cors_config, _get_configured_key and verify_api_key are covered by
# tests/test_api_auth_middleware.py (the cases here duplicated them; TSA-06).
# ---------------------------------------------------------------------------


class TestVerifyWsKey:
    _KEY = "w" * 32

    def _set_key(self):
        return patch.dict(os.environ, {"API_SECRET_KEY": self._KEY}, clear=False)

    def _mock_ws(self, key=None, query_key=None):
        ws = MagicMock()
        ws.headers = {"x-api-key": key} if key else {}
        # verify_ws_key falls back to ?api_key= for browser clients, which
        # cannot set upgrade headers. Without a real mapping here the
        # MagicMock returns a MagicMock and the fallback "succeeds" with a
        # non-string, so this has to be an explicit empty dict.
        ws.query_params = {"api_key": query_key} if query_key else {}
        ws.close = AsyncMock()
        ws.client = ("127.0.0.1", 9000)
        return ws

    @pytest.mark.asyncio
    async def test_valid_header_passes(self):
        from src.api.auth import verify_ws_key

        with self._set_key():
            await verify_ws_key(self._mock_ws(key=self._KEY))  # must not raise

    @pytest.mark.asyncio
    async def test_missing_header_raises_401(self):
        from src.api.auth import verify_ws_key

        ws = self._mock_ws()
        with self._set_key(), pytest.raises(HTTPException) as exc:
            await verify_ws_key(ws)
        assert exc.value.status_code == 401
        ws.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_wrong_key_raises_401(self):
        from src.api.auth import verify_ws_key

        ws = self._mock_ws(key="bad")
        with self._set_key(), pytest.raises(HTTPException) as exc:
            await verify_ws_key(ws)
        assert exc.value.status_code == 401

    @pytest.mark.asyncio
    async def test_server_key_not_set_closes_4503(self):
        from src.api.auth import verify_ws_key

        ws = self._mock_ws(key="anything")
        with patch.dict(os.environ, {"API_SECRET_KEY": ""}, clear=False):
            with pytest.raises((HTTPException, RuntimeError)):
                await verify_ws_key(ws)
        ws.close.assert_called()


# ---------------------------------------------------------------------------
# /intelligence/coverage and /intelligence/providers endpoint tests
# ---------------------------------------------------------------------------


class TestIntelligenceEndpoints:
    """OCI-012: coverage and provider-status endpoints."""

    def _make_state(self):
        from unittest.mock import AsyncMock, MagicMock

        from src.api.main import AppState as _AppState

        state = _AppState()
        orch = MagicMock()
        storage = MagicMock()
        storage.intelligence_feature_coverage = AsyncMock(
            return_value={
                "total_rows": 100,
                "coverage": {
                    "intelligence_binance_funding_rate_pct": 1.0,
                    "intelligence_defi_tvl_7d_change_pct": 0.95,
                    "intelligence_mvrv_z_score": 0.0,
                    "intelligence_sopr": 0.0,
                },
            }
        )
        orch._storage = storage

        cfg = MagicMock()
        cfg.symbol = "BTC/USDT"
        cfg.primary_timeframe.value = "1h"
        orch._cfg = cfg
        state.orchestrator = orch

        # VF-022 fix: get_intelligence_coverage() now calls get_settings() directly
        # (not _state.runtime_config, which was never an AppState attribute).
        # Tests patch get_settings at the api.main import site instead.
        return state

    @pytest.mark.asyncio
    async def test_coverage_returns_total_rows_and_coverage_dict(self):
        from unittest.mock import MagicMock, patch

        import src.api.main as api_mod
        from src.api.main import get_intelligence_coverage

        state = self._make_state()
        mock_settings = MagicMock()
        mock_settings.primary_symbol = "BTC/USDT"
        mock_settings.primary_timeframe.value = "1h"

        orig = api_mod._state
        try:
            api_mod._state = state
            with patch("src.api.main.get_settings", return_value=mock_settings):
                result = await get_intelligence_coverage()
        finally:
            api_mod._state = orig

        assert result["total_rows"] == 100
        assert "coverage" in result
        assert result["coverage"]["intelligence_defi_tvl_7d_change_pct"] == 0.95

    @pytest.mark.asyncio
    async def test_coverage_no_orchestrator_returns_error(self):
        import src.api.main as api_mod
        from src.api.main import AppState as _AppState
        from src.api.main import get_intelligence_coverage

        state = _AppState()
        orig = api_mod._state
        try:
            api_mod._state = state
            result = await get_intelligence_coverage()
        finally:
            api_mod._state = orig

        assert "error" in result

    @pytest.mark.asyncio
    async def test_providers_returns_five_providers(self):
        from src.api.main import get_intelligence_providers

        result = await get_intelligence_providers()
        assert "providers" in result
        providers = result["providers"]
        assert len(providers) == 5
        ids = {p["exchange_id"] for p in providers}
        assert ids == {"arkham_intel", "defillama", "dune_analytics", "cryptoquant", "coinglass"}

    @pytest.mark.asyncio
    async def test_defillama_always_enabled(self):
        from src.api.main import get_intelligence_providers

        result = await get_intelligence_providers()
        defillama = next(p for p in result["providers"] if p["exchange_id"] == "defillama")
        assert defillama["enabled"] is True
