
data = __MACD ( data )
data = __WR  ( data, 20 )

if ( data["WR_20"][i-1] > -50 and data["WR_20"][i] < -50 and data["MACD"][i] > data["MACD_SIGNAL"][i] ):
   print_log ( '119_MACD_WR_20', 'LONG', [ 'MACD', 'WR_20' ] )

if ( data["WR_20"][i-1] < -50 and data["WR_20"][i] > -50 and data["MACD"][i] < data["MACD_SIGNAL"][i] ):
   print_log ( '119_MACD_WR_20', 'SHORT', [ 'MACD', 'WR_20' ] )
