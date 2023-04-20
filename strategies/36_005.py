###################################
#####  S36: Strategy 005 hlhb #####
###################################

data = __RSI ( data, 10 )
data = __EMA ( data, 5 )
data = __EMA ( data, 10 )
data = __ADX ( data, 14 )

if (  ( ( data["RSI_10"][-1]  > 50 ) & ( data["RSI_10"][-2] < 50 ) )
    & ( ( data["EMA_5"][-1]   > data["EMA_10"][-1] ) & ( data["EMA_5"][-2]  < data["EMA_10"][-2] ) )
    & (   data['ADX_14'][-1]  > 25) 
    & (   data['Volume'][-1]  > 0) ):
    print ( "LONG ::: S35_005\n")

if (  ( (  data["RSI_10"][-1] < 50 ) & ( data["RSI_10"][-2] > 50 ) )
    &  ( ( data["EMA_5"][-1]  < data["EMA_10"][-1] ) & ( data["EMA_5"][-2]  > data["EMA_10"][-2] ) )
    &  (   data['ADX_14'][-1] > 25)
    &  (   data['Volume'][-1] > 0) ):
    print ( "SHORT ::: S35_005\n")
