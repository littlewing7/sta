data = __CCI ( data, 34 )
data = __CCI ( data, 170 )

#_freq/user_data/strategies/berlinguyinca/CCIStrategy.py
if (  ( data['CCI_170'][-1] < -100)
    & ( data['CCI_34'][-1]  < -100)
    & ( data['CMF'][-1]     < -0.1)
    & ( data['MFI_14'][-1]  < 25) ):

    ## insurance
    #& (dataframe['resample_medium'] > dataframe['resample_short'])
    #& (dataframe['resample_long'] < dataframe['close'])
    print ( f"{ticker} {interval} ---> LONG ::: 23_CCI_MFI_RSI\n" )

if  ( ( data['CCI_170'][-1] > 100 )
    & ( data['CCI_34'][-1]  > 100 )
    & ( data['CMF'][-1]     > 0.3 ) ):
    #& ( data['resample_sma'] < data['resample_medium'])
    #& ( data['resample_medium'] < data['resample_short'])
    print ( f"{ticker} {interval} ---> SHORT ::: 23_CCI_MFI_RSI\n" )

