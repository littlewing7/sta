#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def __AO ( data, window1=5, window2=34 ):
    """
    Calculates the Awesome Oscillator for a given DataFrame containing historical stock data.

    Parameters:
        data (pandas.DataFrame): DataFrame containing the historical stock data.
        window1 (int): Window size for the first simple moving average (default is 5).
        window2 (int): Window size for the second simple moving average (default is 34).

    Returns:
        data (pandas.DataFrame): DataFrame with an additional column containing the Awesome Oscillator.
    """
    # Calculate the Awesome Oscillator (AO)
    high = data["High"]
    low = data["Low"]
    median_price = (high + low) / 2
    ao = median_price.rolling(window=window1).mean() - median_price.rolling(window=window2).mean()
    #return ao

    # Add the AO to the DataFrame
    data["AO"] = ao

    return data


plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')

symbol = 'AAPL'

# EXTRACTING STOCK DATA
data = yf.download ( symbol, start='2020-01-01', progress=False)

data = __AO ( data, 5, 34)
data = data.dropna()


def implement_ao_crossover(price, ao):
    buy_price = []
    sell_price = []
    ao_signal = []
    signal = 0

    for i in range(len(ao)):
        if ao[i] > 0 and ao[i-1] < 0:
            if signal != 1:
                buy_price.append(price[i])
                sell_price.append(np.nan)
                signal = 1
                ao_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ao_signal.append(0)
        elif ao[i] < 0 and ao[i-1] > 0:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(price[i])
                signal = -1
                ao_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ao_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            ao_signal.append(0)
    return buy_price, sell_price, ao_signal

buy_price, sell_price, ao_signal = implement_ao_crossover( data['Close'], data['AO'])

ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 4, colspan = 1)

ax1.plot( data['Close'], label = symbol, color = 'skyblue')
ax1.plot( data.index, buy_price, marker = '^', markersize = 12, color = '#26a69a', linewidth = 0, label = 'BUY SIGNAL')
ax1.plot( data.index, sell_price, marker = 'v', markersize = 12, color = '#f44336', linewidth = 0, label = 'SELL SIGNAL')
ax1.legend()
ax1.set_title(f'{symbol} CLOSING PRICE')

for i in range(len( data )):
    if data['AO'][i-1] > data['AO'][i]:
        ax2.bar( data.index[i], data['AO'][i], color = '#f44336')
    else:
        ax2.bar ( data.index[i], data['AO'][i], color = '#26a69a')
ax2.set_title(f'{symbol} AWESOME OSCILLATOR 5,34')
#plt.show()
plt.savefig ('_plots/' + symbol + '_AO.png')


