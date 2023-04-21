'''
The Elder Ray Index measures the amount of buying and selling power in a market with two indicators: Bull Power and Bear Power.
This index is used in conjunction with a 21 EMA to further gauge the trend.
We buy when Bear Power is negative but increasing, Bull Power is increasing and EMA is positively sloped.
We sell when Bull Power is positive but decreasing, Bear Power is decreasing and EMA is negatively sloped.

Author: Cheryl
'''

data = __EMA ( data, 21 )

data['bull_power'] = data['High'] - data['EMA_21']
data['bear_power'] = data['Low'] - data['EMA_21']

ema_dist = data['Close'].iloc[-1] - data['EMA_21'].iloc[-1]

# BUY CRITERIA: Bear power’s value is negative but increasing, Bull power’s value is increasing and 21 EMA is increasing.
if data['bear_power'].iloc[-1] < 0 and data['bear_power'].iloc[-1] > data['bear_power'].iloc[-2] \
    and data['bull_power'].iloc[-1] > data['bull_power'].iloc[-2] and data['EMA_21'].iloc[-1] > data['EMA_21'].iloc[-2] :
    print ( f"{ticker} {interval} ---> LONG ::: 46_MQL5_elder_ray\n")

# SELL CRITERIA: Bull power’s value is positive but decreasing,  Bear power’s value is decreasing and 21 EMA is decreasing.
if data['bull_power'].iloc[-1] > 0 and data['bull_power'].iloc[-1] < data['bull_power'].iloc[-2] \
   and data['bear_power'].iloc[-1] < data['bear_power'].iloc[-2] and data['EMA_21'].iloc[-1] < data['EMA_21'].iloc[-2] :
    print ( f"{ticker} {interval} ---> SHORT ::: 46_MQL5_elder_ray\n")

