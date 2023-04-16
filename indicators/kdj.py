#!/usr/bin/env python3

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

#def __KDJ (df)
from util.kdj   import __KDJ


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
if data.loc[today, 'KDJ_LONG_Signal'] == 1:
    print(f"Buy signal detected for {symbol} on {today.date()}")

if data.loc[today, 'KDJ_SHORT_Signal'] == 1:
    print(f"Sell signal detected for {symbol} on {today.date()}")


# Print the data
print(data.tail(10))
