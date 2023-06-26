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

#def __SMA (df, n=5):
from util.sma   import __SMA

def _crossover(a, b):
    return a[-1] < b[-1] and a[0] > b[0]

def _crossunder(a, b):
    return a[-1] > b[-1] and a[0] < b[0]

#####################
##### SMA 5, 8  #####
#####################

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)

    # Calculate the df['SMA_5'] and df['SMA_8']
    data = __SMA ( data, 5 )
    data = __SMA ( data, 8 )

    r_data = data.tail(2)

    if ( _crossover ( data["SMA_5"], data["SMA_8"] ) ):
        print ("CrossOver\n")

    # SMA5, SMA8 crossover
    if data.iloc[-1]['SMA_5'] > data.iloc[-1]['SMA_8'] and data.iloc[-2]['SMA_5'] < data.iloc[-2]['SMA_8']:
        print('BUY :: SMA_5 crossed above SMA_8')

    # SMA_5, SMA_8 crossunder
    if data.iloc[-1]['SMA_5'] < data.iloc[-1]['SMA_8'] and data.iloc[-2]['SMA_5'] > data.iloc[-2]['SMA_8']:
        print('SELL :: SMA_5 crossed below SMA_8')

    print ( data.tail(5) )

