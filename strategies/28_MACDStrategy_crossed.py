#######################################
#####  S28: MACDStrategy_crossed  #####
#######################################

data = __CCI ( data, 20 )
data = __MACD ( data )

if ( ( data['MACD_Signal'].iloc[-1] == 2 ) and ( data['CCI_20'][-1] <= -50.0 )):
    print ( f"{ticker} {interval} ---> LONG ::: MACDSTrategy_crossed\n")

if ( ( data['MACD_Signal'].iloc[-1] == -2 ) and ( data['CCI_20'][0] >= 100.0) ):
    print ( f"{ticker} {interval} ---> SHORT ::: S28 MACDStrategy_crossed\n")

