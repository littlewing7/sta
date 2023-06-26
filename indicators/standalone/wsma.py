#!/usr/bin/env python3

import argparse

import pandas as pd
import numpy as np

import yfinance as yf

def __WSMA( data, n):
    # sma = data.rolling(window=n).mean()
    # ema = data.ewm(span=n, adjust=False).mean()
    weights = np.arange(1, n+1)
    wma = data['Adj Close'].rolling(n).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
    data['WSMA_{}'.format(n)] = pd.Series(wma)

    return data


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)
    window = 20
    data = __WSMA ( data, window )
    print ( data.tail(3) )

