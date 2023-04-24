
#############################
#####  26: EMASkipPump  #####
#############################

data = __EMA ( data, 5 )
data = __EMA ( data, 12 )
data = __EMA ( data, 21 )

Vol_SMA_30 = data['Volume'].rolling(window=30).mean().shift(1) * 20

if (( data['Volume'][-1]  < Vol_SMA_30[-1] ) &
    ( data['Close'][-1]   < data['EMA_5'][-1] ) &
    ( data['Close'][-1]   < data['EMA_12'][-1] ) &
    #( data['Close'][0]  == data['min'][0]) &
    ( data['Close'][-1]  <= data['BB_lower'][-1] ) ):
    print_log ( '26_EMASkipPump', 'LONG', [ 'BB', 'EMA_5', 'EMA_12', 'EMA_21', 'Vol' ] )

if (( data['Close'][0] > data['EMA_5'][-1] ) &
    ( data['Close'][0] > data['EMA_12'][-1] ) &
    #( data['Close'][0] >= data['max'][-1] ) &
    ( data['Close'][0] >= data['BB_upper'][-1] ) ):
    print_log ( '26_EMASkipPump', 'SHORT', [ 'BB', 'EMA_5', 'EMA_12', 'EMA_21', 'Vol' ] )

