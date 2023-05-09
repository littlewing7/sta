#!/usr/bin/env python3

import os

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)


def __WSMA( data, n):
    # sma = data.rolling(window=n).mean()
    # ema = data.ewm(span=n, adjust=False).mean()
    weights = np.arange(1, n+1)
    wma = data['Close'].rolling(n).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
    data['WSMA_{}'.format(n)] = pd.Series(wma)

    return data

filename, ext =  os.path.splitext(os.path.basename(__file__))

symbol = 'AAPL'

# Load stock data
data = yf.download( symbol, start="2020-01-01", progress=False)

# SMA 20, 50
data = __WSMA ( data, 20 )
data = __WSMA ( data, 50 )

# Buy/sell signals for  SMA crosses
data["Signal"] = 0.0
data['WSMA_20_50_Signal'] = np.select(
    [ ( data['WSMA_20'].shift(1) <  data['WSMA_50'].shift(1) ) & ( data['WSMA_20'] >  data['WSMA_50'] ) ,
      ( data['WSMA_20'].shift(1) >  data['WSMA_50'].shift(1) ) & ( data['WSMA_20'] <  data['WSMA_50'] ) ],
[2, -2])


#print ( data.tail ( 60 ))

# Plot the trading signals
plt.figure(figsize=(14,7))

plt.plot ( data['Close'],  alpha = 0.3, linewidth = 2,                  label = symbol,  )
plt.plot ( data["WSMA_20"], alpha = 0.6, linewidth = 2, color='orange',  label = 'WSMA_20',  )
plt.plot ( data["WSMA_50"], alpha = 0.6, linewidth = 3, color='#FF006E', label = 'WSMA_50' )

plt.plot ( data.loc[data["WSMA_20_50_Signal"] ==  2.0].index, data["WSMA_20"][data["WSMA_20_50_Signal"] ==  2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
plt.plot ( data.loc[data["WSMA_20_50_Signal"] == -2.0].index, data["WSMA_20"][data["WSMA_20_50_Signal"] == -2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

plt.legend(loc = 'upper left')
plt.title(f'{symbol}_{filename}')


#plt.show()

filename = "_plots/{}_{}.png".format ( symbol, filename )
plt.savefig ( filename )

