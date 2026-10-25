"""
The dashboard's WebSocket could never authenticate.

frontend/src/App.jsx connects with ``?api_key=...`` and says why in its own
comment: browsers cannot set headers on a WebSocket upgrade. verify_ws_key
read only the header, so every browser connection was closed 4401 -- which
went unnoticed because the REST polling that fills most of the UI does set
the header and kept working.

Decides:
  - API-005 — WebSocket payloads are validated regardless of connection state
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from src.api.access_control import Role
from src.api.auth import verify_ws_key

_PRIMARY = "a" * 40
_READONLY = "b" * 40


@pytest.fixture(autouse=True)
def _keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_SECRET_KEY", _PRIMARY)
    monkeypatch.delenv("API_READONLY_KEY", raising=False)


def _proto(key: str) -> str:
    return f"tradebot.v1, apikey.{key.encode().hex()}"


def _ws(
    header: str | None = None, query: str | None = None, proto: str | None = None
) -> MagicMock:
    ws = MagicMock()
    ws.headers = {"x-api-key": header} if header else {}
    if proto:
        ws.headers["sec-websocket-protocol"] = proto
    ws.query_params = {"api_key": query} if query else {}
    ws.close = AsyncMock()
    return ws


class TestSubprotocolFallback:
    """SEC-1014: the browser key rides Sec-WebSocket-Protocol, not the URL."""

    @pytest.mark.asyncio
    async def test_a_browser_style_subprotocol_authenticates(self) -> None:
        """The exact shape frontend/src/hooks/useApi.js sends."""
        assert await verify_ws_key(_ws(proto=_proto(_PRIMARY))) is Role.TRADE_AUTHORIZING

    @pytest.mark.asyncio
    async def test_a_query_param_key_is_no_longer_accepted(self) -> None:
        """
        uvicorn logs the handshake URL in cleartext; a key accepted from the
        query string is a key written to the log. Would fail before SEC-1014.
        """
        ws = _ws(query=_PRIMARY)
        with pytest.raises(HTTPException):
            await verify_ws_key(ws)
        ws.close.assert_awaited_once_with(code=4401)

    @pytest.mark.asyncio
    async def test_a_wrong_subprotocol_key_is_rejected(self) -> None:
        ws = _ws(proto=_proto("z" * 40))
        with pytest.raises(HTTPException):
            await verify_ws_key(ws)
        ws.close.assert_awaited_once_with(code=4401)

    @pytest.mark.asyncio
    async def test_a_malformed_hex_subprotocol_is_rejected(self) -> None:
        ws = _ws(proto="tradebot.v1, apikey.not-hex")
        with pytest.raises(HTTPException):
            await verify_ws_key(ws)

    @pytest.mark.asyncio
    async def test_a_read_only_key_resolves_to_its_role(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("API_READONLY_KEY", _READONLY)
        assert await verify_ws_key(_ws(proto=_proto(_READONLY))) is Role.READ_ONLY


class TestHeaderStillPreferred:
    @pytest.mark.asyncio
    async def test_the_header_path_is_unchanged(self) -> None:
        assert await verify_ws_key(_ws(header=_PRIMARY)) is Role.TRADE_AUTHORIZING

    @pytest.mark.asyncio
    async def test_the_header_wins_when_both_are_present(self) -> None:
        """
        Query strings appear in proxy and access logs where headers do not,
        so a client that can set a header must keep using it.
        """
        assert await verify_ws_key(_ws(header=_PRIMARY, proto=_proto("z" * 40))) is (
            Role.TRADE_AUTHORIZING
        )

    @pytest.mark.asyncio
    async def test_neither_supplied_is_rejected(self) -> None:
        ws = _ws()
        with pytest.raises(HTTPException):
            await verify_ws_key(ws)
        ws.close.assert_awaited_once_with(code=4401)


def test_the_frontend_sends_the_subprotocol_the_server_reads() -> None:
    """
    The break was a name/mechanism mismatch across the boundary, so pin the
    contract from the frontend side too — the server's own tests could not
    have caught it.
    """
    from pathlib import Path

    # Scan the whole frontend source rather than a single file. The call
    # lives in hooks/useApi.js, not App.jsx where this test used to look, so
    # pinning the filename reported a broken contract when the contract was
    # intact and only the file had changed.
    frontend_src = Path(__file__).resolve().parent.parent / "frontend" / "src"
    sources = [
        path.read_text(encoding="utf-8")
        for pattern in ("*.js", "*.jsx")
        for path in frontend_src.rglob(pattern)
    ]
    assert sources, f"no frontend sources found under {frontend_src}"
    assert any("apikey." in text for text in sources), (
        "frontend no longer sends the apikey.<hex> subprotocol — update the server"
    )
    assert not any("?api_key=" in text for text in sources), (
        "frontend puts the API key in the URL, where uvicorn logs it"
    )
