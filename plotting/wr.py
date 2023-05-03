#!/usr/bin/env python3

# https://github.com/carlpaulus/Memoire
# https://medium.com/codex/algorithmic-trading-with-williams-r-in-python-5a8e0db9ff1f

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def __WR (data, t):
    highh = data["High"].rolling(t).max()
    lowl  = data["Low"].rolling(t).min()
    close = data["Close"]

    data['WR_{}'.format(t)] = -100 * ((highh - close) / (highh - lowl))

    return data

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')


symbol = 'AAPL'
data = yf.download(symbol, start='2020-01-01', progress=False).drop('Adj Close', axis=1)

data = __WR ( data, 20 )
data = data.dropna()


def implement_wr_strategy(prices, wr):
    buy_price = []
    sell_price = []
    wr_signal = []
    signal = 0

    for i in range(len(wr)):
        if wr[i - 1] > -80 and wr[i] < -80:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                wr_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                wr_signal.append(0)
        elif wr[i - 1] < -20 and wr[i] > -20:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                wr_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                wr_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            wr_signal.append(0)

    return buy_price, sell_price, wr_signal


buy_price, sell_price, wr_signal = implement_wr_strategy ( data['Close'], data['WR_20'])

#  plotting the trading signals
ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)

ax1.plot ( data['Close'], linewidth=2, label='SPY')
ax1.plot ( data.index, buy_price, marker='^', markersize=10, linewidth=0, color='green', label='BUY SIGNAL')
ax1.plot ( data.index, sell_price, marker='v', markersize=10, linewidth=0, color='r', label='SELL SIGNAL')
ax1.legend(loc='upper left', fontsize=12)
ax1.set_title(f'{symbol} W%R TRADING SIGNALS')

ax2.plot ( data['WR_20'], color='orange', linewidth=2)
ax2.axhline ( -20, linewidth=1.5, linestyle='--', color='grey')
ax2.axhline ( -80, linewidth=1.5, linestyle='--', color='grey')
ax2.set_title (f'{symbol} W%R')

#plt.show()
plt.savefig ('_plots/' + symbol + '_WR.png')

