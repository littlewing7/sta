#!/usr/bin/env python3

import argparse
import yfinance as yf
import pandas as pd
import numpy as np

import os, datetime

import warnings
warnings.simplefilter ( action='ignore', category=Warning )

def append_to_log(logfile, line):
    with open(logfile, 'a') as file:
        file.write(line + '\n')

def __CCI(df, ndays = 20):
    df['TP'] = (df['High'] + df['Low'] + df['Adj Close']) / 3
    df['sma'] = df['TP'].rolling(ndays).mean()
    df['mad'] = df['TP'].rolling(ndays).apply(lambda x: np.abs(x - x.mean()).mean())

    df['CCI_20'] = (df['TP'] - df['sma']) / (0.015 * df['mad'])

    df = df.drop('TP', axis=1)
    df = df.drop('sma', axis=1)
    df = df.drop('mad', axis=1)


    cci_upper_level  =  100
    cci_lower_level  =  (-100)
    cci_window = 20

    df['CCI_Signal'] = np.select(
        [ ( df['CCI_{}'.format(cci_window)].shift(1) < cci_lower_level ) & ( df['CCI_{}'.format(cci_window)] > cci_lower_level ) ,
          ( df['CCI_{}'.format(cci_window)].shift(1) > cci_upper_level ) & ( df['CCI_{}'.format(cci_window)] < cci_upper_level ) ],
        [2, -2])

    return df

def __WR (data, t):
    highh = data["High"].rolling(t).max()
    lowl  = data["Low"].rolling(t).min()
    close = data["Adj Close"]

    data['WR_{}'.format(t)] = -100 * ((highh - close) / (highh - lowl))


    wr_window      = 20
    wr_upper_level = -20
    wr_lower_level = -80

    # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
    data['WR_Signal'] = np.select(
         [ ( data['WR_{}'.format(wr_window)].shift(1) > wr_upper_level ) & ( data['WR_{}'.format(wr_window)] < wr_upper_level ),
           ( data['WR_{}'.format(wr_window)].shift(1) < wr_lower_level ) & ( data['WR_{}'.format(wr_window)] > wr_lower_level )],
         [-2, 2])

    return data



def backtest_strategy(stock, start_date, logfile ):
    """
    Function to backtest a strategy
    """

    csv_file = "../data/{}_1d.csv".format( stock )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if  ( ( os.path.exists ( csv_file ) ) and ( datetime.datetime.fromtimestamp ( os.path.getmtime ( csv_file ) ).date() == today ) ):
        data = pd.read_csv ( csv_file, index_col='Date' )
    else:
        # Download data
        data = yf.download(stock, start=start_date, progress=False)
        data.to_csv ( csv_file )


    # Calculate Stochastic RSI
    data = __CCI ( data, 20 )
    data = __WR ( data, 20 )

    #print ( data.tail(60))

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []


    # Loop through data
    for i in range(len(data)):
        go_long  = 0
        go_short = 0

        if ( data['CCI_Signal'][i] == 2 ):
            go_long += 1
        if ( data['WR_Signal'][i] == 2 ):
            go_long += 1

        if ( data['CCI_Signal'][i] == -2 ):
            go_short += 1
        if ( data['WR_Signal'][i] == -2 ):
            go_short += 1

        # Buy signal
        #if ( data['MFI_Signal'][i] == 2 and  (position == 0 )):
        if ( go_long >= 2 and  (position == 0 )):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        #elif ( data['MFI_Signal'][i] == -2 and  (position == 1 )):
        elif ( go_short >= 2 and ( position == 1 )):
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000

    import sys
    name = sys.argv[0]

    # Print results
    print(f"\n{name} ::: {stock} Backtest Results ({start_date} - today)")
    print(f"---------------------------------------------")
    print(f"{name} ::: {stock} - Total Returns: ${total_returns:,.0f}")
    print(f"{name} ::: {stock} - Profit/Loss: {((total_returns - 100000) / 100000) * 100:.0f}%")

    append_line = (f"{name} ::: {stock} - Profit/Loss: {((total_returns - 100000) / 100000) * 100:.0f}%")
    append_to_log ( logfile, append_line )

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--ticker', nargs='+', required=True,  type=str, help='ticker')
    parser.add_argument('-l', '--logfile',  required=True, type=str, help='ticker')

    args = parser.parse_args()
    start_date = "2020-01-01"

    for symbol in args.ticker:

        backtest_strategy(symbol, start_date, args.logfile )

