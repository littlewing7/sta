#!/usr/bin/env python3

# https://github.com/carlpaulus/Memoire

# https://medium.com/codex/algorithmic-trading-with-sma-in-python-7d66008d37b1
# https://towardsdatascience.com/trading-toolbox-02-wma-ema-62c22205e2a9
# https://www.investopedia.com/ask/answers/071414/whats-difference-between-moving-average-and-weighted-moving-average.asp

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import math
import numpy as np

def __EMAV ( data, n=9 ):
    data['EMAV_{}'.format(n)] = data['Volume'].ewm(span = n ,adjust = False).mean()
    return data

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (15, 8)


symbol = 'AAPL'

data = yf.download ( symbol, start='2020-01-01', progress=False )

n = [20, 50]
for i in n:
    data = __EMAV ( data, i)

def implement_sma_strategy(data, short_window, long_window):
    sma1 = short_window
    sma2 = long_window
    buy_price = []
    sell_price = []
    sma_signal = []
    signal = 0

    for i in range(len(data)):
        if sma1[i] > sma2[i]:
            if signal != 1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 1
                sma_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                sma_signal.append(0)
        elif sma2[i] > sma1[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                sma_signal.append(-1)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                sma_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            sma_signal.append(0)

    return buy_price, sell_price, sma_signal


EMAV_20 = data['EMAV_20']
EMAV_50 = data['EMAV_50']

buy_price, sell_price, signal = implement_sma_strategy ( data['Close'], EMAV_20, EMAV_50)

# PLOTTING SMA TRADE SIGNALS
ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)

ax1.plot ( data['Close'], alpha=0.3, label=symbol)
ax1.plot ( data.index, buy_price, marker='^', markersize=12, linewidth=0, color='darkblue', label='BUY SIGNAL')
ax1.plot ( data.index, sell_price, marker='v', markersize=12, linewidth=0, color='crimson', label='SELL SIGNAL')
ax1.legend ( loc='upper left', fontsize=12)
ax1.set_title ( 'EMA VOLUME TRADING SIGNALS')

ax2.plot ( EMAV_20, alpha=0.6, label='EMA Vol 20')
ax2.plot ( EMAV_50, alpha=0.6, label='SMA Vol 50')
ax2.legend ( loc='upper left', fontsize=12)
ax2.set_title ( 'EMA VOLUME CROSSOVER')
#plt.show()
plt.savefig ('_plots/' + symbol + '_EMAV_20_50_cross.png')

# OUR POSITION IN STOCK (HOLD/SOLD)

position = []
for i in range(len(signal)):
    if signal[i] > 1:
        position.append(0)
    else:
        position.append(1)

for i in range( len ( data['Volume'])):
    if signal[i] == 1:
        position[i] = 1
    elif signal[i] == -1:
        position[i] = 0
    else:
        position[i] = position[i - 1]

# CONSOLIDATING LISTS TO DATAFRAME

EMAV_20 = pd.DataFrame(EMAV_20).rename(columns={0: 'EMAV_20'})
EMAV_50 = pd.DataFrame(EMAV_50).rename(columns={0: 'EMAV_50'})

buy_price = pd.DataFrame(buy_price).rename(columns={0: 'buy_price'}).set_index ( data.index)
sell_price = pd.DataFrame(sell_price).rename(columns={0: 'sell_price'}).set_index ( data.index)
signal = pd.DataFrame(signal).rename(columns={0: 'sma_signal'}).set_index ( data.index)
position = pd.DataFrame(position).rename(columns={0: 'sma_position'}).set_index ( data.index)

frames = [ EMAV_20, EMAV_50, buy_price, sell_price, signal, position]
strategy = pd.concat(frames, join='inner', axis=1)
strategy = strategy.reset_index().drop('Date', axis=1)
# print(strategy)

# BACKTESTING THE STRAGEGY

msft_ret = pd.DataFrame(np.diff ( data['Close'])).rename(columns={0: 'returns'})
#print(msft_ret)
sma_strategy_ret = []

for i in range(len(msft_ret)):
    try:
        returns = msft_ret['returns'][i] * strategy['sma_position'][i]
        sma_strategy_ret.append(returns)
    except:
        pass

sma_strategy_ret_df = pd.DataFrame(sma_strategy_ret).rename(columns={0: 'sma_returns'})

investment_value = 100000
number_of_stocks = math.floor(investment_value / data['Close'][1])
sma_investment_ret = []

for i in range(len(sma_strategy_ret_df['sma_returns'])):
    returns = number_of_stocks * sma_strategy_ret_df['sma_returns'][i]
    sma_investment_ret.append(returns)

sma_investment_ret_df = pd.DataFrame(sma_investment_ret).rename(columns={0: 'investment_returns'})
total_investment_ret = round(sum(sma_investment_ret_df['investment_returns']), 2)
print ('Profit gained from the strategy by investing $100K in {} : ${} in 1 Year'.format(symbol, total_investment_ret))

