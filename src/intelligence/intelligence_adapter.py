"""
IntelligenceAdapter — bridges CryptoIntelligence v6 signals into TradeBot's
existing storage schema (store_intelligence_features).

The orchestrator already reads from storage.fetch_intelligence_features() and
joins the columns into the training FeatureMatrix. This adapter calls
CryptoIntelligence.on_bar() for each incoming bar and writes the produced
IntelSignal as intelligence features. V6 decision outputs are mapped to
dedicated nullable columns and JSON fields, separate from older provider data.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import structlog

if TYPE_CHECKING:
    from src.data.storage import Storage

log: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class IntelligenceAdapter:
    """
    Wraps CryptoIntelligence and writes its signals to TradeBot's storage.

    Instantiate alongside the Orchestrator; call on_bar() on each new OHLCV row.
    The Orchestrator's _attach_intelligence_features() will pick up the stored
    rows and join them into the training FeatureMatrix automatically.
    """

    def __init__(self, intelligence: Any, storage: Storage) -> None:
        # `intelligence` is a `src.intel.CryptoIntelligence`; typed as Any here
        # to keep the analytics layer from importing back up into orchestration
        # (GOV-024). The caller wires the concrete type in.
        self._intel = intelligence
        self._storage = storage

    async def on_bar(
        self,
        symbol: str,
        timeframe: str,
        bar_ts_ms: int,
        ohlcv: dict,
        bids: list | None = None,
        asks: list | None = None,
        regime_id: int | None = None,
        regime_confidences: list[float] | None = None,
        derivatives_data: dict | None = None,
        alt_prices: dict[str, list[float]] | None = None,
    ) -> None:
        """
        Process one bar through CryptoIntelligence and persist the signal.

        Does NOT block the caller — IO errors are caught and logged.
        """
        try:
            signal = await self._intel.on_bar(
                symbol=symbol,
                ohlcv=ohlcv,
                bids=bids,
                asks=asks,
                regime_id=regime_id,
                regime_confidences=regime_confidences,
                derivatives_data=derivatives_data,
                alt_prices=alt_prices,
                event_ts=bar_ts_ms / 1000.0,
                event_id=f"{symbol}:{timeframe}:{bar_ts_ms}",
                source_timeframe=timeframe,
            )
        except Exception as exc:
            log.warning("intelligence_on_bar_failed", symbol=symbol, exc=str(exc))
            return

        confidence = 0.0
        features: dict[str, Any] | None = None
        if signal is None:
            # No sized signal (ABSTAIN, suppressed risk context, drift): the
            # fused decision is still the V6 output for this bar, so persist
            # it with zero direction/size instead of dropping the row (INT-008).
            decision = getattr(self._intel, "last_decision", None)
            if not isinstance(decision, dict):
                return
            features = self._decision_to_features(decision)
        else:
            confidence = signal.confidence

        try:
            if features is None:
                features = self._signal_to_features(signal)
        except ValueError as exc:
            log.warning(
                "intelligence_feature_contract_unsupported",
                symbol=symbol,
                timeframe=timeframe,
                error=str(exc),
            )
            return

        try:
            await self._storage.store_intelligence_features(
                symbol=symbol,
                timeframe=timeframe,
                bar_ts=bar_ts_ms,
                features=features,
                confidence=confidence,
                source="crypto_intel_v6",
            )
        except Exception as exc:
            log.warning("intelligence_store_failed", symbol=symbol, exc=str(exc))

    @staticmethod
    def _decision_to_features(decision: dict[str, Any]) -> dict[str, Any]:
        """Features for a bar that produced a fused decision but no sized signal."""

        def _js(key: str) -> str:
            raw = decision.get(key) or {}
            return json.dumps({str(k): v for k, v in raw.items()}, sort_keys=True)

        regime = decision.get("regime_id")
        return {
            "direction_v6": 0.0,
            "size_pct_v6": 0.0,
            "confidence_v6": 0.0,
            "conflict_v6": float(bool(decision.get("conflict"))),
            "regime_id_v6": float(regime) if regime is not None else None,
            "expected_return_v6": _optional_float(decision.get("expected_return")),
            "uncertainty_v6": _optional_float(decision.get("uncertainty")),
            "algo_v6": str(decision.get("action", "ABSTAIN")),
            "horizon_contributions_v6": _js("contributions"),
            "model_versions_v6": _js("model_versions"),
            "freshness_seconds_v6": _js("freshness_seconds"),
        }

    def _signal_to_features(self, signal: Any) -> dict[str, Any]:
        """Map each unified V6 decision field to a durable storage column."""
        meta = signal.meta or {}
        return {
            "direction_v6": float(signal.direction),
            "size_pct_v6": float(signal.size_pct),
            "confidence_v6": float(signal.confidence),
            "horizon_idx_v6": float(signal.horizon_idx),
            "ecc_anomaly_v6": (
                float(signal.ecc_anomaly) if signal.ecc_anomaly is not None else None
            ),
            "conflict_v6": float(bool(signal.conflict)),
            "regime_id_v6": float(signal.regime_id),
            "agreement_ratio_v6": _optional_float(meta.get("agreement_ratio")),
            "kyle_lambda_v6": _optional_float(meta.get("kyle_lambda")),
            "ofi_v6": _optional_float(meta.get("ofi")),
            "vpin_v6": _optional_float(meta.get("vpin")),
            "expected_return_v6": _optional_float(meta.get("expected_return")),
            "uncertainty_v6": _optional_float(meta.get("uncertainty")),
            "algo_v6": str(signal.algo),
            "horizon_contributions_v6": json.dumps(
                meta.get("horizon_contributions", {}), sort_keys=True
            ),
            "model_versions_v6": json.dumps(meta.get("model_versions", {}), sort_keys=True),
            "freshness_seconds_v6": json.dumps(meta.get("freshness_seconds", {}), sort_keys=True),
        }


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    return float(value)
