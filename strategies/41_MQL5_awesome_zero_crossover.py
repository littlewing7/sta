# AO CROSSOVER https://github.com/Amar0628/MQL5-Python-Backtesting/tree/929e492930347ce660931a4998dfc991feceac49/trading_strategies 

data = __AO ( data, 5, 34 )

'''
The Awesome Oscillator Zero Crossover strategy signals buying and selling opportunities when the Awesome Oscillator (AO) crosses to above or below 0.
When the AO crosses above 0, we wait for 3 consecutive increasing values of AO to confirm bullish movement and then buy. 
When the AO crosses below 0, we wait for 3 consecutive decreasing values of AO to confirm bearish movement and then sell.
Author: Cheryl
'''
# BUY CRITERIA: awesome oscillator crosses from below to above the zero line, followed by 3 increasing values
if  data['AO'].iloc[-4] <= 0 and data['AO'].iloc[-3] >= 0 and \
    data['AO'].iloc[-2] > data['AO'].iloc[-3] and \
    data['AO'].iloc[-1] > data['AO'].iloc[-2]:
    print ("LONG ::: 41_MQL5_awesome_zero_crossover\n") 

# SELL CRITERIA: awesome oscillator crosses from above to below the zero line, followed by 3 decreasing values
if data['AO'].iloc[-4]  >= 0 and data['AO'].iloc[-3] <= 0 and \
    data['AO'].iloc[-2] < data['AO'].iloc[-3] and \
    data['AO'].iloc[-1] < data['AO'].iloc[-2]:
    print ("SHORT ::: 41_MQL5_awesome_zero_crossover\n")

