#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

symbol = 'AAPL'
data = yf.download ( symbol, start='2022-01-01', progress=False)
data = __TEMA ( data, 30 )


def implement_tsi_strategy(prices, tema, close):
    buy_price = []
    sell_price = []
    tema_signal = []
    signal = 0

    for i in range(len(prices)):
        if tema[i-1] < close[i-1] and tema[i] > close[i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                tema_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                tema_signal.append(0)
        elif tema[i-1] > close[i-1] and tema[i] < close[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                tema_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                tema_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            tema_signal.append(0)

    return buy_price, sell_price, tema_signal

buy_price, sell_price, tema_signal = implement_tsi_strategy( data['Close'], data['TEMA_30'], data['Close'])

# TSI PLOT
ax1 = plt.subplot2grid((11,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((11,1), (6,0), rowspan = 5, colspan = 1)

ax1.plot ( data['Close'], linewidth = 2)
ax1.plot ( data.index, buy_price, marker = '^', markersize = 12, color = 'green', linewidth = 0, label = 'BUY SIGNAL')
ax1.plot ( data.index, sell_price, marker = 'v', markersize = 12, color = 'r', linewidth = 0, label = 'SELL SIGNAL')
ax1.legend()
ax1.set_title(f'{symbol} TEMA TRADING SIGNALS')

ax2.plot ( data['TEMA_30'],        linewidth = 2, color = 'orange', label = 'TSI LINE')
ax2.plot ( data['Close'], linewidth = 2, color = '#FF006E', label = 'Close')
ax2.set_title(f'{symbol} TEMA 30')
ax2.legend()

#plt.show()
plt.savefig ('_plots/' + symbol + '_TEMA.png')

