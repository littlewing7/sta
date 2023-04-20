#!/usr/bin/env python3

##################
#####  PSAR  #####
##################

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
from util.psar  import __PSAR

# Define the stock symbol and timeframe
symbol = "AAPL"

data = yf.download(symbol, period="5y")

# Calculate the PSAR indicator and print the current value
data = __PSAR ( data )

print ( data.tail(2))


