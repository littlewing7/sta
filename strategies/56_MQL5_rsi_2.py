'''
Larry Connors' 2 period RSI strategy uses mean reversion to provide a short-term buy or sell signal.
When the price is above the 200 Moving Average, and 2-period RSI is below 10, this is a buy signal
When the price is below the 200 Moving Average, and 2-period RSI is above 90, this is a sell signal
'''
data = __SMA ( data, 5 )
data = __SMA ( data, 200 )
data = __RSI ( data, 14 )
data = __RSI ( data, 2 )

# Buy when RSI2 between 0 and 10, and price above 200sma but below 5sma
if data['RSI_2'].iloc[-1] < 10 and data['Close'].iloc[-1] > data['SMA_200'].iloc[-1] and data['Close'].iloc[-1] < data['SMA_5'].iloc[-1]:
    print ("LONG ::: 56_MQL5_rsi_2\n")

# Sell when RSI2 between 90 and 100, and price below 200sma but above 5sma
if data['RSI_2'].iloc[-1] > 90 and data['Close'].iloc[-1] < data['SMA_200'].iloc[-1] and data['Close'].iloc[-1] > data['SMA_5'].iloc[-1]:
    print ("SHORT ::: 56_MQL5_rsi_2\n")

