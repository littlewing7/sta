#!/usr/bin/env python3

import pandas as pd
import yfinance as yf

def calculate_macd(stock_data):
    # Calculate the MACD line and signal line
    ema12 = stock_data["Close"].ewm(span=12, adjust=False).mean()
    ema26 = stock_data["Close"].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    # Find the MACD crossover and crossunder
    macd_crossover = (macd > signal) & (macd.shift(1) < signal.shift(1))
    macd_crossunder = (macd < signal) & (macd.shift(1) > signal.shift(1))

    return macd, signal, macd_crossover, macd_crossunder

# Define the stock symbol and timeframe
symbol = "AAPL"

# Download the stock data using yfinance
stock_data = yf.download(symbol, period='5y')

# Calculate the MACD
macd, signal, macd_crossover, macd_crossunder = calculate_macd(stock_data)

# Check if the lines intersected above 0
intersected_above_0 = (macd_crossover & (macd > 0)).any()

# Check if the lines intersected below 0
intersected_below_0 = (macd_crossunder & (macd < 0)).any()

if intersected_above_0:
    print("MACD lines intersected above 0")

if intersected_below_0:
    print("MACD lines intersected below 0")

