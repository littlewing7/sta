import pandas as pd
import numpy as np

# def __RSI ( df, 14 )
from util.rsi   import __RSI

#def stoch_rsi(rsi, d_window=3, k_window=3, window=14):
#    """
#    Computes the stochastic RSI. Default values are d=3, k=3, window=14.
#    """
#    minrsi = rsi.rolling(window=window, center=False).min()
#    maxrsi = rsi.rolling(window=window, center=False).max()
#    stoch = ((rsi - minrsi) / (maxrsi - minrsi)) * 100
#    K = stoch.rolling(window=k_window, center=False).mean()
#    D = K.rolling(window=d_window, center=False).mean()
#    return K, D

#def stoch_rsi(data_frame):
#    min_price = data_frame['low'].rolling(window = 14).min()
#    max_price = data_frame['high'].rolling(window = 14).max()
#    
#    ma_up = data_frame['close'] - min_price
#    ma_down = max_price - min_price
#    
#    data_frame['stoch_rsi'] = ma_up / ma_down
#    data_frame['stoch_rsi'] = 100 * data_frame['stoch_rsi']
#    data_frame['stoch_rsi_sma'] = data_frame['stoch_rsi'].rolling(window = 3).mean() 


def __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3):
    # RSI
    data = __RSI ( data, period)

    # Stochastic RSI
    stochrsi  = (data['RSI_14'] - data['RSI_14'].rolling(period).min()) / (data['RSI_14'].rolling(period).max() - data['RSI_14'].rolling(period).min())
    data['SRSI_K'] = stochrsi.rolling(SmoothK).mean() * 100
    data['SRSI_D'] = data['SRSI_K'].rolling(SmoothD).mean()
    return data


