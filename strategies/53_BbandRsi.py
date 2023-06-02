# BBANDRSI.py
# Optimal timeframe for the strategy
timeframe = '1h'

data = __RSI ( data, 14 )
data = __BB ( data )

if ( (  data["RSI_14"][-1] < 30 ) & ( data["Close"][-1]  < data["BB_lower"][-1] ) ):
    print_log ( '53_BbandRsi1', 'LONG', [ 'BB', 'RSI_14' ] )

if ( data["RSI_14"][-1] > 70 ):
    print_log ( '53_BbandRsi1', 'SHORT', [ 'RSI_14' ] )


'''
### Author: Wilson ###
Strategy from:

https://www.theancientbabylonians.com/the-bollinger-bands-and-relative-strength-index-rsi-strategy/

This strategy identifies over bought and over sold conditions and back checks this against the bollinger band
to ensure robustness of signals.

'''

#BUY if price is below low bollinger band and rsi is less than 30
if(( data['Close'].iloc[-1] <= data['BB_lower'].iloc[-1]) & (data['RSI_14'].iloc[-1] <= 30)):
    print_log ( '53_BbandRsi2', 'LONG', [ 'BB', 'RSI_14' ] )

#SELL if price is above high bollinger band as rsi is greater than 70
if((data['Close'].iloc[-1] >= data['BB_upper'].iloc[-1]) & (data['RSI_14'].iloc[-1] >= 70)):
    print_log ( '53_BbandRsi2', 'SHORT', [ 'BB', 'RSI_14' ] )
