"""REG-1602: the runtime control plane's in-memory state is bounded (audit API-021).

* Rejected and cancelled changes beyond the bound are forgotten, oldest first;
  an executed change is never forgotten, so its id cannot be replayed.
* The in-memory change audit keeps the most recent entries only.
* ``AuditPersister`` keeps at most its bound while storage is down, dropping
  the oldest and counting it, and a drop during a write never removes an
  entry that was not written.
* ``RuntimeRegistry`` forgets old version strings, never the current,
  previous or desired one.

Decides: REG-1602"""

from __future__ import annotations

from typing import Any

import pytest

from src.runtime import changes as changes_mod
from src.runtime import persistence as persistence_mod
from src.runtime import registry as registry_mod
from src.runtime.changes import ChangeError, ChangeRequest, ChangeStatus
from src.runtime.contracts import HealthReport, LifecycleAction, LifecycleState
from src.runtime.persistence import AuditPersister
from src.runtime.registry import RuntimeRegistry

from ._support import HUMAN, build_platform, spec

A = LifecycleAction
S = LifecycleState


def _request(cid: str, action: A) -> ChangeRequest:
    return ChangeRequest(component_id=cid, action=action, actor=HUMAN, reason="because")


def test_only_unexecuted_changes_are_forgotten(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(changes_mod, "_UNEXECUTED_LIMIT", 2)
    p = build_platform()
    p.registry.register(spec("w"), observed_state=S.ACTIVE)
    executed = p.changes.submit(_request("worker:w", A.DRAIN))
    assert p.changes.execute(executed.change_id, HUMAN).status is ChangeStatus.PROMOTED
    rejected = [p.changes.submit(_request("worker:nope", A.STOP)) for _ in range(5)]
    assert all(c.status is ChangeStatus.REJECTED for c in rejected)

    kept = {c.change_id for c in p.changes.changes()}
    assert kept == {executed.change_id, rejected[-2].change_id, rejected[-1].change_id}
    with pytest.raises(ChangeError, match="unknown change"):
        p.changes.get(rejected[0].change_id)
    # The executed change is still known, so resubmitting it stays idempotent.
    assert p.changes.submit(executed.request).status is ChangeStatus.PROMOTED


def test_in_memory_audit_keeps_the_most_recent_entries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(changes_mod, "_AUDIT_LIMIT", 3)
    p = build_platform()
    submitted = [p.changes.submit(_request("worker:nope", A.STOP)) for _ in range(5)]
    assert [e.change_id for e in p.changes.audit_log()] == [c.change_id for c in submitted[-3:]]
    assert len(p.audit) == 5  # every entry still reached the sinks


class _Entry:
    def __init__(self, n: int) -> None:
        self.n = n

    def to_dict(self) -> dict[str, Any]:
        return {"change_id": f"chg-{self.n}", "actor": "operator"}


class _Backend:
    def __init__(self) -> None:
        self.fail = False
        self.written: list[str] = []
        self.during_write: Any = None

    async def insert_audit_event(
        self, event_type: str, operator: str, details: dict[str, Any] | None = None
    ) -> None:
        if self.fail:
            raise ConnectionError("storage down")
        if self.during_write is not None:
            hook, self.during_write = self.during_write, None
            hook()
        assert details is not None
        self.written.append(details["change_id"])


async def test_audit_persister_drops_the_oldest_beyond_its_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(persistence_mod, "_PENDING_LIMIT", 2)
    backend = _Backend()
    persister = AuditPersister(backend)
    backend.fail = True
    for n in range(3):
        persister.enqueue(_Entry(n))
    assert persister.pending == 2 and persister.dropped == 1
    assert await persister.flush() == 0

    # Two more arrive while chg-1 is being written: chg-1 itself is dropped
    # by the overflow, and the flush must not then pop chg-2 unwritten.
    backend.fail = False
    backend.during_write = lambda: [persister.enqueue(_Entry(n)) for n in (3, 4)]
    assert await persister.flush() == 3
    assert backend.written == ["chg-1", "chg-3", "chg-4"]
    assert persister.dropped == 3 and persister.pending == 0


def test_registry_forgets_old_versions_but_never_those_in_use(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(registry_mod, "_VERSIONS_LIMIT", 3)
    monkeypatch.setattr(registry_mod, "_PREVIOUS_LIMIT", 2)
    registry = RuntimeRegistry()
    registry.register(spec("w", v="1"), observed_state=S.ACTIVE)
    for v in range(2, 11):
        registry.resync(spec("w", v=str(v)), S.ACTIVE, HealthReport())
    record = registry.get("worker:w")
    assert [v.version for v in record.previous_versions] == ["8", "9"]
    assert [v.version for v in registry.versions("worker:w")] == ["8", "9", "10"]
