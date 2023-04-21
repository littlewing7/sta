data       = __ADX ( data , 14 )

# BUY SIGNAL: adx is above 25 and the positive DI crosses over negative DI indicates a strong uptrend
if data['ADX_14'].iloc[-1] > 25 and data['ADX_14_plus_di'].iloc[-1] > data['ADX_14_minus_di'].iloc[-1] and data['ADX_14_plus_di'].iloc[-2] <= data['ADX_14_minus_di'].iloc[-2]:
    print ( f"{ticker} {interval} ---> LONG ::: S40_MQL5_adx_crossover\n")

# SELL SIGNAL: adx is above 25 and the negative DI crosses over positive DI indicates a strong downtrend
if data['ADX_14'].iloc[-1] > 25 and data['ADX_14_plus_di'].iloc[-1] < data['ADX_14_minus_di'].iloc[-1] and data['ADX_14_plus_di'].iloc[-2] >= data['ADX_14_minus_di'].iloc[-2]:
    print ( f"{ticker} {interval} ---> SHORT S40_MQL5_adx_crossover\n")

