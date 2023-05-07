#!/usr/bin/env python3

import os

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)


def __EMA ( data, n=9 ):
    data['EMA_{}'.format(n)] = data['Close'].ewm(span = n ,adjust = False).mean()
    return data

filename, ext =  os.path.splitext(os.path.basename(__file__))

symbol = 'AAPL'

# Load stock data
data = yf.download( symbol, start="2020-01-01", progress=False)

# SMA 20, 50
data = __EMA ( data, 20 )
data = __EMA ( data, 50 )

# Buy/sell signals for  SMA crosses
data["Signal"] = 0.0
data['EMA_20_50_Signal'] = np.select(
    [ ( data['EMA_20'].shift(1) <  data['EMA_50'].shift(1) ) & ( data['EMA_20'] >  data['EMA_50'] ) ,
      ( data['EMA_20'].shift(1) >  data['EMA_50'].shift(1) ) & ( data['EMA_20'] <  data['EMA_50'] ) ],
[2, -2])


#print ( data.tail ( 60 ))

# Plot the trading signals
plt.figure(figsize=(14,7))

plt.plot ( data['Close'],  alpha = 0.3, linewidth = 2,                  label = symbol,  )
plt.plot ( data["EMA_20"], alpha = 0.6, linewidth = 2, color='orange',  label = 'EMA_20',  )
plt.plot ( data["EMA_50"], alpha = 0.6, linewidth = 3, color='#FF006E', label = 'EMA_50' )

plt.plot ( data.loc[data["EMA_20_50_Signal"] ==  2.0].index, data["EMA_20"][data["EMA_20_50_Signal"] ==  2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
plt.plot ( data.loc[data["EMA_20_50_Signal"] == -2.0].index, data["EMA_20"][data["EMA_20_50_Signal"] == -2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

plt.legend(loc = 'upper left')
plt.title(f'{symbol}_{filename}')


#plt.show()

filename = "_plots/{}_{}.png".format ( symbol, filename )
plt.savefig ( filename )

