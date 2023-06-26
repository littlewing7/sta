#!/usr/bin/env python3

import argparse

import yfinance as yf
import pandas as pd

def __TEMA(data, n=30):
    """
    Triple Exponential Moving Average (TEMA)
    """
    ema1 = data['Adj Close'].ewm(span=n, adjust=False).mean()
    ema2 = ema1.ewm(span=n, adjust=False).mean()
    ema3 = ema2.ewm(span=n, adjust=False).mean()
    tema = 3 * (ema1 - ema2) + ema3
    data['TEMA_{}'.format(n)] = tema
    return data


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)
    data = __TEMA ( data, 30 )

    # Check if price crosses above/below the TEMA
    today_close = data['Adj Close'].iloc[-1]
    yesterday_close = data['Adj Close'].iloc[-2]

    today_tema = data['TEMA_30'].iloc[-1]
    yesterday_tema = data['TEMA_30'].iloc[-2]


    if yesterday_close < yesterday_tema and today_close > today_tema:
        print(f"{symbol} price crossed above the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")
    elif yesterday_close > yesterday_tema and today_close < today_tema:
        print(f"{symbol} price crossed below the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")
    else:
        if today_close > today_tema:
            print(f"{symbol} price closed above the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")
        else:
            print(f"{symbol} price closed below the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")

