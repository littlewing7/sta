# AwesomeMacd.py
#timeframe = '1h'

data = __MACD ( data )
data = __AO ( data )

if (  ( data["MACD"][-1] > 0 )
    & ( data['AO'][-1]   > 0 )
    & ( data['AO'][-2]   < 0 ) ):
    print ( f"{ticker} {interval} ---> LONG ::: AwesomeMacd\n")

if (  ( data["MACD"][-1] < 0 )
    & ( data['AO'][-1]   < 0 )
    & ( data['AO'][-2]   > 0 ) ):
    print ( f"{ticker} {interval} ---> SHORT ::: AwesomeMacd\n")


