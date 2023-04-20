data = __KC ( data )
data = __ADX ( data, 14 )

# BUY SIGNAL: candle close is below lower keltner band, stochastic signal is <=20, psar is below the candle
if ((data['High'][-1] < data['KC_lower'][-1] ) & ( data['STO_K'][-1] <= 20 ) & ( data['ADX_14'][-1] >= 20)):
    print ("LONG ::: 49_MQL5_k_stoch_adx\n")

# SELL SIGNAL: candle close above upper keltner band, stochastic signal >= 80, psar below candle
if ((data['Low'][-1] > data['KC_upper'][-1] ) & ( data['STO_K'][-1] >= 80 ) & ( data['ADX_14'][-1] >= 20) ):
    print ("SHORT ::: 49_MQL5_k_stoch_adx\n")

