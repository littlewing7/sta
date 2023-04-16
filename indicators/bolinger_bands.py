#!/usr/bin/env python3

import os,sys
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

# def __SMA ( df['Close'], 21 )
from util.sma   import __SMA

#def __BB (df, window=20):
from util.bolinger_bands   import __BB


##################
#####  MAIN  #####
##################
# Ticker symbol of the stock to analyze
ticker_symbol = 'AAPL'

# Get the stock data for the past 5 years
stock_data = yf.download(ticker_symbol, period='5y')

# Remove the 'Adj Close' column from the dataframe
stock_data.drop('Adj Close', axis=1, inplace=True)

bb_window = 20

# Calculate the Bollinger Bands for the stock data
stock_data = __BB (stock_data, bb_window)


# keep 2 decimals
#stock_data['BB_upper'] = stock_data['BB_upper'].apply(lambda x: float("{:.2f}".format(x)))
#stock_data['BB_lower'] = stock_data['BB_lower'].apply(lambda x: float("{:.2f}".format(x)))

# Calculate the cross over and cross under values
bb_cross_over  = np.where ( stock_data['Close'] > stock_data['BB_upper'], 1, 0 )
bb_cross_under = np.where ( stock_data['Close'] < stock_data['BB_lower'], 1, 0 )

# Add cross over and cross under columns to the dataframe
#stock_data['BB_Cross_Over']  = bb_cross_over
#stock_data['BB_Cross_Under'] = bb_cross_under


# Print the dataframe
print(stock_data.tail (60) )

# Check for the crossunder and crossover conditions
if stock_data['BB_Cross_Over'].iloc[-1] == 1:
    print("BB [SELL] Stock has crossed over bolinger band on the upside")
elif stock_data['BB_Cross_Under'].iloc[-1] == 1:
    print("BB [BUY] Stock has crossed under bolinger band on the downside")
else:
    print("No conditions are met")

stock_data.plot(y=['Close', 'BB_upper', 'BB_middle', 'BB_lower'])
plt.title('Apple Close Prices & Bollinger Bands BB(20,2)')
plt.legend(loc='upper left')
plt.show()

