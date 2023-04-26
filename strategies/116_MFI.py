data = __MFI ( data, 14 )

if ( data['MFI_Signal'][-1] == 2 ):
   print_log ( '116_MFI', 'LONG', [ 'MFI' ] )

if ( data['MFI_Signal'][-1] == -2 ):
   print_log ( '116_MFI', 'SHORT', [ 'MFI' ] )

