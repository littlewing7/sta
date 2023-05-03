#!/usr/bin/env python3

import os,sys

import yfinance as yf
import numpy as np
import pandas as pd

pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")

# def __WILLR (high, low, close, period):
from util.uo   import __UO


symbol = 'AAPL'

# Read data 
data = yf.download(symbol,start='2020-01-01')
data = __UO ( data )


print ( data.tail(3) )

