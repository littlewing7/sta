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

# def STOCHASTIC_RSI ( data, period=14, smoothD=3, SmoothK=3)
from util.stochastic_rsi   import __STOCHASTIC_RSI



# Define the overbought and oversold levels
overbought = 80
oversold = 20

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)

    print (data.tail (5) )

    #rsi = data['RSI']
    data = __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3 )

    #stochrsi  = (data['RSI'] - data['RSI'].rolling(period).min()) / (data['RSI'].rolling(period).max() - data['RSI'].rolling(period).min())
    #data['TV_SRSI_k'] = stochrsi.rolling(SmoothK).mean() * 100
    #data['TV_SRSI_d'] = data['TV_SRSI_k'].rolling(smoothD).mean()

    print (data.tail (5) )
