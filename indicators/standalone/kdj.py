#!/usr/bin/env python3

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

def __KDJ (data):
    low_min = data['Low'].rolling(window=9).min()
    high_max = data['High'].rolling(window=9).max()
    rsv = (data['Close'] - low_min) / (high_max - low_min) * 100

    # this is not compabible with tradingview TV
    #data['KDJ_K'] = rsv.rolling(window=3).mean()
    #data['KDJ_D'] = data['KDJ_K'].rolling(window=3).mean()

    # compatible with tradingview and webull
    data['KDJ_K'] = rsv.ewm(com=2, adjust=False).mean()
    data['KDJ_D'] = data['KDJ_K'].ewm(com=2, adjust=False).mean()

    data['KDJ_J'] = 3 * data['KDJ_K'] - 2 * data['KDJ_D']

    data['KDJ_Overbought'] = np.where(data['KDJ_K'] > 80, 1, 0)
    data['KDJ_Oversold'] = np.where(data['KDJ_K'] < 20, 1, 0)

    # Wait for confirmation
    data['KDJ_Buy_Signal'] = np.where  ((data['KDJ_K'] > data['KDJ_D']) & (data['KDJ_K'].shift(1) < data['KDJ_D'].shift(1)), 1, 0)
    data['KDJ_Sell_Signal'] = np.where ((data['KDJ_K'] < data['KDJ_D']) & (data['KDJ_K'].shift(1) > data['KDJ_D'].shift(1)), 1, 0)

    return data



# Set the ticker symbol and date range
symbol = "AAPL"

# Retrieve the daily price data
data = yf.download(symbol, period='5y')

data = data.drop(['Adj Close'], axis=1).dropna()

# Calculate the KDJ indicator using the function
data = __KDJ (data)

# Check for overbought and oversold conditions
if data['KDJ_Overbought'].tail(1).values[0] == 1:
    print(f"{symbol} is currently overbought.")
if data['KDJ_Oversold'].tail(1).values[0] == 1:
    print(f"{symbol} is currently oversold.")

# Check for buy or sell signal today
today = data.index[-1]
if data.loc[today, 'KDJ_Buy_Signal'] == 1:
    print(f"Buy signal detected for {symbol} on {today.date()}")

if data.loc[today, 'KDJ_Sell_Signal'] == 1:
    print(f"Sell signal detected for {symbol} on {today.date()}")


# Print the data
print(data.tail(10))
