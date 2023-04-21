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
    print_log ( '22_BB_RSI', 'LONG', [ 'CMF', 'MFI_14', 'CCI_34', 'CCI_170' ] )

if  ( ( data['CCI_170'][-1] > 100 )
    & ( data['CCI_34'][-1]  > 100 )
    & ( data['CMF'][-1]     > 0.3 ) ):
    #& ( data['resample_sma'] < data['resample_medium'])
    #& ( data['resample_medium'] < data['resample_short'])
    print_log ( '22_BB_RSI', 'SHORT', [ 'CMF', 'MFI_14', 'CCI_34', 'CCI_170' ] )

