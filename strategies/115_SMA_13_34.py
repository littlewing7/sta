# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
#import os
#import numpy as np
#import pandas as pd
#from pandas import DataFrame


# Optimal ticker interval for the strategy.
timeframe = '5m'

# SMA 5, SMA 8
data = __SMA  ( data, 13 )
data = __SMA ( data, 34 )


if data["SMA_13"][-1] > data["SMA_34"][-1] and data["SMA_13"][-2] < data["SMA_34"][-2]:
    print_log ( '115_SMA_13_34', 'LONG', [ 'SMA_13', 'SMA_34', 'SMA_13_34_cross' ] )

if data["SMA_3"][-1] < data["SMA_34"][-1] and data["SMA_13"][-2]  > data["SMA_34"][-2]:
    print_log ( '115_SMA_13_34', 'SHORT', [ 'SMA_13', 'SMA_34', 'SMA_13_34_cross' ] )


