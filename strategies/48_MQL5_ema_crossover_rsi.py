# EMA, RSI
data = __EMA ( data, 6 )
data = __EMA ( data, 12 )
data = __RSI ( data, 14 )

ema6  = data['EMA_6']
ema12 = data['EMA_12']
rsi   = data['RSI_14']
close = data['Close']

# SELL CRITERIA: when 6EMA crosses above 12EMA and RSI value has crossed below 50
if (ema6.iloc[-1] < ema12.iloc[-1] and ema6.iloc[-2] > ema12.iloc[-2]) and ( rsi.iloc[-1] < 50 and rsi.iloc[-2] > 50):
    print ( f"{ticker} {interval} ---> LONG ::: 48_MQL5_ema_crossover_rsi\n")

# BUY CRITERIA: when 6EMA crosses below 12EMA and RSI value has crossed above 50
if (ema6.iloc[-1] > ema12.iloc[-1] and ema6.iloc[-2] < ema12.iloc[-2]) and ( rsi.iloc[-1] > 50 and rsi.iloc[-2] < 50):
    print ( f"{ticker} {interval} ---> SHORT ::: 48_MQL5_ema_crossover_rsi\n")


'''
This strategy combines ema_crossover_rsi_alternative and a modified ema_crossover_macd to determine buy and sell
signals. Ema_crossover_macd was modified such that 9EMA only needs to be below/above 21EMA to fulfill sell/buy
signals respectively rather than a crossover below or above.
'''
for i in [ 6, 9, 12, 21 ]:
    data = __EMA ( data, i )
data = __RSI ( data, 14 )
data = __MACD ( data )

close = data['Close']
ema6  = data['EMA_6']
ema9  = data['EMA_9']
ema12 = data['EMA_12']
ema21 = data['EMA_21']
histogram = data['MACD_HIST']
rsi = data['RSI_14']

# BUY CRITERIA: 9EMA crosses above 21EMA followed by a MACD histogram crossover ito positives
if ((ema9.iloc[-2] > ema21.iloc[-2]) and (
    (histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0) or (histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0))) \
    or ((ema6.iloc[-1] > ema12.iloc[-1]) and (rsi.iloc[-1] > 50)):
    print_log ( '20_AO_SAUCER', 'LONG', [ 'EMA_6', 'EMA_9', 'EMA_21', 'MACD', 'RSI' ] )

# SELL CRITERIA: 9EMA crosses below 21EMA followed by a MACD histogram crossover into negatives
if ((ema9.iloc[-2] < ema21.iloc[-2]) and (
    (histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0) or (histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0))) \
    or ((ema6.iloc[-1] < ema12.iloc[-1]) and (rsi.iloc[-1] < 50)):
    print_log ( '20_AO_SAUCER', 'SHORT', [ 'EMA_6', 'EMA_9', 'EMA_21', 'MACD', 'RSI' ] )

