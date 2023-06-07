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

# SMA
data = __EMA ( data, 20 )

# Buy/sell signals for  SMA crosses
data["Signal"] = 0.0
data['EMA_20_Close_Signal'] = np.select(
    [ ( data['EMA_20'].shift(1) <  data['Adj Close'].shift(1) ) & ( data['EMA_20'] >  data['Adj Close'] ) ,
      ( data['EMA_20'].shift(1) >  data['Adj Close'].shift(1) ) & ( data['EMA_20'] <  data['Adj Close'] ) ],
[2, -2])


#print ( data.tail ( 60 ))

# Plot the trading signals
#plt.figure(figsize=(14,7))

plt.plot ( data['Adj Close'],  alpha = 0.3, linewidth = 2,                  label = symbol + ' Price'  )
plt.plot ( data["EMA_20"], alpha = 0.6, linewidth = 2, color='#FF006E', label = 'EMA_20' )

plt.plot ( data.loc[data["EMA_20_Close_Signal"] == -2.0].index, data["EMA_20"][data["EMA_20_Close_Signal"] ==  -2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
plt.plot ( data.loc[data["EMA_20_Close_Signal"] ==  2.0].index, data["EMA_20"][data["EMA_20_Close_Signal"] ==  2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

plt.legend(loc = 'upper left')
plt.title(f'{symbol}_{filename}')

plt.xlabel('Date')
plt.ylabel('Closing Prices')
plt.legend(loc = 'upper left')


#plt.show()

filename = "_plots/{}_{}.png".format ( symbol, filename )
plt.savefig ( filename )

