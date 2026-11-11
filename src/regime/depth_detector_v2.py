"""
Depth Detector v2 — 9-regime HMM (Crypto-Box CAT-4).

Extends the 3-state detector with 6 new regimes derived from engine features.
Backward-compatible: the existing RegimeDetector is unchanged.

Activated via CRYPTO_BOX=true env flag. Falls back to existing 3-state
detector otherwise.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd
import structlog
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler

log: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

# Specialist labels are available only when the fitted state features support them.
REGIME_LABELS: Final[list[str]] = [
    "Ranging",  # 0 — low vol, mean-reverting
    "Accumulation",  # 1 — low vol + on-chain inflow
    "Trending",  # 2 — directional momentum
    "Transition",  # 3 — between regimes
    "Volatile",  # 4 — high vol
    "OptionsDriven",  # 5 — options dominate
    "MacroDominated",  # 6 — macro coupling high
    "LiquidityCrisis",  # 7 — liquidity stressed
    "Capitulation",  # 8 — sentiment extremes + liquidation
]

# Extended feature vector (12 features for 9-regime separation)
FEATURE_COLS_V2: Final[list[str]] = [
    "e01_confidence",  # HMM/ARIMA confidence
    "e03_entropy_score",  # information entropy
    "e06_hurst",  # DFA persistence
    "e02_order_flow_tox",  # microstructure imbalance
    "e05_net_flow",  # on-chain net flow
    "e10_deviation_pct",  # S2F deviation
    "e12_gex",  # gamma exposure (0 if unavailable)
    "e13_contagion_score",  # macro coupling
    "e14_contrarian_signal",  # sentiment extremes
    "e17_amihud_ratio",  # liquidity stress
    "adx_14",  # trend strength
    "bb_width",  # Bollinger Band squeeze
]


@dataclass
class RegimePrediction:
    label: str  # one of REGIME_LABELS
    confidence: float  # posterior probability of winning state
    weight_vector: list[float]  # 18 engine weights for this regime
    raw_state: int  # raw HMM state index


class DepthDetectorV2:
    """
    9-regime GaussianHMM detector.

    Must be fit on a feature DataFrame with columns matching FEATURE_COLS_V2.
    """

    N_COMPONENTS = 9

    def __init__(self, symbol: str = "BTC/USDT", timeframe: str = "1h") -> None:
        self._symbol = symbol
        self._timeframe = timeframe
        self._model: GaussianHMM | None = None
        self._scaler: StandardScaler | None = None
        self._state_to_label: dict[int, str] = {}

    def fit(self, feature_df: pd.DataFrame) -> None:
        """Train the 9-regime HMM on a feature matrix."""
        cols = [c for c in FEATURE_COLS_V2 if c in feature_df.columns]
        if not cols:
            raise ValueError(
                f"No matching feature columns in dataframe. Expected: {FEATURE_COLS_V2}"
            )

        X = feature_df[cols].dropna().values
        if len(X) < self.N_COMPONENTS * 20:
            raise ValueError(
                f"Need at least {self.N_COMPONENTS * 20} rows to fit 9-regime HMM, got {len(X)}"
            )

        self._scaler = StandardScaler()
        X_scaled = self._scaler.fit_transform(X)

        model = GaussianHMM(
            n_components=self.N_COMPONENTS,
            covariance_type="full",
            n_iter=200,
            random_state=42,
        )
        model.fit(X_scaled)
        self._model = model
        self._feature_cols = list(cols)
        self._state_to_label = self._assign_labels(model, X_scaled, cols)
        log.info("depth_detector_v2_fitted", n_samples=len(X), n_regimes=self.N_COMPONENTS)

    def predict(self, feature_df: pd.DataFrame) -> RegimePrediction:
        """Predict regime from a recent feature slice."""
        from src.engines.consensus import REGIME_WEIGHTS

        unknown = RegimePrediction(
            label="Unknown",
            confidence=0.0,
            weight_vector=list(REGIME_WEIGHTS["Transition"]),
            raw_state=0,
        )
        if self._model is None or self._scaler is None or not self._feature_cols:
            return unknown

        if not set(self._feature_cols).issubset(feature_df.columns):
            return unknown
        cols = self._feature_cols
        X = feature_df[cols].fillna(0.0).values
        if len(X) == 0:
            return unknown

        X_scaled = self._scaler.transform(X)
        posteriors = self._model.predict_proba(X_scaled)
        last = posteriors[-1]  # shape (N_COMPONENTS,)
        best_state = int(np.argmax(last))
        confidence = float(last[best_state])
        label = self._state_to_label.get(best_state, "Unknown")
        weights = REGIME_WEIGHTS.get(label, REGIME_WEIGHTS["Transition"])

        return RegimePrediction(
            label=label,
            confidence=confidence,
            weight_vector=weights,
            raw_state=best_state,
        )

    def save(self, model_dir: Path) -> None:
        import joblib

        model_dir.mkdir(parents=True, exist_ok=True)
        stem = self._model_stem()
        paths = (
            model_dir / f"{stem}_hmm9.pkl",
            model_dir / f"{stem}_scaler9.pkl",
            model_dir / f"{stem}_labels9.pkl",
            model_dir / f"{stem}_features9.pkl",
        )
        values = (self._model, self._scaler, self._state_to_label, self._feature_cols)
        for path, value in zip(paths, values, strict=True):
            joblib.dump(value, path)
        from src.regime.detector import _write_manifest

        for path in paths:
            _write_manifest(path)

    def load(self, model_dir: Path) -> bool:
        import joblib

        stem = self._model_stem()
        paths = (
            model_dir / f"{stem}_hmm9.pkl",
            model_dir / f"{stem}_scaler9.pkl",
            model_dir / f"{stem}_labels9.pkl",
            model_dir / f"{stem}_features9.pkl",
        )
        if not all(path.is_file() for path in paths):
            return False
        from src.regime.detector import _verify_manifest

        try:
            for path in paths:
                _verify_manifest(path)
            model, scaler, labels, feature_cols = (joblib.load(path) for path in paths)
            if not isinstance(labels, dict) or not isinstance(feature_cols, list):
                raise ValueError("invalid DepthDetectorV2 model metadata")
        except Exception as exc:
            log.error("depth_detector_v2_integrity_failed", exc=str(exc))
            return False
        self._model = model
        self._scaler = scaler
        self._state_to_label = labels
        self._feature_cols = feature_cols
        return True

    def _model_stem(self) -> str:
        key = f"{self._symbol}_{self._timeframe}"
        # SHA-256 over the cache key, matching RegimeDetector._train_hash.
        return hashlib.sha256(key.encode()).hexdigest()[:8]

    def _assign_labels(
        self,
        model: GaussianHMM,
        X_scaled: np.ndarray,
        feature_cols: list[str] | None = None,
    ) -> dict[int, str]:
        """Label states from measured feature evidence, not volatility rank alone.

        Volatility ranking supplies only broad fallback labels. Specialized
        labels require supporting feature means from observations assigned to
        that state, so a high-variance cluster cannot be called "Accumulation"
        or "MacroDominated" without the corresponding signal.
        """
        covars = model.covars_
        covar_type = model.covariance_type
        if covar_type == "full":
            vol_proxy = np.array([np.trace(c) for c in covars])
        elif covar_type == "tied":
            vol_proxy = np.var(model.means_, axis=1)
        else:
            vol_proxy = np.array([float(np.sum(c)) for c in covars])
        sorted_states = np.argsort(vol_proxy)
        feature_names = feature_cols or FEATURE_COLS_V2
        col_index = {name: index for index, name in enumerate(feature_names)}
        assignments = np.asarray(model.predict(X_scaled), dtype=int)
        means: dict[int, np.ndarray] = {}
        for state in range(self.N_COMPONENTS):
            state_rows = X_scaled[assignments == state]
            if len(state_rows) >= 5:
                means[state] = np.mean(state_rows, axis=0)

        def signal(state_mean: np.ndarray, name: str) -> float:
            index = col_index.get(name)
            if index is None or index >= len(state_mean):
                return 0.0
            return float(state_mean[index])

        labels: dict[int, str] = {}
        used_special: set[str] = set()
        n_states = max(1, len(sorted_states))
        for rank, raw_state in enumerate(sorted_states):
            state = int(raw_state)
            mean = means.get(state)
            if mean is None:
                # No stable empirical cluster: use only a broad volatility label.
                if rank == 0:
                    labels[state] = "Ranging"
                elif rank >= n_states // 2:
                    labels[state] = "Volatile"
                else:
                    labels[state] = "Transition"
                continue

            net_flow = signal(mean, "e05_net_flow")
            options = abs(signal(mean, "e12_gex"))
            macro = signal(mean, "e13_contagion_score")
            liquidity = signal(mean, "e17_amihud_ratio")
            contrarian = abs(signal(mean, "e14_contrarian_signal"))
            entropy = signal(mean, "e03_entropy_score")
            adx = signal(mean, "adx_14")

            supported: list[tuple[float, str]] = []
            if net_flow <= -0.75 and contrarian >= 0.75 and liquidity >= 0.5:
                supported.append((min(abs(net_flow), contrarian, liquidity), "Capitulation"))
            if liquidity >= 0.9:
                supported.append((liquidity, "LiquidityCrisis"))
            if macro >= 0.9:
                supported.append((macro, "MacroDominated"))
            if options >= 0.9:
                supported.append((options, "OptionsDriven"))
            if net_flow >= 0.9:
                supported.append((net_flow, "Accumulation"))
            supported.sort(reverse=True)
            selected = next((name for _, name in supported if name not in used_special), None)
            if selected is not None:
                labels[state] = selected
                used_special.add(selected)
            elif rank == 0:
                labels[state] = "Ranging"
            elif adx >= 0.9:
                labels[state] = "Trending"
            elif entropy >= 0.9:
                labels[state] = "Transition"
            else:
                labels[state] = "Volatile" if rank >= n_states // 2 else "Transition"
        return labels


def _compute_adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> float:
    """Compute ADX (Average Directional Index) — measures trend strength (0-100)."""
    try:
        n = len(close)
        if n < period + 1:
            return 0.0
        tr = pd.concat(
            [
                high - low,
                (high - close.shift(1)).abs(),
                (low - close.shift(1)).abs(),
            ],
            axis=1,
        ).max(axis=1)
        dm_pos = (high.diff()).clip(lower=0)
        dm_neg = (-low.diff()).clip(lower=0)
        # Smooth with Wilder's EMA
        alpha = 1.0 / period
        atr = tr.ewm(alpha=alpha, adjust=False).mean()
        di_pos = (
            dm_pos.ewm(alpha=alpha, adjust=False).mean() / atr.replace(0, float("nan"))
        ).fillna(0) * 100
        di_neg = (
            dm_neg.ewm(alpha=alpha, adjust=False).mean() / atr.replace(0, float("nan"))
        ).fillna(0) * 100
        dx = ((di_pos - di_neg).abs() / (di_pos + di_neg).replace(0, float("nan"))).fillna(0) * 100
        adx = dx.ewm(alpha=alpha, adjust=False).mean()
        return float(adx.iloc[-1]) if not pd.isna(adx.iloc[-1]) else 0.0
    except Exception:
        return 0.0


def _compute_bb_width(close: pd.Series, period: int = 20) -> float:
    """Bollinger Band width (upper - lower) / middle — measures volatility regime."""
    try:
        if len(close) < period:
            return 0.0
        roll = close.rolling(period)
        mid = roll.mean()
        std = roll.std()
        upper = mid + 2 * std
        lower = mid - 2 * std
        width = (upper - lower) / mid.replace(0, float("nan"))
        val = float(width.iloc[-1])
        return val if not pd.isna(val) else 0.0
    except Exception:
        return 0.0


def build_v2_features_from_engine_outputs(
    engine_outputs: dict,
    ohlcv: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Build a single-row feature DataFrame from engine output metadata.

    engine_outputs : dict keyed by engine_id → EngineOutput
    ohlcv          : optional OHLCV DataFrame (columns: high, low, close) used to
                     compute adx_14 and bb_width; both default to 0.0 when absent.
    """
    from src.engines.schema import EngineOutput

    def _meta(eid: str, key: str, default: float = 0.0) -> float:
        out = engine_outputs.get(eid)
        if isinstance(out, EngineOutput):
            return float(out.metadata.get(key, default))
        return default

    def _conf(eid: str) -> float:
        out = engine_outputs.get(eid)
        if hasattr(out, "confidence"):
            return float(out.confidence)  # type: ignore[union-attr]
        return 0.0

    adx_14 = 0.0
    bb_width = 0.0
    if (
        ohlcv is not None
        and not ohlcv.empty
        and all(c in ohlcv.columns for c in ("high", "low", "close"))
    ):
        adx_14 = _compute_adx(ohlcv["high"], ohlcv["low"], ohlcv["close"])
        bb_width = _compute_bb_width(ohlcv["close"])

    row = {
        "e01_confidence": _conf("E-01"),
        "e03_entropy_score": _meta("E-03", "entropy_score"),
        "e06_hurst": _meta("E-06", "hurst", 0.5),
        "e02_order_flow_tox": _meta("E-02", "order_flow_toxicity"),
        "e05_net_flow": _meta("E-05", "net_flow_normalized"),
        "e10_deviation_pct": _meta("E-10", "deviation_pct"),
        "e12_gex": _meta("E-12", "gex"),
        "e13_contagion_score": _meta("E-13", "contagion_score"),
        "e14_contrarian_signal": _meta("E-14", "contrarian_signal"),
        "e17_amihud_ratio": _meta("E-17", "amihud_ratio"),
        "adx_14": adx_14,
        "bb_width": bb_width,
    }
    return pd.DataFrame([row])
