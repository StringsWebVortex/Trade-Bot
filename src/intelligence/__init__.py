"""
Crypto intelligence layer — on-chain metrics, exchange flows, whale tracking.

Providers (implemented in src/intelligence/providers/ and
src/intelligence/onchain/): Binance, OKX, Bybit, CoinGecko, CryptoQuant,
Coinglass, Arkham. Glassnode and LunarCrush are NOT implemented.

Authority:
  - Glassnode API Docs: https://docs.glassnode.com/
  - CryptoQuant API Docs: https://docs.cryptoquant.com/
  - Research: Chainalysis, Coin Metrics on flow analysis
"""

from src.intelligence.client import IntelligenceAggregator
from src.intelligence.metrics import IntelligenceMetrics

__all__ = ["IntelligenceAggregator", "IntelligenceMetrics"]
