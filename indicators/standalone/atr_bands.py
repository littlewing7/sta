#!/usr/bin/env python3

#######################
#####  ATR BANDS  #####
#######################

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
#from util.atr   import __ATR
#from util.atr_bands   import __ATR_BANDS


def calculate_ATR_bands(data, window=20, multiplier=2):
    """
    Calculate the ATR (Average True Range) bands for the given data.
    The ATR bands consist of an upper and a lower band, which are calculated
    as the moving average of the high/low prices plus/minus the ATR times
    a given multiplier.
    """
    # Calculate the True Range
    data['tr0'] = abs(data['High'] - data['Low'])
    data['tr1'] = abs(data['High'] - data['Close'].shift())
    data['tr2'] = abs(data['Low'] - data['Close'].shift())
    data['TR'] = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    data.drop(['tr0', 'tr1', 'tr2'], axis=1, inplace=True)

    # Calculate the ATR
    data['ATR'] = data['TR'].rolling(window=window).mean()

    # Calculate the upper and lower bands
    data['upper_band'] = data['High'].rolling(window=window).mean() + multiplier * data['ATR']
    data['lower_band'] = data['Low'].rolling(window=window).mean() - multiplier * data['ATR']

    return data[['Close', 'upper_band', 'lower_band']].iloc[window:]

# Define the ticker and download the historical data
ticker = 'AAPL'
data = yf.download(ticker, period='5y')

# Calculate the ATR bands
data = calculate_ATR_bands(data)

# Get the latest price and check if it's within the ATR bands
latest_price = data.iloc[-1]['Close']
upper_band = data.iloc[-1]['upper_band']
lower_band = data.iloc[-1]['lower_band']

if latest_price > upper_band:
    print(f"SELL signal for {ticker} at {latest_price}, above the upper ATR band of {upper_band}")
elif latest_price < lower_band:
    print(f"BUY signal for {ticker} at {latest_price}, below the lower ATR band of {lower_band}")
elif latest_price > 0.98*upper_band:
    print(f"Warning for {ticker}: the price is within 2% of touching the upper ATR band of {upper_band}")
elif latest_price < 1.02*lower_band:
    print(f"Warning for {ticker}: the price is within 2% of touching the lower ATR band of {lower_band}")
else:
    print(f"No signal or warning for {ticker} at {latest_price}")

