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

# def __WILLR (high, low, close, period):
from util.uo   import __UO

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)
    data = __UO ( data )


    print ( data.tail(3) )

