#!/usr/bin/env python3

import os,sys
import yfinance as yf
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

#def __MACD (data, m=12, n=26, p=9, pc='Close'):
from util.macd   import __MACD

import yfinance as yf
import numpy as np


# Download historical data for a stock
symbol = "AAPL"
data = yf.download(symbol, period='3y')

# Calculate the MACD and signal lines using the calculate_macd function
data = __MACD (data)

## Find the MACD crossover and crossunder
#macd_crossover = (macd > signal) & (macd.shift(1) < signal.shift(1))
#macd_crossunder = (macd < signal) & (macd.shift(1) > signal.shift(1))

# Get the most recent day and the previous day in the dataframe
today_data = data.iloc[-1]
yesterday_data = data.iloc[-2]

# Check if the MACD line crossed above or below the signal line on the most recent day
if today_data["MACD"] > today_data["MACD_SIGNAL"] and yesterday_data["MACD"] <= yesterday_data["MACD_SIGNAL"]:
    print("BUY :: MACD crossed above signal on", today_data.name)
elif today_data["MACD"] < today_data["MACD_SIGNAL"] and yesterday_data["MACD"] >= yesterday_data["MACD_SIGNAL"]:
    print("SELL :: MACD crossed below signal on", today_data.name)

# Print the full dataframe with MACD and signal lines
print(data.tail(5))

