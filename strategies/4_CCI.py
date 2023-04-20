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
data = __SMA  ( data, 5 )
data = __SMA ( data, 8 )


if data['CCI_Signal'][-1] == 2:
    print ( "LONG [e] 4_CCI cross_over from below\n" )

if data['CCI_Signal'][-1] == -2:
    print ( "SHORT [e] 4_CCI cross_under from above\n" )

