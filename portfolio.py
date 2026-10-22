# Stock Portfolio Performance Tracker - Task 2
# Run: python portfolio.py
# Keep sp500.csv (the S&P 500 ticker dataset) in the same folder.

import csv
import os
from datetime import datetime

folder = os.path.dirname(os.path.abspath(__file__))
TICKER_FILE = os.path.join(folder, "sp500.csv")
SUMMARY_FILE = os.path.join(folder, "portfolio_summary.csv")


def load_tickers():
    # reads the S&P 500 csv and stores symbol -> company name and sector
    tickers = {}
    try:
        with open(TICKER_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tickers[row["Symbol"].upper()] = {
                    "name": row["Security"],
                    "sector": row["GICS Sector"],
                }
    except FileNotFoundError:
        print("sp500.csv not found, so ticker symbols will not be checked.")
    return tickers


def get_number(message):
    # keeps asking until the user types a number greater than 0
    while True:
        text = input(message).strip()
        try:
            value = float(text)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if value <= 0:
            print("The number must be greater than 0.")
            continue
        return value


def add_stocks(tickers):
    # portfolio is a dictionary: symbol -> {"shares": .., "buy_price": ..}
    portfolio = {}

    print("Add your stocks. Type 'done' when you are finished.")
    while True:
        symbol = input("\nTicker symbol (e.g. AAPL): ").strip().upper()

        if symbol == "":
            continue

        if symbol == "DONE":
            if len(portfolio) == 0:
                print("Please add at least one stock first.")
                continue
            break

        if len(tickers) > 0 and symbol not in tickers:
            print("'" + symbol + "' is not in the S&P 500 list. Try again.")
            continue

        if symbol in tickers:
            print("Found:", tickers[symbol]["name"])

        buy_price = get_number("Buy price per share ($): ")
        shares = get_number("Number of shares: ")

        if symbol in portfolio:
            # same stock bought again -> work out the average buy price
            old = portfolio[symbol]
            total_cost = old["shares"] * old["buy_price"] + shares * buy_price
            total_shares = old["shares"] + shares
            portfolio[symbol] = {"shares": total_shares,
                                 "buy_price": total_cost / total_shares}
            print("Added to your existing", symbol, "position.")
        else:
            portfolio[symbol] = {"shares": shares, "buy_price": buy_price}
            print("Added", symbol)

    return portfolio


def get_live_price(symbol):
    # tries to get the latest price from yfinance, returns None if it fails
    try:
        import yfinance
        data = yfinance.Ticker(symbol.replace(".", "-")).history(period="1d")
        return float(data["Close"].iloc[-1])
    except Exception:
        return None


def get_current_prices(portfolio):
    prices = {}

    print("\nThe S&P 500 dataset has no prices, so current prices")
    print("come from the internet (yfinance) or you type them in.")
    choice = input("Fetch live prices with yfinance? (y/n): ").strip().lower()

    for symbol in portfolio:
        price = None
        if choice == "y":
            price = get_live_price(symbol)
            if price is None:
                print("Could not get a live price for", symbol)
        if price is None:
            price = get_number("Enter current price of " + symbol + " ($): ")
        prices[symbol] = price

    return prices


def calculate(portfolio, prices, tickers):
    results = []
    for symbol in portfolio:
        shares = portfolio[symbol]["shares"]
        buy_price = portfolio[symbol]["buy_price"]
        current_price = prices[symbol]

        invested = shares * buy_price
        current_value = shares * current_price
        gain = current_value - invested
        percent = gain / invested * 100

        if symbol in tickers:
            name = tickers[symbol]["name"]
            sector = tickers[symbol]["sector"]
        else:
            name = "Unknown"
            sector = "Unknown"

        results.append({
            "symbol": symbol, "name": name, "sector": sector,
            "shares": shares, "buy_price": buy_price,
            "current_price": current_price, "invested": invested,
            "current_value": current_value, "gain": gain, "percent": percent,
        })
    return results


def show_report(results):
    line = "=" * 82
    print("\n" + line)
    print("                       PORTFOLIO PERFORMANCE REPORT")
    print(line)
    print(f"{'Symbol':<8}{'Shares':>9}{'Buy $':>11}{'Now $':>11}"
          f"{'Invested':>13}{'Value':>13}{'Gain/Loss %':>13}")
    print("-" * 82)

    total_invested = 0
    total_value = 0

    for r in results:
        print(f"{r['symbol']:<8}{r['shares']:>9g}{r['buy_price']:>11.2f}"
              f"{r['current_price']:>11.2f}{r['invested']:>13.2f}"
              f"{r['current_value']:>13.2f}{r['percent']:>+12.2f}%")
        total_invested += r["invested"]
        total_value += r["current_value"]

    total_gain = total_value - total_invested
    total_percent = total_gain / total_invested * 100

    print("-" * 82)
    print("Total invested :", f"${total_invested:,.2f}")
    print("Current value  :", f"${total_value:,.2f}")
    if total_gain >= 0:
        print("Overall result : PROFIT", f"${total_gain:,.2f}", f"({total_percent:+.2f}%)")
    else:
        print("Overall result : LOSS  ", f"${-total_gain:,.2f}", f"({total_percent:+.2f}%)")
    print(line)

    return total_invested, total_value, total_gain, total_percent


def save_to_csv(results, totals):
    # every run is added to the file (like a log), header only written once
    new_file = not os.path.exists(SUMMARY_FILE)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(SUMMARY_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["Date", "Symbol", "Company", "Sector", "Shares",
                             "Buy Price", "Current Price", "Invested",
                             "Current Value", "Gain/Loss", "Gain/Loss %"])
        for r in results:
            writer.writerow([now, r["symbol"], r["name"], r["sector"],
                             r["shares"], round(r["buy_price"], 2),
                             round(r["current_price"], 2),
                             round(r["invested"], 2),
                             round(r["current_value"], 2),
                             round(r["gain"], 2), round(r["percent"], 2)])
        writer.writerow([now, "TOTAL", "", "", "", "", "",
                         round(totals[0], 2), round(totals[1], 2),
                         round(totals[2], 2), round(totals[3], 2)])

    print("\nSummary saved to", SUMMARY_FILE)


def main():
    print("===== STOCK PORTFOLIO TRACKER =====\n")
    tickers = load_tickers()
    portfolio = add_stocks(tickers)
    prices = get_current_prices(portfolio)
    results = calculate(portfolio, prices, tickers)
    totals = show_report(results)
    save_to_csv(results, totals)


main()
