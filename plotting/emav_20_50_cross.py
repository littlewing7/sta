#!/usr/bin/env python3

#!/usr/bin/env python3

import argparse

import os, datetime

import pandas as pd
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

import matplotlib.dates as mdates

def __EMAV ( data, n=9 ):
    data['EMAV_{}'.format(n)] = data['Volume'].ewm(span = n ,adjust = False).mean()
    return data

filename, ext =  os.path.splitext(os.path.basename(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+', required=True,  type=str, help='ticker')
args = parser.parse_args()

start_date = "2020-01-01"

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

for symbol in args.ticker:

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

    # EMA 20, 50
    data = __EMAV ( data, 20 )
    data = __EMAV ( data, 50 )

    latest_price = data['Adj Close'][-1]

    # Buy/sell signals for  SMA crosses
    data["Signal"] = 0.0
    data['EMAV_20_50_Signal'] = np.select(
        [ ( data['EMAV_20'].shift(1) <  data['EMAV_50'].shift(1) ) & ( data['EMAV_20'] >  data['EMAV_50'] ) ,
          ( data['EMAV_20'].shift(1) >  data['EMAV_50'].shift(1) ) & ( data['EMAV_20'] <  data['EMAV_50'] ) ],
    [2, -2])

    data.index = pd.to_datetime(data.index)

    #print ( data.tail ( 60 ))

    # Plot the trading signals
    plt.figure(figsize=(14,7))

    plt.plot ( data['Adj Close'],  alpha = 0.3, linewidth = 2,                  label = symbol,  )
    plt.plot ( data["EMAV_20"], alpha = 0.6, linewidth = 2, color='orange',  label = 'EMAV_20',  )
    plt.plot ( data["EMAV_50"], alpha = 0.6, linewidth = 3, color='#FF006E', label = 'EMAV_50' )

    plt.plot ( data.loc[data["EMAV_20_50_Signal"] ==  2.0].index, data["EMAV_20"][data["EMAV_20_50_Signal"] ==  2.0], "^", markersize=10, color="g", label = 'BUY SIGNAL')
    plt.plot ( data.loc[data["EMAV_20_50_Signal"] == -2.0].index, data["EMAV_20"][data["EMAV_20_50_Signal"] == -2.0], "v", markersize=10, color="r", label = 'SELL SIGNAL')

    plt.legend(loc = 'upper left')
    plt.title(f'{symbol}_{filename}')

    plt.xticks(rotation=45)
    plt.grid(True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = f"Current Price: ${latest_price:.2f}\n{timestamp}"
    plt.text(0.05, 0.05, label, transform=plt.gca().transAxes, verticalalignment='bottom', bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})

    #plt.show()

    filename = "{}/plotting/_plots/{}_{}.png".format ( parent_dir, symbol, filename )
    plt.savefig ( filename )
    plt.clf()  # Clear the plot for the next iteration


