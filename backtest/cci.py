#!/usr/bin/env python3

import argparse
import yfinance as yf
import pandas as pd

import numpy as np

import warnings
warnings.simplefilter ( action='ignore', category=Warning )


def __CCI(df, ndays = 20):
    df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['sma'] = df['TP'].rolling(ndays).mean()
    df['mad'] = df['TP'].rolling(ndays).apply(lambda x: pd.Series(x).mad())

    df['CCI_{}'.format(ndays)] = (df['TP'] - df['sma']) / (0.015 * df['mad'])

    df['CCI_CrossOverBought'] = np.where ( ( df['CCI_20'].shift(1) < 100)  & ( df['CCI_20'] >= 100),  1, 0 )
    df['CCI_CrossOverSold']   = np.where ( ( df['CCI_20'].shift(1) > -100) & ( df['CCI_20'] <= -100), 1, 0 )

    # 2 = LONG, -2 = SHORT
    #df['CCI_Signal'] = np.select(
    #    [ ( df['CCI_20'] > -100 ) & ( df['CCI_20'].shift(1) < -100 ),
    #      ( df['CCI_20'] <  100)  & ( df['CCI_20'].shift(1) >  100 ) ],
    #    [2, -2])


    df = df.drop('TP', axis=1)
    df = df.drop('sma', axis=1)
    df = df.drop('mad', axis=1)

    return df

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download ( stock, start=start_date, progress=False )

    # Calculate indicators
    data = __CCI ( data, 20 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( data['CCI_20'][i-1] < -100 ) & ( data['CCI_20'][i] > -100 ) and position == 0:
            position = 1
            buy_price = data["Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( data["CCI_20"][i-1] > 100 and data["CCI_20"][i] < 100 ) and position == 1:
            position = 0
            sell_price = data["Close"][i]
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
    print(f"{name} ::: {stock} - Total Returns: ${total_returns:,.2f}")
    print(f"{name} ::: {stock} - Profit/Loss: {((total_returns - 100000) / 100000) * 100:.2f}%")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('ticker', nargs='+',  type=str, help='your name')

    args = parser.parse_args()
    start_date = "2020-01-01"

    for symbol in args.ticker:

        backtest_strategy(symbol, start_date )
        print  ("\n")

