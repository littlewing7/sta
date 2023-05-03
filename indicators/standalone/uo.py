#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import yfinance as yf

def __UO ( data ):
    data['Prior_Close'] = data['Close'].shift()
    data['BP']          = data['Close'] - data[['Low','Prior_Close']].min(axis=1)
    data['TR']          = data[['High','Prior_Close']].max(axis=1) - data[['Low','Prior_Close']].min(axis=1)

    data['Average7']  = data['BP'].rolling(7).sum()/data['TR'].rolling(7).sum()
    data['Average14'] = data['BP'].rolling(14).sum()/data['TR'].rolling(14).sum()
    data['Average28'] = data['BP'].rolling(28).sum()/data['TR'].rolling(28).sum()

    data['UO'] = 100 * (4*data['Average7']+2*data['Average14']+data['Average28'])/(4+2+1)
    data = data.drop(['Prior_Close','BP','TR','Average7','Average14','Average28'],axis=1)

    return data


symbol = 'AAPL'

# Read data 
data = yf.download(symbol,start='2020-01-01')
data = __UO ( data )


print ( data.tail(3))

