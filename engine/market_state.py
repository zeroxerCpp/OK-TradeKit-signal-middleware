"""
engine/market_state.py — ADX/ATR/Volume market-state classifier.

Produces a MarketState with dynamic signal weights per signal_skill.md.
"""
from __future__ import annotations

from typing import List

from .models import Candle, MarketState
from .indicators import adx, atr_list, sma


def detect_market_state(
    candles_4h: List[Candle],
    candles_1h: List[Candle],
) -> MarketState:
    """
    Classify the current market state and return ADX-based dynamic weights.

    Priority (highest → lowest):
      Low Liquidity > High Volatility > Trending > Ranging > Normal

    Thresholds:
      - vol_ratio  < 0.5  → Low Liquidity  (abort signal)
      - atr_ratio  > 1.5  → High Volatility
      - ADX(14)    > 25   → Trending
      - ADX(14)    < 20   → Ranging
      - otherwise         → Normal

    Weight matrix (w_trend, w_vol, w_osc):
      Low Liquidity  : 0.00, 0.00, 0.00  (abort)
      High Volatility: 0.35, 0.45, 0.20
      Trending       : 0.60, 0.25, 0.15
      Ranging        : 0.25, 0.30, 0.45
      Normal         : 0.40, 0.35, 0.25
    """
    h4 = [c.high  for c in candles_4h]
    l4 = [c.low   for c in candles_4h]
    c4 = [c.close for c in candles_4h]
    vol1 = [c.vol for c in candles_1h]

    adx_val = adx(h4, l4, c4, 14) or 0.0

    atr14_series = atr_list(h4, l4, c4, 14)
    atr14_valid  = [v for v in atr14_series if v is not None]
    atr14_cur    = atr14_valid[-1] if atr14_valid else 0.0
    atr14_ma10   = (
        sum(atr14_valid[-10:]) / 10 if len(atr14_valid) >= 10 else atr14_cur
    )

    vol_cur  = vol1[-1] if vol1 else 0.0
    vol_ma20 = sma(vol1, 20) or vol_cur

    vol_ratio = vol_cur / vol_ma20 if vol_ma20 else 1.0
    atr_ratio = atr14_cur / atr14_ma10 if atr14_ma10 else 1.0

    if vol_ratio < 0.5:
        state = "Low Liquidity"
        wt, wv, wo = 0.0, 0.0, 0.0
    elif atr_ratio > 1.5:
        state = "High Volatility"
        wt, wv, wo = 0.35, 0.45, 0.20
    elif adx_val > 25:
        state = "Trending"
        wt, wv, wo = 0.60, 0.25, 0.15
    elif adx_val < 20:
        state = "Ranging"
        wt, wv, wo = 0.25, 0.30, 0.45
    else:
        state = "Normal"
        wt, wv, wo = 0.40, 0.35, 0.25

    return MarketState(
        state=state,
        adx=adx_val,
        atr14=atr14_cur,
        atr_ma10=atr14_ma10,
        vol_ratio=vol_ratio,
        w_trend=wt,
        w_vol=wv,
        w_osc=wo,
    )
