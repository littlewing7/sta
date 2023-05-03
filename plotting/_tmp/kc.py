#!/usr/bin/env python3

# IMPORTING PACKAGES

import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from termcolor import colored as cl
from math import floor

import warnings
warnings.simplefilter ( action='ignore', category=Warning )

import yfinance as yf


plt.rcParams['figure.figsize'] = (20,10)
plt.style.use('fivethirtyeight')


# KELTNER CHANNEL CALCULATION
def get_kc(high, low, close, kc_lookback, multiplier, atr_lookback):
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift()))
    tr3 = pd.DataFrame(abs(low - close.shift()))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.ewm(alpha = 1/atr_lookback).mean()
    
    kc_middle = close.ewm(kc_lookback).mean()
    kc_upper = close.ewm(kc_lookback).mean() + multiplier * atr
    kc_lower = close.ewm(kc_lookback).mean() - multiplier * atr
    
    return kc_middle, kc_upper, kc_lower

#intc = get_historical_data('INTC', '2020-01-01')
# EXTRACTING STOCK DATA
intc = yf.download ('AAPL', period='5y')

intc['high'] = intc["High"]
intc['low'] = intc["Low"]
intc['close'] = intc["Close"]
print(intc.tail())


    
intc = intc.iloc[:,:4]
intc['kc_middle'], intc['kc_upper'], intc['kc_lower'] = get_kc(intc['High'], intc['Low'], intc['Close'], 20, 2, 10)
print(intc.tail())


# KELTNER CHANNEL PLOT
plt.plot(intc['Close'], linewidth = 2, label = 'AAPL')
plt.plot(intc['kc_upper'], linewidth = 2, color = 'orange', linestyle = '--', label = 'KC UPPER 20')
plt.plot(intc['kc_middle'], linewidth = 1.5, color = 'grey', label = 'KC MIDDLE 20')
plt.plot(intc['kc_lower'], linewidth = 2, color = 'orange', linestyle = '--', label = 'KC LOWER 20')
plt.legend(loc = 'lower right', fontsize = 15)
plt.title('AAPL KELTNER CHANNEL 20')
plt.show()

