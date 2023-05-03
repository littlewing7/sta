#!/usr/bin/env python3

# IMPORTING PACKAGES

import pandas as pd
import matplotlib.pyplot as plt
import requests
import math
from termcolor import colored as cl
import numpy as np

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (15, 8)

# EXTRACTING DATA

def get_historic_data(symbol):
    ticker = symbol
    iex_api_key = 'Tsk_30a2677082d54c7b8697675d84baf94b'
    api_url = f'https://sandbox.iexapis.com/stable/stock/{ticker}/chart/max?token={iex_api_key}'
    df = requests.get(api_url).json()
    
    date = []
    open = []
    high = []
    low = []
    close = []
    
    for i in range(len(df)):
        date.append(df[i]['date'])
        open.append(df[i]['open'])
        high.append(df[i]['high'])
        low.append(df[i]['low'])
        close.append(df[i]['close'])
    
    date_df = pd.DataFrame(date).rename(columns = {0:'date'})
    open_df = pd.DataFrame(open).rename(columns = {0:'open'})
    high_df = pd.DataFrame(high).rename(columns = {0:'high'})
    low_df = pd.DataFrame(low).rename(columns = {0:'low'})
    close_df = pd.DataFrame(close).rename(columns = {0:'close'})
    
    frames = [date_df, open_df, high_df, low_df, close_df]
    df = pd.concat(frames, axis = 1, join = 'inner')
    return df

msft = get_historic_data('AAPL')
msft = msft.set_index('date')
msft = msft[msft.index >= '2020-01-01']
msft.index = pd.to_datetime(msft.index)
msft.to_csv('msft.csv')

# IMPORTING DATA

msft = pd.read_csv('msft.csv').set_index('date')
msft.index = pd.to_datetime(msft.index)

# DEFINING SMA FUNCTION

def sma(data, n):
    sma = data.rolling(window = n).mean()
    return pd.DataFrame(sma)

n = [20, 50]
for i in n:
    msft[f'sma_{i}'] = sma(msft['close'], i)

# CREATING TRADING STRATEGY

def implement_ma_strategy(data, short_window, long_window):
    ma1 = short_window
    ma2 = long_window
    buy_price = []
    sell_price = []
    ma_signal = []
    signal = 0
    
    for i in range(len(data)):
        if ma1[i] > ma2[i]:
            if signal != 1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 1
                ma_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ma_signal.append(0)
        elif ma2[i] > ma1[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                ma_signal.append(-1)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ma_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            ma_signal.append(0)
            
    return buy_price, sell_price, ma_signal

sma_20 = msft['sma_20']
sma_50 = msft['sma_50']

buy_price, sell_price, signal = implement_ma_strategy(msft['close'], sma_20, sma_50)

# PLOTTING SMA TRADE SIGNALS

plt.plot(msft['close'], alpha = 0.3, label = 'MSFT')
plt.plot(sma_20, alpha = 0.6, label = 'SMA 20')
plt.plot(sma_50, alpha = 0.6, label = 'SMA 50')
plt.scatter(msft.index, buy_price, marker = '^', s = 200, color = 'darkblue')
plt.scatter(msft.index, sell_price, marker = 'v', s = 200, color = 'crimson')
plt.legend(loc = 'upper left')
plt.title('MSFT SMA CROSSOVER TRADING SIGNALS')
plt.show()

# OUR POSITION IN STOCK (HOLD/SOLD)

position = []
for i in range(len(signal)):
    if signal[i] > 1:
        position.append(0)
    else:
        position.append(1)
        
for i in range(len(msft['close'])):
    if signal[i] == 1:
        position[i] = 1
    elif signal[i] == -1:
        position[i] = 0
    else:
        position[i] = position[i-1]
        
sma_20 = pd.DataFrame(sma_20).rename(columns = {0:'sma_20'})
sma_50 = pd.DataFrame(sma_50).rename(columns = {0:'sma_50'})
buy_price = pd.DataFrame(buy_price).rename(columns = {0:'buy_price'}).set_index(msft.index)
sell_price = pd.DataFrame(sell_price).rename(columns = {0:'sell_price'}).set_index(msft.index)
signal = pd.DataFrame(signal).rename(columns = {0:'sma_signal'}).set_index(msft.index)
position = pd.DataFrame(position).rename(columns = {0:'sma_position'}).set_index(msft.index)

frames = [sma_20, sma_50, buy_price, sell_price, signal, position]
strategy = pd.concat(frames, join = 'inner', axis = 1)
strategy = strategy.reset_index().drop('date', axis = 1)

# BACKTESTING THE STRAGEGY

msft_ret = pd.DataFrame(np.diff(msft['close'])).rename(columns = {0:'returns'})
sma_strategy_ret = []

for i in range(len(msft_ret)):
    try:
        returns = msft_ret['returns'][i]*strategy['sma_position'][i]
        sma_strategy_ret.append(returns)
    except:
        pass
    
sma_strategy_ret_df = pd.DataFrame(sma_strategy_ret).rename(columns = {0:'sma_returns'})

investment_value = 100000
number_of_stocks = math.floor(investment_value/msft['close'][1])
sma_investment_ret = []

for i in range(len(sma_strategy_ret_df['sma_returns'])):
    returns = number_of_stocks*sma_strategy_ret_df['sma_returns'][i]
    sma_investment_ret.append(returns)

sma_investment_ret_df = pd.DataFrame(sma_investment_ret).rename(columns = {0:'investment_returns'})
total_investment_ret = round(sum(sma_investment_ret_df['investment_returns']), 2)
print(cl('Profit gained from the strategy by investing $100K in MSFT : ${} in 1 Year'.format(total_investment_ret), attrs = ['bold']))
