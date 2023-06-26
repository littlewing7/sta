#!/usr/bin/env python3

import argparse

import os,sys,datetime
import yfinance as yf
import pandas as pd
pd.set_option('display.precision', 2)

#sys.path.insert(0, '../utils')
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.append("..")


################################
#####  External functions  #####
################################

#def __EMA (df, window=9):
from util.ema   import __EMA


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:

    csv_file = "../data/{}_1d.csv".format( symbol )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if os.path.exists(csv_file) and (lambda file_path: datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < datetime.timedelta(minutes=60))(csv_file):
        data = pd.read_csv ( csv_file, index_col='Date' )
    else:
        # Download data
        data = yf.download(symbol, start=start_date, progress=False)
        data.to_csv ( csv_file )

    # Calculate EMA 9 and EMA 21
    data  = __EMA (data, 9)
    data  = __EMA (data, 21)

    # Get the most recent two rows of data
    recent_data = data.tail(2)

    # Check for crossover events
    if recent_data['EMA_9'][0] > recent_data['EMA_21'][0] and recent_data['EMA_9'][1] <= recent_data['EMA_21'][1]:
        print(f"Crossover event: {symbol} {recent_data.index[0].date()} EMA_9 crossed over EMA_21")
    elif recent_data['EMA_9'][0] < recent_data['EMA_21'][0] and recent_data['EMA_9'][1] >= recent_data['EMA_21'][1]:
        print(f"Crossover event: {symbol} {recent_data.index[0].date()} EMA_9 crossed under EMA_21")

    # Check for signal events
    if recent_data['Adj Close'][1] > recent_data['Adj Close'][0] and recent_data['EMA_9'][0] > recent_data['EMA_21'][0]:
        print(f"Signal event: {symbol} {recent_data.index[0].date()} Yesterday's close price is below today's close price and 9 EMA is higher than 21 EMA")

    print ( recent_data )
