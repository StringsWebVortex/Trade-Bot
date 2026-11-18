"""Orchestrator.shutdown() must not block the event loop (audit defect B)."""

from __future__ import annotations

import asyncio
import time
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.test_orchestrator_coverage import _make_orch


async def _run_shutdown_with_ticker(orch: Any) -> tuple[int, float]:
    ticks = 0
    stop = asyncio.Event()

    async def ticker() -> None:
        nonlocal ticks
        while not stop.is_set():
            ticks += 1
            await asyncio.sleep(0.01)

    task = asyncio.create_task(ticker())
    mon = MagicMock()
    mon.stop = AsyncMock(return_value=None)
    start = time.monotonic()
    with patch("src.engine.orchestrator.get_monitor", return_value=mon):
        await orch.shutdown()
    elapsed = time.monotonic() - start
    stop.set()
    await task
    return ticks, elapsed


@pytest.mark.asyncio
async def test_shutdown_waits_for_train_job_off_the_loop() -> None:
    orch = _make_orch()
    orch._executor = None
    done: list[int] = []

    def job() -> None:
        time.sleep(0.6)
        done.append(1)

    orch._train_executor.submit(job)
    await asyncio.sleep(0.05)  # let the worker pick the job up

    ticks, elapsed = await _run_shutdown_with_ticker(orch)

    assert done == [1]  # the in-flight job was still awaited
    assert elapsed >= 0.4
    assert ticks >= 20  # the loop kept running while we waited


@pytest.mark.asyncio
async def test_shutdown_wait_is_bounded_by_timeout() -> None:
    orch = _make_orch()
    orch._executor = None
    orch._train_executor.submit(time.sleep, 1.5)
    await asyncio.sleep(0.05)
    with patch("src.engine.orchestrator.EXECUTOR_SHUTDOWN_TIMEOUT_S", 0.2):
        ticks, elapsed = await _run_shutdown_with_ticker(orch)
    assert elapsed < 1.0
    assert ticks >= 5
