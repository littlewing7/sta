#!/usr/bin/env python3
# RETURN 53%

import yfinance as yf
import pandas as pd

import numpy as np

import warnings
warnings.simplefilter ( action='ignore', category=Warning )


def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download ( stock, start=start_date, progress=False )


    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( position == 0 ) and ( data["Close"][i] < data["Close"][i - 1] < data["Close"][i - 2] < data["Close"][i - 3] ):
            position = 1
            buy_price = data["Close"][i]
            #print(f"Buying {stock} at {buy_price} on {data.index[i]}")

        # Sell signal
        elif ( position == 1 ) and ( data["Close"][i] > data["Close"][i - 1] > data["Close"][i - 2] ):
            position = 0
            sell_price = data["Close"][i]
            #print(f"Selling {stock} at {sell_price} {data.index[i]}")

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

    parser = argparse.ArgumentParser()
    parser.add_argument('ticker', nargs='+',  type=str, help='your name')

    args = parser.parse_args()
    start_date = "2020-01-01"

    for symbol in args.ticker:

        backtest_strategy(symbol, start_date )
        print  ("\n")

