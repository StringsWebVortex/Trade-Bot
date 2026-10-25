"""
The operator second factor, checked in one place with a global lockout.

API-007: the secret used to be compared inline at six call sites, each behind
at most a per-endpoint, per-IP rate limit, so wrong guesses across ~15
endpoints (and /execution-mode checked the secret before any limit at all)
were effectively unbounded. Every check now goes through verify_operator_secret
and shares one failure budget: MAX_FAILURES wrong guesses inside WINDOW_S locks
every operator-secret route, correct secret included, until the oldest failure
ages out. Rotating the source IP does not reset it.
"""

from __future__ import annotations

import collections
import hmac
import os
import time

MIN_SECRET_LENGTH = 32
MAX_FAILURES = 5
WINDOW_S = 300.0


class OperatorSecretError(Exception):
    """A refused operator-secret check. Carries the HTTP status to use."""

    def __init__(self, status: int, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.detail = detail


_failures: collections.deque[float] = collections.deque(maxlen=MAX_FAILURES)


def reset_failures() -> None:
    """Clear the failure budget (tests, and an operator restart)."""
    _failures.clear()


def _prune(now: float) -> None:
    while _failures and now - _failures[0] >= WINDOW_S:
        _failures.popleft()


def verify_operator_secret(provided: str) -> None:
    """Raise OperatorSecretError unless *provided* is the configured secret."""
    expected = os.environ.get("OPERATOR_SECRET", "").strip()
    if not expected:
        raise OperatorSecretError(503, "OPERATOR_SECRET is not configured on the server.")
    now = time.monotonic()
    _prune(now)
    if len(_failures) >= MAX_FAILURES:
        raise OperatorSecretError(
            429, "Too many failed operator-secret attempts. Try again later."
        )
    if not hmac.compare_digest((provided or "").encode("utf-8"), expected.encode("utf-8")):
        _failures.append(now)
        raise OperatorSecretError(401, "Invalid operator secret.")
