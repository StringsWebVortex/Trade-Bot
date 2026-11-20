"""
Mempool features: fee pressure and transaction count.

Fetches mempool statistics from the local Bitcoin node (bitcoind RPC).
Used as a leading indicator of on-chain activity surge / congestion.

Returns NaN features when the node is unavailable (REG-0008 NaN policy: a
down node is not "no congestion").
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass

import structlog

log: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

_RPC_URL = os.environ.get("BTC_RPC_URL", "http://127.0.0.1:8332")
_RPC_USER = os.environ.get("BTC_RPC_USER", "crypto")
_RPC_PASS = os.environ.get("BTC_RPC_PASS", "crypto")


@dataclass(frozen=True)
class MempoolFeatures:
    tx_count: float  # number of unconfirmed transactions
    fee_rate_p50_sat: float  # median fee rate in sat/vB
    fee_rate_p90_sat: float  # 90th-pct fee rate in sat/vB (congestion signal)
    mempool_bytes: float  # total mempool size in bytes
    fee_pressure: float  # normalised [0, 1]: p90_fee / 1000 capped at 1.0


async def fetch_mempool_features(
    rpc_url: str = _RPC_URL,
    rpc_user: str = _RPC_USER,
    rpc_pass: str = _RPC_PASS,
) -> MempoolFeatures:
    """Fetch live mempool statistics from bitcoind."""
    try:
        import aiohttp

        from src.features._rpc_auth import basic_auth_header

        payload_info = {"jsonrpc": "1.0", "id": "info", "method": "getmempoolinfo", "params": []}
        payload_fees = {
            "jsonrpc": "1.0",
            "id": "fees",
            "method": "estimatesmartfee",
            "params": [1, "CONSERVATIVE"],
        }
        headers = basic_auth_header(rpc_user, rpc_pass)
        async with aiohttp.ClientSession() as sess:
            async with sess.post(
                rpc_url, json=payload_info, headers=headers, timeout=aiohttp.ClientTimeout(total=5)
            ) as r_info:
                info = (await r_info.json(content_type=None))["result"]
            async with sess.post(
                rpc_url, json=payload_fees, headers=headers, timeout=aiohttp.ClientTimeout(total=5)
            ) as r_fees:
                fees = (await r_fees.json(content_type=None))["result"]

        tx_count = float(info["size"])
        mempool_bytes = float(info["bytes"])
        # estimatesmartfee returns BTC/kB; convert to sat/vB. It omits
        # "feerate" when it cannot estimate: that is unknown, not 0.0001.
        fee_btc_per_kb = float(fees["feerate"])
        fee_sat_vb = fee_btc_per_kb * 1e8 / 1000.0

        return MempoolFeatures(
            tx_count=tx_count,
            fee_rate_p50_sat=fee_sat_vb,
            fee_rate_p90_sat=fee_sat_vb * 1.5,  # p90 heuristic without histogram
            mempool_bytes=mempool_bytes,
            fee_pressure=min(fee_sat_vb / 1000.0, 1.0),
        )
    except Exception as exc:
        log.warning("mempool_rpc_failed", exc=str(exc))
        return MempoolFeatures(
            tx_count=math.nan,
            fee_rate_p50_sat=math.nan,
            fee_rate_p90_sat=math.nan,
            mempool_bytes=math.nan,
            fee_pressure=math.nan,
        )
