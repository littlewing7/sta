#!/usr/bin/env python3

# https://medium.com/codex/algorithmic-trading-with-macd-in-python-1c2769a6ad1b

import yfinance as yf
import pandas as pd
import numpy as np
from math import floor
import matplotlib.pyplot as plt

def __MACD (data, m=12, n=26, p=9, pc='Close'):

    data = data.copy()
    data['EMA_s'] = data[pc].ewm(span=m, adjust=False).mean()
    data['EMA_l'] = data[pc].ewm(span=n, adjust=False).mean()

    data['MACD']  = data['EMA_s'] - data['EMA_l']
    #data["MACD"] = data.apply(lambda x: (x["EMA_s"]-x["EMA_l"]), axis=1)
    data['MACD_SIGNAL'] = data['MACD'].ewm(span=p, adjust=False).mean()
    data['MACD_HIST']   = (data['MACD'] - data['MACD_SIGNAL'])


    data.drop(['EMA_s', 'EMA_l'], axis=1, inplace=True)

    return data


plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')



symbol= 'AAPL'
data = yf.download ('AAPL', start='2020-01-01', progress=False )
data = __MACD ( data )




ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

ax1.plot ( data['Close'] )
ax2.plot ( data['MACD'], color='grey', linewidth=1.5, label='MACD')
ax2.plot ( data['MACD_SIGNAL'], color='skyblue', linewidth=1.5, label='SIGNAL')

for i in range(len( data['Close'])):
    if str( data['MACD_HIST'][i])[0] == '-':
        ax2.bar( data.index[i], data['MACD_HIST'][i], color='#ef5350')
    else:
        ax2.bar( data.index[i], data['MACD_HIST'][i], color='#26a69a')

plt.legend(loc='lower right')

#plt.show()
plt.savefig ('_plots/' + symbol + '_MACD2_simple.png')

