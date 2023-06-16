import pandas as pd
import numpy as np

##Keltner Channel
#def KELCH(df, n):
#    KelChM = pd.Series(pd.rolling_mean((df['high'] + df['low'] + df['close']) / 3, n), name = 'KelChM_' + str(n))
#    KelChU = pd.Series(pd.rolling_mean((4 * df['high'] - 2 * df['low'] + df['close']) / 3, n), name = 'KelChU_' + str(n))
#    KelChD = pd.Series(pd.rolling_mean((-2 * df['high'] + 4 * df['low'] + df['close']) / 3, n), name = 'KelChD_' + str(n))
#    df = df.join(KelChM)
#    df = df.join(KelChU)
#    df = df.join(KelChD)
#    return df

def __KC(dataframe, period=20, multiplier=2):
    """
    Calculates the Keltner Channels for a given DataFrame.

    Parameters:
    dataframe (pd.DataFrame): DataFrame containing the OHLC data of the asset.
    period (int): Period to calculate the Keltner Channels (default: 20).
    multiplier (float): Multiplier for the Average True Range (ATR) (default: 2).

    Returns:
    pd.DataFrame: A new DataFrame containing the Keltner Channels for the given OHLC data.
    """

    atr_lookback = 10

    tr = pd.DataFrame()
    tr['h_l'] = dataframe['High'] - dataframe['Low']
    tr['h_pc'] = abs(dataframe['High'] - dataframe['Adj Close'].shift())
    tr['l_pc'] = abs(dataframe['Low'] - dataframe['Adj Close'].shift())
    tr['tr'] = tr[['h_l', 'h_pc', 'l_pc']].max(axis=1)

    atr = tr['tr'].rolling(atr_lookback).mean()
    #atr = tr['tr'].ewm(alpha = 1/atr_lookback).mean()

    kc_middle = dataframe['Adj Close'].rolling(period).mean()
    kc_upper = kc_middle + multiplier * atr
    kc_lower = kc_middle - multiplier * atr

    dataframe['KC_upper'] = kc_upper
    dataframe['KC_middle'] = kc_middle
    dataframe['KC_lower'] = kc_lower

    return dataframe

"""
def __KC2 ( data, period=20, multiplier=2 ):

    atr_lookback = 10

    tr1 = data['High'] - data['Low']
    tr2 = abs(data['High'] - data['Close'].shift())
    tr3 = abs(data['Low'] - data['Close'].shift())

    frames = [tr1, tr2, tr3]

    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)

    atr = tr.ewm(alpha = 1/atr_lookback).mean()

    kc_middle = data['Close'].ewm(period).mean()
    kc_upper = data['Close'].ewm(period).mean() + multiplier * atr
    kc_lower = data['Close'].ewm(period).mean() - multiplier * atr

    data['KC_upper'] = kc_upper
    data['KC_middle'] = kc_middle
    data['KC_lower'] = kc_lower
    return data

"""
