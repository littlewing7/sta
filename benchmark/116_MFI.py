#!/usr/bin/env python3
# RETURN 30%

import yfinance as yf
import pandas as pd

import numpy as np

import warnings
warnings.simplefilter ( action='ignore', category=Warning )

def __MFI ( data, window=14):
    # Calculate the Money Flow Index (MFI)
    typical_price = ( data['High'] + data['Low'] + data['Close']) / 3
    money_flow = typical_price * data['Volume']
    positive_money_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_money_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    money_ratio = positive_money_flow.rolling(window=window).sum() / negative_money_flow.rolling(window=window).sum()
    mfi = 100 - (100 / (1 + money_ratio))

    data['MFI_{}'.format(window)] = mfi

    return data

def backtest_strategy(stock, start_date, end_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download(stock, start=start_date, end=end_date)

    # Calculate Stochastic RSI
    data = __MFI ( data, 14 )


# BUY CRITERIA: if TSI line and signal line is below 0 and tsi crosses signal line

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if (position == 0) and ( data["MFI_14"].iloc[i-1] < 25 and data["MFI_14"][i] > 25 ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data["MFI_14"].iloc[i-1] > 75 and data["MFI_14"][i] < 75 ):
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
    end_date   = "2023-04-19"

    backtest_strategy("AAPL", start_date, end_date)
    backtest_strategy("SPY", start_date, end_date)
