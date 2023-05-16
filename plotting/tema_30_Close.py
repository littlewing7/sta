#!/usr/bin/env python3

import os

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

def __TEMA(data, n=30):
    """
    Triple Exponential Moving Average (TEMA)
    """
    ema1 = data['Close'].ewm(span=n, adjust=False).mean()
    ema2 = ema1.ewm(span=n, adjust=False).mean()
    ema3 = ema2.ewm(span=n, adjust=False).mean()
    tema = 3 * (ema1 - ema2) + ema3
    data['TEMA_{}'.format(n)] = tema
    return data

filename, ext =  os.path.splitext(os.path.basename(__file__))

symbol = 'AAPL'



# Load stock data
data = yf.download( symbol, start="2022-01-01", progress=False)

# SMA
data = __TEMA ( data, 30 )

# Buy/sell signals for  SMA crosses
data["TEMA_30_Close_Signal"] = 0.0
data['TEMA_30_Close_Signal'] = np.select(
    [ ( data['TEMA_30'].shift(1) <  data['Close'].shift(1) ) & ( data['TEMA_30'] >  data['Close'] ) ,
      ( data['TEMA_30'].shift(1) >  data['Close'].shift(1) ) & ( data['TEMA_30'] <  data['Close'] ) ],
[-2, 2])


#print ( data.tail ( 60 ))

# Plot the trading signals
#plt.figure(figsize=(14,7))

plt.plot ( data['Close'],  alpha = 0.3, linewidth = 2,                  label = symbol + ' Price'  )
plt.plot ( data["TEMA_30"], alpha = 0.6, linewidth = 2, color='#FF006E', label = 'TEMA_30' )

plt.plot ( data.loc[data["TEMA_30_Close_Signal"] ==  2.0].index, data["TEMA_30"][data["TEMA_30_Close_Signal"] ==  2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
plt.plot ( data.loc[data["TEMA_30_Close_Signal"] == -2.0].index, data["TEMA_30"][data["TEMA_30_Close_Signal"] == -2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

plt.legend(loc = 'upper left')
plt.title(f'{symbol}_{filename}')

plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend(loc = 'upper left')


#plt.show()

filename = "_plots/{}_{}.png".format ( symbol, filename )
plt.savefig ( filename )

