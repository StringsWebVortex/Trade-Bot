"""Regression tests for fail-closed edge paths included in aggregate coverage."""

from __future__ import annotations

import logging
from types import SimpleNamespace

import numpy as np
import pytest

from src.agent_control.git_safety import guarded_operations
from src.logging_setup import RedactUrlSecretsFilter, _redact_value, redact_event
from src.mathcore.probability.committee import (
    chernoff_committee_bound,
    committee_failure_probability,
    min_committee_size,
)
from src.regime.garch import (
    Garch11Params,
    _conditional_variance_path,
    rolling_garch_forecast,
)
from src.risk.state_persistence import (
    StateUnreadableError,
    load_state,
    save_state,
    state_dir,
    state_file,
)


def test_state_path_override_and_name_sanitization(tmp_path, monkeypatch):
    monkeypatch.setenv("RISK_STATE_DIR", f" {tmp_path} ")
    assert state_dir() == tmp_path
    assert state_file("../risk state/active").name == ".._risk_state_active.json"


def test_state_dir_uses_default_when_override_is_blank(monkeypatch):
    from src.risk.state_persistence import DEFAULT_STATE_DIR

    monkeypatch.setenv("RISK_STATE_DIR", "  ")
    assert state_dir() == DEFAULT_STATE_DIR


def test_load_state_missing_file_is_first_start(tmp_path):
    assert load_state(tmp_path / "missing.json") is None


@pytest.mark.parametrize(
    "payload",
    [
        "[]",
        "null",
        "{bad json",
        '{"version":2,"state":{}}',
        '{"version":1}',
        '{"version":1,"state":[]}',
    ],
)
def test_load_state_rejects_untrusted_shapes(tmp_path, payload):
    path = tmp_path / "state.json"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(StateUnreadableError):
        load_state(path)


def test_save_state_is_atomic_and_round_trips(tmp_path):
    path = tmp_path / "nested" / "state.json"
    save_state(path, {"halted": True, "reason": "drawdown"})
    assert load_state(path) == {"halted": True, "reason": "drawdown"}
    assert list(path.parent.glob(".risk_state-*")) == []


def test_conditional_variance_handles_empty_and_singleton_inputs():
    assert _conditional_variance_path(np.array([]), 0.1, 0.2, 0.3, 1.0).size == 0
    result = _conditional_variance_path(np.array([2.0]), 0.1, 0.2, 0.3, -1.0)
    assert result.tolist() == [1e-12]


def test_conditional_variance_has_guarded_beta_ge_one_fallback():
    result = _conditional_variance_path(np.array([1.0, 2.0, 3.0]), 0.1, 0.2, 1.0, 1.0)
    assert np.all(np.isfinite(result))
    assert result[1] == pytest.approx(1.3)


def test_rolling_garch_rejects_invalid_refit_interval():
    with pytest.raises(ValueError, match="refit_every"):
        rolling_garch_forecast(__import__("pandas").Series(np.ones(60)), window=50, refit_every=0)


def test_rolling_garch_falls_back_when_optimizer_reports_nonconvergence(monkeypatch):
    import pandas as pd

    import src.regime.garch as garch

    monkeypatch.setattr(
        garch,
        "minimize",
        lambda *a, **k: SimpleNamespace(
            success=False, message="no converge", x=np.array([1.0, 0.1, 0.8])
        ),
    )
    forecast = rolling_garch_forecast(pd.Series(np.linspace(-0.01, 0.01, 55)), window=50)
    assert forecast.iloc[50:].isna().all()


def test_rolling_garch_falls_back_when_optimizer_returns_nonfinite(monkeypatch):
    import pandas as pd

    import src.regime.garch as garch

    monkeypatch.setattr(
        garch,
        "minimize",
        lambda *a, **k: SimpleNamespace(success=True, message="ok", x=np.array([np.nan, 0.1, 0.8])),
    )
    forecast = rolling_garch_forecast(pd.Series(np.linspace(-0.01, 0.01, 55)), window=50)
    assert forecast.iloc[50:].isna().all()


def test_garch_unconditional_variance_degenerate_persistence_is_nan():
    params = Garch11Params(omega=0.1, alpha=0.2, beta=0.8, scale=100.0)
    assert np.isnan(params.unconditional_variance)


@pytest.mark.parametrize("args", [(10, -1, 3, 1), (10, 5, -1, 1), (10, 5, 3, -1)])
def test_committee_exact_probability_rejects_invalid_counts(args):
    with pytest.raises(ValueError):
        committee_failure_probability(*args)


def test_committee_bound_handles_threshold_at_one_and_trivial_tail():
    assert 0.0 < chernoff_committee_bound(0.2, 10, 1.0) < 1.0
    assert chernoff_committee_bound(0.2, 10, 0.2) == 1.0


def test_min_committee_size_handles_single_member_solution():
    assert min_committee_size(0.01, 0.99, 0.5) == 1


def test_logging_redacts_nested_secret_keys_and_embedded_tokens():
    value = {"public": ["token=abc123", {"db_password": "visible"}], "safe": 7}
    redacted = _redact_value(value)
    assert redacted["public"][0] != "token=abc123"
    assert redacted["public"][1]["db_password"] == "[REDACTED]"
    assert redacted["safe"] == 7


def test_logging_redaction_stops_at_maximum_depth():
    value = {"leaf": "token=abc123"}
    for _ in range(9):
        value = {"nested": value}
    assert _redact_value(value) == value


def test_redact_event_handles_non_string_keys_and_secret_fragments():
    event = {"timescale_dsn": "postgres://private", "message": "api_key=abc", 7: "unchanged"}
    assert redact_event(None, "info", event) is event
    assert event["timescale_dsn"] == "[REDACTED]"
    assert event[7] == "unchanged"


def test_url_filter_redacts_query_values_and_preserves_safe_records():
    filt = RedactUrlSecretsFilter()
    record = logging.LogRecord("uvicorn", logging.INFO, "", 1, "/?api_key=secret&x=1", (), None)
    assert filt.filter(record) is True
    assert "api_key=[REDACTED]" in record.getMessage()
    safe = logging.LogRecord("uvicorn", logging.INFO, "", 1, "/?x=1", (), None)
    assert filt.filter(safe) is True
    assert safe.getMessage() == "/?x=1"


def test_git_invocation_handles_wrappers_and_nested_substitutions():
    assert guarded_operations("command timeout 2 git -C repo switch main") == ["switch"]
    assert guarded_operations("echo $(printf x$(git stash drop))") == ["stash"]
    assert guarded_operations("git -c alias.empty='' empty") == []


def test_git_invocation_handles_malformed_alias_and_shell_depth_limit():
    assert guarded_operations("git -c alias.x='unterminated x") == []
    assert guarded_operations("eval eval eval eval git reset") == []


def test_git_invocation_handles_find_exec_plus_and_ok_forms():
    assert guarded_operations("find . -exec git clean -fd {} +") == ["clean"]
    assert guarded_operations("find . -ok git restore {} \\\\;") == ["restore"]


def test_git_invocation_does_not_treat_shell_arithmetic_as_substitution():
    assert guarded_operations("echo $((1 + 2)) && git status") == []
