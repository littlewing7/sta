#!/usr/bin/env python3

import yfinance as yf
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)


########################
#####  PANDAS SMA  #####
########################
#def SMA ( close, t ):
#    import talib
#    return talib.SMA( close, t)
# https://github.com/Priyanshu154/Backtest/blob/511e2e8525b23a14ecdf5a48c28399c7fd41eb14/Backtest/Backtest/Indicator.py
def __SMA(close, t):
    mas = []
    for i in range(t - 1):
        mas.append(-1)
    for i in range(len(close) - t + 1):
        summ = 0
        for j in range(i, t + i):
            summ = summ + close[j]
        meann = summ / t
        mas.append(meann)
    return mas
#SMA Ends here

#def calculate_bollinger_bands(data, window=20):
#    rolling_mean = data['Close'].rolling(window=window).mean()
#    rolling_std = data['Close'].rolling(window=window).std()
#    upper_band = rolling_mean + 2 * rolling_std
#    lower_band = rolling_mean - 2 * rolling_std
#    return rolling_mean, upper_band, lower_band

####################################
#####  PANDAS BOLLINGER BANDS  #####
####################################
def __BB (data, window=20):
    std = data['Close'].rolling(window).std()
    upper_bb  = __SMA(data['Close'], window) + std * 2
    lower_bb  = __SMA(data['Close'], window) - std * 2
    middle_bb = __SMA(data['Close'], window)
    return upper_bb, lower_bb, middle_bb



# Ticker symbol of the stock to analyze
ticker_symbol = 'AAPL'

# Get the stock data for the past 5 years
stock_data = yf.download(ticker_symbol, period='5y')

# Remove the 'Adj Close' column from the dataframe
stock_data.drop('Adj Close', axis=1, inplace=True)

# Calculate the Bollinger Bands for the stock data
upper_band, lower_band, middle_band = __BB (stock_data)

# Add Bollinger Bands columns to the dataframe with prefix "BB_"
#stock_data['BB_middle'] = middle_band
stock_data['BB_upper'] = upper_band
stock_data['BB_lower'] = lower_band

# keep 2 decimals
stock_data['BB_upper'] = stock_data['BB_upper'].apply(lambda x: float("{:.2f}".format(x)))
stock_data['BB_lower'] = stock_data['BB_lower'].apply(lambda x: float("{:.2f}".format(x)))

# Calculate the cross over and cross under values
cross_over  = np.where ( stock_data['Close'] > stock_data['BB_upper'], 1, 0 )
cross_under = np.where ( stock_data['Close'] < stock_data['BB_lower'], 1, 0 )

# Add cross over and cross under columns to the dataframe
stock_data['BB_Cross_Over']  = cross_over
stock_data['BB_Cross_Under'] = cross_under


# Print the dataframe
print(stock_data.tail (5) )

# Check for the crossunder and crossover conditions
if stock_data['BB_Cross_Over'].iloc[-1] == 1:
    print("BB [SELL] Stock has crossed over bolinger band on the upside")
elif stock_data['BB_Cross_Under'].iloc[-1] == 1:
    print("BB [BUY] Stock has crossed under bolinger band on the downside")
else:
    print("No conditions are met")

