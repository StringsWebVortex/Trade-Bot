"""
Pure-logic tests for src/api/auth.py and src/api/middleware.py.

Tests input validation and CORS config enforcement without any HTTP server
or exchange connectivity.
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException

from src.api.access_control import Role
from src.api.auth import (
    _MIN_KEY_LENGTH,
    _get_configured_key,
    _get_readonly_key,
    verify_api_key,
)
from src.api.middleware import validate_cors_config


@pytest.fixture(autouse=True)
def _no_ambient_readonly_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every test in this module starts from "no read-only key configured"."""
    monkeypatch.delenv("API_READONLY_KEY", raising=False)


# ---------------------------------------------------------------------------
# src/api/middleware.py — validate_cors_config
# ---------------------------------------------------------------------------


class TestValidateCorsConfig:
    @pytest.mark.parametrize(
        ("origins", "allow_credentials"),
        [
            (["https://example.com"], False),
            (["http://localhost:3000"], True),
            (["https://app.example.com", "https://api.example.com"], True),
            ([], True),
            (["https://sub.domain.example.co.uk"], False),
            (["https://api.example.com:8443"], False),
        ],
        ids=["https", "http-port", "multiple", "empty", "subdomain", "https-port"],
    )
    def test_valid_origins_pass(self, origins: list[str], allow_credentials: bool) -> None:
        assert validate_cors_config(origins, allow_credentials=allow_credentials) is None

    @pytest.mark.parametrize(
        ("origins", "allow_credentials", "match"),
        [
            # '*' fails the hostname regex regardless of allow_credentials
            (["*"], False, "does not match"),
            (["*"], True, "allow_credentials"),
            (["null"], False, "null"),
            (["NULL"], False, "null"),
            (["192.168.1.1:8080"], False, "does not match"),
            (["192.168.1.1"], False, "does not match"),
            (["example.com"], False, "does not match"),
            (["https://good.example.com", "bad-origin"], False, "bad-origin"),
        ],
        ids=[
            "wildcard",
            "wildcard-credentials",
            "null",
            "null-uppercase",
            "bare-ip-port",
            "bare-ip",
            "schemeless",
            "first-invalid-of-many",
        ],
    )
    def test_invalid_origins_raise(
        self, origins: list[str], allow_credentials: bool, match: str
    ) -> None:
        with pytest.raises(RuntimeError, match=match):
            validate_cors_config(origins, allow_credentials=allow_credentials)


# ---------------------------------------------------------------------------
# src/api/auth.py — _get_configured_key
# ---------------------------------------------------------------------------


class TestGetConfiguredKey:
    def test_missing_key_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("API_SECRET_KEY", raising=False)
        with pytest.raises(RuntimeError, match="not set"):
            _get_configured_key()

    def test_empty_key_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", "")
        with pytest.raises(RuntimeError, match="not set"):
            _get_configured_key()

    def test_short_key_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", "tooshort")
        with pytest.raises(RuntimeError, match="too short"):
            _get_configured_key()

    def test_exactly_min_length_passes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        key = "a" * _MIN_KEY_LENGTH
        monkeypatch.setenv("API_SECRET_KEY", key)
        assert _get_configured_key() == key

    def test_long_key_passes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        key = "x" * 64
        monkeypatch.setenv("API_SECRET_KEY", key)
        assert _get_configured_key() == key

    def test_key_stripped_of_whitespace(self, monkeypatch: pytest.MonkeyPatch) -> None:
        key = "a" * _MIN_KEY_LENGTH
        monkeypatch.setenv("API_SECRET_KEY", f"  {key}  ")
        assert _get_configured_key() == key


class TestVerifyApiKey:
    def test_valid_key_passes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        key = "a" * _MIN_KEY_LENGTH
        monkeypatch.setenv("API_SECRET_KEY", key)
        verify_api_key(key)  # should not raise

    def test_wrong_key_raises_401(self, monkeypatch: pytest.MonkeyPatch) -> None:
        key = "a" * _MIN_KEY_LENGTH
        monkeypatch.setenv("API_SECRET_KEY", key)
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key("wrong" * 10)
        assert exc_info.value.status_code == 401

    def test_none_key_raises_401(self, monkeypatch: pytest.MonkeyPatch) -> None:
        key = "a" * _MIN_KEY_LENGTH
        monkeypatch.setenv("API_SECRET_KEY", key)
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(None)
        assert exc_info.value.status_code == 401

    def test_server_unconfigured_raises_503(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("API_SECRET_KEY", raising=False)
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key("anything")
        assert exc_info.value.status_code == 503

    def test_min_key_length_constant(self) -> None:
        assert _MIN_KEY_LENGTH >= 32  # 256-bit minimum


# ---------------------------------------------------------------------------
# src/api/auth.py — read-only key / role resolution
# ---------------------------------------------------------------------------

_TRADE_KEY = "t" * _MIN_KEY_LENGTH
_READ_KEY = "r" * _MIN_KEY_LENGTH


class TestGetReadonlyKey:
    def test_unset_returns_none(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        assert _get_readonly_key() is None

    def test_empty_returns_none(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        monkeypatch.setenv("API_READONLY_KEY", "   ")
        assert _get_readonly_key() is None

    def test_short_key_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        monkeypatch.setenv("API_READONLY_KEY", "tooshort")
        with pytest.raises(RuntimeError, match="too short"):
            _get_readonly_key()

    def test_key_identical_to_secret_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        monkeypatch.setenv("API_READONLY_KEY", _TRADE_KEY)
        with pytest.raises(RuntimeError, match="identical to API_SECRET_KEY"):
            _get_readonly_key()

    def test_distinct_key_returned_stripped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        monkeypatch.setenv("API_READONLY_KEY", f"  {_READ_KEY}  ")
        assert _get_readonly_key() == _READ_KEY


class TestResolveRole:
    def test_secret_key_is_trade_authorizing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        assert verify_api_key(_TRADE_KEY) is Role.TRADE_AUTHORIZING

    def test_readonly_key_is_read_only(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        monkeypatch.setenv("API_READONLY_KEY", _READ_KEY)
        assert verify_api_key(_READ_KEY) is Role.READ_ONLY

    def test_secret_key_still_trade_authorizing_with_readonly_set(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        monkeypatch.setenv("API_READONLY_KEY", _READ_KEY)
        assert verify_api_key(_TRADE_KEY) is Role.TRADE_AUTHORIZING

    def test_unknown_key_raises_401(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        monkeypatch.setenv("API_READONLY_KEY", _READ_KEY)
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key("x" * _MIN_KEY_LENGTH)
        assert exc_info.value.status_code == 401

    def test_none_key_raises_401(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(None)
        assert exc_info.value.status_code == 401

    def test_readonly_key_rejected_when_not_configured(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(_READ_KEY)
        assert exc_info.value.status_code == 401

    def test_misconfigured_readonly_key_raises_503(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # A weak read-only key must not degrade into "single-key mode" — it
        # fails closed with 503 so the operator notices the misconfiguration.
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        monkeypatch.setenv("API_READONLY_KEY", "weak")
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(_TRADE_KEY)
        assert exc_info.value.status_code == 503

    def test_verify_api_key_accepts_readonly_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("API_SECRET_KEY", _TRADE_KEY)
        monkeypatch.setenv("API_READONLY_KEY", _READ_KEY)
        verify_api_key(_READ_KEY)  # authentication only — should not raise
