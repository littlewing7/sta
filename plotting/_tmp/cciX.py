#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import yfinance as yf
yf.pdr_override()
import datetime as dt

# input
symbol = 'AAPL'
start = dt.date.today() - dt.timedelta(days = 365*3)
end = dt.date.today()

# Read data 
df = yf.download(symbol,start,end)

n = 20
df['TP'] = (df['High'] + df['Low'] + df['Adj Close'])/3
df['SMA_TP'] = df['TP'].rolling(n).mean()
df['SMA_STD'] = df['TP'].rolling(n).std()
df['CCI'] = (df['TP'] - df['SMA_TP']) / (0.015*df['SMA_STD'])
df = df.drop(['TP', 'SMA_TP', 'SMA_STD'],axis=1)



fig, axs = plt.subplots(3, sharex=True, figsize=(12, 8))

symbol = 'AAPL'

axs[0].set_ylabel("Price")
axs[0].grid(True)
axs[0].plot(df['Close'], color='blue')
axs[0].set_title('Stock '+ symbol +' Closing Price')



# Plot the volume data as a candlestick chart
axs[1].set_ylabel("Volume")
axs[1].grid(True)
axs[1].bar(df.index, df["Volume"], color=np.where(df["Close"].diff() > 0, 'g', 'r'))
axs[1].set_xlabel('Date')



# Plot the CCI indicator

axs[2].set_ylabel("CCI")
axs[2].grid(True)
axs[2].plot(df['CCI'], color='blue', label="CCI blah")

axs[2].axhline(y=100, color='red')
axs[2].axhline(y=-100, color='red')
axs[2].axhline(y=200, color='darkblue')
axs[2].axhline(y=-200, color='darkblue')
axs[2].grid()
axs[2].set_ylabel('CCI')
axs[2].set_xlabel('Date')

fig.suptitle(f"{symbol} - 1d")

plt.show()

