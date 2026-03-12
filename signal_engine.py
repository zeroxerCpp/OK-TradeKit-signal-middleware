"""
signal_engine.py — CLI entry point for OK Trading Advisor.

All business logic lives in the `engine/` package.
This file is a thin wrapper that parses arguments and calls the engine.

Usage
-----
Single instrument:
    python3 signal_engine.py BTC-USDT-SWAP 10000

Portfolio scan:
    python3 signal_engine.py --scan BTC-USDT-SWAP ETH-USDT-SWAP SOL-USDT-SWAP 10000

Requirements
------------
    okx CLI  (npm install -g @okx_ai/okx-trade-cli)
    Python 3.8+  (no third-party packages needed)
"""

import sys
from engine import fetch_all, SignalEngine, scan_portfolio

if __name__ == "__main__":
    args = sys.argv[1:]

    # ── Portfolio scan mode ──────────────────────────────────────────────────
    # python3 signal_engine.py --scan BTC-USDT-SWAP ETH-USDT-SWAP 10000
    if args and args[0] == "--scan":
        rest    = args[1:]
        account = 10_000.0
        ids     = []
        for a in rest:
            try:
                account = float(a)
            except ValueError:
                ids.append(a)
        if not ids:
            ids = ["BTC-USDT-SWAP", "ETH-USDT-SWAP", "SOL-USDT-SWAP"]
        print(f"Scanning {len(ids)} instruments with account={account:,.0f} USDT ...")
        print(scan_portfolio(ids, account_size=account))

    # ── Single-instrument mode ───────────────────────────────────────────────
    # python3 signal_engine.py BTC-USDT-SWAP 10000
    else:
        inst_id = args[0] if args else "BTC-USDT-SWAP"
        account = float(args[1]) if len(args) > 1 else 10_000.0
        is_swap = "SWAP" in inst_id.upper()

        print(f"Fetching data for {inst_id} ...")
        data   = fetch_all(inst_id, is_swap=is_swap)
        engine = SignalEngine(data, account_size=account, is_swap=is_swap)
        report = engine.run()
        print(report.text)
