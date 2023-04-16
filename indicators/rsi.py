#!/usr/bin/env python3

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd

pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")

# def __RSI ( df, window=14 )
from util.rsi   import __RSI


ticker = 'AAPL'
data = yf.download(ticker, period='5y')
data = data.drop(['Adj Close'], axis=1).dropna()

# RSI
data = __RSI ( data, 14)

# Define the overbought and oversold levels
rsi_overbought = 70
rsi_oversold = 30

#data['RSI_Crossover']  = np.where ( ( ( data['RSI'].shift(1) < oversold ) & ( data['RSI'] > oversold ) ), 1, 0 )
#data['RSI_Crossunder'] = np.where ( ( ( data['RSI'].shift(1) > overbought ) & ( data['RSI'] < overbought ) ), 1, 0 )

print (data.tail (5) )

if data['RSI_Crossover'].iloc[-1] == 1:
    print("RSI :: SELL :: Stock has crossed over")
elif data['RSI_Crossunder'].iloc[-1] == 1:
    print("RSI :: SELL :: Stock has crossed under")
else:
    print("No conditions are met")

rsi = data['RSI_14']

# Check if the RSI crosses the overbought or oversold levels
if rsi[-2] < rsi_oversold and rsi[-1] > rsi_oversold:
    print("RSI crossed oversold level from below")
elif rsi[-2] > rsi_overbought and rsi[-1] < rsi_overbought:
    print("RSI crossed overbought level from above")
elif rsi[-2] > rsi_oversold and rsi[-1] < rsi_oversold:
    print("RSI crossed oversold level from above")
elif rsi[-2] < rsi_overbought and rsi[-1] > rsi_overbought:
    print("RSI crossed overbought level from below")
else:
    print("RSI is within normal range")


