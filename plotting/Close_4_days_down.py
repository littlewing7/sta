#!/usr/bin/env python3

import argparse

import os, datetime

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

    args = parser.parse_args()
    start_date = "2020-01-01"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)

    for symbol in args.ticker:


        # Load stock data
        filename, ext =  os.path.splitext(os.path.basename(__file__))

        csv_file = "{}/data/{}_1d.csv".format( parent_dir, symbol )

        # Get today's date
        today = datetime.datetime.now().date()

        # if the file was downloaded today, read from it
        if  ( ( os.path.exists ( csv_file ) ) and ( datetime.datetime.fromtimestamp ( os.path.getmtime ( csv_file ) ).date() == today ) ):
            data = pd.read_csv ( csv_file, index_col='Date' )
        else:
            # Download data
            data = yf.download ( symbol, start=start_date, progress=False)
            data.to_csv ( csv_file )

        data["Signal"] = 0.0
        data['Close_4_days_Signal'] = np.select(
            [ ( data['Adj Close'] < data['Adj Close'].shift(1) ) & ( data['Adj Close'].shift(1) <  data['Adj Close'].shift(2) ) & ( data['Adj Close'].shift(2) <  data['Adj Close'].shift(3) ) & ( data['Adj Close'].shift(3) <  data['Adj Close'].shift(4) ),
              ( data['Adj Close'] > data['Adj Close'].shift(1) ) & ( data['Adj Close'].shift(1) >  data['Adj Close'].shift(2) ) ],
        [2, -2])

        #print ( data.tail ( 60 ))

        # Plot the trading signals
        plt.figure(figsize=(14,7))

        plt.plot ( data['Adj Close'],  alpha = 0.3, linewidth = 2,                  label = symbol  )

        plt.plot ( data.loc[data["Close_4_days_Signal"] ==  2.0].index, data["Adj Close"][data["Close_4_days_Signal"] ==  2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
        plt.plot ( data.loc[data["Close_4_days_Signal"] == -2.0].index, data["Adj Close"][data["Close_4_days_Signal"] == -2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

        plt.legend(loc = 'upper left')
        plt.title(f'{symbol}_{filename}')

        #plt.show()
        filename = "{}/plotting/_plots/{}_{}.png".format ( parent_dir, symbol, filename )
        plt.savefig ( filename )

