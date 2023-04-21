# awesome saucer
'''
The Awesome Oscillator Saucers strategy looks for a bullish or bearish saucer pattern in the Awesome Oscillator, where close price is greater than 200 EMA.
A bullish saucer pattern consists of 3 positive AO bars which form the curve of a saucer (i.e. the middle value is smallest).
A bearish saucer patter consists of 3 negative AO bars which form the curve of an upside down saucer (i.e. the middle value is greatest (least negative)).
Author: Cheryl
'''
data = __EMA ( data, 200 )
ema_dist = data['Close'].iloc[-1] - data['EMA_200'].iloc[-1]

bar_1 = data['AO'].iloc[-3]
bar_2 = data['AO'].iloc[-2]
bar_3 = data['AO'].iloc[-1]

curr_close = data['Close'].iloc[-1]
curr_200ema = data['EMA_200'].iloc[-1]

# BUY CRITERIA: CONSECUTIVELY: all 3 bars positive, 2 decreasing awesome oscillator values followed by an increase, and close is above the 200EMA
if bar_1 > 0 and bar_2 > 0 and bar_3 > 0 and \
    bar_1 > bar_2 and bar_2 < bar_3 and curr_close > curr_200ema:
    print ( f"{ticker} {interval} ---> LONG ::: 20_AO_SAUCER\n")

# SELL CRITERIA: CONSECUTIVELY: all 3 bars negative, 2 increasing awesome oscillator values followed by a decrease, and close is below the 200EMA
if bar_1 < 0 and bar_2 < 0 and bar_3 < 0 and\
    bar_1 < bar_2 and bar_2 > bar_3 and curr_close < curr_200ema:
    print ( f"{ticker} {interval} ---> SHORT :::  20_AO_SAUCER\n")
