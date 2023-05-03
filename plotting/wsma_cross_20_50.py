#!/usr/bin/env python3

import pandas as pd 
import matplotlib.pyplot as plt 
#import math
import numpy as np
import yfinance as yf

def __WSMA( data, n):
    # sma = data.rolling(window=n).mean()
    # ema = data.ewm(span=n, adjust=False).mean()
    weights = np.arange(1, n+1)
    wma = data['Close'].rolling(n).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
    data['WSMA_{}'.format(n)] = pd.Series(wma)

    return data


plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

symbol = 'AAPL'
data = yf.download ( symbol, start="2020-01-01", progress=False)

data = __WSMA ( data, 20 )
data = __WSMA ( data, 50 )


def implement_sma_strategy(data, short_window, long_window):
    sma1 = short_window
    sma2 = long_window
    buy_price = []
    sell_price = []
    sma_signal = []
    signal = 0

    for i in range(len(data)):
        if sma1[i] > sma2[i]:
            if signal != 1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 1
                sma_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                sma_signal.append(0)
        elif sma2[i] > sma1[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                sma_signal.append(-1)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                sma_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            sma_signal.append(0)
            
    return buy_price, sell_price, sma_signal

sma_20 = data['WSMA_20']
sma_50 = data['WSMA_50']

buy_price, sell_price, signal = implement_sma_strategy ( data['Close'], sma_20, sma_50)

plt.plot ( data['Close'], alpha = 0.3, label = symbol)
plt.plot ( sma_20, alpha = 0.6, label = 'SMA_20')
plt.plot ( sma_50, alpha = 0.6, label = 'SMA_50')
plt.scatter ( data.index, buy_price, marker = '^', s = 200, color = 'darkblue', label = 'BUY SIGNAL')
plt.scatter ( data.index, sell_price, marker = 'v', s = 200, color = 'crimson', label = 'SELL SIGNAL')
plt.legend(loc = 'upper left')
plt.title(f'{symbol} Weighted SMA CROSSOVER TRADING SIGNALS')

#plt.show()
plt.savefig ('_plots/' + symbol + '_WSMA_20_50_cross.png')

