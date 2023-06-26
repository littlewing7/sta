#!/usr/bin/env python3

import argparse

import os,sys
import yfinance as yf
import pandas as pd
pd.set_option('display.precision', 2)

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Adj Close'].rolling(window=n).mean()
    return data


#####################
##### SMA 5, 8  #####
#####################

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)

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

