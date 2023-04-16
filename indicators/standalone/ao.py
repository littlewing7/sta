import yfinance as yf
import pandas as pd

def __AO ( data, window1=5, window2=34 ):
    """
    Calculates the Awesome Oscillator for a given DataFrame containing historical stock data.

    Parameters:
        data (pandas.DataFrame): DataFrame containing the historical stock data.
        window1 (int): Window size for the first simple moving average (default is 5).
        window2 (int): Window size for the second simple moving average (default is 34).

    Returns:
        data (pandas.DataFrame): DataFrame with an additional column containing the Awesome Oscillator.
    """
    # Calculate the Awesome Oscillator (AO)
    high = data["High"]
    low = data["Low"]
    median_price = (high + low) / 2
    ao = median_price.rolling(window=window1).mean() - median_price.rolling(window=window2).mean()

    # Add the AO to the DataFrame
    data["AO"] = ao

    return data

# Download data for a particular stock
stock = yf.Ticker("AAPL")
data = stock.history(period="5y")

# Calculate the Awesome Oscillator and print the last few rows
data = __AO (data, 5, 34)
print(data.tail())

