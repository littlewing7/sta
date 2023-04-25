#!/usr/bin/env python3
import os,sys

import pandas as pd
import numpy as np
#import math

#def calculate_wr(high, low, close, window=20):
#    wr = (high.rolling(window=window).max() - close) / (high.rolling(window=window).max() - low.rolling(window=window).min()) * -100
#    return wr

def __WR (data, t):
    highh = data["High"].rolling(t).max()
    lowl  = data["Low"].rolling(t).min()
    close = data["Close"]
    #data["WR"] = -100 * ((highh - close) / (highh - lowl))
    #data["WR_prev"] = data["WR"].shift(1)

    data['WR_{}'.format(t)] = -100 * ((highh - close) / (highh - lowl))

#    # Reorder columns: WR_prev   WR
#    cols = list(data.columns)
#    a, b = cols.index('WR'), cols.index('WR_prev')
#    cols[b], cols[a] = cols[a], cols[b]
#    data = data[cols]

    data['Trend_20'] = data['Close'] / data['Close'].rolling(20).mean()

    #data["WR_Signal"] = 0
    # 2 = LONG, -2 = SHORT
    
    #data['WR_Signal'] = np.select(
    #    [   ( data['WR_20'] > -80 ) & ( data['WR_20'].shift(1) < -80 ),
    #        ( data['WR_20'] < -20 ) & ( data['WR_20'].shift(1) > -20 ) ],
    #    [2, -2])

    return data


