#!/usr/bin/env python3

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def __MFI ( data, window=14):
    # Calculate the Money Flow Index (MFI)
    typical_price = ( data['High'] + data['Low'] + data['Close']) / 3
    money_flow = typical_price * data['Volume']
    positive_money_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_money_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    money_ratio = positive_money_flow.rolling(window=window).sum() / negative_money_flow.rolling(window=window).sum()
    mfi = 100 - (100 / (1 + money_ratio))

    data["MFI"] = mfi
    return data

# Set the ticker symbol and the date range
symbol = "AAPL"

# Retrieve the historical data for the ticker
ticker_data = yf.download(symbol, period="5y")
ticker_data = __MFI ( ticker_data, window=14 )
print ( ticker_data.tail (5) )

# Plot the MFI indicator
plt.figure(figsize=(10,5))
plt.plot(ticker_data.index, ticker_data["MFI"], label='MFI')
plt.title(symbol + ' MFI')
plt.legend()
plt.show()

