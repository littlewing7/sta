import pandas as pd
import numpy as np

#def cci(data, ndays):
#    TP = (data['High'] + data['Low'] + data['Close']) / 3
#    CCI = pd.Series((TP - TP.rolling(ndays).mean()) / (0.015 * TP.rolling(ndays).std()), name = 'CCI')
#    return CCI
#def calculate_levels(data, ndays):
#    data['CCI'] = cci(data, ndays)
#    data['CCI_Overbought'] = np.where(data['CCI'] > 100, 1, 0)
#    data['CCI_Oversold'] = np.where(data['CCI'] < -100, 1, 0)
#    data['CCI_CrossOver'] = np.where((data['CCI'] > 0) & (data['CCI'].shift(1) < 0), 1, 0)
#    data['CCI_CrossUnder'] = np.where((data['CCI'] < 0) & (data['CCI'].shift(1) > 0), 1, 0)
#    return data

#def calculate_cci(df, window=20):
#    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
#    mean_deviation = np.abs(typical_price - typical_price.rolling(window=window).mean()).rolling(window=window).mean()
#    cci = (typical_price - typical_price.rolling(window=window).mean()) / (0.015 * mean_deviation)
#    return cci

##Commodity Channel Index
#def CCI(df, n):
#    PP = (df['high'] + df['low'] + df['close']) / 3
#
#    CCI = pd.Series((PP - PP.rolling(center=False, window=n).mean()) / PP.rolling(center=False, window=n).mean(), name = 'CCI_' + str(n))
#    df = df.join(CCI)
#    return df

def __CCI(df, ndays = 20):
    df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['sma'] = df['TP'].rolling(ndays).mean()
    df['mad'] = df['TP'].rolling(ndays).apply(lambda x: pd.Series(x).mad())

    df['CCI_{}'.format(ndays)] = (df['TP'] - df['sma']) / (0.015 * df['mad'])

    df['CCI_CrossOverBought'] = np.where ( ( df['CCI_20'].shift(1) < 100)  & ( df['CCI_20'] >= 100),  1, 0 )
    df['CCI_CrossOverSold']   = np.where ( ( df['CCI_20'].shift(1) > -100) & ( df['CCI_20'] <= -100), 1, 0 )

    # 2 = LONG, -2 = SHORT
    #df['CCI_Signal'] = np.select(
    #    [ ( df['CCI_20'] > -100 ) & ( df['CCI_20'].shift(1) < -100 ),
    #      ( df['CCI_20'] <  100)  & ( df['CCI_20'].shift(1) >  100 ) ],
    #    [2, -2])


    df = df.drop('TP', axis=1)
    df = df.drop('sma', axis=1)
    df = df.drop('mad', axis=1)

    return df
