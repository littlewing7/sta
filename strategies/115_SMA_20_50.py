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
data = __SMA  ( data, 20 )
data = __SMA ( data, 50 )


if data["SMA_20"][-1] > data["SMA_50"][-1] and data["SMA_20"][-2] < data["SMA_50"][-2]:
    print_log ( '115_SMA_20_50', 'LONG', [ 'SMA_20', 'SMA_50', 'SMA_20_50_cross' ] )

if data["SMA_20"][-1] < data["SMA_50"][-1] and data["SMA_20"][-2]  > data["SMA_50"][-2]:
    print_log ( '115_SMA_20_50', 'SHORT', [ 'SMA_20', 'SMA_50', 'SMA_20_50_cross' ] )


