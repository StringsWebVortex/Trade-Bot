"""
Bayesian online changepoint detection — v4 Adaptive Regime & Model Layer.

Complements the existing single HMM regime detector (src/regime/detector.py)
with a model-free signal for "the underlying return-generating process just
changed," independent of any specific regime label. Implements a simplified
version of Adams & MacKay (2007) BOCPD: maintains a run-length distribution
and flags a changepoint when the probability mass shifts sharply toward
run-length 0 (i.e. "we just started a new regime").

This is deliberately simpler than the full BOCPD (constant hazard rate,
Gaussian predictive model with online mean/variance) — sufficient to serve
as one vote in the v4 regime ensemble, not a standalone research artifact.

Authority:
  - Adams & MacKay (2007) "Bayesian Online Changepoint Detection"
  - Domain Prior: treat HMM transitions as probabilistic; avoid hard-coded
    regime logic — this detector outputs a continuous changepoint
    probability, never a hard boolean regime switch.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass(slots=True)
class _RunLengthHypothesis:
    """One hypothesis in the run-length distribution: (run_length, prob, mean, var, n)."""

    run_length: int
    log_prob: float
    mean: float
    m2: float  # sum of squared deviations, Welford's algorithm
    n: int

    @property
    def variance(self) -> float:
        return self.m2 / self.n if self.n > 0 else 1.0


def _log_gaussian_pdf(x: float, mean: float, variance: float) -> float:
    variance = max(variance, 1e-8)
    return -0.5 * math.log(2 * math.pi * variance) - ((x - mean) ** 2) / (2 * variance)


@dataclass(slots=True)
class BayesianOnlineChangepointDetector:
    """
    Online changepoint detector over a scalar stream (e.g. bar returns).

    hazard_rate: prior probability of a changepoint at any given step
    (constant-hazard assumption — simplification vs. full BOCPD's
    arbitrary hazard function, adequate for an ensemble vote).
    """

    hazard_rate: float = 1.0 / 250.0  # ~once per 250 bars, a priori
    _hypotheses: list[_RunLengthHypothesis] = field(default_factory=list)
    _last_changepoint_prob: float = 0.0
    _last_expected_run_length: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 < self.hazard_rate < 1.0:
            raise ValueError(f"hazard_rate must be in (0, 1), got {self.hazard_rate}")
        self._hypotheses = [_RunLengthHypothesis(run_length=0, log_prob=0.0, mean=0.0, m2=0.0, n=0)]

    def update(self, x: float) -> float:
        """
        Process one new observation. Returns a changepoint signal in [0, 1]:
        the relative drop of the posterior expected run length versus its
        no-change trajectory (mass on r=0 alone is constant = hazard rate).
        """
        # Predictive probability of x under each existing hypothesis
        pred_log_probs = [
            _log_gaussian_pdf(x, h.mean, h.variance if h.n > 1 else 1.0) for h in self._hypotheses
        ]

        # Growth probabilities: hypothesis survives, run length += 1
        growth_log_probs = [
            h.log_prob + p + math.log(1.0 - self.hazard_rate)
            for h, p in zip(self._hypotheses, pred_log_probs, strict=True)
        ]

        # Changepoint probability: total mass restarting at run_length=0
        cp_terms = [
            h.log_prob + p + math.log(self.hazard_rate)
            for h, p in zip(self._hypotheses, pred_log_probs, strict=True)
        ]
        cp_log_prob = _logsumexp(cp_terms) if cp_terms else math.log(1.0)

        # Build new hypothesis list: one fresh (run_length=0) + grown survivors
        new_hypotheses = [
            _RunLengthHypothesis(run_length=0, log_prob=cp_log_prob, mean=x, m2=0.0, n=1)
        ]
        for h, glp in zip(self._hypotheses, growth_log_probs, strict=True):
            new_mean = h.mean + (x - h.mean) / (h.n + 1)
            new_m2 = h.m2 + (x - h.mean) * (x - new_mean)
            new_hypotheses.append(
                _RunLengthHypothesis(
                    run_length=h.run_length + 1, log_prob=glp, mean=new_mean, m2=new_m2, n=h.n + 1
                )
            )

        # Normalize
        total_log = _logsumexp([h.log_prob for h in new_hypotheses])
        for h in new_hypotheses:
            h.log_prob -= total_log

        # Bound hypothesis count to keep this O(1)-ish per step long-run.
        # The run_length=0 hypothesis always survives pruning (DAT-003).
        new_hypotheses.sort(key=lambda h: h.log_prob, reverse=True)
        kept = new_hypotheses[:200]
        if not any(h.run_length == 0 for h in kept):
            kept[-1] = next(h for h in new_hypotheses if h.run_length == 0)
        renorm = _logsumexp([h.log_prob for h in kept])
        for h in kept:
            h.log_prob -= renorm
        self._hypotheses = kept

        # DAT-003: with a constant hazard the posterior mass on r=0 is
        # identically the hazard rate, so it carries no information. Report
        # instead the relative collapse of the expected run length: under a
        # stable regime E[r_t] ~ E[r_{t-1}] + 1 (signal ~ 0); after a
        # changepoint the mass moves to short runs and E[r_t] falls far below
        # that (signal -> 1).
        expected_rl = sum(h.run_length * math.exp(h.log_prob) for h in self._hypotheses)
        baseline = self._last_expected_run_length + 1.0
        self._last_expected_run_length = expected_rl
        self._last_changepoint_prob = min(1.0, max(0.0, 1.0 - expected_rl / baseline))
        return self._last_changepoint_prob

    @property
    def changepoint_probability(self) -> float:
        return self._last_changepoint_prob

    @property
    def most_likely_run_length(self) -> int:
        return max(self._hypotheses, key=lambda h: h.log_prob).run_length


def _logsumexp(log_values: list[float]) -> float:
    if not log_values:
        return float("-inf")
    m = max(log_values)
    if m == float("-inf"):
        return float("-inf")
    return m + math.log(sum(math.exp(v - m) for v in log_values))
