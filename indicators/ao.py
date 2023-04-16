#!/usr/bin/env python3

import os,sys
import yfinance as yf
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################
from util.sma import __SMA
from util.ao  import __AO


data = yf.download("AAPL", period="5y")

data = __AO ( data, 5, 34)
data = data.dropna()
print ( data.tail() )


