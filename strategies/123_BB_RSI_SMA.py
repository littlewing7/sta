
data = __RSI ( data, 14 )
data = __BB ( data, 20 )
data = __SMA ( data, 13 )


if ( ( data['SMA_13'][-1] > data['BB_middle'][-1] ) and ( data['RSI_14'][-1] < 50 ) ):
    print_log ( '123_BB_RSI_SMA', 'LONG', [ 'BB', 'RSI', 'SMA_13' ] )

if ( ( data['SMA_13'][-1] < data['BB_middle'][-1] ) and ( data["RSI_14"][-1] > 50 ) ):
    print_log ( '123_BB_RSI_SMA', 'SHORT', [ 'BB', 'RSI', 'SMA_13' ] )

