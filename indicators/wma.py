#!/usr/bin/env python3

import argparse

import pandas as pd
import yfinance as yf

def WMA(df, window):
    weights = pd.Series(range(1,window+1))
    wma = df['Close'].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    #df_wma = pd.concat([df['Close'], wma], axis=1)
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
    window = 14

    # Calculate Double WMA with window size of 10
    data = WMA(data, window)

    # Print first 10 rows of updated dataframe
    print ( data.tail(3) )

