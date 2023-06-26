#!/usr/bin/env python3

import argparse

import os,sys
import yfinance as yf
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")

from util.kc   import __KC


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)
    # Calculate the Keltner Channels using the function
    kc_df = __KC ( data )


    # Loop through each row in the DataFrame and check if the Close price touches the Upper or Lower Keltner Channel
    #for i, row in kc_df.iterrows():
    #    if df['Adj Close'][i] >= row['KC Upper']:
    #        print("Price touched the Upper Keltner Channel on", i.date())
    #    elif df['Adj Close'][i] <= row['KC Lower']:
    #        print("Price touched the Lower Keltner Channel on", i.date())

    # Check yesterday's close price and send a BUY or SELL message if it touches the KC Upper or Lower band
    yesterday_close = df.iloc[-2]['Close']
    if kc_df.iloc[-2]['KC_lower'] * 1.01 <= yesterday_close < kc_df.iloc[-1]['KC_lower'] and df.iloc[-1]['Close'] > yesterday_close:
        print("BUY message")
    elif kc_df.iloc[-2]['KC_upper'] * 0.99 >= yesterday_close > kc_df.iloc[-1]['KC_upper'] and df.iloc[-1]['Close'] < yesterday_close:
        print("SELL message")

    print (kc_df.tail (5) )
