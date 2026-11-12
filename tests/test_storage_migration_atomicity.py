"""
REG-1709, REG-1710 (DAT-021): a storage write that fails leaves nothing half done.

REG-1709: each schema migration and its user_version bump are one
transaction. A migration whose second statement fails used to leave the
first applied and the version unbumped, so every later start failed on
"duplicate column" and the database could not be opened again.

REG-1710: update_trade_ensemble_fields holds the write lock through
_write_ctx, so a failed UPDATE is rolled back instead of stranding an open
transaction on the shared connection (the BUGFIX-001 deadlock).
"""

from __future__ import annotations

import pathlib
import sqlite3

import pytest

import src.data.storage as storage
from src.data.storage import StorageBackend, TradeRecord

_CREATE = "CREATE TABLE dat021 (id INTEGER PRIMARY KEY);"
_BROKEN = "ALTER TABLE dat021 ADD COLUMN a INTEGER;\nALTER TABLE dat021 ADD COLUMN;"
_FIXED = "ALTER TABLE dat021 ADD COLUMN a INTEGER;\nALTER TABLE dat021 ADD COLUMN b INTEGER;"


async def _columns_and_version(backend: StorageBackend) -> tuple[list[str], int]:
    conn = backend._require_conn()
    cols = [r[1] for r in await (await conn.execute("PRAGMA table_info(dat021)")).fetchall()]
    version = (await (await conn.execute("PRAGMA user_version")).fetchone())[0]
    return cols, version


def _use_migrations(monkeypatch: pytest.MonkeyPatch, second: str) -> None:
    migrations = [(1, "create", _CREATE), (2, "two columns", second)]
    monkeypatch.setattr(storage, "_MIGRATIONS", migrations)
    monkeypatch.setattr(storage, "_SCHEMA_VERSION", len(migrations))


async def test_a_partial_migration_rolls_back_and_a_retry_succeeds(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = str(tmp_path / "migrate.db")

    _use_migrations(monkeypatch, _BROKEN)
    failed = StorageBackend(db)
    with pytest.raises(sqlite3.OperationalError):
        await failed.initialize()
    try:
        cols, version = await _columns_and_version(failed)
        assert cols == ["id"]  # the first ALTER of migration 2 was rolled back
        assert version == 1  # migration 1 committed on its own
    finally:
        await failed.close()

    _use_migrations(monkeypatch, _FIXED)
    retried = StorageBackend(db)
    await retried.initialize()
    try:
        assert await _columns_and_version(retried) == (["id", "a", "b"], 2)
    finally:
        await retried.close()


def _trade(trade_id: str) -> TradeRecord:
    return TradeRecord(
        id=trade_id,
        symbol="BTC/USDT",
        timeframe="15m",
        trading_mode="paper",
        execution_mode="paper",
        direction=1,
        entry_price=100.0,
        exit_price=None,
        quantity=1.0,
        notional_usd=100.0,
        entry_ts=1000,
        exit_ts=None,
        pnl_usd=None,
        pnl_pct=None,
        fee_usd=0.1,
        kelly_fraction=0.1,
        regime_at_entry=1,
        meta_label_prob=0.6,
        exit_reason=None,
        approved_by="system",
        raw_signal=0.5,
    )


async def test_a_failed_ensemble_update_does_not_strand_a_transaction(
    tmp_path: pathlib.Path,
) -> None:
    backend = StorageBackend(str(tmp_path / "trades.db"))
    await backend.initialize()
    try:
        await backend.insert_trade(_trade("t1"))
        conn = backend._require_conn()
        # A BEFORE UPDATE trigger aborts the statement after the implicit
        # BEGIN, which is how a constraint or I/O failure leaves it open.
        await conn.execute(
            "CREATE TRIGGER dat021_abort BEFORE UPDATE ON trades "
            "BEGIN SELECT RAISE(ABORT, 'dat021'); END"
        )
        await conn.commit()

        with pytest.raises(sqlite3.IntegrityError, match="dat021"):
            await backend.update_trade_ensemble_fields("t1", 1.0, 0.5)
        assert not conn.in_transaction

        await conn.execute("DROP TRIGGER dat021_abort")
        await conn.commit()
        await backend.insert_trade(_trade("t2"))  # the connection still writes
    finally:
        await backend.close()
