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
    print ( "LONG ::: 8_EMA 8, 21 crossover\n" )

if ( ( ( data["EMA_8"][-1] < data["EMA_21"][-1] ) & ( data["EMA_8"][-2] > data["EMA_21"][-2] ) ) & ( data['Volume'][-1] > 0 ) ):
    print ("SHORT ::: 8_EMA 8, 21 crossunder\n")



# EMA_20 crossover EMA_50
if ( ( ( data["EMA_20"][-1] > data["EMA_50"][-1] ) & ( data["EMA_20"][-2] < data["EMA_50"][-2] ) ) & 
    #( r_data['Close'][0] > dataframe[f'resample_{self.resample_interval}_sma']) &
    ( data['Volume'][0] > 0 ) ):
    print ( "LONG ::: 8_EMA 20, 50 crossover\n" )

if ( ( ( data["EMA_20"][-1] < data["EMA_50"][-1] ) & ( data["EMA_20"][-2] > data["EMA_50"][-2] ) ) & ( data['Volume'][-1] > 0 ) ):
    print ("SHORT ::: 8_EMA 20, 50 crossunder\n")



if data['EMA_9_21_Signal'][-1] == 2:
    print ( "LONG  8_EMA.py 9, 21 cross_over\n" )

if data['EMA_9_21_Signal'][-1] == -2:
    print ( "SHORT  8_EMA 9, 21 cross_under\n" )


if data['EMA_20_50_Signal'][-1] == 2:
    print ( "LONG  8_EMA.py 20, 50 cross_over\n" )

if data['EMA_20_50_Signal'][-1] == -2:
    print ( "SHORT  8_EMA 20, 50 cross_under\n" )
