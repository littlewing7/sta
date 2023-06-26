
import argparse

import yfinance as yf
import pandas as pd

# Define the ticker symbol
tickerSymbol = 'AAPL'

# Define function to calculate the CMO indicator and add it to the DataFrame
def __CMO (df, periods=14):
    tp = (df['High'] + df['Low'] + df['Adj Close']) / 3
    cmo = (tp - tp.shift(periods)) / (tp + tp.shift(periods)) * 100
    df['CMO'] = cmo
    return df

# Define overbought and oversold levels
overbought_level = 50
oversold_level = -50

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)

    # Calculate the CMO indicator using the function
    data = __CMO (data, 14)

    # Check if CMO crosses overbought or oversold levels and print a message
    if data['CMO'][-2] <= oversold_level and data['CMO'][-1] > oversold_level:
        print("CMO crossed above oversold level at", data.index[-1])
    elif data['CMO'][-2] >= overbought_level and data['CMO'][-1] < overbought_level:
        print("CMO crossed below overbought level at", data.index[-1])

    # Print the DataFrame with the CMO column added
    print(data)

