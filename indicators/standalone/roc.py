#!/usr/bin/env python3

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

def __ROC (df, n=12, m=6):
    df['ROC']   = ( df["Close"] - df["Close"].shift(n))/df["Close"].shift(n) * 100
    df['ROCMA'] = df["ROC"].rolling(m).mean()
    return df


# Set the ticker symbol and date range
symbol = "AAPL"

# Retrieve the daily price data
data = yf.download(symbol, period='5y')

data = data.drop(['Adj Close'], axis=1).dropna()

# Calculate the KDJ indicator using the function
data = __ROC (data)

# Print the data
print(data.tail(10))
