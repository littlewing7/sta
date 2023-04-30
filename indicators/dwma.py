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
from util.wma   import WMA


# Download stock data
data = yf.download("AAPL", start="2020-01-01", progress=False)

# Calculate WMA with window size of 10
data = WMA(data, 14)

# Print first 10 rows of updated dataframe
print ( data.tail (3) )

