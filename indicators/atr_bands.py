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
from util.atr        import __ATR
from util.atr_bands  import __ATR_BANDS


# Define the ticker and download the historical data
ticker = 'AAPL'
data = yf.download(ticker, period='5y')
data = data.drop(['Adj Close'], axis=1).dropna()

#atr_lower_band, atr_upper_band, atr_middle_band = __ATR_bands ( data, 14 )
data = __ATR_BANDS ( data, 14 )

print ( data.tail(5))
# Get the latest price and check if it's within the ATR bands
latest_price = data.iloc[-1]['Close']

atr_bands_upper = data['ATR_BANDS_UPPER'][-1]
atr_bands_lower = data['ATR_BANDS_LOWER'][-1]


if latest_price > atr_bands_upper:
    print(f"SELL signal for {ticker} at {latest_price}, above the upper ATR band of {atr_bands_upper}")
elif latest_price < atr_bands_lower:
    print(f"BUY signal for {ticker} at {latest_price}, below the lower ATR band of {atr_bands_lower}")
elif latest_price > 0.98 * atr_bands_upper:
    print(f"Warning for {ticker}: the price is within 2% of touching the upper ATR band of {atr_bands_upper}")
elif latest_price < 1.02* atr_bands_lower:
    print(f"Warning for {ticker}: the price is within 2% of touching the lower ATR band of {atr_bands_lower}")
else:
    print(f"No signal or warning for {ticker} at {latest_price}")

print (data.tail(5))
