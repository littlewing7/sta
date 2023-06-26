#!/usr/bin/env python3

import argparse

import os,sys

import yfinance as yf
import numpy as np
import pandas as pd

pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")

# def __WILLR (high, low, close, period):
from util.wr   import __WR


# Calculate Williams %R and add prefix to column names
wr_period = 20
wr_upper_level = -20
wr_lower_level = -80

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)

    data = __WR ( data, wr_period )

    wr_today     = data["WR_20"].iloc[-1]
    wr_yesterday = data["WR_20"].iloc[-2]


    if wr_today <= wr_lower_level:
        print(f"Lower oversold level: {wr_today:.2f}")
    elif wr_today >= wr_upper_level:
        print(f"Upper overbought level: {wr_today:.2f}")
    elif wr_yesterday > wr_upper_level and wr_today < wr_upper_level:
        print(f"Upper overbought level breached from above going down today: {wr_today:.2f}")
    elif wr_yesterday < wr_lower_level and wr_today > wr_lower_level:
        print(f"W%R indicator crossed over from below the lower level today: {wr_today:.2f}")

    print ( data.tail (5) )
