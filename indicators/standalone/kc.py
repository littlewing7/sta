#!/usr/bin/env python3

import argparse

import os,sys
import yfinance as yf
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


def __KC (dataframe, period=20, multiplier=2):
    """
    Calculates the Keltner Channels for a given DataFrame.
    
    Parameters:
    dataframe (pd.DataFrame): DataFrame containing the OHLC data of the asset.
    period (int): Period to calculate the Keltner Channels (default: 20).
    multiplier (float): Multiplier for the Average True Range (ATR) (default: 2).
    
    Returns:
    pd.DataFrame: A new DataFrame containing the Keltner Channels for the given OHLC data.
    """
    tr = pd.DataFrame()
    tr['h_l'] = dataframe['High'] - dataframe['Low']
    tr['h_pc'] = abs(dataframe['High'] - dataframe['Adj Close'].shift())
    tr['l_pc'] = abs(dataframe['Low'] - dataframe['Adj Close'].shift())
    tr['tr'] = tr[['h_l', 'h_pc', 'l_pc']].max(axis=1)
    atr = tr['tr'].rolling(period).mean()
    kc_middle = dataframe['Adj Close'].rolling(period).mean()
    kc_upper = kc_middle + multiplier * atr
    kc_lower = kc_middle - multiplier * atr
    kc_df = pd.concat([kc_middle, kc_upper, kc_lower], axis=1)
    kc_df.columns = ['KC_middle', 'KC_upper', 'KC_lower']
    return kc_df


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)

    # Calculate the Keltner Channels using the function
    kc_df = __KC (data)


    # Loop through each row in the DataFrame and check if the Close price touches the Upper or Lower Keltner Channel
    #for i, row in kc_df.iterrows():
    #    if df['Adj Close'][i] >= row['KC Upper']:
    #        print("Price touched the Upper Keltner Channel on", i.date())
    #    elif df['Adj Close'][i] <= row['KC Lower']:
    #        print("Price touched the Lower Keltner Channel on", i.date())

    # Check yesterday's close price and send a BUY or SELL message if it touches the KC Upper or Lower band
    yesterday_close = df.iloc[-2]['Adj Close']
    if kc_df.iloc[-2]['KC_lower'] * 1.01 <= yesterday_close < kc_df.iloc[-1]['KC_lower'] and df.iloc[-1]['Adj Close'] > yesterday_close:
        print("BUY message")
    elif kc_df.iloc[-2]['KC_upper'] * 0.99 >= yesterday_close > kc_df.iloc[-1]['KC_upper'] and df.iloc[-1]['Adj Close'] < yesterday_close:
        print("SELL message")

