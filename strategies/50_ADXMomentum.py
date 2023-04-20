# ADXMomentum.py _freq/usedata/strategies/berlinguyinca/ADXMomentum.py
# timeframe = "1h"

data = __ADX ( data, 14 )
data = __MOM ( data, 14 )

if (  ( data['ADX_14'][-1]         > 25)
    & ( data['MOM_14'][-1]         > 0)
    & ( data['ADX_14_plus_di'][-1] > 25)
    & ( data['ADX_14_plus_di'][-1] > data['ADX_14_minus_di'][-1] ) ):
    print ( "LONG ::: S50_ADXMomentum\n")

if (  ( data['ADX_14'][-1]          > 25) 
    & ( data['MOM_14'][-1]          < 0)
    & ( data['ADX_14_minus_di'][-1] > 25)
    & ( data['ADX_14_plus_di'][-1]  < data['ADX_14_minus_di'][-1]) ):
    print ("SHORT ::: S50_ADXMomentum\n")

