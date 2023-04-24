'''
### Author: Wilson ###
Strategy from:
https://www.ig.com/au/trading-strategies/best-forex-trading-strategies-and-tips-190520#Bladerunner
The first candlestick that touches the EMA is called the ‘signal candle’,
The second candle that moves away from the EMA again is the ‘confirmatory candle’.
Traders would place their open orders at this price level to take advantage of the rebounding price.
'''

data = __EMA ( data, 20 )

# BUY if first candle stick touches ema and then next candle stick rebounds off it
if ( ( data['Low'].iloc[-2] <= data['EMA_20'].iloc[-2] and data['EMA_20'].iloc[-2] <= data['High'].iloc[-2]) & (data['Close'].iloc[-1] > data['Close'].iloc[-2])):
    print_log ( '43_MQL5_BladeRunner.py', 'LONG', [ 'EMA_20' ] )

# SELL if first candle stick touches ema and then next candle stick rebounds off it
if ( ( data['Low'].iloc[-2] <= data['EMA_20'].iloc[-2] and data['EMA_20'].iloc[-2] <= data['High'].iloc[-2]) & (data['Close'].iloc[-1] < data['Close'].iloc[-2])):
    print_log ( '43_MQL5_BladeRunner.py', 'SHORT', [ 'EMA_20' ] )
