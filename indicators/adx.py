#!/usr/bin/env python3

#######################
#####  ATR BANDS  #####
#######################
import argparse

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################
from util.adx        import __ADX

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:
    data = yf.download ( symbol, start=start_date)
    #data = data.drop(['Adj Close'], axis=1).dropna()

    data = __ADX ( data, 14 )

    print ( data.tail(5) )



