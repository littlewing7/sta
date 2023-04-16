#####  EMA  #####
#def EMA(close, t):
#    import numpy as np
#    import talib
#    return talib.EMA ( np.array(close), t)
def __EMA ( data, n=9 ):
    #ema = data['Close'].ewm(span = period ,adjust = False).mean()
    #return ( ema )

    data['EMA_{}'.format(n)] = data['Close'].ewm(span = n ,adjust = False).mean()
    return data

