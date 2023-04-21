# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame


# Optimal ticker interval for the strategy.
timeframe = '15m'

# CCI 20 crossover, crossunder
data = __MACD  ( data )


if data['MACD_Signal'][-1] == 2:
    print ( f"{ticker} {interval} ---> LONG [e] 8_MACD cross_over from below\n" )

if data['MACD_Signal'][-1] == -2:
    print ( f"{ticker} {interval} ---> SHORT [e] 8_MACD cross_under from above\n" )
