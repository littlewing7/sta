data = __SMA ( data, 5 )

data = __EMA ( data, 144 )
data = __EMA ( data, 169 )

#data['EMA_144'] = data['Adj Close'].ewm(span=144, min_periods=144, adjust=False).mean()
#data['EMA_169'] = data['Adj Close'].ewm(span=169, min_periods=169, adjust=False).mean()
#data['SMA_5'] = data['Adj Close'].rolling(window=5).mean()


close   = data['Adj Close']
ema_144 = data['EMA_144']
ema_169 = data['EMA_169']
sma_5   = data['SMA_5']

# BUY CRITERIA: closing price is above SMA and 144-period EMA is above 169-period EMA
if (close.iloc[-1] > sma_5.iloc[-1]) and (ema_144.iloc[-1] > ema_169.iloc[-1] ):
    print_log ( 'ema_144_169_sma_5.py', 'LONG', [ 'EMA_144', 'EMA_169', 'SMA_5' ] )

# SELL CRITERIA: if closing price is below SMA and 169-period EMA is above 144-period EMA
if (close.iloc[-1] < sma_5.iloc[-1]) and (ema_169.iloc[-1] > ema_144.iloc[-1] ):
    print_log ( 'ema_144_169_sma_5.py', 'SHORT', [ 'EMA_144', 'EMA_169', 'SMA_5' ] )

