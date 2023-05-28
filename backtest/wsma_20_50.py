#!/usr/bin/env python3

import argparse
import yfinance as yf
import pandas as pd
import numpy as np

import os, datetime

#def __SMA ( data, n ):
#    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
#    return data

def __WSMA( data, n):
    weights = np.arange(1, n+1)
    wma = data['Close'].rolling(n).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
    data['WSMA_{}'.format(n)] = pd.Series(wma)

    return data


def backtest_strategy(stock, start_date):
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
    data = __WSMA (data, 20)
    data = __WSMA (data, 50)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["WSMA_20"][i] > data["WSMA_50"][i] and data["WSMA_20"][i - 1] < data["WSMA_50"][i - 1] and position == 0:
            position = 1
            buy_price = data["Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["WSMA_20"][i] < data["WSMA_50"][i] and data["WSMA_20"][i - 1]  > data["WSMA_50"][i - 1] and position == 1:
            position = 0
            sell_price = data["Close"][i]
            today = data.index[i]
            #print(f"Selling {stock} at {sell_price} @ {today}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000

    import sys
    name = sys.argv[0]

    # Print results
    print(f"\n{name} ::: {stock} Backtest Results ({start_date} - today)")
    print(f"---------------------------------------------")
    print(f"{name} ::: {stock} - Total Returns: ${total_returns:,.2f}")
    print(f"{name} ::: {stock} - Profit/Loss: {((total_returns - 100000) / 100000) * 100:.2f}%")

    #import matplotlib.pyplot as plt
    #plt.style.use('fivethirtyeight')
    #plt.rcParams['figure.figsize'] = (15, 8)

    #plt.plot(data['Close'],   label='AAPL', linewidth=5, alpha=0.3)
    #plt.plot(data['WSMA_20'], label='SMA 20')
    #plt.plot(data['WSMA_50'], label='SMA 50')
    #plt.title('AAPL Weighted Simple Moving Averages (20, 50)')
    #plt.legend(loc='upper left')
    #plt.show()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--ticker', nargs='+',  type=str, help='ticker')

    args = parser.parse_args()
    start_date = "2020-01-01"

    for symbol in args.ticker:

        backtest_strategy(symbol, start_date )
        print  ("\n")

