"""
engine/__init__.py — Public API of the `engine` package.

Consumers only need to import from here:

    from engine import fetch_all, SignalEngine, scan_portfolio
    from engine import Candle, MarketData, Report
"""
from .models import (
    Candle,
    MarketData,
    SignalResult,
    GroupScore,
    MarketState,
    Report,
    ScanResult,
)
from .fetcher       import fetch_all
from .indicators    import (
    ema_list, ema_scalar, sma,
    macd, bollinger_bands, rsi, kdj,
    atr_list, supertrend, ichimoku, adx,
)
from .market_state  import detect_market_state
from .signals       import SignalEngine
from .scanner       import scan_portfolio

__all__ = [
    # data structures
    "Candle", "MarketData", "SignalResult", "GroupScore",
    "MarketState", "Report", "ScanResult",
    # fetcher
    "fetch_all",
    # indicators
    "ema_list", "ema_scalar", "sma",
    "macd", "bollinger_bands", "rsi", "kdj",
    "atr_list", "supertrend", "ichimoku", "adx",
    # state + engine
    "detect_market_state",
    "SignalEngine",
    "scan_portfolio",
]
