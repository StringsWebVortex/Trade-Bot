"""Atomicity of the SQLite schema-migration runner (audit defect A)."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from unittest.mock import patch

import pytest

from src.data import storage as storage_mod
from src.data.storage import _MIGRATIONS, _SCHEMA_VERSION, StorageBackend


def _columns(db: Path, table: str) -> set[str]:
    with sqlite3.connect(db) as c:
        return {r[1] for r in c.execute(f"PRAGMA table_info({table})")}


def _user_version(db: Path) -> int:
    with sqlite3.connect(db) as c:
        return int(c.execute("PRAGMA user_version").fetchone()[0])


def _last_add_column_migration() -> tuple[int, list[tuple[str, str]]]:
    for version, _desc, sql in reversed(_MIGRATIONS):
        cols = [
            (m.group(1), m.group(2))
            for stmt in storage_mod._split_sql_statements(sql)
            if (m := storage_mod._ADD_COLUMN_RE.match(stmt))
        ]
        if len(cols) >= 2:
            return version, cols
    raise AssertionError("no multi-column ADD COLUMN migration found")


async def _fresh_db_at(db: Path, version: int) -> None:
    """Build a DB fully migrated to ``version`` (not beyond)."""
    sb = StorageBackend(db_path=str(db))
    with (
        patch.object(storage_mod, "_MIGRATIONS", _MIGRATIONS[:version]),
        patch.object(storage_mod, "_SCHEMA_VERSION", version),
    ):
        await sb.initialize()
    await sb.close()
    assert _user_version(db) == version


def test_splitter_respects_literals_and_triggers() -> None:
    sql = (
        "INSERT INTO t VALUES ('a;b');\n"
        "-- comment; only\n"
        "CREATE TRIGGER tr AFTER INSERT ON t BEGIN\n"
        "  UPDATE t SET x = 1;\n"
        "END;\n"
    )
    stmts = storage_mod._split_sql_statements(sql)
    assert len(stmts) == 2
    assert stmts[0].endswith("('a;b');")
    assert "END;" in stmts[1]


@pytest.mark.asyncio
async def test_pre_added_column_from_partial_apply_is_tolerated(tmp_path: Path) -> None:
    db = tmp_path / "t.db"
    version, cols = _last_add_column_migration()
    await _fresh_db_at(db, version - 1)
    table, first_col = cols[0]
    with sqlite3.connect(db) as c:  # simulate a pre-fix partial executescript
        c.execute(f"ALTER TABLE {table} ADD COLUMN {first_col} REAL")

    sb = StorageBackend(db_path=str(db))
    await sb.initialize()
    await sb.close()

    assert _user_version(db) == _SCHEMA_VERSION
    assert {c for _, c in cols} <= _columns(db, table)


@pytest.mark.asyncio
async def test_failure_mid_migration_rolls_back_columns_and_version(tmp_path: Path) -> None:
    db = tmp_path / "t.db"
    version, cols = _last_add_column_migration()
    await _fresh_db_at(db, version - 1)
    table = cols[0][0]
    before = _columns(db, table)

    _v, desc, sql = _MIGRATIONS[version - 1]
    stmts = storage_mod._split_sql_statements(sql)
    broken = "\n".join([*stmts[:2], "INSERT INTO no_such_table_xyz VALUES (1);", *stmts[2:]])
    patched = [*_MIGRATIONS[: version - 1], (version, desc, broken)]

    sb = StorageBackend(db_path=str(db))
    with (
        patch.object(storage_mod, "_MIGRATIONS", patched),
        patch.object(storage_mod, "_SCHEMA_VERSION", version),
        pytest.raises(sqlite3.OperationalError),
    ):
        await sb.initialize()
    if sb._conn is not None:
        await sb._conn.close()
        sb._conn = None

    assert _user_version(db) == version - 1
    assert _columns(db, table) == before

    # The unpatched runner then completes cleanly from the rolled-back state.
    sb2 = StorageBackend(db_path=str(db))
    await sb2.initialize()
    await sb2.close()
    assert _user_version(db) == _SCHEMA_VERSION
