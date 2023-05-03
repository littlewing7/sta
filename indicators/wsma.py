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
from util.wsma   import __WSMA



# Download stock data
data = yf.download("AAPL", start="2020-01-01", progress=False)

window = 20

data = __WSMA ( data, window )

# Print first 10 rows of updated dataframe
print ( data.tail(3) )

