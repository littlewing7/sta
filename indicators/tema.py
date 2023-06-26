#!/usr/bin/env python3

import argparse

import os,sys
import yfinance as yf
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

#def __TEMA (df, window=30):
from util.tema   import __TEMA


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)
    # Calculate the TEMA
    data = __TEMA (data, 30)

    # Remove the "Adj Close" column and drop any missing values


    # Check if price crosses above/below the TEMA
    close_today     = data['Adj Close'].iloc[-1]
    close_yesterday = data['Adj Close'].iloc[-2]

    tema_30_today     = data['TEMA_30'].iloc[-1]
    tema_30_yesterday = data['TEMA_30'].iloc[-2]


    if close_today > tema_30_today and close_yesterday < tema_30_yesterday:
        print(f"TEMA30 :: STRONG BUY :: {symbol} price crossed above the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")
    elif close_today < tema_30_today and close_yesterday > tema_30_yesterday  :
        print(f"TEMA30 :: STRONG SELL :: {symbol} price crossed below the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")
    else:
        if close_today > tema_30_today:
            print(f"TEMA_30 :: BUY :: {symbol} price closed above the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")
        else:
            print(f"TEMA_30 :: SELL :: {symbol} price closed below the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")

