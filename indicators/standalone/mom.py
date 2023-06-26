
import argparse

import yfinance as yf
import pandas as pd

def __MOM (data, window=14):
    # Download the stock data using yfinance

    # Calculate the Momentum (MOM) indicator
    mom = pd.Series(data["Adj Close"]).diff(window)

    # Add the MOM indicator to the DataFrame
    data["MOM"] = mom

    return data

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    data = yf.download ( symbol, start=start_date, progress=False)

    window_mom = 14

    # Calculate the MOM indicator and print the current value
    data = __MOM ( data , window_mom )
    current_mom = data["MOM"].iloc[-1]

    print("Current MOM value for", symbol, "is:", current_mom)


