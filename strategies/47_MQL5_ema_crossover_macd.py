# EMA, MACD
"""
@author: vita
This strategy uses the crossover between 9EMA and 21EMA with MACD histogram as confirmation to avoid false signals
http://www.forexfunction.com/trading-strategy-of-ema-crossover-with-macd
"""
data = __EMA ( data, 9 )
data = __EMA ( data, 21 )
data = __MACD ( data )

ema9 = data['EMA_9']
ema21 = data['EMA_21']
histogram = data['MACD_HIST']
close = data['Close']


# BUY CRITERIA: 9EMA crosses above 21EMA followed by a MACD histogram crossover ito positives
if (ema9.iloc[-2] > ema21.iloc[-2] and ema9.iloc[-3]<ema21.iloc[-3]) and ((histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0) or (histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0)):
    print_log ( '47_MQL5_ema_crossover_macd', 'LONG', [ 'EMA_9', 'EMA_21', 'MACD' ] )

# SELL CRITERIA: 9EMA crosses below 21EMA followed by a MACD histogram crossover into negatives
if (ema9.iloc[-2] < ema21.iloc[-2] and ema9.iloc[-3]>ema21.iloc[-3]) and ((histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0) or (histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0)):
    print_log ( '47_MQL5_ema_crossover_macd', 'SHORT', [ 'EMA_9', 'EMA_21', 'MACD' ] )
