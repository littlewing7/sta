import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import yfinance as yf

def __EMA ( data, n=9 ):
    #ema = data['Close'].ewm(span = period ,adjust = False).mean()
    #return ( ema )

    data['EMA_{}'.format(n)] = data['Close'].ewm(span = n ,adjust = False).mean()
    return data

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
    tr = pd.DataFrame()
    tr['h_l'] = dataframe['High'] - dataframe['Low']
    tr['h_pc'] = abs(dataframe['High'] - dataframe['Close'].shift())
    tr['l_pc'] = abs(dataframe['Low'] - dataframe['Close'].shift())
    tr['tr'] = tr[['h_l', 'h_pc', 'l_pc']].max(axis=1)

    atr = tr['tr'].rolling(period).mean()

    kc_middle = dataframe['Close'].rolling(period).mean()
    kc_upper = kc_middle + multiplier * atr
    kc_lower = kc_middle - multiplier * atr

    dataframe['KC_upper'] = kc_upper
    dataframe['KC_middle'] = kc_middle
    dataframe['KC_lower'] = kc_lower
    return dataframe


# input
symbol = 'AAPL'

# Read data 
data = yf.download(symbol,start='2020-01-01', progress=False)
data = __EMA ( data, 20 )
data = __KC ( data, 20, 2 )


plt.figure ( figsize=(14,7))
plt.plot ( data['Close'])
plt.plot ( data['EMA_20'], label='Middle Line', linestyle='--')
plt.plot ( data['KC_upper'], color='g')
plt.plot ( data['KC_lower'], color='r')
plt.ylabel ('Price')
plt.xlabel ('Date')
plt.title (symbol + ' Closing Price of Keltners Channels')
plt.legend (loc='best')
plt.show()


