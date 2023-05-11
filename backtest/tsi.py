#!/usr/bin/env python3

import yfinance as yf
import pandas as pd

import numpy as np

import warnings
warnings.simplefilter ( action='ignore', category=Warning )

def __TSI ( data, long, short, signal):
    close = data["Close"]
    diff = close - close.shift(1)
    abs_diff = abs(diff)

    diff_smoothed = diff.ewm(span = long, adjust = False).mean()
    diff_double_smoothed = diff_smoothed.ewm(span = short, adjust = False).mean()
    abs_diff_smoothed = abs_diff.ewm(span = long, adjust = False).mean()
    abs_diff_double_smoothed = abs_diff_smoothed.ewm(span = short, adjust = False).mean()

    tsi = (diff_double_smoothed / abs_diff_double_smoothed) * 100
    signal = tsi.ewm(span = signal, adjust = False).mean()
    #tsi = tsi[tsi.index >= '2020-01-01'].dropna()
    #signal = signal[signal.index >= '2020-01-01'].dropna()
    data['TSI'] = tsi
    data['TSI_SIGNAL'] = signal
    return data


def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download(stock, start=start_date, progress=False )

    # Calculate Stochastic RSI
    data = __TSI ( data, 25, 13, 12 )

    line = data['TSI']
    signal = data['TSI_SIGNAL']


# BUY CRITERIA: if TSI line and signal line is below 0 and tsi crosses signal line

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if (position == 0) and  (  line.iloc[i] < 0 and signal.iloc[i] < 0 and line.iloc[i-1] < 0 and signal.iloc[i-1] < 0) and \
            ((line.iloc[i] > signal.iloc[i] and line.iloc[i-1] < signal.iloc[i-1]) or (
              line.iloc[i] < signal.iloc[i] and line.iloc[i-1] > signal.iloc[i-1])):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and (line.iloc[i] > 0 and signal.iloc[i] > 0 and line.iloc[i-1] > 0 and signal.iloc[i-1] > 0) and \
            ((line.iloc[i] < signal.iloc[i] and line.iloc[i-1] > signal.iloc[i-1]) or (
              line.iloc[i] > signal.iloc[i] and line.iloc[i-1] < signal.iloc[i-1])):
            position = 0
            sell_price = data["Adj Close"][i]
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

