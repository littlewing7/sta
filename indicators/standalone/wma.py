#!/usr/bin/env python3

import argparse

import pandas as pd
import yfinance as yf

def WMA(df, window):
    weights = pd.Series(range(1,window+1))
    wma = df['Adj Close'].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    #df_wma = pd.concat([df['Adj Close'], wma], axis=1)
    #df_wma.columns = ['Close', 'WMA']
    #return df_wma
    df["WMA"] = wma
    return df

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:

    data = yf.download ( symbol, start=start_date, progress=False)
    # Calculate WMA with window size of 10
    data = WMA(data, 10)
    print ( data.tail(10) )

