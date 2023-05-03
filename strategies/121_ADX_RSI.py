data = __RSI ( data, 14 )
data = __ADX ( data, 14 )

if data["ADX_14"][-1] > 35 and data["ADX_14_plus_di"][-1] < data["ADX_14_minus_di"][-1] and data["RSI_14"][-1] < 50:
   print_log ( '121_ADX_RSI', 'LONG', [ 'ADX', 'RSI' ] )

if data["ADX_14"][-1] > 35 and data["ADX_14_plus_di"][-1] > data["ADX_14_minus_di"][-1] and data["RSI_14"][-1] > 50:
   print_log ( '121_ADX_RSI', 'SHORT', [ 'ADX', 'RSI' ] )

