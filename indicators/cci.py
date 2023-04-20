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

r_data = data.tail(2)
print (r_data)

print ( r_data["CCI_20"][0] )

print ( r_data["CCI_20"][1] )

today_cci     = data['CCI_20'].iloc[-1]
yesterday_cci = data['CCI_20'].iloc[-2]

overbought_level = 100
oversold_level = -100

if data['CCI_CrossOverBought'].iloc[-1] == 1:
    print(f'CCI HOLD :: {ticker} has crossed OverBought level.')
if data['CCI_CrossOverSold'].iloc[-1] == 1:
    print(f'CCI HOLD :: {ticker} has crossed OverSold level.')




if yesterday_cci < overbought_level and today_cci >= overbought_level:
    print(f"SELL CCI has crossed above the overbought level of {overbought_level} with a value of {today_cci}")
elif yesterday_cci > overbought_level and today_cci <= overbought_level:
    print(f"SELL SETRONG :: CCI has crossed below the overbought level of {overbought_level} with a value of {today_cci}")
elif yesterday_cci > oversold_level and today_cci <= oversold_level:
    print(f"CCI has crossed below the oversold level of {oversold_level} with a value of {today_cci}")
elif yesterday_cci < oversold_level and today_cci >= oversold_level:
    print(f"BUY STRONG :: CCI has crossed above the oversold level of {oversold_level} with a value of {today_cci}")



# Print the last 5 rows of the data to check the results
print(data.tail(5))


