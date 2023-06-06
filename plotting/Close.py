#!/usr/bin/env python3

import argparse

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

import os, datetime

#def __SMA ( data, n ):
#    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
#    return data

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--ticker', nargs='+', required=True,  type=str, help='ticker')

    args = parser.parse_args()
    start_date = "2020-01-01"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)

    for symbol in args.ticker:

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

        #data = __SMA ( data, 20 )

        plt.plot ( data.index, data['Adj Close'])
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.title(f'{symbol} Adj Closing Price')
        #plt.legend(loc = 'upper left')

        #plt.show()
        filename = "{}/plotting/_plots/{}_{}.png".format ( parent_dir, symbol, filename )
        plt.savefig ( filename )

