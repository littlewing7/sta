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

plt.plot ( data.index, data['Close'])
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title(f'{symbol} Closing Price')
plt.legend(loc = 'upper left')

#plt.show()
plt.savefig ('_plots/' + symbol + '_Close.png')
