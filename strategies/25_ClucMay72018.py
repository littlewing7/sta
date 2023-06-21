#############################
##### 25: CLUCMAY72018  #####
#############################
# _freq/user_data/strategies/berlinguyinca/25_ClucMay72018.py
Vol_SMA_30 = data['Volume'].rolling(window=30).mean().shift(1) * 20

data = __EMA ( data, 100 )
data = __BB ( data )

if  ( ( data['Adj Close'][-1]   < data['EMA_100'][-1] ) &
    (   data['Adj Close'][-1]   < 0.985 * data['BB_lower'][-1] ) &
    (   data['Volume'][-1]  < Vol_SMA_30[-1] ) ):
    print_log ( '25_CLUCMAY72018', 'LONG', [ 'BB', 'EMA_100' ] )

#if ( ( data['Adj Close'][-1] > data['BB_middle'][-1] )):
#    print ( f"{ticker} {interval} ---> SHORT ::: 25_CLUCMAY72018 close > BB middle\n" )

