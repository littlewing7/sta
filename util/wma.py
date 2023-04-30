##################################################
#####  PANDAS  Weighted Moving Average(WMA)  #####
##################################################
import pandas as pd
import numpy as np

"""
#def wma(src, length):
#    import talib
#    return talib.WMA(src, length)
#
# https://github.com/Priyanshu154/Backtest/blob/511e2e8525b23a14ecdf5a48c28399c7fd41eb14/Backtest/Backtest/Indicator.py
# Reference for code is taken from tradingview

def WMA(data, n):

    ws = np.zeros(data.shape[0])
    t_sum = sum(range(1, n+1))

    for i in range(n-1, data.shape[0]):
        ws[i] = sum(data[i-n+1 : i+1] * np.linspace(1, n, n))/ t_sum

    return ws
df['WMA'] = WMA(df['Close'], 5)
"""

def __WMA(close, t):
    wma = []
    for i in range(t - 1):
        wma.append(-1)
    for i in range(t-1, len(close)):
        norm = 0.0
        summ = 0.0
        for j in range(0, t):
            weight = (t-j)*t
            norm = norm + weight
            summ = summ + (close[i-j]*weight)
        wma.append(summ/norm)
    return wma
# WMA Ends Here


#  WMA and Double WMA
def WMA(df, window):
    weights = pd.Series(range(1,window+1))
    wma = df['Close'].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    #df_wma = pd.concat([df['Close'], wma], axis=1)
    #df_wma.columns = ['Close', 'WMA']
    #return df_wma
    df['WMA_{}'.format(window)] = wma
    df['DWMA_{}'.format(window)] = df['WMA_{}'.format(window)].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    return df

