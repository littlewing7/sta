# ADX RSI https://github.com/Amar0628/MQL5-Python-Backtesting/tree/929e492930347ce660931a4998dfc991feceac49/trading_strategies
'''
### Author:Vita ###
Strategy from:
https://forextester.com/blog/adx-14-ema-strategy
This strategy uses ADX and 14EMA for buy and sell signals
'''
data = __EMA ( data, 14 )

if (data["Close"].iloc[-1] > data["Open"].iloc[-1]) and ( data["Close"].iloc[-1] > data["EMA_14"].iloc[-1]) and ( data["ADX_14"].iloc[-2] < 25 and data["ADX_14"].iloc[-1] > 25):
    print ( f"{ticker} {interval} ---> LONG ADX_RSI\n")

# SELL CRITERIA: if candlestick is bearish, close is less than 14 EMA and ADX indicator has crossed above 25:
if ( data["Open"].iloc[-1] > data["Close"].iloc[-1]) and ( data["Close"].iloc[-1] < data["EMA_14"].iloc[-1]) and ( data["ADX_14"].iloc[-2] < 25 and data["ADX_14"].iloc[-1] > 25):
    print ( f"{ticker} {interval} ---> SHORT ::: 41_ADX_RSI\n")


