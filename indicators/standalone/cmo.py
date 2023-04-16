import yfinance as yf
import pandas as pd

# Define the ticker symbol
tickerSymbol = 'AAPL'

# Define function to calculate the CMO indicator and add it to the DataFrame
def __CMO (df, periods=14):
    tp = (df['High'] + df['Low'] + df['Close']) / 3
    cmo = (tp - tp.shift(periods)) / (tp + tp.shift(periods)) * 100
    df['CMO'] = cmo
    return df

# Define overbought and oversold levels
overbought_level = 50
oversold_level = -50

# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# Get the historical prices for this ticker
tickerDf = tickerData.history(period='5y')

# Calculate the CMO indicator using the function
tickerDf = __CMO (tickerDf, 14)

# Check if CMO crosses overbought or oversold levels and print a message
if tickerDf['CMO'][-2] <= oversold_level and tickerDf['CMO'][-1] > oversold_level:
    print("CMO crossed above oversold level at", tickerDf.index[-1])
elif tickerDf['CMO'][-2] >= overbought_level and tickerDf['CMO'][-1] < overbought_level:
    print("CMO crossed below overbought level at", tickerDf.index[-1])

# Print the DataFrame with the CMO column added
print(tickerDf)

