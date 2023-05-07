#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import yfinance as yf

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
    return data

def __BB (data, window=20):
    std = data['Close'].rolling(window).std()
    data = __SMA ( data, window )
    data['BB_upper']   = data["SMA_20"] + std * 2
    data['BB_lower']   = data["SMA_20"] - std * 2
    data['BB_middle']  = data["SMA_20"]

    return data

# https://github.com/lukaszbinden/rsi_tradingview/blob/main/rsi.py
def __RSI ( data: pd.DataFrame, window: int = 14, round_rsi: bool = True):

    delta = data["Close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm ( up, alpha =1 / window ).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha = 1 / window ).mean()

    rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

    if ( round_rsi ):
        data['RSI_{}'.format ( window )] = np.round (rsi, 2)
    else:
        data['RSI_{}'.format( window )] = rsi

    return data

symbol = 'AAPL'
data = yf.download( symbol, start='2020-01-01', progress=False)

data = __SMA ( data, 13 )
data = __SMA ( data, 20 )
data = __BB ( data, 20 )
data = __RSI ( data, 14 )

buy_price = []
sell_price = []
bb_signal = []
signal = 0

for i in range(len(data)):
    if ( data['SMA_13'][i] > data['BB_middle'][i] ) and ( data["RSI_14"][i] < 50 ):
        if signal != 1:
            buy_price.append(data[i])
            sell_price.append(np.nan)
            signal = 1
            bb_signal.append(signal)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)
    elif  ( data['SMA_13'][i] < data['BB_middle'][i] ) and ( data["RSI_14"][i] > 50 ):
        if signal != -1:
            buy_price.append(np.nan)
            sell_price.append(data[i])
            signal = -1
            bb_signal.append(signal)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)
    else:
        buy_price.append(np.nan)
        sell_price.append(np.nan)
        bb_signal.append(0)



data['Close'].plot    ( label = 'Close PRICE', alpha = 0.3)
data['BB_upper'].plot (label = 'UPPER BB', linestyle = '--', linewidth = 1, color = 'black')
data['SMA_20'].plot   (label = 'MIDDLE BB', linestyle = '--', linewidth = 1.2, color = 'grey')
data['BB_lower'].plot (label = 'LOWER BB', linestyle = '--', linewidth = 1, color = 'black')

plt.scatter ( data.index, buy_price, marker = '^', color = 'green', label = 'BUY', s = 200)
plt.scatter ( data.index, sell_price, marker = 'v', color = 'red', label = 'SELL', s = 200)

plt.title(f'{symbol} BB STRATEGY TRADING SIGNALS')
plt.legend(loc = 'upper left')

plt.show()
#plt.savefig ('_plots/' + symbol + '_BB.png')

