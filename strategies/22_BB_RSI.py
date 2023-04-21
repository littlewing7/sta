
data = __RSI ( data, 14 )

if ( ( data['RSI_14'][-1] < 30 ) & ( data['Close'][-1] < data['BB_lower'][-1]) ):
    print_log ( '22_BB_RSI', 'LONG', [ 'BB', 'RSI', 'Close' ] )

if ( data['RSI_14'][0] > 70 ):
    print_log ( '22_BB_RSI', 'SHORT', [ 'BB', 'RSI', 'Close' ] )

