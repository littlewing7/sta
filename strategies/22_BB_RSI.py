
data = __RSI ( data, 14 )

if ( ( data['RSI_14'][-1] < 30 ) & ( data['Close'][-1] < data['BB_lower'][-1]) ):
    print ("LONG ::: 22_BB_RSI\n")

if ( data['RSI_14'][0] > 70 ):
    print ( "SHORT ::: 22_BB_RSI\n")

