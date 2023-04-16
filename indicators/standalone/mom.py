import yfinance as yf
import pandas as pd

def __MOM (data, window=14):
    # Download the stock data using yfinance

    # Calculate the Momentum (MOM) indicator
    mom = pd.Series(data["Close"]).diff(window)

    # Add the MOM indicator to the DataFrame
    data["MOM"] = mom

    return data

# Define the stock symbol and timeframe
symbol = "AAPL"
window_mom = 14

data = yf.download(symbol, period="5y")

# Calculate the MOM indicator and print the current value
data = __MOM ( data , window_mom )
current_mom = data["MOM"].iloc[-1]

print("Current MOM value for", symbol, "is:", current_mom)


