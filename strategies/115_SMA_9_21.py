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
data = __SMA  ( data, 9 )
data = __SMA ( data, 21 )


if data["SMA_9"][-1] > data["SMA_21"][-1] and data["SMA_9"][-2] < data["SMA_21"][-2]:
    print_log ( '115_SMA_9_21', 'LONG', [ 'SMA_9', 'SMA_21', 'SMA_9_21_cross' ] )

if data["SMA_9"][-1] < data["SMA_21"][-1] and data["SMA_9"][-2]  > data["SMA_21"][-2]:
    print_log ( '115_SMA_9_21', 'SHORT', [ 'SMA_9', 'SMA_21', 'SMA_9_21_cross' ] )


