#!/usr/bin/env python3

import argparse

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
from util.mom  import __MOM

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)
    window_mom = 14

    # Calculate the MOM indicator and print the current value
    data = __MOM ( data , window_mom )
    current_mom = data["MOM_14"].iloc[-1]

    print("Current MOM value for", symbol, "is:", current_mom)


