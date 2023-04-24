# AwesomeMacd.py
#timeframe = '1h'

data = __MACD ( data )
data = __AO ( data )

if (  ( data["MACD"][-1] > 0 )
    & ( data['AO'][-1]   > 0 )
    & ( data['AO'][-2]   < 0 ) ):
    print_log ( '52_AwesomeMacd', 'LONG', [ 'AO', 'MACD' ] )

if (  ( data["MACD"][-1] < 0 )
    & ( data['AO'][-1]   < 0 )
    & ( data['AO'][-2]   > 0 ) ):
    print_log ( '52_AwesomeMacd', 'SHORT', [ 'AO', 'MACD' ] )
