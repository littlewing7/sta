
data = __MACD ( data )
data = __WR  ( data, 20 )
data = __WR  ( data, 14 )

go_long  = 0
go_short = 0


if ( data["WR_20"][i-1] > -50 and data["WR_20"][i] < -50 and data["MACD"][i] > data["MACD_SIGNAL"][i] ):
   print_log ( '119_MACD_WR', 'LONG', [ 'MACD', 'WR_20' ] )

if ( data["WR_20"][i-1] < -50 and data["WR_20"][i] > -50 and data["MACD"][i] < data["MACD_SIGNAL"][i] ):
   print_log ( '119_MACD_WR', 'SHORT', [ 'MACD', 'WR_20' ] )


if ( data["WR_14"][i-1] > -50 and data["WR_14"][i] < -50 and data["MACD"][i] > data["MACD_SIGNAL"][i] ):
   print_log ( '119_MACD_WR', 'LONG', [ 'MACD', 'WR_14' ] )

if ( data["WR_14"][i-1] < -50 and data["WR_14"][i] > -50 and data["MACD"][i] < data["MACD_SIGNAL"][i] ):
   print_log ( '119_MACD_WR', 'SHORT', [ 'MACD', 'WR_14' ] )
