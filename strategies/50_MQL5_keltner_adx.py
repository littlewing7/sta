#KeltnerAdx
'''
@author: Caitlin
This strategy combines Keltner Channels with ADX. Buy signals are given when at least 3 candles
are at or below the low band, and oversold conditions are confirmed by an adx reading of at least 25.
Sell signals are given when at least 3 candles are at or above the high band, and overbought conditions are
confirmed by an adx reading of at least 20.
'''

data = __KC ( data )
data = __ADX ( data, 14 )

# BUY SIGNAL: adx is >= 25 and at least 3 candles are less than or touch the lower keltner band
if ( ( data['High'][-1] <= data['KC_lower'][-1] )
    & (data['High'][-2] <= data['KC_lower'][-2] )
    & (data['High'][-3] <= data['KC_lower'][-3] ) & ( data['ADX_14'][-1] >= 20) ):
    print ("LONG ::: 50_MQL5_keltner_adx\n")

# SELL SIGNAL: adx is >=25 and at least 3 candles are greater than or touch the upper keltner band
if ( ( data['Low'][-1] >= data['KC_upper'][-1] )
    & (data['Low'][-2] >= data['KC_upper'][-2] )
    & (data['Low'][-3] >= data['KC_upper'][-3] ) & ( data['ADX_14'][-1] >= 20) ):
    print ("SHORT ::: 50_MQL5_keltner_adx\n")
