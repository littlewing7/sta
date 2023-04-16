#!/usr/bin/env python3

import os,sys
import yfinance as yf
import pandas as pd
pd.set_option('display.precision', 2)

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
    return data


#####################
##### SMA 5, 8  #####
#####################

# Define the tickers and time period to retrieve data for
ticker = 'AAPL'

# Retrieve the data using yfinance
data = yf.download(ticker, period='5y', interval='1d')

# Calculate the df['SMA_5'] and df['SMA_8']
data = __SMA ( data, 5 )
data = __SMA ( data, 8 )

# SMA5, SMA8 crossover
if data.iloc[-1]['SMA_5'] > data.iloc[-1]['SMA_8'] and data.iloc[-2]['SMA_5'] < data.iloc[-2]['SMA_8']:
    print('BUY :: SMA_5 crossed above SMA_8')

# SMA_5, SMA_8 crossunder
if data.iloc[-1]['SMA_5'] < data.iloc[-1]['SMA_8'] and data.iloc[-2]['SMA_5'] > data.iloc[-2]['SMA_8']:
    print('SELL :: SMA_5 crossed below SMA_8')

print ( data.tail(5) )

