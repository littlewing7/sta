# https://github.com/WaveyTechLtd/Stock_market_trader_EMA_RSI_ATR
"""
17/01/2021
Code which trys to back test strategy in this video ... https://www.youtube.com/watch?v=7NM7bR2mL7U
Required info is 
- 50EMA 
- 14EMA 
- 8EMA
- Stocastic RSI (K=3, D=3, RSI_length=14, Stocastic_length=14, source=close) 
- ATR - length 14, RMA smoothing
- He was using EURUSD market, not individual stocks
- buying stocks forces you to trade n=1 stock minium, rather than always a percentage of your capital?

# For a Long position 
(1) 8EMA > 14EMA > 50EMA, indicates upward trend
(2) Stocastic cross over
(3) Adj Close > all EMAs

Target is 2 x ATR value, stop loss is 3 x ATR value

# For a short position
(1) 8EMA < 14EMA < 50EMA
(2) Stocastic cross over
(3) Close < all EMAs
Target 2 x ATR value, stop loss is 3 x ATR value.

#############
He reported a 76% win rate over 100 trades ... lets find out if I get the same 
The adjusted closing price amends a stock's closing price to reflect that stock's value after accounting for any corporate actions (stock splits, dividends etc)
More accurate reflection of the value of the stock at the historical time
Use this instead of Close price, better for back testing.
"""

data = __RSI ( data, 14 )

data["ATR"] = __ATR ( data, 14 )

data = __EMA ( data, 50 )
data = __EMA ( data, 14 )
data = __EMA ( data, 8 )
data = __STOCHASTIC (data, 14, 3)

if ( ( ( data["EMA_8"][-1]   > data["EMA_14"][-1] ) & ( data["EMA_8"][-1] > data["EMA_50"][-1] ) & ( data["EMA_14"][-1] > data["EMA_50"][-1] ) )
    &  ( data['Close'][-1]   > data['EMA_8'][-1] )
    &  ( data['STO_Signal'].iloc[-1] == 2 ) ):
    print ("LONG ::: 70_3EMA_RSI_ATR\n")

if ( ( ( data['EMA_8'][-1]     < data['EMA_14'][-1] ) and ( data['EMA_8'][-1] < data['EMA_50'][-1] ) and ( data['EMA_14'][-1] < data['EMA_50'][-1] ) )
    & (  data['Adj Close'][-1] < data['EMA_8'][-1] )
    &  ( data['STO_Signal'].iloc[-1] == -2 ) ):
    print ("SHORT ::: 70_3EMA_RSI_ATR\n")

