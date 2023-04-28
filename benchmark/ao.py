#!/usr/bin/env python3
# RETURN 53%

import yfinance as yf
import pandas as pd

import numpy as np

import warnings
warnings.simplefilter ( action='ignore', category=Warning )


def __AO ( data, window1=5, window2=34 ):
    """
    Calculates the Awesome Oscillator for a given DataFrame containing historical stock data.

    Parameters:
        data (pandas.DataFrame): DataFrame containing the historical stock data.
        window1 (int): Window size for the first simple moving average (default is 5).
        window2 (int): Window size for the second simple moving average (default is 34).

    Returns:
        data (pandas.DataFrame): DataFrame with an additional column containing the Awesome Oscillator.
    """
    # Calculate the Awesome Oscillator (AO)
    high = data["High"]
    low = data["Low"]
    median_price = (high + low) / 2
    ao = median_price.rolling(window=window1).mean() - median_price.rolling(window=window2).mean()

    # Add the AO to the DataFrame
    data["AO"] = ao

    return data


def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download ( stock, start=start_date )

    # Calculate indicators
    data = __AO ( data, 5, 34 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if  data["AO"][i] > 0 and data["AO"][i-1] < 0 and position == 0:
            position = 1
            buy_price = data["Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif data["AO"][i] < 0 and data["AO"][i-1] > 0 and position == 1:
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

    start_date = "2020-01-01"

    backtest_strategy("AAPL", start_date)
    print("\n")
    backtest_strategy("SPY", start_date)


