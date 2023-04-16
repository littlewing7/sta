#!/usr/bin/env python3

import yfinance as yf

def calculate_EMA(data, window):
    ema = data['Close'].ewm(span=window, adjust=False).mean()
    return ema

# Download historical data for the past 5 years
symbol = 'AAPL'
data = yf.download(symbol, period='5y')

# Calculate EMA 9 and EMA 21
data['EMA9'] = calculate_EMA(data, 9)
data['EMA21'] = calculate_EMA(data, 21)

# Get the most recent two rows of data
recent_data = data.tail(2)

# Check for crossover events
if recent_data['EMA9'][0] > recent_data['EMA21'][0] and recent_data['EMA9'][1] <= recent_data['EMA21'][1]:
    print(f"Crossover event: {symbol} {recent_data.index[0].date()} EMA9 crossed over EMA21")
elif recent_data['EMA9'][0] < recent_data['EMA21'][0] and recent_data['EMA9'][1] >= recent_data['EMA21'][1]:
    print(f"Crossover event: {symbol} {recent_data.index[0].date()} EMA9 crossed under EMA21")
        
# Check for signal events
if recent_data['Close'][1] > recent_data['Close'][0] and recent_data['EMA9'][0] > recent_data['EMA21'][0]:
    print(f"Signal event: {symbol} {recent_data.index[0].date()} Yesterday's close price is below today's close price and 9 EMA is higher than 21 EMA")

print ( data.tail(5) )
