
data = __MACD ( data )

today_data = data.iloc[-1]
yesterday_data = data.iloc[-2]

if (  yesterday_data["MACD"] <  yesterday_data["MACD_SIGNAL"] ) & ( today_data["MACD"] > today_data["MACD_SIGNAL"] ):
   print_log ( '119_MACD', 'LONG', [ 'MACD' ] )

if data['MACD_Signal'][-1] == 2:
    print_log ( '119_MACD', 'LONG', [ 'MACD CROSSOVER' ] )


if (  yesterday_data["MACD"] >  yesterday_data["MACD_SIGNAL"] ) & ( today_data["MACD"] < today_data["MACD_SIGNAL"] ):
   print_log ( '119_MACD', 'SHORT', [ 'MACD' ] )

if data['MACD_Signal'][-1] == -2:
     print_log ( '119_MACD', 'SHORT', [ 'MACD CROSSUNDER' ] )

