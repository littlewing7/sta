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

#def __EMA (df, window=9):
from util.ema   import __EMA


# Download historical data for the past 5 years
symbol = 'AAPL'
data = yf.download(symbol, period='5y')

# Calculate EMA 9 and EMA 21
data  = __EMA (data, 9)
data  = __EMA (data, 21)

# Get the most recent two rows of data
recent_data = data.tail(2)

# Check for crossover events
if recent_data['EMA_9'][0] > recent_data['EMA_21'][0] and recent_data['EMA_9'][1] <= recent_data['EMA_21'][1]:
    print(f"Crossover event: {symbol} {recent_data.index[0].date()} EMA_9 crossed over EMA_21")
elif recent_data['EMA_9'][0] < recent_data['EMA_21'][0] and recent_data['EMA_9'][1] >= recent_data['EMA_21'][1]:
    print(f"Crossover event: {symbol} {recent_data.index[0].date()} EMA_9 crossed under EMA_21")

# Check for signal events
if recent_data['Close'][1] > recent_data['Close'][0] and recent_data['EMA_9'][0] > recent_data['EMA_21'][0]:
    print(f"Signal event: {symbol} {recent_data.index[0].date()} Yesterday's close price is below today's close price and 9 EMA is higher than 21 EMA")

