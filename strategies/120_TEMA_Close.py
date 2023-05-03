# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame


# Optimal ticker interval for the strategy.
timeframe = '5m'

# TEMA 30
data = __TEMA ( data, 30 )

_close     = data["Close"].iloc[-1]
_close_1   = data["Close"].iloc[-2]

tema_30    = data['TEMA_30'].iloc[-1]
tema_30_1  = data['TEMA_30'].iloc[-2]


if ( _close > tema_30 ) and ( tema_30 > tema_30_1 ) and ( _close > _close_1 ):
    print_log ( '120_TEMA_Close', 'LONG', [ 'Close', 'TEMA_30' ] )

if ( _close < tema_30 ) and ( tema_30 < tema_30_1 ) and ( _close < _close_1):
    print_log ( '120_TEMA_Close', 'SHORT', [ 'Close', 'TEMA_30' ] )

