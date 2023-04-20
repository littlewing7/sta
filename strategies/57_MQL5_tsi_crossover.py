"""
@author: vita
https://www.investopedia.com/terms/t/tsi.asp
"""
data   = __TSI ( data, 25, 13, 12)
line   = data['TSI']
signal = data['TSI_SIGNAL']

# BUY CRITERIA: if TSI line and signal line is below 0 and tsi crosses signal line
if (line.iloc[-1] < 0 and signal.iloc[-1] < 0 and line.iloc[-2] < 0 and signal.iloc[-2] < 0) and \
    ((line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2]) or (line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2])):
    print ("LONG ::: 57_MQL5_tsi_crossover\n")

# SELL CRITERIA: if TSI line and signal line has crossed above 0 and TSI line crosses signal
if (line.iloc[-1] > 0 and signal.iloc[-1] > 0 and line.iloc[-2] > 0 and signal.iloc[-2] > 0) and \
    ((line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2]) or (line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2])):
    print ("SHORT ::: 57_MQL5_tsi_crossover\n")


