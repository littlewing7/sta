data = __SMA ( data, 5 )
data = __EMA ( data, 13 )

data['bull_power'] = data['High'] - data['EMA_13']

data['bear_power'] = data['Low'] - data['EMA_13']

ema_dist = data['Adj Close'].iloc[-1] - data['EMA_13'].iloc[-1]

# BUY CRITERIA: Bear power’s value is negative but increasing, Bull power’s value is increasing and 13 EMA is increasing. AND price is greater than 5 sma
if  data['bear_power'].iloc[-1] < 0 and data['bear_power'].iloc[-1] > data['bear_power'].iloc[-2] \
    and data['bull_power'].iloc[-1] > data['bull_power'].iloc[-2] and data['EMA_13'].iloc[-1] > data['EMA_13'].iloc[-2] \
    and data['Adj Close'].iloc[-1] > data['SMA_5'].iloc[-1]:
    print_log ( '46_MQL5_elder_ray3', 'LONG', [ 'SMA_5', 'EMA_13' ] )

# SELL CRITERIA: Bull power’s value is positive but decreasing,  Bear power’s value is decreasing and 13 EMA is decreasing. AND price is less than 5 sma
if data['bull_power'].iloc[-1] > 0 and data['bull_power'].iloc[-1] < data['bull_power'].iloc[-2] \
    and data['bear_power'].iloc[-1] < data['bear_power'].iloc[-2] and data['EMA_13'].iloc[-1] < data['EMA_13'].iloc[-2] \
    and data['Adj Close'].iloc[-1] < data['SMA_5'].iloc[-1]:
    print_log ( '46_MQL5_elder_ray3', 'SHORT', [ 'SMA_5', 'EMA_13' ] )

