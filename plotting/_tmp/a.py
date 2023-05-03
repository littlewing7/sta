import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import yfinance as yf
yf.pdr_override()
import datetime as dt 

# input
symbol = 'NIO'
start = dt.date.today() - dt.timedelta(days = 365*2)
end = dt.date.today()

# Read data 
df = yf.download(symbol,start,end)

n = 14
df['HL'] = df['High'] - df['Low']
df['HC'] = abs(df['High'] - df['Adj Close'].shift())
df['LC'] = abs(df['Low'] - df['Adj Close'].shift())
df['TR'] = df[['HL','HC','LC']].max(axis=1)
df['ATR'] = df['TR'].rolling(n).mean()
df = df.drop(['HL','HC','LC','TR'],axis=1)

fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(df['Adj Close'])
ax1.set_title('Stock '+ symbol +' Closing Price')
ax1.set_ylabel('Price')
ax1.legend(loc='best')

ax2 = plt.subplot(2, 1, 2)
ax2.plot(df['ATR'], label='ATR')
ax2.axhline(y=1, color='black')
ax2.grid()
ax2.legend(loc='best')
ax2.set_ylabel('Average True Range')
ax2.set_xlabel('Date')
plt.show()
