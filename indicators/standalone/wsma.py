#!/usr/bin/env python3

import pandas as pd
import numpy as np

import yfinance as yf

def __WSMA( data, n):
    # sma = data.rolling(window=n).mean()
    # ema = data.ewm(span=n, adjust=False).mean()
    weights = np.arange(1, n+1)
    wma = data['Close'].rolling(n).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
    data['WSMA_{}'.format(n)] = pd.Series(wma)

    return data


# Download stock data
data = yf.download("AAPL", start="2020-01-01", progress=False)

window = 20

data = __WSMA ( data, window )

# Print first 10 rows of updated dataframe
print ( data.tail(3) )

