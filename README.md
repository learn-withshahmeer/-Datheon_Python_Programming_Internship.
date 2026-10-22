# Stock Portfolio Performance Tracker (Console)

A Python 3 utility that tracks an investment portfolio and logs a summary to a CSV file.

## Features
- Enter ticker symbols, buy price and number of shares
- Ticker symbols are validated against the S&P 500 dataset (`sp500.csv`)
- Buying the same stock twice merges into one position with an average buy price
- Current prices: live via `yfinance` (optional) or typed in manually
- Calculates invested capital, current value, gain/loss in $ and % per holding, and totals
- Formatted console report
- Every run is appended to `portfolio_summary.csv` (with date/time and a TOTAL row)

## How to run
1. Install Python 3
2. Keep `portfolio.py` and `sp500.csv` in the same folder
3. Run:

```
python portfolio.py
```

Optional, for live prices: `pip install yfinance`

## Files
| File | Description |
|------|-------------|
| `portfolio.py` | The program |
| `sp500.csv` | S&P 500 ticker dataset (symbol, company, sector, ...) |
| `portfolio_summary.csv` | Generated log of portfolio summaries |

## Concepts used
Dictionaries, functions, loops, input validation, `csv` module (read + write/append), file I/O, f-string formatting, `datetime`.
