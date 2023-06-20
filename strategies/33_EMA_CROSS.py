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
    & ( data['Adj Close'][-1] > data['EMA_9'][-1] )
    & ( data['Open'][-1]  < data['Adj Close'][-1]) ):
    print_log ( '33_EMA_CROSS', 'LONG', [ 'EMA_9', 'EMA_21', 'EMA_cross' ] )

if (  ( data['EMA_9_21_Signal'][-1] == -2 )
    & ( data['Adj Close'][-1]   < data['EMA_9'][-1] )
    & ( data['Open'][-1]    > data['Adj Close'][-1] ) ):
    print_log ( '33_EMA_CROSS', 'SHORT', [ 'EMA_9', 'EMA_21', 'EMA_cross' ] )


# EMA 20, 50
if (  ( data['EMA_20_50_Signal'][-1] == 2 )
    & ( data['Adj Close'][-1] > data['EMA_20'][-1] )
    & ( data['Open'][-1]  < data['Adj Close'][-1]) ):
    print_log ( '33_EMA_CROSS', 'LONG', [ 'EMA_20', 'EMA_50', 'EMA_20_50_cross' ] )

if (  ( data['EMA_20_50_Signal'][-1] == -2 )
    & ( data['Adj Close'][-1]   < data['EMA_20'][-1] )
    & ( data['Open'][-1]    > data['Adj Close'][-1] ) ):
    print_log ( '33_EMA_CROSS', 'SHORT', [ 'EMA_20', 'EMA_50', 'EMA_20_50_cross' ] )



