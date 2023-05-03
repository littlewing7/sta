#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import yfinance as yf

def __TSI ( data, long, short, signal):
    close = data["Close"]
    diff = close - close.shift(1)
    abs_diff = abs(diff)

    diff_smoothed = diff.ewm(span = long, adjust = False).mean()
    diff_double_smoothed = diff_smoothed.ewm(span = short, adjust = False).mean()
    abs_diff_smoothed = abs_diff.ewm(span = long, adjust = False).mean()
    abs_diff_double_smoothed = abs_diff_smoothed.ewm(span = short, adjust = False).mean()

    tsi = (diff_double_smoothed / abs_diff_double_smoothed) * 100
    signal = tsi.ewm(span = signal, adjust = False).mean()
    data['TSI'] = tsi
    data['TSI_SIGNAL'] = signal
    return data

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

symbol = 'AAPL'
data = yf.download ( symbol, start='2020-01-01', progress=False)
data = __TSI ( data, 25, 13, 12 )


def implement_tsi_strategy(prices, tsi, signal_line):
    buy_price = []
    sell_price = []
    tsi_signal = []
    signal = 0

    for i in range(len(prices)):
        if tsi[i-1] < signal_line[i-1] and tsi[i] > signal_line[i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                tsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                tsi_signal.append(0)
        elif tsi[i-1] > signal_line[i-1] and tsi[i] < signal_line[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                tsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                tsi_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            tsi_signal.append(0)

    return buy_price, sell_price, tsi_signal

buy_price, sell_price, tsi_signal = implement_tsi_strategy( data['Close'], data['TSI'], data['TSI_SIGNAL'])

# TSI PLOT
ax1 = plt.subplot2grid((11,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((11,1), (6,0), rowspan = 5, colspan = 1)

ax1.plot ( data['Close'], linewidth = 2)
ax1.plot ( data.index, buy_price, marker = '^', markersize = 12, color = 'green', linewidth = 0, label = 'BUY SIGNAL')
ax1.plot ( data.index, sell_price, marker = 'v', markersize = 12, color = 'r', linewidth = 0, label = 'SELL SIGNAL')
ax1.legend()
ax1.set_title(f'{symbol} TSI TRADING SIGNALS')

ax2.plot ( data['TSI'],        linewidth = 2, color = 'orange', label = 'TSI LINE')
ax2.plot ( data['TSI_SIGNAL'], linewidth = 2, color = '#FF006E', label = 'SIGNAL LINE')
ax2.set_title(f'{symbol} TSI 25,13,12')
ax2.legend()

#plt.show()
plt.savefig ('_plots/' + symbol + '_TSI.png')

