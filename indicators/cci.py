#!/usr/bin/env python3

import os,sys
import yfinance as yf
import pandas as pd
import numpy as np

pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

#def __CCI (df, window=20):
from util.cci   import __CCI


# Define the ticker for the data
ticker = 'AAPL'

# Download all available historical stock price data from Yahoo Finance
data = yf.download(ticker, period="5y")
data = data.drop(['Adj Close'], axis=1).dropna()


# Calculate the CCI and levels
data = __CCI (data, 20)
#data["CCI_prev"] = data["CCI"].shift(1)


today_cci     = data['CCI_20'].iloc[-1]
yesterday_cci = data['CCI_20'].iloc[-2]

overbought_level = 100
oversold_level = -100

if data['CCI_CrossOverBought'].iloc[-1] == 1:
    print(f'CCI HOLD :: {ticker} has crossed OverBought level.')
if data['CCI_CrossOverSold'].iloc[-1] == 1:
    print(f'CCI HOLD :: {ticker} has crossed OverSold level.')


#if ( today_cci > yesterday_cci ) and ( today_cci > 100 ) and ( yesterday_cci > 100 ):
#    print(f'CCI SELL :: {ticker} is continuing to be OverBought')
#if ( today_cci < yesterday_cci ) and ( today_cci < -100 ) and ( yesterday_cci < -100 ):
#    print(f'CCI BUY :: {ticker} is continuing to be OverSold')
#
#if ( today_cci < yesterday_cci ) and ( today_cci < 100 ) and (yesterday_cci > 100 ):
#    print(f'CCI STRONG SELL :: {ticker} is going down!')
#if ( today_cci > yesterday_cci ) and ( today_cci > -100 ) and ( yesterday_cci < -100 ):
#    print(f'CCI STRONG BUY :: {ticker} is going UP!')




if yesterday_cci < overbought_level and today_cci >= overbought_level:
    print(f"SELL CCI has crossed above the overbought level of {overbought_level} with a value of {today_cci}")
elif yesterday_cci > overbought_level and today_cci <= overbought_level:
    print(f"SELL SETRONG :: CCI has crossed below the overbought level of {overbought_level} with a value of {today_cci}")
elif yesterday_cci > oversold_level and today_cci <= oversold_level:
    print(f"CCI has crossed below the oversold level of {oversold_level} with a value of {today_cci}")
elif yesterday_cci < oversold_level and today_cci >= oversold_level:
    print(f"BUY STRONG :: CCI has crossed above the oversold level of {oversold_level} with a value of {today_cci}")


## Define the overbought and oversold levels
#overbought = 100
#oversold = -100
#CCI = __CCI(data, 20)
#if CCI[-1] > overbought and CCI[-2] <= overbought:
#    print('CCI crossed above overbought level on', CCI.index[-1])
#elif CCI[-1] < overbought and CCI[-2] >= overbought:
#    print('CCI crossed below overbought level on', CCI.index[-1])
#elif CCI[-1] < oversold and CCI[-2] >= oversold:
#    print('CCI crossed below oversold level on', CCI.index[-1])
#elif CCI[-1] > oversold and CCI[-2] <= oversold:
#    print('CCI crossed above oversold level on', CCI.index[-1])


# Print the last 5 rows of the data to check the results
print(data.tail(5))

