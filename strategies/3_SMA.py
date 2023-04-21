# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame


# Optimal ticker interval for the strategy.
timeframe = '5m'

# SMA 5, SMA 8
data = __SMA  ( data, 5 )
data = __SMA ( data, 8 )
data = __BB  ( data )

_vol   = data["Volume"].iloc[-1]

_rsi   = data["RSI_14"].iloc[-1]
_rsi_1 = data["RSI_14"].iloc[-2]


if data['SMA_5_8_Signal'][-1] == 2:
    print ( f"{ticker} {interval} ---> LONG ::: 3_SMA.py 5, 8 cross_over\n" )

if data['SMA_5_8_Signal'][-1] == -2:
    print ( f"{ticker} {interval} ---> SHORT ::: 3_SMA 5, 8 cross_under\n" )

if ( _rsi >= 30 ) and ( _rsi_1 < 30 ) and ( data['TEMA_9'][-1] <= data['BB_middle'][-1] ) and ( data['TEMA_9'][-1] > data['TEMA_9'][-2] ) and ( _vol > 0):
    print ( f"{ticker} {interval} ---> LONG  3_SMA  SMA 5 > 8\n")

if ( _rsi >=70 ) and ( _rsi_1 < 70 ) and ( data['TEMA_9'][-1]  > data['BB_middle'][-1] )  and ( data['TEMA_9'][-1] < data['TEMA_9'][-2] ) and ( _vol > 0):
    print ( f"{ticker} {interval} ---> SHORT  3_SMA  SMA 5 < 8\n")

#print ( data.tail(2) )


