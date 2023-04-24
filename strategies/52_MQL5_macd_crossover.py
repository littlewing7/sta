'''
@ Vita
https://www.dailyfx.com/forex/education/trading_tips/daily_trading_lesson/2020/01/09/macd-histogram.html

'''

data   = __MACD ( data )

macd   = data['MACD']
signal = data['MACD_SIGNAL']

# BUY CRITERIA: if MACD line has crossed signal line and are < 0
if (    macd.iloc[-1] < 0 and signal.iloc[-1] < 0 and macd.iloc[-2] < 0 and signal.iloc[-2] < 0 and
        macd.iloc[-3] < 0 and signal.iloc[-3] < 0) and \
    ( ( macd.iloc[-3] > signal.iloc[-3] and macd.iloc[-1] < signal.iloc[-1]) or ( macd.iloc[-3] < signal.iloc[-3] and macd.iloc[-1] > signal.iloc[-1])):
    print_log ( '52_MQL5_macd_crossover', 'LONG', [ 'MACD' ] )

# SELL CRITERIA: if MACD line has crossed signal line and are > 0
if (    macd.iloc[-1] > 0 and signal.iloc[-1] > 0 and macd.iloc[-2] > 0 and signal.iloc[-2] > 0 and macd.iloc[-3]>0 and signal.iloc[-3]>0) and \
    ( ( macd.iloc[-3] < signal.iloc[-3] and macd.iloc[-1] > signal.iloc[-1]) or (macd.iloc[-3] > signal.iloc[-3] and macd.iloc[-1] < signal.iloc[-1])):
    print_log ( '52_MQL5_macd_crossover', 'SHORT', [ 'MACD' ] )
