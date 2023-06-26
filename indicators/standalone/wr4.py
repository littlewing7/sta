#!/usr/bin/env python3

import argparse

import yfinance as yf
import pandas as pd

def download_data(ticker, period):
    data = yf.download(ticker, period=period)
    return data

def calculate_wr(high, low, close, window=20):
    wr = (high.rolling(window=window).max() - close) / (high.rolling(window=window).max() - low.rolling(window=window).min()) * -100
    return wr

def __WR (high, low, close, t=20):
    highh = high.rolling(t).max()
    lowl = low.rolling(t).min()
    wr = -100 * ((highh - close) / (highh - lowl))
    return wr

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)

    wr = __WR(data['High'], data['Low'], data['Adj Close'], t=20)

    upper_level = -20
    lower_level = -80

    today_wr = wr.iloc[-1]
    yesterday_wr = wr.iloc[-2]


    if today_wr <= lower_level:
        print(f"Lower oversold level: {today_wr:.2f}")
    elif today_wr >= upper_level:
        print(f"Upper overbought level: {today_wr:.2f}")
    elif yesterday_wr > upper_level and today_wr < upper_level:
        print(f"Upper overbought level breached from above going down today: {today_wr:.2f}")
    elif yesterday_wr < lower_level and today_wr > lower_level:
        print(f"W%R indicator crossed over from below the lower level today: {today_wr:.2f}")

