#!/usr/bin/env python3

import pandas as pd
import yfinance as yf
import numpy as np

"""
def __RSI ( data, window):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI___{}'.format(window)] = rsi
    return data
"""

# https://github.com/lukaszbinden/rsi_tradingview/blob/main/rsi.py
def __RSI ( data: pd.DataFrame, window: int = 14, round_rsi: bool = True):
    """ Implements the RSI indicator as defined by TradingView on March 15, 2021.
        The TradingView code is as follows:
        //@version=4
        study(title="Relative Strength Index", shorttitle="RSI", format=format.price, precision=2, resolution="")
        len = input(14, minval=1, title="Length")
        src = input(close, "Source", type = input.source)
        up = rma(max(change(src), 0), len)
        down = rma(-min(change(src), 0), len)
        rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
        plot(rsi, "RSI", color=#8E1599)
        band1 = hline(70, "Upper Band", color=#C0C0C0)
        band0 = hline(30, "Lower Band", color=#C0C0C0)
        fill(band1, band0, color=#9915FF, transp=90, title="Background")
    :param data:
    :param window:
    :param round_rsi:
    :return: an array with the RSI indicator values
    """

    delta = data["Close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm ( up, alpha =1 / window ).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha = 1 / window ).mean()

    rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

    if ( round_rsi ):
        data['RSI_{}'.format ( window )] = np.round (rsi, 2)
    else:
        data['RSI_{}'.format( window )] = rsi

    return data

symbol = "AAPL"

# Fetch stock data from Yahoo Finance API
stock_data = yf.download(symbol, period="5y")

# Calculate RSI using a window of 14 days
rsi_window = 14
stock_data = __RSI ( stock_data, rsi_window )

data['RSI_Crossover']  = np.where ( ( ( data['RSI_14'].shift(1) < 30 ) & ( data['RSI_14'] > 30 ) ), 1, 0 )
data['RSI_Crossunder'] = np.where ( ( ( data['RSI_14'].shift(1) > 70 ) & ( data['RSI_14'] < 70 ) ), 1, 0 )

# Output the results
print(stock_data.tail())

if data['RSI_Crossover'].iloc[-1] == 1:
    print("RSI :: SELL :: Stock has crossed over")
elif data['RSI_Crossunder'].iloc[-1] == 1:
    print("RSI :: SELL :: Stock has crossed under")
else:
    print("No conditions are met")

