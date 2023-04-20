#################################
# https://github.com/alisalavati/freq
#AdxSmas.py: ADX 14, SMA 3, SMA 6
#timeframe = '1h'
data = __ADX ( data, 14 )   
data = __SMA ( data, 3 )
data = __SMA ( data, 6 )

if ( (    data['ADX_14'][-1] > 25)
    & ( ( data["SMA_3"][-1]  > data["SMA_6"][-1] ) & ( data["SMA_3"][-2] < data["SMA_6"][-2] ) ) ):
    print ("LONG ::: S51_AdxSmas\n")

if ( (    data['ADX_14'][-1] < 25 )
    & ( ( data["SMA_6"][-1]  > data["SMA_3"][-1] ) & ( data["SMA_6"][-2] < data["SMA_3"][-2] ) ) ):
    print ("SHORT ::: S51_AdxSmas\n\n")

