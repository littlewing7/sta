import numpy as np
import pandas as pd

##True Strength Index
#def TSI(df, r, s):
#    M = pd.Series(df['close'].diff(1))
#    aM = abs(M)
#    EMA1 = pd.Series(pd.ewma(M, span = r, min_periods = r - 1))
#    aEMA1 = pd.Series(pd.ewma(aM, span = r, min_periods = r - 1))
#    EMA2 = pd.Series(pd.ewma(EMA1, span = s, min_periods = s - 1))
#    aEMA2 = pd.Series(pd.ewma(aEMA1, span = s, min_periods = s - 1))
#    TSI = pd.Series(EMA2 / aEMA2, name = 'TSI_' + str(r) + '_' + str(s))
#    df = df.join(TSI)
#    return df

def __TSI ( data, long, short, signal):
    close = data["Close"]
    diff = close - close.shift(1)
    abs_diff = abs(diff)

    diff_smoothed = diff.ewm(span = long, adjust = False).mean()
    diff_double_smoothed = diff_smoothed.ewm(span = short, adjust = False).mean()
    abs_diff_smoothed = abs_diff.ewm(span = long, adjust = False).mean()
    abs_diff_double_smoothed = abs_diff_smoothed.ewm(span = short, adjust = False).mean()

    tsi = (diff_double_smoothed / abs_diff_double_smoothed) * 100
    signal = tsi.ewm(span = signal, adjust = False).mean()
    #tsi = tsi[tsi.index >= '2020-01-01'].dropna()
    #signal = signal[signal.index >= '2020-01-01'].dropna()
    data['TSI'] = tsi
    data['TSI_SIGNAL'] = signal
    return data


#line = dframe['tsi_line']
#signal = dframe['tsi_signal']
#
## SELL CRITERIA: if TSI line and signal line has crossed above 0 and TSI line crosses signal
#if (line.iloc[-1] > 0 and signal.iloc[-1] > 0 and line.iloc[-2] > 0 and signal.iloc[-2] > 0) and \
#    ((line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2]) or (
#    line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2])):
#    action = -1
#
## BUY CRITERIA: if TSI line and signal line is below 0 and tsi crosses signal line
#if (line.iloc[-1] < 0 and signal.iloc[-1] < 0 and line.iloc[-2] < 0 and signal.iloc[-2] < 0) and \
#    ((line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2]) or (
#    line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2])):
#    action = 1

