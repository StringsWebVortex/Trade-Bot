"""REG-1607: the static-invariant checks see what they claim to (audits SCR-011, OPS-023).

Each case is a synthetic tree holding a defect the check used to miss, so a
check that cannot fail on it fails here instead:

* a cycle or package edge written with a relative import;
* a route module other than src/api/main.py, a route added with
  ``add_api_route``, and an in-body auth call that comes after a side effect;
* no route module at all, and a renamed GateStatus, which used to pass as
  "nothing to report";
* ``eval`` in scripts/, and ``yaml.load`` with an explicit SafeLoader, which is
  safe and used to be flagged.

Decides: REG-1607"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_static_invariants.py"


@pytest.fixture(scope="module")
def invariants() -> ModuleType:
    spec = importlib.util.spec_from_file_location("check_static_invariants_reg1607", _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def fake_tree(invariants, tmp_path, monkeypatch):
    (tmp_path / "src").mkdir()
    monkeypatch.setattr(invariants, "REPO", tmp_path)
    monkeypatch.setattr(invariants, "SRC", tmp_path / "src")

    def write(relative: str, source: str) -> None:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source, encoding="utf-8")

    return write


def test_a_relative_import_cycle_is_flagged(invariants, fake_tree) -> None:
    fake_tree("src/pkg/__init__.py", "")
    fake_tree("src/pkg/a.py", "from .b import go\n")
    fake_tree("src/pkg/b.py", "from . import a\n")
    problems = invariants.check_import_cycles()
    assert any("src.pkg.a" in p and "src.pkg.b" in p for p in problems)


def test_a_relative_import_crossing_packages_is_a_package_edge(invariants, fake_tree) -> None:
    fake_tree("src/low/__init__.py", "")
    fake_tree("src/low/x.py", "from ..high.y import thing\n")
    fake_tree("src/high/__init__.py", "")
    fake_tree("src/high/y.py", "thing = 1\n")
    edges, _ = invariants._package_edges()
    assert ("low", "high") in edges


def test_a_router_outside_main_is_scanned(invariants, fake_tree) -> None:
    fake_tree("src/api/main.py", "app = FastAPI()\n")
    fake_tree(
        "src/api/extra.py",
        'router = APIRouter()\n@router.get("/open")\nasync def o():\n    return 1\n',
    )
    problems = invariants.check_every_route_is_authenticated()
    assert any("src/api/extra.py" in p and "/open" in p for p in problems)


@pytest.mark.parametrize(
    ("call", "flagged"),
    [
        ('app.add_api_route("/x", handler)', True),
        ('app.add_api_route("/x", handler, dependencies=[Depends(api_key_header)])', False),
    ],
)
def test_add_api_route_needs_a_guard(invariants, fake_tree, call: str, flagged: bool) -> None:
    fake_tree("src/api/main.py", f"app = FastAPI()\n{call}\n")
    assert bool(invariants.check_every_route_is_authenticated()) is flagged


@pytest.mark.parametrize(
    ("body", "flagged"),
    [
        ("    await verify_ws_key(ws)\n    await add_ws_client(ws)\n", False),
        ('    """Docstring."""\n    await verify_ws_key(ws)\n', False),
        ("    await add_ws_client(ws)\n    await verify_ws_key(ws)\n", True),
    ],
)
def test_in_body_auth_counts_only_as_the_first_statement(
    invariants, fake_tree, body: str, flagged: bool
) -> None:
    fake_tree("src/api/main.py", f'@app.websocket("/ws")\nasync def w(ws):\n{body}')
    assert bool(invariants.check_every_route_is_authenticated()) is flagged


def test_no_route_module_is_reported_not_passed(invariants, fake_tree) -> None:
    fake_tree("src/other.py", "x = 1\n")
    assert invariants.check_every_route_is_authenticated() != []


def test_a_renamed_gate_status_is_reported_not_passed(invariants, fake_tree) -> None:
    fake_tree(
        "src/risk/gates.py",
        "class GateOutcome:\n    PASS = 'pass'\n    HALT_X = 'x'\n"
        "def evaluate_all_gates(state):\n    return []\n",
    )
    assert invariants.check_every_gate_status_is_reachable() != []


def test_eval_in_scripts_is_flagged(invariants, fake_tree) -> None:
    fake_tree("scripts/tool.py", "def go(text):\n    return eval(text)\n")
    problems = invariants.check_no_eval_or_exec()
    assert any("scripts/tool.py" in p for p in problems)


@pytest.mark.parametrize(
    "call",
    [
        "yaml.load(text, Loader=yaml.SafeLoader)",
        "yaml.load(text, Loader=CSafeLoader)",
        "yaml.load(text, yaml.SafeLoader)",
    ],
)
def test_yaml_load_with_a_safe_loader_passes(invariants, fake_tree, call: str) -> None:
    fake_tree("src/conf.py", f"import yaml\ndef go(text):\n    return {call}\n")
    assert invariants.check_yaml_uses_safe_load() == []


def test_yaml_load_with_an_unsafe_loader_is_still_flagged(invariants, fake_tree) -> None:
    unsafe = "import yaml\ndef go(text):\n    return yaml.load(text, Loader=yaml.Loader)\n"
    fake_tree("src/conf.py", unsafe)
    assert invariants.check_yaml_uses_safe_load() != []
