#!/usr/bin/env python3

import pandas as pd
import yfinance as yf

def WMA(df, window):
    weights = pd.Series(range(1,window+1))
    wma = df['Close'].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    #df_wma = pd.concat([df['Close'], wma], axis=1)
    #df_wma.columns = ['Close', 'WMA']
    #return df_wma
    df["WMA"] = wma
    return df

# Download stock data
data = yf.download("AAPL", start="2020-01-01", progress=False)

# Calculate WMA with window size of 10
data = WMA(data, 10)

# Print first 10 rows of updated dataframe
print ( data.tail(10) )

