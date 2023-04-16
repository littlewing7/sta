#!/usr/bin/env python3

import yfinance as yf
import pandas as pd

#########################
#####  PANDAS TEMA  #####
#########################
#def TEMA ( close, t):
#    import talib
#    return talib.TEMA(close, timeperiod=t)
def __TEMA(data, n=30):
    """
    Triple Exponential Moving Average (TEMA)
    """
    ema1 = data['Close'].ewm(span=n, adjust=False).mean()
    ema2 = ema1.ewm(span=n, adjust=False).mean()
    ema3 = ema2.ewm(span=n, adjust=False).mean()
    tema = 3 * (ema1 - ema2) + ema3
    return tema

# Set the stock ticker and timeframe
ticker = "AAPL"
start_date = pd.Timestamp.today() - pd.DateOffset(years=5)

# Download the stock data
df = yf.download(ticker, start=start_date)

# Calculate the TEMA
df['TEMA'] = __TEMA (df, 30)

# Remove the "Adj Close" column and drop any missing values
df = df.drop(columns=['Adj Close']).dropna()

# Check if price crosses above/below the TEMA
today_close = df['Close'].iloc[-1]
yesterday_close = df['Close'].iloc[-2]

today_tema = df['TEMA'].iloc[-1]
yesterday_tema = df['TEMA'].iloc[-2]


if yesterday_close < yesterday_tema and today_close > today_tema:
    print(f"{ticker} price crossed above the TEMA on {df.index[-1].strftime('%Y-%m-%d')}")
elif yesterday_close > yesterday_tema and today_close < today_tema:
    print(f"{ticker} price crossed below the TEMA on {df.index[-1].strftime('%Y-%m-%d')}")
else:
    if today_close > today_tema:
        print(f"{ticker} price closed above the TEMA on {df.index[-1].strftime('%Y-%m-%d')}")
    else:
        print(f"{ticker} price closed below the TEMA on {df.index[-1].strftime('%Y-%m-%d')}")

