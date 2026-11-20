"""
SEC-0017 -- outbound provider requests connect to the address the SSRF guard vetted.

The guard used to resolve the host with a blocking `socket.getaddrinfo`, and
httpx then resolved it a second time to connect. A DNS-rebinding server can
answer the first lookup with a public address and the second with a private
one, so the check passed and the request reached the internal address.

These tests drive the real `resolve_allowed` and `PinnedTransport` with an
injected resolver and an `httpx.MockTransport` inner transport: no DNS, no
socket.
"""

from __future__ import annotations

import asyncio
import socket

import httpx
import pytest

from src.security import ssrf
from src.security.ssrf import PinnedTarget, PinnedTransport, SSRFError, resolve_allowed


def _rebinding_resolver(first: str, then: str):
    """Answers `first` once, then `then` for every later lookup."""
    calls: list[str] = []

    async def _resolve(host: str) -> tuple[str, ...]:
        calls.append(host)
        return (first,) if len(calls) == 1 else (then,)

    return _resolve, calls


def _recording_inner():
    seen: list[httpx.Request] = []

    def _handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"ok": True})

    return httpx.MockTransport(_handler), seen


def _target(**overrides) -> PinnedTarget:
    fields = {
        "url": "https://api.example.com/v1",
        "scheme": "https",
        "host": "api.example.com",
        "port": 443,
        "addresses": ("93.184.216.34",),
    }
    fields.update(overrides)
    return PinnedTarget(**fields)


@pytest.mark.parametrize("vetted", ["93.184.216.34", "2606:2800:220:1::1"])
async def test_request_uses_vetted_address_after_rebind(vetted):
    resolver, calls = _rebinding_resolver(vetted, "10.0.0.5")
    target = await resolve_allowed("https://api.example.com/v1", resolver=resolver)
    inner, seen = _recording_inner()

    async with httpx.AsyncClient(transport=PinnedTransport(target, inner=inner)) as client:
        response = await client.get(f"{target.url}/metrics")

    assert response.status_code == 200
    assert calls == ["api.example.com"]  # one lookup; the rebound answer is never asked for
    (sent,) = seen
    assert sent.url.host == vetted
    assert sent.url.path == "/v1/metrics"
    assert sent.headers["Host"] == "api.example.com"
    assert sent.extensions["sni_hostname"] == "api.example.com"


async def test_a_rebound_private_answer_is_refused_at_resolution():
    resolver, _ = _rebinding_resolver("10.0.0.5", "93.184.216.34")
    with pytest.raises(SSRFError, match="private network"):
        await resolve_allowed("https://api.example.com/v1", resolver=resolver)


@pytest.mark.parametrize(
    ("url", "reason"),
    [
        ("file:///etc/passwd", "scheme"),
        ("https:///no-host", "no host"),
        ("https://api.example.com:99999/", "invalid port"),
    ],
)
async def test_resolve_allowed_refuses_a_malformed_destination(url, reason):
    async def _public(_host: str) -> tuple[str, ...]:
        return ("93.184.216.34",)

    with pytest.raises(SSRFError, match=reason):
        await resolve_allowed(url, resolver=_public)


@pytest.mark.parametrize(
    "url",
    [
        "https://other.example.com/v1",
        "https://api.example.com:8443/v1",
        "http://api.example.com/v1",
    ],
)
async def test_the_transport_refuses_an_origin_it_did_not_vet(url):
    inner, seen = _recording_inner()
    async with httpx.AsyncClient(transport=PinnedTransport(_target(), inner=inner)) as client:
        with pytest.raises(SSRFError, match="was vetted"):
            await client.get(url)
    assert seen == []


def test_a_target_without_an_address_cannot_be_pinned():
    inner, _ = _recording_inner()
    with pytest.raises(SSRFError, match="no vetted address"):
        PinnedTransport(_target(addresses=()), inner=inner)


async def test_resolution_runs_on_the_loop_resolver_not_blocking_getaddrinfo(monkeypatch):
    def _blocking(*_args, **_kwargs):
        raise AssertionError("socket.getaddrinfo called on the event loop")

    loop_calls: list[str] = []

    async def _loop_getaddrinfo(host, port, *, proto=0, **_kwargs):
        loop_calls.append(host)
        assert proto == socket.IPPROTO_TCP
        return [(socket.AF_INET, socket.SOCK_STREAM, proto, "", ("93.184.216.34", 0))]

    monkeypatch.setattr(ssrf.socket, "getaddrinfo", _blocking)
    monkeypatch.setattr(asyncio.get_running_loop(), "getaddrinfo", _loop_getaddrinfo)

    target = await resolve_allowed("https://api.example.com/v1")

    assert loop_calls == ["api.example.com"]
    assert target.addresses == ("93.184.216.34",)
    assert target.port == 443


async def test_a_name_the_loop_cannot_resolve_is_refused(monkeypatch):
    async def _fails(*_args, **_kwargs):
        raise socket.gaierror("nodename nor servname provided")

    monkeypatch.setattr(asyncio.get_running_loop(), "getaddrinfo", _fails)
    with pytest.raises(SSRFError, match="does not resolve"):
        await resolve_allowed("https://api.example.com/v1")
