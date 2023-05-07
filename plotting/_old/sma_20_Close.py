#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
    return data

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

symbol = 'AAPL'
data = yf.download( symbol, start='2020-01-01', progress=False)
data = __SMA ( data, 20 )

data['Close'].plot(label = 'Close', alpha = 0.6)
data['SMA_20'].plot(label = 'SMA 20', linewidth = 2)
plt.xlabel('Date')
plt.ylabel('Closing Prices')
plt.legend(loc = 'upper left')

#plt.show()
plt.savefig ('_plots/' + symbol + '_SMA20_Close.png')
