########################
#####  S14: Simple #####
########################
if ( (  data['MACD'][-1]     > 0)  # over 0
    & ( data['MACD'][-1]     > data['MACD_SIGNAL'][-1] )  # over signal
    & ( data['BB_upper'][-1] > data['BB_upper'][-2] )  # pointed up
    & ( data['RSI_14'][-1]   > 70 )  # optional filter, need to investigate
    ):
    print ( f"{ticker} {interval} ---> LONG ::: S30_Simple\n" )

if ( data['RSI_14'][-1] > 80 ):
    print ( f"{ticker} {interval} ---> SHORT ::: S30_Simple\n" )

