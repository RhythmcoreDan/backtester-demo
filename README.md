# Backtester Demo

A lightweight backtesting engine demo that converts trading signals into:
- trades via a simple execution model
- an equity curve over time
- basic performance metrics (P&L, drawdown, win/loss counts)

This is a simplified, safe, public example of how I structure a backtesting layer inside a trading system.

---

## 🚀 What This Demo Does

Given a stream of:
- **time**
- **price**
- **signal** (target position: `-1`, `0`, `+1`)

The engine will:
1. Interpret signals as **target positions** (short / flat / long).
2. Apply a simple execution model (fills at provided price, no fees).
3. Track:
   - position  
   - average entry price  
   - realized PnL  
   - equity over time  
4. Compute basic performance statistics.

---

## 📂 Project Structure

```text
backtester-demo/
│
├── backtester_demo.py   # Core backtest + stats engine
├── run_demo.py          # Demo runner
├── sample_signals.csv   # Example signal stream
└── README.md            # Documentation

📊 Example Output

=== BACKTEST TIMELINE (last 10 rows) ===
          time   price  signal  position  avg_price  realized_pnl  equity
...       ...    ...      ...      ...       ...          ...       ...

=== BACKTEST STATS ===
start_equity: 0.0
end_equity: 0.0
net_pl: 0.0
total_steps: 14
total_trades: X
wins: Y
losses: Z
max_drawdown: -0.0...

🧠 About This Project

This demo represents the "lab layer" of a trading system:

connecting signals to an execution model

generating equity curves

quantifying performance in a repeatable way

In my larger RhythmCore system, this kind of backtesting engine is wired to:

emotional/behavioral indicators

regime maps

strategy logic

execution engines

All working together as independent, testable modules.


