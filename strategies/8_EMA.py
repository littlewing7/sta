############################################
#####  S12: ReinForcedAverageStrategy  #####
############################################
data = __EMA ( data, 8 )
data = __EMA ( data, 21 )
data = __EMA ( data, 20 )
data = __EMA ( data, 50 )



# EMA_8 crossover EMA_21
if ( ( ( data["EMA_8"][-1] > data["EMA_21"][-1] ) & ( data["EMA_8"][-2] < data["EMA_21"][-2] ) ) & 
    #( r_data['Close'][0] > dataframe[f'resample_{self.resample_interval}_sma']) &
    ( data['Volume'][0] > 0 ) ):
    print_log ( '8_EMA', 'LONG', [ 'EMA_8', 'EMA_21' ] )

if ( ( ( data["EMA_8"][-1] < data["EMA_21"][-1] ) & ( data["EMA_8"][-2] > data["EMA_21"][-2] ) ) & ( data['Volume'][-1] > 0 ) ):
    print_log ( '8_EMA', 'SHORT', [ 'EMA_8', 'EMA_21' ] )



# EMA_20 crossover EMA_50
if ( ( ( data["EMA_20"][-1] > data["EMA_50"][-1] ) & ( data["EMA_20"][-2] < data["EMA_50"][-2] ) ) & 
    #( r_data['Close'][0] > dataframe[f'resample_{self.resample_interval}_sma']) &
    ( data['Volume'][0] > 0 ) ):
    print_log ( '8_EMA', 'LONG', [ 'EMA_20', 'EMA_50', 'EMA_20_50_crossover' ] )

if ( ( ( data["EMA_20"][-1] < data["EMA_50"][-1] ) & ( data["EMA_20"][-2] > data["EMA_50"][-2] ) ) & ( data['Volume'][-1] > 0 ) ):
    print_log ( '8_EMA', 'SHORT', [ 'EMA_20', 'EMA_50', 'EMA_20_50_crossunder' ] )



if data['EMA_9_21_Signal'][-1] == 2:
    print_log ( '8_EMA', 'LONG', [ 'EMA_9', 'EMA_21', 'EMA_9_21_crossover' ] )

if data['EMA_9_21_Signal'][-1] == -2:
    print_log ( '8_EMA', 'SHORT', [ 'EMA_8', 'EMA_21', 'EMA_9_21_cross_under' ] )


if data['EMA_20_50_Signal'][-1] == 2:
    print_log ( '8_EMA', 'LONG', [ 'EMA_20', 'EMA_50', 'EMA_20_50_crossover' ] )

if data['EMA_20_50_Signal'][-1] == -2:
    print_log ( '8_EMA', 'SHORT', [ 'EMA_20', 'EMA_50', 'EMA_20_50_cross_under' ] )
