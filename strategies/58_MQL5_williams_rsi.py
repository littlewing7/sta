# WilliamsRsi
"""
@author: caitlin
This strategy uses the Williams%R indicator. This momentum indicator oscillates between 0 and -100, and shows
how the current price compares to a 14 day look back period, where a reading near -100 indicates the market is
near the lowest low and a reading near 0 indicates the market is near the highest high. This strategy combines
an 8 period rsi.
"""
high = data['High']
low = data['Low']
close = data['Close']

data = __RSI ( data, 8 )
data = __WR ( data, 14 )

# BUY signal: when williams indicator is less than -70 and rsi is less than 30 within the last 3 candles
if ( ( ( data['WR_14'][-3] < -70) | (data['WR_14'][-2] < -70) | (data['WR_14'][-1] < -70) | (data['WR_14'][-4] < -70))
    & (( data['RSI_8'][-1] < 30) | (data['RSI_8'][-2] < 30) | (data['RSI_8'][-3] < 30)) ):
    print ( f"{ticker} {interval} ---> LONG ::: 58_MQL5_williams_rsi\n")

# SELL signal: when williams indicator is greater than -30 and rsi is greater than 70 within last 3 candles
if ( ( ( data['WR_14'][-3] > -30) | (data['WR_14'][-2] > -30) | (data['WR_14'][-1] > -30) | (data['WR_14'][-4] > -30))
    & ((data['RSI_8'][-1] > 70) | (data['RSI_8'][-2] > 70) | (data['RSI_8'][-3] > 70)) ):
    print ( f"{ticker} {interval} ---> SHORT ::: 58_MQL5_williams_rsi\n")


