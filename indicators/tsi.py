#!/usr/bin/env python3

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd

pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")

# def __TSI ( df, 25, 13, 12 )
from util.tsi   import __TSI


ticker = 'AAPL'
data = yf.download(ticker, period='5y')
data = data.drop(['Adj Close'], axis=1).dropna()

data = __TSI ( data, 25, 13, 12)
print ( data.tail(2) )



