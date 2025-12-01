"""
run_demo.py
-----------
Runs the backtesting engine on a small signal stream
and prints both the equity curve and summary statistics.
"""

import pandas as pd
from backtester_demo import run_backtest


def main():
    df = pd.read_csv("sample_signals.csv")

    result = run_backtest(df)

    print("=== BACKTEST TIMELINE (last 10 rows) ===")
    print(result.timeline.tail(10))

    print("\n=== BACKTEST STATS ===")
    for k, v in result.stats.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
