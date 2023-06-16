import pandas as pd
import numpy as np

#def __SMA ( data, n ):
#    data['SMA_{}'.format(n)] = data['Adj Close'].rolling(window=n).mean()
#    return data

def __WSMA( data, n):
    weights = np.arange(1, n+1)
    wma = data['Adj Close'].rolling(n).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
    data['WSMA_{}'.format(n)] = pd.Series(wma)

    return data

