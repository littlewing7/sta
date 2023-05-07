#!/usr/bin/env python3

import os

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (9, 10)

filename, ext =  os.path.splitext(os.path.basename(__file__))

symbol = 'AAPL'

# Load stock data
data = yf.download( symbol, start="2020-01-01", progress=False)

# SMA 9, 21
data["SMA_9"] = data["Close"].rolling(window=9).mean()
data["SMA_21"] = data["Close"].rolling(window=21).mean()

# Buy/sell signals for  SMA crosses
data["Signal"] = 0.0
data['SMA_9_21_Signal'] = np.select(
    [ ( data['SMA_9'].shift(1) <  data['SMA_21'].shift(1) ) & ( data['SMA_9'] >  data['SMA_21'] ) ,
      ( data['SMA_9'].shift(1) >  data['SMA_21'].shift(1) ) & ( data['SMA_9'] <  data['SMA_21'] ) ],
[2, -2])


#print ( data.tail ( 60 ))

# Plot the trading signals
plt.figure(figsize=(14,7))

plt.plot ( data['Close'],  alpha = 0.3, linewidth = 2,                  label = symbol,  )
plt.plot ( data["SMA_9"], alpha = 0.6, linewidth = 2, color='orange',  label = 'SMA_9',  )
plt.plot ( data["SMA_21"], alpha = 0.6, linewidth = 3, color='#FF006E', label = 'SMA_21' )

plt.plot ( data.loc[data["SMA_9_21_Signal"] ==  2.0].index, data["SMA_9"][data["SMA_9_21_Signal"] ==  2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
plt.plot ( data.loc[data["SMA_9_21_Signal"] == -2.0].index, data["SMA_9"][data["SMA_9_21_Signal"] == -2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

plt.legend(loc = 'upper left')
plt.title(f'{symbol}_{filename}')


#plt.show()

filename = "_plots/{}_{}.png".format ( symbol, filename )
plt.savefig ( filename )

