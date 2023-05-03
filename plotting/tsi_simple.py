#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import yfinance as yf

def __TSI ( data, long, short, signal):
    close = data["Close"]
    diff = close - close.shift(1)
    abs_diff = abs(diff)

    diff_smoothed = diff.ewm(span = long, adjust = False).mean()
    diff_double_smoothed = diff_smoothed.ewm(span = short, adjust = False).mean()
    abs_diff_smoothed = abs_diff.ewm(span = long, adjust = False).mean()
    abs_diff_double_smoothed = abs_diff_smoothed.ewm(span = short, adjust = False).mean()

    tsi = (diff_double_smoothed / abs_diff_double_smoothed) * 100
    signal = tsi.ewm(span = signal, adjust = False).mean()
    #tsi = tsi[tsi.index >= '2020-01-01'].dropna()
    #signal = signal[signal.index >= '2020-01-01'].dropna()
    data['TSI'] = tsi
    data['TSI_SIGNAL'] = signal
    return data

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

symbol = 'AAPL'
data = yf.download ( symbol, start='2020-01-01', progress=False)
data = __TSI ( data, 25, 13, 12 )

# TSI PLOT
ax1 = plt.subplot2grid((11,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((11,1), (6,0), rowspan = 5, colspan = 1)

ax1.plot ( data['Close'], linewidth = 2.5)
ax1.set_title(f'{symbol} CLOSING PRICE')
ax2.plot ( data['TSI'], linewidth = 2, color = 'orange', label = 'TSI LINE')
ax2.plot ( data['TSI_SIGNAL'], linewidth = 2, color = '#FF006E', label = 'SIGNAL LINE')
ax2.set_title(f'{symbol} TSI 25,13,12')
ax2.legend()
#plt.show()
plt.savefig ('_plots/' + symbol + '_TSI_simple.png')

