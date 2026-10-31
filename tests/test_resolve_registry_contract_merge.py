from __future__ import annotations

from importlib import util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "resolve_registry_contract_merge.py"
SPEC = util.spec_from_file_location("resolve_registry_contract_merge", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
resolver = util.module_from_spec(SPEC)
SPEC.loader.exec_module(resolver)


BASE = '''
class Registry:
    def test_the_filed_defects_are_the_ones_we_know_about(self, registry):
        assert {e.id for e in registry.by_kind("regression")} == {"REG-0001"}

class Metrics:
    def test_a_filed_defect_is_counted_against_its_layer(self, collector):
        assert metric["value"] == {"test-suite": 1}
'''


def test_accepts_only_additive_registry_ids_and_layer_counts() -> None:
    branch = BASE.replace('{"REG-0001"}', '{"REG-0001", "REG-0002"}').replace(
        '{"test-suite": 1}', '{"test-suite": 2, "review": 1}'
    )
    assert resolver.can_discard_legacy_pins(BASE, branch)


def test_rejects_behavioral_changes_outside_the_pins() -> None:
    branch = BASE.replace(
        'assert {e.id for e in registry.by_kind("regression")} == {"REG-0001"}',
        'assert {e.id for e in registry.by_kind("regression")} == '
        '{"REG-0001", "REG-0002"}\n        assert registry.kind_definitions',
    ).replace('{"test-suite": 1}', '{"test-suite": 2}')
    assert not resolver.can_discard_legacy_pins(BASE, branch)


def test_rejects_removed_ids_or_decreased_layer_counts() -> None:
    removed_id = BASE.replace('{"REG-0001"}', 'set()')
    fewer_counts = BASE.replace('{"test-suite": 1}', '{"test-suite": 0}')
    assert not resolver.can_discard_legacy_pins(BASE, removed_id)
    assert not resolver.can_discard_legacy_pins(BASE, fewer_counts)
