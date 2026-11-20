"""
Macro daily data provider for E-13 (cross-asset contagion engine).

Sources: yfinance SPX / DXY / GLD / VIX — free, no auth.
Polls once per 24h (market-close cadence).
"""

from __future__ import annotations

import asyncio
from datetime import UTC, date, datetime
from pathlib import Path

import pandas as pd
import structlog

log: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

_TICKERS = {
    "spx": "^GSPC",
    "dxy": "DX-Y.NYB",
    "gld": "GLD",
    "vix": "^VIX",
}
_POLL_INTERVAL = 86_400  # 24 hours


class MacroProvider:
    def __init__(self, data_root: Path = Path("data")) -> None:
        self._data_root = data_root
        self._latest: dict | None = None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def latest(self) -> dict | None:
        if self._latest is not None:
            if self._is_fresh(self._latest):
                return self._latest
            self._latest = None
        return self._load_cached()

    @staticmethod
    def _is_fresh(row: dict) -> bool:
        from src.data.quality_gate import DataQualityGate

        return DataQualityGate().check_macro(row).passed

    async def fetch_once(self) -> dict | None:
        return await asyncio.get_running_loop().run_in_executor(None, self._fetch_sync)

    async def run_loop(self) -> None:
        while True:
            result = await self.fetch_once()
            if result and self._is_fresh(result):
                self._latest = result
                try:
                    from src.data.provider_cache import get_provider_cache

                    get_provider_cache().set_macro(result)
                except Exception as exc:
                    log.warning("provider_cache_publish_failed", field="macro", exc=str(exc))
            await asyncio.sleep(_POLL_INTERVAL)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _fetch_sync(self) -> dict | None:
        try:
            import yfinance as yf  # type: ignore[import]

            closes: dict[str, float] = {}
            returns: dict[str, float] = {}
            series: dict[str, list] = {}
            market_dates: list[date] = []
            for key, ticker in _TICKERS.items():
                # 90-day window to support Granger causality in E-13
                hist = yf.download(ticker, period="90d", interval="1d", progress=False)
                if hist.empty:
                    continue
                close_col = "Close"
                if close_col not in hist.columns:
                    continue
                close_vals = hist[close_col]
                if isinstance(close_vals, pd.DataFrame):
                    # Newer yfinance returns one-column frames (MultiIndex
                    # columns) for a single ticker: squeeze to a Series.
                    close_vals = close_vals.iloc[:, 0]
                close_vals = close_vals.dropna()
                if close_vals.empty:
                    continue
                market_dates.append(pd.Timestamp(close_vals.index[-1]).date())
                closes[f"{key}_close"] = float(close_vals.iloc[-1])
                ret_series = close_vals.pct_change().dropna()
                if len(ret_series) >= 2:
                    returns[f"{key}_ret"] = float(ret_series.iloc[-1])
                    series[f"{key}_series"] = ret_series.values.tolist()

            if not closes:
                return None

            row: dict = {
                # Market date of the stalest series, not the fetch date, so
                # check_macro's staleness budget can actually trip (DAT-010).
                "date": min(market_dates).isoformat(),
                **closes,
                **returns,
                **series,
            }
            if not self._is_fresh(row):
                return None
            self._persist(row)
            return row
        except Exception as exc:
            log.warning("macro_fetch_error", exc=str(exc))
            return None

    def _persist(self, row: dict) -> None:
        date_str = datetime.now(UTC).strftime("%Y-%m-%d")
        path = self._data_root / "macro" / f"{date_str}.parquet"
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame([row]).to_parquet(path, index=False)

    def _load_cached(self) -> dict | None:
        macro_dir = self._data_root / "macro"
        if not macro_dir.exists():
            return None
        # Scan a bounded history of fetch snapshots. The filename records the
        # fetch date; freshness is determined only by the market date inside
        # the row, otherwise a fresh fetch can make stale market data look new.
        files = sorted(macro_dir.glob("*.parquet"), reverse=True)
        for f in files[:14]:
            try:
                df = pd.read_parquet(f)
                if df.empty:
                    continue
                row = df.iloc[-1].to_dict()
                if self._is_fresh(row):
                    return row
                log.warning("macro_snapshot_stale", path=str(f), market_date=row.get("date"))
            except Exception as exc:
                # A corrupt or half-written parquet must not hide the older
                # snapshots behind it, so fall through to the next file.
                log.warning("macro_snapshot_unreadable", path=str(f), exc=str(exc))
                continue
        return None
