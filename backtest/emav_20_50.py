#!/usr/bin/env python3

import yfinance as yf
import pandas as pd

def __EMAV ( data, n=9 ):
    data['EMAV_{}'.format(n)] = data['Volume'].ewm(span = n ,adjust = False).mean()
    return data

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download(stock, start=start_date, progress=False)

    data = __EMAV (data, 20)
    data = __EMAV (data, 50)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["EMAV_20"][i] > data["EMAV_50"][i] and data["EMAV_20"][i - 1] < data["EMAV_50"][i - 1] and position == 0:
            position = 1
            buy_price = data["Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["EMAV_20"][i] < data["EMAV_50"][i] and data["EMAV_20"][i - 1]  > data["EMAV_50"][i - 1] and position == 1:
            position = 0
            sell_price = data["Close"][i]
            today = data.index[i]
            #print(f"Selling {stock} at {sell_price} @ {today}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000

    import sys
    name = sys.argv[0]

    # Print results
    print(f"\n{name} ::: {stock} Backtest Results ({start_date} - today)")
    print(f"---------------------------------------------")
    print(f"{name} ::: {stock} - Total Returns: ${total_returns:,.2f}")
    print(f"{name} ::: {stock} - Profit/Loss: {((total_returns - 100000) / 100000) * 100:.2f}%")


if __name__ == '__main__':

    start_date = "2020-01-01"

    backtest_strategy("AAPL", start_date)
    print ("\n")
    backtest_strategy("SPY", start_date)

