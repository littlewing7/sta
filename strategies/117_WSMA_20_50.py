# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame


# Optimal ticker interval for the strategy.
timeframe = '5m'

data = __WSMA  ( data, 20 )
data = __WSMA ( data, 50 )


if data["WSMA_20_50_Signal"][-1] == 2:
    print_log ( '117_WSMA_20_50', 'LONG', [ 'WSMA_20', 'WSMA_50', 'WSMA_20_50_cross' ] )

if data["SMA_20_50_Signal"][-1] == -2:
    print_log ( '117_WSMA_20_50', 'SHORT', [ 'WSMA_20', 'WSMA_50', 'SMA_20_50_cross' ] )


