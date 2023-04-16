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

#def __TEMA (df, window=30):
from util.tema   import __TEMA


# Set the stock ticker and timeframe
ticker = "AAPL"

# Download the stock data
data = yf.download(ticker, period="5y")

# Calculate the TEMA
#data['TEMA_30'] = __TEMA (data, 30)
data = __TEMA (data, 30)

# Remove the "Adj Close" column and drop any missing values
data = data.drop(columns=['Adj Close']).dropna()


# Check if price crosses above/below the TEMA
close_today     = data['Close'].iloc[-1]
close_yesterday = data['Close'].iloc[-2]

tema_30_today     = data['TEMA_30'].iloc[-1]
tema_30_yesterday = data['TEMA_30'].iloc[-2]


if close_today > tema_30_today and close_yesterday < tema_30_yesterday:
    print(f"TEMA30 :: STRONG BUY :: {ticker} price crossed above the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")
elif close_today < tema_30_today and close_yesterday > tema_30_yesterday  :
    print(f"TEMA30 :: STRONG SELL :: {ticker} price crossed below the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")
else:
    if close_today > tema_30_today:
        print(f"TEMA_30 :: BUY :: {ticker} price closed above the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")
    else:
        print(f"TEMA_30 :: SELL :: {ticker} price closed below the TEMA on {data.index[-1].strftime('%Y-%m-%d')}")

