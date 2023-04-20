###############################################
#####  S33: EMA 20, 50 CROSS Strategy001  #####
###############################################

data = __EMA ( data, 9 )
data = __EMA ( data, 20 )
data = __EMA ( data, 21 )
data = __EMA ( data, 50 )
#data = __EMA ( data, 100 )

# EMA 9, 21
if (  ( data['EMA_9_21_Signal'][-1] == 2 )
    & ( data['Close'][-1] > data['EMA_9'][-1] )
    & ( data['Open'][-1]  < data['Close'][-1]) ):
    print ("LONG ::: S33_EMA_CROSS OVER 9, 21\n")

if (  ( data['EMA_9_21_Signal'][-1] == -2 )
    & ( data['Close'][-1]   < data['EMA_9'][-1] )
    & ( data['Open'][-1]    > data['Close'][-1] ) ):
    print ("SHOSRT :: S33_EMA_CROSS UNDER 9, 21\n")


# EMA 20, 50
if (  ( data['EMA_20_50_Signal'][-1] == 2 )
    & ( data['Close'][-1] > data['EMA_20'][-1] )
    & ( data['Open'][-1]  < data['Close'][-1]) ):
    print ("LONG ::: S33_EMA_CROSS OVER 20, 50\n")

if (  ( data['EMA_20_50_Signal'][-1] == -2 )
    & ( data['Close'][-1]   < data['EMA_20'][-1] )
    & ( data['Open'][-1]    > data['Close'][-1] ) ):
    print ("SHOSRT :: S33_EMA_CROSS UNDER 20, 50\n")



