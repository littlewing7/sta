#!/usr/bin/env python3
# RETURN 53%

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

def __TEMA(data, n=30):
    """
    Triple Exponential Moving Average (TEMA)
    """
    ema1 = data['Close'].ewm(span=n, adjust=False).mean()
    ema2 = ema1.ewm(span=n, adjust=False).mean()
    ema3 = ema2.ewm(span=n, adjust=False).mean()
    tema = 3 * (ema1 - ema2) + ema3
    data['TEMA_{}'.format(n)] = tema
    return data


def backtest_strategy(stock, start_date, end_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download(stock, start=start_date, end=end_date, progress=False)

    # EMA 9, TEMA 30
    data = __EMA  ( data, 9 )
    data = __TEMA ( data, 30 )

    #print ( data.tail(2))

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if ( data["Close"][i] > data["TEMA_30"][i] ) and ( data["TEMA_30"][i] > data["TEMA_30"][i - 1] ) and ( data["Close"][i] > data["Close"][i - 1] ) and ( data["Close"][i] > data["EMA_9"][i] ) and ( data["EMA_9"][i] > data["EMA_9"][i -1] ) and ( data["EMA_9"][i] > data["TEMA_30"][i] ) and (position == 0):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( data["Close"][i] < data["TEMA_30"][i] ) and ( data["TEMA_30"][i] < data["TEMA_30"][i - 1] ) and ( data["Close"][i] < data["Close"][i - 1]) and ( data["Close"][i] < data["EMA_9"][i] ) and ( data["EMA_9"][i] < data["EMA_9"][i - 1] ) and position == 1:
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000

    # Print results
    print(f"\n{stock} Backtest Results ({start_date} - {end_date})")
    print(f"---------------------------------------------")
    print(f"Total Returns: ${total_returns:,.2f}")
    print(f"Profit/Loss: {((total_returns - 100000) / 100000) * 100:.2f}%")

if __name__ == '__main__':

    start_date = "2020-01-01"
    end_date = "2023-04-19"

    backtest_strategy("AAPL", start_date, end_date)

    print ("\n\n")

    backtest_strategy("SPY", start_date, end_date)

