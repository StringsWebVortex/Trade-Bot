"""Tests for the v4 Bayesian online changepoint detector.

Decides:
  - REG-1090 — BOCPD changepoint probability responds to a mean shift
"""

from __future__ import annotations

import math
import random

import pytest

from src.regime.changepoint import BayesianOnlineChangepointDetector, _logsumexp


def test_rejects_invalid_hazard_rate() -> None:
    with pytest.raises(ValueError, match="hazard_rate"):
        BayesianOnlineChangepointDetector(hazard_rate=0.0)
    with pytest.raises(ValueError, match="hazard_rate"):
        BayesianOnlineChangepointDetector(hazard_rate=1.0)


class TestLogsumexp:
    def test_empty_list_returns_negative_infinity(self) -> None:
        assert _logsumexp([]) == float("-inf")

    def test_all_negative_infinity_returns_negative_infinity(self) -> None:
        assert _logsumexp([float("-inf"), float("-inf")]) == float("-inf")

    def test_matches_naive_sum_for_typical_values(self) -> None:
        values = [-1.0, -2.0, -0.5]
        expected = math.log(sum(math.exp(v) for v in values))
        assert _logsumexp(values) == pytest.approx(expected)

    def test_single_value_returns_itself(self) -> None:
        assert _logsumexp([-3.2]) == pytest.approx(-3.2)


def test_stable_stream_keeps_changepoint_probability_low() -> None:
    rng = random.Random(1)
    detector = BayesianOnlineChangepointDetector(hazard_rate=1.0 / 250.0)
    probs = [detector.update(rng.gauss(0, 1)) for _ in range(150)]
    assert sum(probs[-20:]) / 20 < 0.5


def test_run_length_grows_on_stable_stream() -> None:
    rng = random.Random(2)
    detector = BayesianOnlineChangepointDetector(hazard_rate=1.0 / 250.0)
    for _ in range(100):
        detector.update(rng.gauss(0, 1))
    assert detector.most_likely_run_length > 0


def test_regime_shift_eventually_collapses_run_length() -> None:
    # Per Adams & MacKay (2007): the exact outlier step does not spike
    # changepoint_probability (it's equally surprising to every existing
    # hypothesis, so the hazard-rate ratio is preserved through
    # normalization). What DOES happen is that short-run hypotheses
    # fitted to the new cluster quickly dominate the posterior once a
    # few post-shift points confirm the new regime — observable via
    # most_likely_run_length collapsing back toward 0.
    rng = random.Random(3)
    detector = BayesianOnlineChangepointDetector(hazard_rate=1.0 / 50.0)
    for _ in range(80):
        detector.update(rng.gauss(0, 0.5))
    pre_shift_run_length = detector.most_likely_run_length
    for _ in range(15):
        detector.update(rng.gauss(20, 0.5))
    assert detector.most_likely_run_length < pre_shift_run_length


def test_changepoint_probability_property_matches_last_update() -> None:
    detector = BayesianOnlineChangepointDetector()
    p = detector.update(0.5)
    assert detector.changepoint_probability == p


def test_first_observation_is_not_a_changepoint_signal() -> None:
    # Warm-up is not a changepoint: the expected run length grows as expected.
    detector = BayesianOnlineChangepointDetector(hazard_rate=1.0 / 250.0)
    assert detector.update(1.0) < 0.05


def test_mean_shift_raises_changepoint_probability_well_above_hazard() -> None:
    # DAT-003: P(r=0) is identically the hazard rate; the reported signal
    # must respond to a step change in the mean.
    hazard = 1.0 / 250.0
    rng = random.Random(7)
    detector = BayesianOnlineChangepointDetector(hazard_rate=hazard)
    pre = [detector.update(rng.gauss(0, 0.5)) for _ in range(80)]
    post = [detector.update(rng.gauss(20, 0.5)) for _ in range(15)]
    assert max(pre[20:]) < 0.5
    assert max(post) > 0.5
    assert max(post) > 50 * hazard


def test_zero_mass_hypothesis_survives_pruning() -> None:
    rng = random.Random(8)
    detector = BayesianOnlineChangepointDetector()
    for _ in range(600):
        detector.update(rng.gauss(0, 1))
    assert any(h.run_length == 0 for h in detector._hypotheses)
