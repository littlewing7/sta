#Chaikin Oscillator
def Chaikin(df):
    ad = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    Chaikin = pd.Series(ad.ewm(ignore_na=False, adjust=True, span=3, min_periods=2).mean() - ad.ewm(ignore_na=False, adjust=True, span=10, min_periods=9).mean(), name = 'Chaikin')
    df = df.join(Chaikin)
    return df

