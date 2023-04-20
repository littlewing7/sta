'''
The Elder Ray Index measures the amount of buying and selling power in a market with two indicators: Bull Power and Bear Power.
This index is used in conjunction with a 21 EMA to further gauge the trend.
We buy when Bear Power is negative but increasing, Bull Power is increasing and EMA is positively sloped.
We sell when Bull Power is positive but decreasing, Bear Power is decreasing and EMA is negatively sloped.

Author: Cheryl
'''

data = __EMA ( data, 13 )

data['bull_power'] = data['High'] - data['EMA_21']
data['bear_power'] = data['Low'] - data['EMA_21']

ema_dist = data['Close'].iloc[-1] - data['EMA_21'].iloc[-1]

# BUY CRITERIA: price is above 13-EMA and both EMA and Bear Power is increasing
if data['Close'].iloc[-1] > data['EMA_13'].iloc[-1] and data['EMA_13'].iloc[-1] > data['EMA_13'].iloc[-2] and data['bear_power'].iloc[-1] > data['bear_power'].iloc[-2]:
    print ( "LONG ::: 46_MQL5_elder_ray 2\n")

# SELL CRITERIA: price is below 13-EMA and both EMA and Bull Power is decreasing
if data['Close'].iloc[-1] < data['EMA_13'].iloc[-1] and data['EMA_13'].iloc[-1] < data['EMA_13'].iloc[-2] and data['bull_power'].iloc[-1] < data['bull_power'].iloc[-2]:
    print ( "SHORT ::: 46_MQL5_elder_ray 2\n")

