########################
#####  S15: Trend  #####
########################
data = __EMA ( data, 14 )
data = __EMA ( data, 28 )
data = __RSI ( data, 14 )
data = __WR ( data, 20 )


if ( (  data['Close'][-1]  > data['EMA_14'][-1] ) 
    & ( data['EMA_14'][-1] > data['EMA_28'][-1] ) 
    & ( data['RSI_14'][-1] > 70 ) 
    & ( data['WR_20'][-1]  < -98 )):
    print ( f"{ticker} {interval} ---> LONG ::: S31_TREND\n")

if ( ( data['Close'][-1]  < data['EMA_14'][-1] ) &
    (  data['EMA_14'][-1] < data['EMA_28'][-1] ) &
    (  data['RSI_14'][-1] < 30 ) &
    (  data['WR_20'][-1]  > -34 ) ):
    print ( f"{ticker} {interval} ---> SHORT ::: S31_TREND\n")

