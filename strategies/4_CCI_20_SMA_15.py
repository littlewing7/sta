# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import os
import numpy as np
import pandas as pd
#from pandas import DataFrame


def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """

    csv_file = "./data/{}_1d.csv".format( stock )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if  ( ( os.path.exists ( csv_file ) ) and ( datetime.datetime.fromtimestamp ( os.path.getmtime ( csv_file ) ).date() == today ) ):
        data = pd.read_csv ( csv_file, index_col='Date' )
    else:
        # Download data
        data = yf.download(stock, start=start_date, progress=False)
        data.to_csv ( csv_file )

    # Calculate indicators
    data = __CCI ( data, 20 )
    data = __SMA ( data, 15 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):


        # Buy signal
        if ( position == 0 ) and ( data['CCI_20'][i-1] < -100 ) and ( data['CCI_20'][i] > -100 ) and ( data['Close'][i] > data['SMA_15'][i] ) and ( data['Close'][i - 1] < data['SMA_15'][i - 1]):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and ( data["CCI_20"][i-1] > 100  ) and ( data["CCI_20"][i] < 100 ) and ( data['Close'][i] < data['SMA_15'][i] ) and ( data['Close'][i - 1] > data['SMA_15'][i - 1]):
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000
    percentage = ( ( (total_returns - 100000) / 100000) * 100)
    percentage = "{:.0f}".format ( percentage )

    return percentage + '%'


# Optimal ticker interval for the strategy.
timeframe = '15m'

data = __CCI ( data, 20 )

if data['CCI_Signal'][-1] == 2:
    print_log ( '4_CCI_20_SMA_15', 'LONG', [ 'CCI_20', 'SMA_15' ], backtest_strategy ( ticker , '2020-01-01' ) )

if data['CCI_Signal'][-1] == -2:
    print_log ( '4_CCI_20_SMA_15', 'SHORT', [ 'CCI_20', 'SMA_15' ], backtest_strategy ( ticker , '2020-01-01' ) )
