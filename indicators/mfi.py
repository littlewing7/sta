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

# def __MFI ( data, window=14 )
from util.mfi   import __MFI

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)
    data = __MFI ( data, window=14)

    # Define the overbought and oversold levels
    mfi_overbought = 75
    mfi_oversold   = 20

    data['MFI_Crossover']  = np.where ( ( ( data['MFI_14'].shift(1)  < mfi_oversold )   & ( data['MFI_14'] > mfi_oversold ) ),   1, 0 )
    data['MFI_Crossunder'] = np.where ( ( ( data['MFI_14'].shift(1)  > mfi_overbought ) & ( data['MFI_14'] < mfi_overbought ) ), 1, 0 )

    print (data.tail (5) )

    if data['MFI_Crossover'].iloc[-1] == 1:
        print("MFI :: SELL :: Stock has crossed over")
    elif data['MFI_Crossunder'].iloc[-1] == 1:
        print("MFI :: SELL :: Stock has crossed under")
    else:
        print("No conditions are met")

    mfi = data['MFI_14']

    # Check if the mfi crosses the overbought or oversold levels
    if mfi[-2] < mfi_oversold and mfi[-1] > mfi_oversold:
        print("mfi crossed oversold level from below")
    elif mfi[-2] > mfi_overbought and mfi[-1] < mfi_overbought:
        print("mfi crossed overbought level from above")
    elif mfi[-2] > mfi_oversold and mfi[-1] < mfi_oversold:
        print("mfi crossed oversold level from above")
    elif mfi[-2] < mfi_overbought and mfi[-1] > mfi_overbought:
        print("mfi crossed overbought level from below")
    else:
        print("mfi is within normal range")



    print ( data.tail (5) )


