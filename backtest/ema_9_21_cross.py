#!/usr/bin/env python3

import yfinance as yf
import pandas as pd

import numpy as np

import warnings
warnings.simplefilter ( action='ignore', category=Warning )


def __EMA ( data, n=9 ):
    #ema = data['Close'].ewm(span = period ,adjust = False).mean()
    #return ( ema )

    data['EMA_{}'.format(n)] = data['Close'].ewm(span = n ,adjust = False).mean()
    return data


def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download(stock, start=start_date, progress=False)

    # Calculate Stochastic RSI
    data = __EMA (data, 9)
    data = __EMA (data, 21)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["EMA_9"][i] > data["EMA_21"][i] and data["EMA_9"][i - 1] < data["EMA_21"][i - 1] and position == 0:
            position = 1
            buy_price = data["Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif data["EMA_9"][i] < data["EMA_21"][i] and data["EMA_9"][i - 1]  > data["EMA_21"][i - 1] and position == 1:
            position = 0
            sell_price = data["Close"][i]
            #print(f"Selling {stock} at {sell_price}")

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

