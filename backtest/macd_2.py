#!/usr/bin/env python3

# https://medium.com/codex/algorithmic-trading-with-macd-in-python-1c2769a6ad1b

import argparse
import yfinance as yf
import pandas as pd
import numpy as np
from math import floor
import matplotlib.pyplot as plt

import os, datetime

def __MACD (data, m=12, n=26, p=9, pc='Close'):

    data = data.copy()
    data['EMA_s'] = data[pc].ewm(span=m, adjust=False).mean()
    data['EMA_l'] = data[pc].ewm(span=n, adjust=False).mean()

    data['MACD']  = data['EMA_s'] - data['EMA_l']
    #data["MACD"] = data.apply(lambda x: (x["EMA_s"]-x["EMA_l"]), axis=1)
    data['MACD_SIGNAL'] = data['MACD'].ewm(span=p, adjust=False).mean()
    data['MACD_HIST']   = (data['MACD'] - data['MACD_SIGNAL'])


    data.drop(['EMA_s', 'EMA_l'], axis=1, inplace=True)

    return data


plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')



symbol= 'AAPL'
data = yf.download ('AAPL', start='2020-01-01', progress=False )
data = __MACD ( data )


# creating the strategy
def implement_macd_strategy(prices, data):
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
        if data['MACD'][i] > data['MACD_SIGNAL'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif data['MACD'][i] < data['MACD_SIGNAL'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)

    return buy_price, sell_price, macd_signal


buy_price, sell_price, macd_signal = implement_macd_strategy( data['Close'], data)


# Creating our position
position = []
for i in range(len(data['MACD_SIGNAL'])):
    if macd_signal[i] > 1:
        position.append(0)
    else:
        position.append(1)

for i in range(len(data['Close'])):
    if macd_signal[i] == 1:
        position[i] = 1
    elif macd_signal[i] == -1:
        position[i] = 0
    else:
        position[i] = position[i - 1]

macd = data['MACD']
signal = data['MACD_SIGNAL']
close_price = data['Close']
macd_signal = pd.DataFrame(macd_signal).rename(columns={0: 'macd_signal'}).set_index( data.index)
position = pd.DataFrame(position).rename(columns={0: 'macd_position'}).set_index(data.index)

frames = [close_price, macd, signal, macd_signal, position]
strategy = pd.concat(frames, join='inner', axis=1)

# Backstesting
googl_ret = pd.DataFrame(np.diff(data['Close'])).rename(columns={0: 'returns'})
macd_strategy_ret = []

for i in range(len(googl_ret)):
    try:
        returns = googl_ret['returns'][i] * strategy['macd_position'][i]
        macd_strategy_ret.append(returns)
    except:
        pass

macd_strategy_ret_df = pd.DataFrame(macd_strategy_ret).rename(columns={0: 'macd_returns'})

investment_value = 100000
number_of_stocks = floor(investment_value / data['Close'][0])
macd_investment_ret = []

for i in range(len(macd_strategy_ret_df['macd_returns'])):
    returns = number_of_stocks * macd_strategy_ret_df['macd_returns'][i]
    macd_investment_ret.append(returns)

macd_investment_ret_df = pd.DataFrame(macd_investment_ret).rename(columns={0: 'investment_returns'})
total_investment_ret = round(sum(macd_investment_ret_df['investment_returns']), 2)
profit_percentage = floor((total_investment_ret / investment_value) * 100)
print('Profit gained from the MACD strategy by investing $100k in {} : {}'.format( symbol, total_investment_ret))
print('Profit percentage of the MACD strategy : {}%'.format(profit_percentage))

