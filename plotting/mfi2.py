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
start = dt.date.today() - dt.timedelta(days = 365*2)
end = dt.date.today()

# Read data 
df = yf.download(symbol, period='3y')

# Calculate the Money Flow Index (MFI)
typical_price = (df['High'] + df['Low'] + df['Close']) / 3
money_flow = typical_price * df['Volume']
positive_money_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
negative_money_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
money_ratio = positive_money_flow.rolling(window=14).sum() / negative_money_flow.rolling(window=14).sum()
mfi = 100 - (100 / (1 + money_ratio))

df['MFI'] = mfi
df['Positive'] = df['MFI'] > 0

df['MFI'] = mfi
fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(df.index, df['Adj Close'])
ax1.axhline(y=df['Adj Close'].mean(),color='r')
ax1.axhline(y=df['Adj Close'].max(),color='b')
ax1.axhline(y=df['Adj Close'].min(),color='b')
ax1.text(s='Max Price', x=df['Adj Close'].index[0], y=df['Adj Close'].max(), fontsize=14)
ax1.text(s='Min Price', x=df['Adj Close'].index[0], y=df['Adj Close'].min(), fontsize=14)
ax1.set_ylabel('Price')
ax1.grid()

ax2 = plt.subplot(2, 1, 2)
# ax2.bar(df.index, df['MFI'], color=df.Positive.map({True: 'g', False: 'r'}))
ax2.bar(df.index, df['MFI'])
ax2.grid()
ax2.set_ylabel('Money Flow Index')
ax2.set_xlabel('Date')
plt.show()

# ## Candlestick with MFI
from matplotlib import dates as mdates

dfc = df.copy()
df['MFI'] = mfi
dfc['VolumePositive'] = dfc['Open'] < dfc['Adj Close']
dfc = dfc.dropna()
dfc = dfc.reset_index()
dfc['Date'] = mdates.date2num(dfc['Date'].tolist())
from mplfinance.original_flavor import candlestick_ohlc
fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(2, 1, 1)
candlestick_ohlc(ax1,dfc.values, width=0.5, colorup='g', colordown='r', alpha=1.0)
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax1.grid(True, which='both')
ax1.minorticks_on()
ax1v = ax1.twinx()
colors = dfc.VolumePositive.map({True: 'g', False: 'r'})
ax1v.bar(dfc.Date, dfc['Volume'], color=colors, alpha=0.4)
ax1v.axes.yaxis.set_ticklabels([])
ax1v.set_ylim(0, 3*df.Volume.max())
ax1.set_title('Stock '+ symbol +' Closing Price')
ax1.set_ylabel('Price')

ax2 = plt.subplot(2, 1, 2)
ax2.bar(df.index, df['MFI'])
ax2.grid()
ax2.set_ylabel('Money Flow Index')
ax2.set_xlabel('Date')
plt.show()
