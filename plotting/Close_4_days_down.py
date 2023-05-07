#!/usr/bin/env python3

import os

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)


filename, ext =  os.path.splitext(os.path.basename(__file__))

symbol = 'AAPL'

# Load stock data
data = yf.download( symbol, start="2020-01-01", progress=False)


data["Signal"] = 0.0
data['Close_4_days_Signal'] = np.select(
    [ ( data['Close'] < data['Close'].shift(1) ) & ( data['Close'].shift(1) <  data['Close'].shift(2) ) & ( data['Close'].shift(2) <  data['Close'].shift(3) ) & ( data['Close'].shift(3) <  data['Close'].shift(4) ),
      ( data['Close'] > data['Close'].shift(1) ) & ( data['Close'].shift(1) >  data['Close'].shift(2) ) ],
[2, -2])


#print ( data.tail ( 60 ))

# Plot the trading signals
plt.figure(figsize=(14,7))

plt.plot ( data['Close'],  alpha = 0.3, linewidth = 2,                  label = symbol  )

plt.plot ( data.loc[data["Close_4_days_Signal"] ==  2.0].index, data["Close"][data["Close_4_days_Signal"] ==  2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
plt.plot ( data.loc[data["Close_4_days_Signal"] == -2.0].index, data["Close"][data["Close_4_days_Signal"] == -2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

plt.legend(loc = 'upper left')
plt.title(f'{symbol}_{filename}')


#plt.show()

filename = "_plots/{}_{}.png".format ( symbol, filename )
plt.savefig ( filename )

