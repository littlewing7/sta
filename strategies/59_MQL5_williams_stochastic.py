# WilliamsStochastic
'''
This strategy uses the Williams%R Indicator and the stochastic signal line to determine buy and sell signals.
Results are compared for a 5 candle period, using williams indicator values of less than -65 for buy and greater
than -35 for sell, and less than or equal to 35 on the stochastic signal line to buy and greater than or equal to
65 to sell.
@author: Caitlin
'''

data = __STOCHASTIC ( data, 14, 3 )
data = __WR ( data, 14 )


# BUY SIGNAL: signal line is less than or equal to 35 and williams indicator is less than -65 within the last 5 candles
if ( ( ( data['STO_D'][-1] <= 35) | (data['STO_D'][-2] <= 35) | ( data['STO_D'][-3] <= 35) | (data['STO_D'][-4] <= 35) | (data['STO_D'][-5] <= 35) | ( data['STO_D'][-6] <= 35))
    & (( data['WR_14'][-1] < -65) | (data['WR_14'][-2] < -65) | ( data['WR_14'][-3] < -65) | (data['WR_14'][-4] < -65) | (data['WR_14'][-5] < -65) | ( data['WR_14'][-6] < -65))):
    print ("LONG ::: 59_MQL5_williams_stochastic")

# SELL SIGNAL: signal line is greater than or equal to 65 and williams indicator is greater than -35 within the last 5 candles
if ( ( ( data['STO_D'][-1] >= 65) | (data['STO_D'][-2] >= 65) | ( data['STO_D'][-3] >= 65) | (data['STO_D'][-4] >= 65) | (data['STO_D'][-5] >= 65) | ( data['STO_D'][-6] >= 65))
    & (( data['WR_14'][-1] > -35) | (data['WR_14'][-2] > -35) | ( data['WR_14'][-3] > -35) | (data['WR_14'][-4] > -35) | (data['WR_14'][-5] > -35) | ( data['WR_14'][-6] > -35))):
    print ("SHORT ::: 59_MQL5_williams_stochastic")
