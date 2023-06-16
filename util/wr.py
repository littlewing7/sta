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
    close = data["Adj Close"]

    data['WR_{}'.format(t)] = -100 * ((highh - close) / (highh - lowl))
    return data


