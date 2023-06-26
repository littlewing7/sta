#!/usr/bin/env python3

import argparse

import os,sys
import yfinance as yf
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

#def __STOCHASTIC (df, k, d):
from util.stochastic   import __STOCHASTIC



parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)

    # Define stochastic indicator parameters
    sto_k = 14
    sto_d = 3
    sto_slow = 3

    sto_overbought = 80
    sto_oversold = 20


    # Calculate stochastic indicator using the function
    data = __STOCHASTIC (data, sto_k, 3)

    print ( data.tail(2) )

    if data['STO_K'][-1] < sto_oversold:
        print(f"BUY :: Stochastic K is oversold, current K value: {data['STO_K'][-1]:.2f}")

    if data['STO_K'][-1] > sto_oversold and data['STO_K'][-2] < sto_oversold:
        print(f"STRONG BUY :: Stochastic K crossed over oversold level from above, current K value: {data['STO_K'][-1]:.2f}")

    if data['STO_K'][-1] < sto_oversold and data['STO_K'][-1] < data['STO_K'][-2]:
        print(f"WEAK BUY, Stochastic continuing down trend, ocurrent K value: {data['STO_K'][-1]:.2f}")


    if data['STO_K'][-1] > sto_overbought:
        print(f"SELL: Stochastic K is overbought, current K value: {data['STO_K'][-1]:.2f}")

    if data['STO_K'][-1] > sto_overbought and data['STO_K'][-1] > data['STO_K'][-2]:
        print(f"SELL: Stochastic K is overbought, going up current K value: {data['STO_K'][-1]:.2f}")

    if data['STO_K'][-1] > sto_overbought and data['STO_K'][-1] < data['STO_K'][-2]:
        print(f"STRONG SELL: Stochastic K is overbought, going down towards 80 level, current K value: {data['STO_K'][-1]:.2f}")

    if data['STO_K'][-2] < sto_overbought and data['STO_K'][-1] > sto_overbought:
        print(f"Stochastic K crossed over overbought level from below, current K value: {data['STO_K'][-1]:.2f}")

    if data['STO_K'][-2] > sto_overbought and data['STO_K'][-1] < sto_overbought:
        print(f"STRONG sell, current K value: {data['STO_K'][-1]:.2f}")

    print ( data.tail (5) )

