#!/usr/bin/env python3
import yfinance as yf
import numpy as np

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    # Calculate the exponential moving averages (EMAs)
    ema_fast = data["Close"].ewm(span=fast_period, adjust=False).mean()
    ema_slow = data["Close"].ewm(span=slow_period, adjust=False).mean()

    # Calculate the MACD line
    macd_line = ema_fast - ema_slow

    # Calculate the signal line
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    # Add the MACD and signal lines to the dataframe
    data["MACD"] = macd_line
    data["Signal"] = signal_line

    return data

# Download historical data for a stock
symbol = "AAPL"
data = yf.download(symbol, period='5y')

# Calculate the MACD and signal lines using the calculate_macd function
data = calculate_macd(data)

## Find the MACD crossover and crossunder
#macd_crossover = (macd > signal) & (macd.shift(1) < signal.shift(1))
#macd_crossunder = (macd < signal) & (macd.shift(1) > signal.shift(1))

# Get the most recent day and the previous day in the dataframe
today_data = data.iloc[-1]
yesterday_data = data.iloc[-2]

# Check if the MACD line crossed above or below the signal line on the most recent day
if today_data["MACD"] > today_data["Signal"] and yesterday_data["MACD"] <= yesterday_data["Signal"]:
    print("MACD crossed above signal on", today_data.name)
elif today_data["MACD"] < today_data["Signal"] and yesterday_data["MACD"] >= yesterday_data["Signal"]:
    print("MACD crossed below signal on", today_data.name)

# Print the full dataframe with MACD and signal lines
print(data.tail(5))

