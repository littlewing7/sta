#TSI

data = __TSI ( data, 25, 13, 12 )

line = data['TSI']
signal = data['TSI_SIGNAL']

# BUY CRITERIA: if TSI line and signal line is below 0 and tsi crosses signal line
if (line.iloc[-1] < 0 and signal.iloc[-1] < 0 and line.iloc[-2] < 0 and signal.iloc[-2] < 0) and \
    ((line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2]) or (
    line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2])):
    print_log ( '114_TSI', 'LONG', [ 'TSI' ] )

# SELL CRITERIA: if TSI line and signal line has crossed above 0 and TSI line crosses signal
if (line.iloc[-1] > 0 and signal.iloc[-1] > 0 and line.iloc[-2] > 0 and signal.iloc[-2] > 0) and \
    ((line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2]) or (
    line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2])):
    print_log ( '114_TSI', 'SHORT', [ 'TSI' ] )


if data["TSI"][-2] < data["TSI_SIGNAL"][-2] and data["TSI"][-1] > data["TSI_SIGNAL"][-1]:
    print_log ( '114_TSI_2', 'LONG', [ 'TSI' ] )

if data["TSI"][-2] > data["TSI_SIGNAL"][-2] and data["TSI"][-1] < data["TSI_SIGNAL"][-1]:
    print_log ( '114_TSI_2', 'SHORT', [ 'TSI' ] )

