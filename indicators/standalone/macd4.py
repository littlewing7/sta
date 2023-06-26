#!/usr/bin/env python3

import argparse

import pandas as pd
import yfinance as yf

def calculate_macd(stock_data):
    # Calculate the MACD line and signal line
    ema12 = stock_data['Adj Close'].ewm(span=12, adjust=False).mean()
    ema26 = stock_data['Adj Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    # Find the MACD crossover and crossunder
    macd_crossover = (macd > signal) & (macd.shift(1) < signal.shift(1))
    macd_crossunder = (macd < signal) & (macd.shift(1) > signal.shift(1))

    return macd, signal, macd_crossover, macd_crossunder

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker', nargs='+',  type=str, required=True, help='ticker')

args = parser.parse_args()
start_date = "2020-01-01"

for symbol in args.ticker:


    stock_data = yf.download ( symbol, start=start_date, progress=False)
        
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

