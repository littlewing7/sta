#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


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


#plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (15, 8)


symbol = 'AAPL'
data = yf.download(symbol,start='2020-01-01', progress=False )
data = __TEMA ( data, 30 )

# Line Chart
fig = plt.figure(figsize=(16,8))
ax1 = plt.subplot(111)
ax1.plot ( data.index, data['Close'] )
ax1.plot ( data.index, data['TEMA_30'] )
ax1.axhline ( y=data['Close'].mean(),color='r')
ax1.grid()
#ax1.grid(True, which='both')
#ax1.grid(which='minor', linestyle='-', linewidth='0.5', color='black')
#ax1.grid(which='major', linestyle='-', linewidth='0.5', color='red')
#ax1.minorticks_on()
ax1.legend(loc='best')
ax1v = ax1.twinx()
ax1v.fill_between ( data.index[0:],0, data.Volume[0:], facecolor='#0079a3', alpha=0.4)
ax1v.axes.yaxis.set_ticklabels([])
ax1v.set_ylim(0, 3*data.Volume.max())
ax1.set_title(symbol +' Closing Price vs TEMA_30')
ax1.set_ylabel('Price')

#plt.show()

plt.savefig ('_plots/' + symbol + '_TEMA_simple.png')
