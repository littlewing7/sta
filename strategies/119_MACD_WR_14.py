
data = __MACD ( data )
data = __WR  ( data, 14 )

if ( data["WR_14"][i-1] > -50 and data["WR_14"][i] < -50 and data["MACD"][i] > data["MACD_SIGNAL"][i] ):
   print_log ( '119_MACD_WR_14', 'LONG', [ 'MACD', 'WR_14' ] )

if ( data["WR_14"][i-1] < -50 and data["WR_14"][i] > -50 and data["MACD"][i] < data["MACD_SIGNAL"][i] ):
   print_log ( '119_MACD_WR_14', 'SHORT', [ 'MACD', 'WR_14' ] )
