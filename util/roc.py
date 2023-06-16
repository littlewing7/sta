########################################
##### PANDAS  Rate Of Change(ROC)  #####
########################################
##def __ROC ( data, t=10):
##  return talib.ROC ( data['Close'], timeperiod=t)
#def __ROC(close, t):
#    roc = []
#    for i in range(t-1):
#        roc.append(-1)
#    for i in range(t-1, len(close)):
#        sum = 100*(close[i]-close[i-t])/close[i-t]
#        roc.append(sum)
#    return roc
## ROC Ends here

import pandas as pd
import numpy as np

#def ROC(df, n):
#    M = df['Close'].diff(n - 1)
#    N = df['Close'].shift(n - 1)
#    ROC = pd.Series(M / N, name = 'ROC_' + str(n))
#    df = df.join(ROC)
#    return df

def __ROC (df, n=12, m=6):
    df['ROC']   = ( df["Adj Close"] - df["Adj Close"].shift(n))/df["Adj Close"].shift(n) * 100
    df['ROCMA'] = df["ROC"].rolling(m).mean()
    return df

