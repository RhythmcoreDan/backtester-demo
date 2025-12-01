"""
backtester_demo.py
------------------
Lightweight backtesting engine demo.

Takes a stream of signals and prices, and produces:
- trades via a simple execution model
- position & equity over time
- basic performance metrics
"""

from __future__ import annotations

import pandas as pd
from dataclasses import dataclass


@dataclass
class BacktestResult:
    timeline: pd.DataFrame
    stats: dict


def run_backtest(signals_df: pd.DataFrame) -> BacktestResult:
    """
    signals_df must contain:
      - time
      - price
      - signal  (target position: -1, 0, +1)

    Execution model:
      - target is desired position in units
      - fills occur at given price
      - no fees / slippage
    """
    position = 0
    avg_price = 0.0
    realized_pnl = 0.0

    rows = []

    for _, row in signals_df.iterrows():
        time = row["time"]
        price = float(row["price"])
        target = int(row["signal"])

        # Handle position changes
        if target != position:
            # Close existing if needed
            if position == 1 and target <= 0:
                realized_pnl += (price - avg_price) * 1.0
                position = 0
                avg_price = 0.0

            elif position == -1 and target >= 0:
                realized_pnl += (avg_price - price) * 1.0
                position = 0
                avg_price = 0.0

            # Open new if going from flat to non-zero
            if position == 0 and target != 0:
                position = target
                avg_price = price

        # Unrealized PnL
        if position == 1:
            unrealized = (price - avg_price) * 1.0
        elif position == -1:
            unrealized = (avg_price - price) * 1.0
        else:
            unrealized = 0.0

        equity = realized_pnl + unrealized

        rows.append(
            {
                "time": time,
                "price": price,
                "signal": target,
                "position": position,
                "avg_price": avg_price,
                "realized_pnl": round(realized_pnl, 5),
                "equity": round(equity, 5),
            }
        )

    timeline = pd.DataFrame(rows)

    stats = compute_stats(timeline)

    return BacktestResult(timeline=timeline, stats=stats)


def compute_stats(timeline: pd.DataFrame) -> dict:
    """
    Compute basic performance metrics from the equity curve.
    """
    eq = timeline["equity"]

    start_eq = float(eq.iloc[0])
    end_eq = float(eq.iloc[-1])
    net_pl = end_eq - start_eq

    # Simple returns series
    returns = eq.diff()
    # Drop first NaN
    returns = returns.iloc[1:]

    win_trades = (returns > 0).sum()
    lose_trades = (returns < 0).sum()
    total_trades = win_trades + lose_trades

    max_equity = eq.cummax()
    drawdowns = eq - max_equity
    max_drawdown = float(drawdowns.min())

    stats = {
        "start_equity": round(start_eq, 5),
        "end_equity": round(end_eq, 5),
        "net_pl": round(net_pl, 5),
        "total_steps": int(len(timeline)),
        "total_trades": int(total_trades),
        "wins": int(win_trades),
        "losses": int(lose_trades),
        "max_drawdown": round(max_drawdown, 5),
    }

    return stats
