#!/usr/bin/env python3

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd

pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")

# def STOCHASTIC_RSI ( data, period=14, smoothD=3, SmoothK=3)
from util.stochastic_rsi   import __STOCHASTIC_RSI


ticker = 'AAPL'
data = yf.download(ticker, period='5y')
data = data.drop(['Adj Close'], axis=1).dropna()

# Define the overbought and oversold levels
srsi_overbought = 80
srsi_oversold = 20

data = __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3 )

# Apply indicator conditions
if data['SRSI_K'][-1] > srsi_oversold and data['SRSI_K'][-2] < srsi_oversold:
    print(f"Weak BUY :: Stochastic RSI crossed over oversold level from above, current SRSI_K value: {data['SRSI_K'][-1]:.2f}")

if data['SRSI_K'][-1] > srsi_oversold and data['SRSI_K'][-2] < srsi_oversold:
    print(f"STRONG BUY, current SRSI_K value: {data['SRSI_K'][-1]:.2f}")

if data['SRSI_K'][-2] < srsi_overbought and data['SRSI_K'][-1] > srsi_overbought:
    print(f"Weak SELL :: Stochastic RSI crossed over overbought level from below, current SRSI_K value: {data['SRSI_K'][-1]:.2f}")

if data['SRSI_K'][-2] > srsi_overbought and data['SRSI_K'][-1] < srsi_overbought:
    print(f"STRONG SELL, current SRSI_K value: {data['SRSI_K'][-1]:.2f}")

print (data.tail (5) )