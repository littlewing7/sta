# MacdRsiSma
"""
@author: caitlin and vita
This strategy combines 3 different indicators: MACD, RSI and SMA in order to determine buy and sell signals
The Moving Average Convergence Divergence (MACD) is a trend following momentum indicator that displays
the relation between 2 moving averages. This strategy uses the macd signal and macd line, where the signal
line trails the macd.
The Relative Strength Index (RSI) is a momentum indicator measuring speed and change of price movements.
The 5 period simple moving average is good for short term trading.
The goal of combining these indicators is to determine more accurate buy/sell signals than any provide by themselves.
"""
data = __SMA ( data, 5 )
data = __MACD ( data )
data = __RSI ( data, 14 )

sma_5       = data['SMA_5']
macd_line   = data['MACD']
macd_signal = data['MACD_SIGNAL']
rsi         = data['RSI_14']
close       = data['Close']

# buy if close price is higher than the moving average, rsi reads less than 30 and the macd line crosses up through macd signal line
if (  sma_5.iloc[-1] < close.iloc[-1]) and (macd_line.iloc[-2] < macd_signal.iloc[-2]) and \
    ( macd_line.iloc[-1] > macd_signal.iloc[-1]) and (macd_line.iloc[-1] < 0 and rsi.iloc[-1] < 30):
    print_log ( '53_MQL5_macd_rsi_sma', 'LONG', [ 'MACD', 'RSI_14', 'SMA_5' ] )

# sell if close price less than moving average, rsi reads over 70, and macd line crosses down through signal line
if (  close.iloc[-1] < sma_5.iloc[-1]) and (macd_line.iloc[-1] > 0 and rsi.iloc[-1] > 70) and \
    ( macd_line.iloc[-2] > macd_signal.iloc[-2]) and (macd_line.iloc[-1] < macd_signal.iloc[-1]):
    print_log ( '53_MQL5_macd_rsi_sma', 'SHORT', [ 'MACD', 'RSI_14', 'SMA_5' ] )
