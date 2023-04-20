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
from util.roc  import __ROC


# Define the ticker and download the historical data
ticker = 'AAPL'
data = yf.download(ticker, period='5y')
data = data.drop(['Adj Close'], axis=1).dropna()


# Calculate the MOM indicator and print the current value
data = __ROC ( data , 12, 6 )

print ( data.tail(2))


current_roc = data["ROC"].iloc[-1]
current_rocma = data["ROCMA"].iloc[-1]

print("Current ROC value for", ticker, "is:", current_roc)
print("Current ROCMA value for", ticker, "is:", current_rocma)



