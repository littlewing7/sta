#!/usr/bin/env python3

import os,sys

import yfinance as yf
import pandas as pd
import numpy as np
import math

def __WR (high, low, close, t):
    highh = high.rolling(t).max()
    lowl = low.rolling(t).min()
    wr = -100 * ((highh - close) / (highh - lowl))
    return wr


# Get stock data from Yahoo Finance
data = yf.download("AAPL", period="5y")

# Calculate Williams %R and add prefix to column names
n = 20
#highest_high = data["High"].rolling(n).max()
#lowest_low = data["Low"].rolling(n).min()

data['WR'] = __WR ( data['High'], data['Low'], data['Close'], n )
data["WR_prev"] = data["WR"].shift(1)

# Reorder columns: WR_prev   WR
cols = list(data.columns)
a, b = cols.index('WR'), cols.index('WR_prev')
cols[b], cols[a] = cols[a], cols[b]
data = data[cols]

# Determine overbought and oversold levels
overbought_level = -20
oversold_level = -80

# Determine cross over and cross under levels
#cross_over = 0
#cross_under = -100

# Use pandas' tail() function to get the last row of data
last_row = data.tail(1)

# Check if the last entry is oversold, overbought, crossunder or crossover
if last_row["WR"].values[0] < oversold_level and last_row["WR_prev"].values[0] >= oversold_level:
    print("Last entry is oversold")
elif last_row["WR"].values[0] > overbought_level and last_row["WR_prev"].values[0] <= overbought_level:
    print("Last entry is overbought")
#elif last_row["WR"].values[0] > cross_over and last_row["WR_prev"].values[0] <= cross_over:
#    print("Last entry is cross over")
#elif last_row["WR"].values[0] < cross_under and last_row["WR_prev"].values[0] >= cross_under:
#    print("Last entry is cross under")
else:
    print("Last entry is not oversold or overbought")

print ( data.tail(5))
