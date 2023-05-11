#!/usr/bin/env python3
# RETURN 53%

import yfinance as yf
import pandas as pd

import numpy as np

import warnings
warnings.simplefilter ( action='ignore', category=Warning )


def __WR (data, t):
    highh = data["High"].rolling(t).max()
    lowl  = data["Low"].rolling(t).min()
    close = data["Close"]

    data['WR_{}'.format(t)] = -100 * ((highh - close) / (highh - lowl))

    return data

def __MACD (data, m=12, n=26, p=9, pc='Close'):

    data = data.copy()
    data['EMA_s'] = data[pc].ewm(span=m, adjust=False).mean()
    data['EMA_l'] = data[pc].ewm(span=n, adjust=False).mean()

    data['MACD']  = data['EMA_s'] - data['EMA_l']
    data['MACD_SIGNAL'] = data['MACD'].ewm(span=p, adjust=False).mean()
    data['MACD_HIST']   = (data['MACD'] - data['MACD_SIGNAL'])


    data.drop(['EMA_s', 'EMA_l'], axis=1, inplace=True)

    return data


def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download ( stock, start=start_date, progress=False )

    # Calculate indicators
    data = __MACD (data)
    data = __WR (data, 20)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if position == 0 and ( data["WR_20"][i-1] > -50 and data["WR_20"][i] < -50 and data["MACD"][i] > data["MACD_SIGNAL"][i] ):
            position = 1
            buy_price = data["Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif position == 1 and ( data["WR_20"][i-1] < -50 and data["WR_20"][i] > -50 and data["MACD"][i] < data["MACD_SIGNAL"][i] ):
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

