#!/usr/bin/env python3

import argparse

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

def __ROC (df, n=12, m=6):
    df['ROC']   = ( df["Adj Close"] - df["Adj Close"].shift(n))/df["Adj Close"].shift(n) * 100
    df['ROCMA'] = df["ROC"].rolling(m).mean()
    return df


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)

    # Calculate the KDJ indicator using the function
    data = __ROC (data)

    # Print the data
    print(data.tail(10))

