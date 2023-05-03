#!/usr/bin/env python3

#######################
#####  ATR BANDS  #####
#######################

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
from util.mom  import __MOM


# Define the ticker and download the historical data
ticker = 'AAPL'
data = yf.download(ticker, start='2020-01-01', progress=False)
data = data.drop(['Adj Close'], axis=1).dropna()

window_mom = 14


# Calculate the MOM indicator and print the current value
data = __MOM ( data , window_mom )
current_mom = data["MOM_14"].iloc[-1]

print("Current MOM value for", ticker, "is:", current_mom)


