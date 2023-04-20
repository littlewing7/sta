# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame


# Optimal ticker interval for the strategy.
timeframe = '5m'

# RSI 14, Bolinger bands 20, TEMA 9
data = __RSI  ( data, 14 )
data = __BB   ( data )
data = __TEMA ( data, 9 )

# github.com/superduong/ALIN/blob/main/freqtrade/templates/sample_.py
# RSI crosses above 30, tema below BB middle, tema is raising, Volume is not 0
if (  ( data["RSI_14"][-1]  >= 30 )
    & ( data["RSI_14"][-2]  < 30 )
    & ( data['TEMA_9'][-1]  <= data['BB_middle'][-1] )
    & ( data['TEMA_9'][-1]  > data['TEMA_9'][-2] )
    & ( data["Volume"][-1]  > 0) ):
    print ( "LONG ::: 1_BB_RSI_TEMA\n")


if (  ( data["RSI_14"][-1] >=70 )
    & ( data["RSI_14"][-2] < 70 )
    & ( data['TEMA_9'][-1] > data['BB_middle'][-1] )
    & ( data['TEMA_9'][-1] < data['TEMA_9'][-2] )
    & ( data["Volume"][-1]  > 0) ):
    print ( "SHORT ::: 1_BB_RSI_TEMA\n")

