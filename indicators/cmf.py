#!/usr/bin/env python3

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

#def __EMA (df, window=14):
from util.cmf   import __CMF


# Download historical data for the past 5 years
symbol = 'AAPL'
tickerDf = yf.download(symbol, period='5y')

# Calculate the CMO indicator using the function
tickerDf = __CMF (tickerDf, period=14)

# Print the DataFrame with the CMO column added
print(tickerDf)

