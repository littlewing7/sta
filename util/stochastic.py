########################
#####  STOCHASTIC  #####
########################

#def calculate_stochastic(df, k, d, slow):
#    low = df['Low'].rolling(window=k).min()
#    high = df['High'].rolling(window=k).max()
#    df['K'] = (df['Close'] - low) / (high - low) * 100
#    df['D'] = df['K'].rolling(window=d).mean()
#    df['Slow'] = df['D'].rolling(window=slow).mean()
#    return df

# https://github.com/Dynami/py-shibumi/blob/master/utils/technical_analysis.py
#Stochastic oscillator %K
#def STOK(df):
#    SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name = 'SO%k')
#    df = df.join(SOk)
#    return df

#Stochastic oscillator %D
#def STO(df, n):
#    SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name = 'SO%k')
#    SOd = pd.Series(pd.ewma(SOk, span = n, min_periods = n - 1), name = 'SO%d_' + str(n))
#    df = df.join(SOd)
#    return df


def __STOCHASTIC (df, k, d):

#     """
#     Fast stochastic calculation
#     %K = (Current Close - Lowest Low)/
#     (Highest High - Lowest Low) * 100
#     %D = 3-day SMA of %K
#
#     Slow stochastic calculation
#     %K = %D of fast stochastic
#     %D = 3-day SMA of %K
#
#     When %K crosses above %D, buy signal
#     When the %K crosses below %D, sell signal
#     """
     temp_df = df.copy()
     # Set minimum low and maximum high of the k stoch
     low_min = temp_df["Low"].rolling(window=k).min()
     high_max = temp_df["High"].rolling(window=k).max()

     # Fast Stochastic
     temp_df['k_fast'] = 100 * (temp_df["Close"] - low_min)/(high_max - low_min)
     temp_df['d_fast'] = temp_df['k_fast'].rolling(window=d).mean()

     # Slow Stochastic
     temp_df['STO_K'] = temp_df["d_fast"]
     temp_df['STO_D'] = temp_df['STO_K'].rolling(window=d).mean()

     temp_df = temp_df.drop(['k_fast'], axis=1)
     temp_df = temp_df.drop(['d_fast'], axis=1)

     #temp_df['Trend_20'] = df['Close'] / df['SMA 20']
     #temp_df['STO_Signal'] = np.select(
     #   [ ( temp_df['Trend_20'] > 1) & ( ( temp_df['STO_D'] > 20 ) & ( temp_df['STO_D'].shift(1) < 20 ) ),
     #     ( temp_df['Trend_20'] < 1) & ( ( temp_df['STO_D'] < 80 ) & ( temp_df['STO_D'].shift(1) > 80 ) ) ],
     #   [2, -2])

     return temp_df

