#!/usr/bin/env python3

import os,sys

import yfinance as yf
import numpy as np
import warnings
warnings.simplefilter ( action='ignore', category=Warning )

import pandas as pd
pd.set_option('display.precision', 2)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Environment settings:
pd.set_option('display.max_column', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_colwidth', 500)
pd.set_option('expand_frame_repr', True)

import logging
#logging.basicConfig(level=logging.INFO)

#####################################
#####  DEPENDENCIES / Includes  #####
#####################################
sys.path.insert(0, './utils')

# def __WR (df, period):
from util.wr     import __WR

# def __TEMA (df, period):
from util.tema   import __TEMA

# def __STOCHASTIC (df, k, d):
from util.stochastic import __STOCHASTIC

# def __RSI (df, window=14):
from util.rsi   import __RSI

# def __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3):
from util.stochastic_rsi import __STOCHASTIC_RSI

# def __SMA (df, n=5):
from util.sma   import __SMA

# def __EMA (df, window=9):
from util.ema   import __EMA

# def __CCI (df, window=20):
from util.cci   import __CCI

# def __BB (df, window=20):
from util.bolinger_bands   import __BB

# def __MACD (data, m=12, n=26, p=9, pc='Close'):
from util.macd   import __MACD

# def __KDJ (df)
from util.kdj   import __KDJ


from util.kc   import __KC

# def __ATR_bands ( data, t=14 ):
from util.atr_bands import __ATR_BANDS

from util.atr        import __ATR

# def __CMO ( data, period )
from util.cmo import __CMO

# def __MFI ( data, window=14 )
from util.mfi   import __MFI

# def __CMF ( data, window=20 )
from util.cmf import __CMF

# def __ADX ( data, lookback )
from util.adx import __ADX

# def __MOM ( data, window=14 )
from util.mom import __MOM

# def __AO ( data, window_1, window_2 )
from util.ao import __AO

#def __TSI ( data, long, short, signal)
from util.tsi import __TSI


from util.candles import hammer


def _crossover(a, b):
    return a[-1] < b[-1] and a[0] > b[0]
#if ( _crossover ( data["SMA_5"], data["SMA_8"] ) ):
#    print ("CrossOver\n")

def _crossunder(a, b):
    return a[-1] > b[-1] and a[0] < b[0]


logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
#logging.warning('Admin logged out')

#######################################
#######################################
#######################################

# Set the stock ticker and timeframe
ticker = "AAPL"

# Get stock data from Yahoo Finance
data = yf.download(ticker, period="5y")



data['Fibonacci_0.236'] = data['Close'].shift(0) * 0.236
data['Fibonacci_0.382'] = data['Close'].shift(0) * 0.382
data['Fibonacci_0.50']  = data['Close'].shift(0) * 0.50
data['Fibonacci_0.618'] = data['Close'].shift(0) * 0.618
data['Fibonacci_1.00']  = data['Close'].shift(0) * 1.00
data['Fibonacci_1.27']  = data['Close'].shift(0) * 1.27
data['Fibonacci_1.618'] = data['Close'].shift(0) * 1.618

data['candle_size'] = ( data['Close'] - data['Open'] ) * ( data['Close'] - data['Open'] ) / 2

data = hammer ( data )

######################
#####  SMA 5, 8  #####
######################
# Calculate the df['SMA_5'] and df['SMA_8']
for i in [ 5, 8, 20, 21, 50, 100, 200]:
    data = __SMA ( data, i )

sma_5_today     = data["SMA_5"].iloc[-1]
sma_5_yesterday = data["SMA_5"].iloc[-2]

sma_8_today     = data["SMA_8"].iloc[-1]
sma_8_yesterday = data["SMA_8"].iloc[-2]

# Trend indicator
data['Trend_20']  = data['Close'] / data['SMA_20']
data['Trend_50']  = data['Close'] / data['SMA_50']
data['Trend_100'] = data['Close'] / data['SMA_100']
data['Trend_200'] = data['Close'] / data['SMA_200']

current = data['Close'].iloc[-1]
sma_20  = data['SMA_20'].iloc[-1]
sma_50  = data['SMA_50'].iloc[-1]
sma_100 = data['SMA_100'].iloc[-1]

print('Current price is ' + str(current) + ', SMA 20 is ' + str(sma_20) + ', SMA 50 is ' + str(sma_50) + ' and SMA 100 is ' + str(sma_100))

if (current > sma_100):
    if (current > sma_20 > sma_50 > sma_100):
        print ('Current price is above SMA 100, SMA 50 and SMA 20. Looks like we are in strong uptrend.')
    else:
        print ('Current price is above SMA 100. Looks like we are in uptrend.')
else:
    if (current < sma_20 < sma_50 < sma_100):
        print ('Current price is below SMA 100, SMA 50 and SMA 20. Looks like we are in strong downtrend.')
    else:
        print ('Current price is above SMA 100. Looks like we are in downtrend.')


#######################
#####  EMA 9, 21  #####
#######################
# Calculate the EMAs
for i in [ 5, 8, 9, 20, 21, 50, 100, 200]:
    data = __EMA ( data, i )

ema9_today     = data["EMA_9"].iloc[-1]
ema9_yesterday = data["EMA_9"].iloc[-2]

ema21_today     = data["EMA_21"].iloc[-1]
ema21_yesterday = data["EMA_21"].iloc[-2]


###################
#####  RSI 14 #####
###################
rsi_window      = 14

rsi_overbought  = 70
rsi_oversold    = 30

data            = __RSI ( data, window=rsi_window )

rsi_today       = data['RSI_{}'.format(rsi_window)].iloc[-1]
rsi_yesterday   = data['RSI_{}'.format(rsi_window)].iloc[-2]

if rsi_today > 70:
    if rsi_todaay > 80:
        print('RSI is above 80. The market is extremely overbought and we may expect trend reversal. It may be considered as a strong SELL signal.')
    else:
        print('RSI is above 70. The market is overbought and we may expect trend reversal. It may be considered as a SELL signal.')
elif rsi_today < 30:
    if rsi_today < 20:
        print('RSI is below 20. The market is extremely oversold and we may expect trend reversal. It may be considered as a strong BUY signal.')
    else:
        print('RSI is below 30. The market is oversold and we may expect trend reversal. It may be considered as a BUY signal.')
else:
    print('RSI is between 30 and 70. There is no clear signal from RSI.')


# 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
data['RSI_Signal'] = np.select(
    [ ( data['Trend_20'] > 1 ) & ( data['RSI_{}'.format(rsi_window)] > 40 ) & ( data['RSI_{}'.format(rsi_window)].shift(1) < 40),
    (   data['Trend_20'] < 1 ) & ( data['RSI_{}'.format(rsi_window)] < 60)  & ( data['RSI_{}'.format(rsi_window)].shift(1) > 60)],
    [2, -2])

#if data['RSI_Crossover'].iloc[-1] == 1:
#    print ("LONG\n")

####################
#####  W%R 20  #####
####################
wr_window      = 20
wr_upper_level = -20
wr_lower_level = -80

data            = __WR ( data, wr_window )

#wr20_today        = data['WR_{}'.format(wr_window)].iloc[-1]
#wr20_yesterday    = data['WR_{}'.format(wr_window)].iloc[-2]

# 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
data['WR_Signal'] = np.select(
    [ ( data['WR_{}'.format(wr_window)] > -80 ) & ( data['WR_{}'.format(wr_window)].shift(1) < -80),
    (   data['WR_{}'.format(wr_window)] < -20 ) & ( data['WR_{}'.format(wr_window)].shift(1) > -20)],
    [2, -2])


##################3333###
#####  TEMA 30 & 9  #####
#########################
tema_window     = 30

data             = __TEMA ( data, tema_window )
tema30_today     = data['TEMA_{}'.format(tema_window)].iloc[-1]
tema30_yesterday  = data['TEMA_{}'.format(tema_window)].iloc[-2]


data            = __TEMA ( data, 9 )
tema9_today      = data["TEMA_9"].iloc[-1]
tema9_yesterday  = data["TEMA_9"].iloc[-2]

###################
#####  STOCH  #####
###################
sto_k                = 14
sto_d                = 3
sto_slow             = 3

sto_overbought       = 80
sto_oversold         = 20

data                 = __STOCHASTIC (data, sto_k, 3)

stochastic_today     = data['STO_K'].iloc[-1]
stochastic_yesterday = data['STO_K'].iloc[-2]

# 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
data['STO_Signal'] = np.select(
    [ ( data['Trend_20'] > 1) & ( ( data['STO_D'] > sto_oversold )   & ( data['STO_D'].shift(1) < sto_oversold ) ),
    (   data['Trend_20'] < 1) & ( ( data['STO_D'] < sto_overbought ) & ( data['STO_D'].shift(1) > sto_overbought ) )],
    [2, -2])


############################
#####  STOCHASTIC RSI  #####
############################
srsi_overbought  = 80
srsi_oversold    = 20

data             = __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3 )

srsi_today       = data['SRSI_K'].iloc[-1]
srsi_yesterday   = data['SRSI_K'].iloc[-2]

#if stoch_rsi > 70:
#    if stoch_rsi > 80:
#        print('Stochastic RSI is above 80. The market is extremely overbought and we may expect trend reversal. It may be considered as a strong SELL signal.')
#    else:
#        print('Stochastic RSI is above 70. The market is overbought and we may expect trend reversal. It may be considered as a SELL signal.')
#elif stoch_rsi < 30:
#    if stoch_rsi < 20:
#        print('Stochastic RSI is below 20. The market is extremely oversold and we may expect trend reversal. It may be considered as a strong BUY signal.')
#    else:
#        print('Stochastic RSI is below 30. The market is oversold and we may expect trend reversal. It may be considered as a BUY signal.')
#else:
#    print('Stochastic RSI is between 30 and 70. There is no clear signal from Stochastic RSI.')

####################
#####  CCI 20  #####
####################
cci_window = 20
data = __CCI (data, cci_window)

#data["CCI_prev"] = data["CCI"].shift(1)

cci20_today     = data['CCI_{}'.format(cci_window)].iloc[-1]
cci20_yesterday = data['CCI_{}'.format(cci_window)].iloc[-2]

# 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
data['CCI_Signal'] = np.select(
    [ ( data['CCI_{}'.format(cci_window)] > -100) & ( data['CCI_{}'.format(cci_window)].shift(1) < -100),
    (   data['CCI_{}'.format(cci_window)] <  100) & ( data['CCI_{}'.format(cci_window)].shift(1) >  100)],
    [2, -2])

data = __CCI ( data, 170 )
data = __CCI ( data, 34 )



################
#####  BB  #####
################
bb_window = 20
# Calculate the Bollinger Bands for the stock data
data = __BB (data, bb_window)

bb20_upper_today     = data['BB_upper'].iloc[-1]
bb20_upper_yesterday = data['BB_upper'].iloc[-2]

bb20_middle_today     = data['BB_middle'].iloc[-1]
bb20_middle_yesterday = data['BB_middle'].iloc[-2]

bb20_lower_today     = data['BB_lower'].iloc[-1]
bb20_lower_yesterday = data['BB_lower'].iloc[-2]

data['BB_percent'] = ( data['Close']    - data['BB_lower'] ) / ( data['BB_upper'] - data['BB_lower'] ) * 100
data['BB_sharp']   = ( data['BB_upper'] - data['BB_lower'] ) / ( data['BB_middle'] )

# 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
data['BB_Signal'] = np.select(
    [ ( data['Close'] < data['BB_lower'] ) & ( data['Close'].shift(1) > data['BB_lower'].shift(1)),
    (   data['Close'] > data['BB_upper'] ) & ( data['Close'].shift(1) < data['BB_upper'].shift(1))],
    [2, -2])


current   = data['Close'][-1]
high      = data['High'][-1]
low       = data['Low'][-1]

if current > bb20_upper_today:
    print('Price is currently above Bollinger Bands. It may be considered as a strong SELL signal.')
elif high > bb20_upper_today:
    print('Price reached top Bollinger Band in the last period. It may be considered as a SELL signal.')
elif current < bb20_upper_today:
    print('Price is currently below upper Bollinger Band. It may be taken as a  BUY signal.')
elif low < bb20_lower_today:
    print('Price reached bottom Bollinger Band in the last period. It may be considered as a BUY signal.')
else:
    print('Price is currently between Bollinger Bands. No clear signals.')

##################
#####  MACD  #####
##################
data = __MACD (data)

# 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
data['MACD_Signal'] = np.select(
    [ ( data['Trend_20'] > 1) & ((data['MACD_HIST'] > 0 ) & ( data['MACD_HIST'].shift(1)<0)) ,
    (   data['Trend_20'] < 1) & ((data['MACD_HIST'] < 0 ) & ( data['MACD_HIST'].shift(1)>0))],
    [2, -2])

#if (data['MACD'][-1] > 0):
#    print ('MACD histogram is currently positive. Seems like we are in an uptrend.')
#else:
#    print ('MACD histogram is currently negative. Seems like we are in an downtrend.')

#################
#####  KDJ  #####
#################
data = __KDJ (data)


#######################
#####  ATR BANDS  #####
#######################
data = __ATR_BANDS ( data, 14 )

atr_bands_upper = data['ATR_BANDS_UPPER'][-1]
atr_bands_lower = data['ATR_BANDS_LOWER'][-1]


################
#####  KC  #####
################
data = __KC (data)


#################
#####  CMO  #####
#################
data = __CMO (data)


#################
#####  CMF  #####
#################
data = __CMF (data)


################
#####  AO  #####
################
data = __AO ( data, 5, 34 )

# 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
data['AO_Signal'] = np.select(
    [ ( data['AO'] > 0 ) & ( data['AO'].shift(1) < 0 ),
    (   data['AO'] < 0 ) & ( data['AO'].shift(1) > 0 )],
    [2, -2])


#################
#####  MFI  #####
#################
mfi_window = 14
data = __MFI ( data, mfi_window )

# Define the overbought and oversold levels
mfi_overbought = 80
mfi_oversold   = 20

# 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
data['MFI_Signal'] = np.select(
    [ ( data['MFI_{}'.format(mfi_window)] > mfi_oversold )   & ( data['MFI_{}'.format(mfi_window)].shift(1) < mfi_oversold ),
    (   data['MFI_{}'.format(mfi_window)] < mfi_overbought)  & ( data['MFI_{}'.format(mfi_window)].shift(1) > mfi_overbought)],
    [2, -2])


#################
#####  ADX  #####
#################
adx_window = 14

data = __ADX ( data , adx_window )


#################
#####  MOM  #####
#################
mom_window = 14

data = __MOM ( data, mom_window )


#################
#####  TSI  #####
#################
data = __TSI ( data, 25, 13, 12)


########################
#
# recent data. Grab last 2 rows. [0] = today, [1] = yesterday
r_data = data.tail(2)
#print ( r_data )
#
#

########################
#####  STRATEGIES  #####
########################

# A list of  messages for a ticker
advice = []



#####  (1) (SMA 5,8): SMA 5, 8 crossover / crossunder  #####
data    = __SMA ( data, 5 )
data    = __SMA ( data, 8 )
_close  = data["Close"].iloc[-1]
_low    = data['Low'].iloc[-1]
_high   = data['High'].iloc[-1]
_open   = data['Open'].iloc[-1]

# today
sma_5 = data['SMA_5'].iloc[-1]
sma_8 = data['SMA_5'].iloc[-1]

# yesterday
sma_5_y = data['SMA_5'].iloc[-2]
sma_8_y = data['SMA_5'].iloc[-2]


if ( sma_5 > sma_8 ) and ( _close > sma_5 ) and ( _close > sma_8 ) and ( _open < _close ):
    advice.append("  [BULLISH]  (SMA 5,8)  {SMA 5 > 8}")

    if ( sma_5_y < sma_8_y ):
        advice.append ("  [BULLISH]  (SMA 5,8)  {SMA 5 crossover SMA 8}")

if ( sma_5 < sma_8 ) and ( _close < sma_5 ) and ( _close < sma_8 ) and ( _open > _close ):
    advice.append("  [BEARISH]  (SMA 5,8)  {SMA 5 > 8}")

    if ( sma_5_y > sma_8_y ):
        advice.append ("  [BEARISH]  (SMA 5,8)  {SMA 5 crossunder SMA 8}")

#####  (3) TEMA 30, EMA 9  #####
data = __TEMA ( data, 30 )
data = __EMA ( data, 9 )
data = __EMA ( data, 9 )

_close  = data["Close"].iloc[-1]
_close_1  = data["Close"].iloc[-2]

r_data = data.tail(2)

if (( r_data["Close"][0]   > r_data["TEMA_30"][0] ) and 
    ( r_data["TEMA_30"][0] > r_data["TEMA_30"][0] ) and 
    ( r_data["Close"][0]   > r_data["Close"][1] ) and ( r_data["Close"][0] > r_data["EMA_9"][0] ) and 
    ( r_data["EMA_9"][0]   > r_data["EMA_9"][1] ) and 
    ( r_data["EMA_9"][0]   > r_data["TEMA_30"][0]) ):
    advice.append("  [BULLISH]  (TEMA 30 1)")

if ( _close < r_data["TEMA_30"][0] ) and ( r_data["TEMA_30"][0] < r_data["TEMA_30"][1] ) and ( _close < close_1) and ( _close < r_data["EMA_9"][0] ) and ( r_data["EMA_9"][0] < r_data["EMA_9"][1] ):
    advice.append("  [BEARISH]  (TEMA 30 1)")



data = __CCI ( data, 20 )
r_data = data.tail(2)
if ( r_data["CCI_20"][0] > -100 ) & ( r_data["CCI_20"][1] < -100  ):
    advice.append("  [BULLISH]  (CCI_20 CROSSOVER)")

if ( r_data["CCI_20"][0] < 100 ) & ( r_data["CCI_20"][1] > 100):
    advice.append("  [BEARISH]  (CCI_20 CROSSUNDER)")
print ( r_data)


#####  (4) ATR_14  & W%R  #####
# To reduce the false signal, check the William %R value and should be on the oversold area and previously reach < -95
data['ATR_14'] = __ATR ( data, 14 )
data = __EMA ( data, 9 )
data = __WR ( data, 20 )
r_data = data.tail(2)

_close = r_data["Close"][0]
_open = r_data["Open"][0]

if ( r_data["EMA_9"][0] - ( 2 * data["ATR_14"][0] ) > _open ) and ( r_data["WR_20"][0] < -80) and ( r_data["WR_20"][1] < -95 ) and ( _close > _open ):
    advice.append("  [BULLISH]  (ATR_14 ; W%R)")

# To reduce the false signal, check the William %R value and should be on the overbought area and previously reach > -5
if ( r_data["EMA_9"][0] + ( 2 * data["ATR_14"][0] ) < _close ) and ( r_data["WR_20"][0] > -20 ) and ( r_data["WR_20"][1] > -5 ):
    advice.append("  [BEARISH]  (ATR_14 ; W%R)")


#####  (10)  KDJ  #####
# You get a buy signal from the KDJ indicator when the three curves converge. 
# The blue K line crosses the D line from bottom to top and then moves above the yellow J line. The purple D line is at the bottom.
# The signal is even stronger when the golden form appears under the 20 line, that is in the oversold area.

#A sell signal is received when the lines converge in a way that the blue line K crosses the line D from top to bottom. The blue line continues below the yellow and the purple one runs above the others.
#The signal is stronger when the dead fork of the KDJ oscillator occurs in the overbought zone that is above the line of 80 value.

data = __KDJ ( data )

# KDJ CROSS  https://github.com/pgvasiliu/futu_algo/blob/master/strategies/KDJ_Cross.py
if ( 20 > r_data['KDJ_D'][0] > r_data['KDJ_D'][1] > r_data['KDJ_K'][1] )  &  ( r_data['KDJ_K'][0] > r_data['KDJ_K'][1] )  &  ( r_data['KDJ_K'][0] > r_data['KDJ_D'][0] ):
    advice.append("  [BULLISH]  (KDJ CROSSOVER)")

if ( 80 < r_data['KDJ_D'][0] < r_data['KDJ_D'][-1] < r_data['KDJ_K'][-1] ) and ( r_data['KDJ_K'][0] < r_data['KDJ_K'][-1] ) and ( r_data['KDJ_K'][0] < r_data['KDJ_D'][0] ):
    advice.append("  [BEARISH]  (KDJ CROSSUNDER)")


#####  (12)  RSI BBOL TEMA  #####
# https://github.com/superduong/ALIN/blob/main/freqtrade/templates/sample_.py
# RSI crosses above 30, tema below BB middle, tema is raising, Volume is not 0

data = __RSI ( data, 14 )
data = __TEMA ( data, 9 )
data = __BB ( data )
_vol = data["Volume"].iloc[-1]

r_data = data.tail(2)

if ( r_data["RSI_14"][0] >= 30 ) and ( r_data["RSI_14"][1] < 30 ) and ( r_data['TEMA_9'][0] <= r_data['BB_middle'][0] ) and ( r_data['TEMA_9'][0] > r_data['TEMA_9'][1] ) and ( _vol > 0):
    advice.append("  [BULLISH]  (RSI_BBOL_TEMA 1)")

if ( r_data["RSI_14"][0] >=70 ) and ( r_data["RSI_14"][1] < 70 ) and ( r-data['TEMA_9'][0] > r_data['BB_middle'][0] )  and ( r_data['TEMA_9'][0] < r_data['TEMA_9'][1] ) and ( _vol > 0):
    advice.append("  [BEARISH]  (RSI_BBOL_TEMA 1)")


print ( advice )

##########################################
# STRATEGY 1:
# https://github.com/JustinG4/algo-server
##########################################

# rsi_14 crosses above 30, tema_9 below bb_middle, tema is rising
if ( ( (  r_data["RSI_14"][1]  <  rsi_oversold ) & ( r_data["RSI_14"][0] > rsi_oversold ) ) &
        ( r_data['TEMA_9'][0]  <= r_data['BB_middle'][0] ) &
        ( r_data['TEMA_9'][0]  >  r_data['TEMA_9'][1] ) &
        ( r_data['Volume'][0] > 0) ):
    print ("S1 enter LONG\n")

#
if ( ( (  r_data["RSI_14"][1]  <  rsi_overbought ) & ( r_data["RSI_14"][0] > rsi_overbought ) ) &
        ( r_data['TEMA_9'][0]  > r_data['BB_middle'][0] ) &  # Guard: tema above BB middle
        ( r_data['TEMA_9'][0]  < r_data['TEMA_9'][1] ) &  # Guard: tema is falling
        ( r_data['Volume'][0] > 0) ):
    print ("S1 enter SHORT\n")


# Signal: RSI crosses above 70
if ( ( (  r_data["RSI_14"][1]  <  rsi_overbought ) & ( r_data["RSI_14"][0] > rsi_overbought ) ) &
    ( r_data['TEMA_9'][0]  > r_data['BB_middle'][0] ) &  # Guard: tema above BB middle
    ( r_data['TEMA_9'][0]  < r_data['TEMA_9'][1] ) &  # Guard: tema is falling
    ( r_data['Volume'][0]  > 0)  # Make sure Volume is not 0
            ):
    print ("S1 exit long\n")

# Signal: RSI crosses above 30
if ( ( (  r_data["RSI_14"][1]  <  rsi_oversold ) & ( r_data["RSI_14"][0] > rsi_oversold ) ) &
    # Guard: tema below BB middle
    ( data['TEMA_9'][0]  <= data['BB_middle'][0] ) &
    ( data['TEMA_9'][0]  > data['TEMA_9'][1] ) &  # Guard: tema is raising
    ( data['Volume'][0]  > 0 )  # Make sure Volume is not 0
            ):
    print ("S1. exit short\n")


#########
# S2 Macd
#########
if ( ( r_data['MACD'][0] > 0 ) & ( r_data['MACD'][0] > r_data['MACD_SIGNAL'][0] ) ):
    print ("S2. Enter Long\n")

if ( r_data['MACD'][0] < r_data['MACD_SIGNAL'][0] ):
    print ("S2. Exit Long\n")

########################
##### S3. BB + RSI #####
########################
if ( ( r_data['RSI_14'][0] < rsi_oversold ) & ( r_data['Close'][0] < r_data['BB_lower'][0]) ):
    print ("S3. Enter Long\n")

if ( r_data['RSI_14'][0] > rsi_overbought ):
    print ( "S3. Exit Long\n")


##################################
#####  S4:  CCI + RSI + MFI  #####
##################################

if (  ( r_data['CCI_170'][0] < -100)
    & ( r_data['CCI_34'][0]  < -100)
    & ( r_data['CMF'][0]     < -0.1)
    & ( r_data['MFI_14'][0]  < 25) ):

    ## insurance
    #& (dataframe['resample_medium'] > dataframe['resample_short'])
    #& (dataframe['resample_long'] < dataframe['close'])

    print ( "S4: enter long\n" )

if  ( ( r_data['CCI_170'][0] > 100 )
    & ( r_data['CCI_34'][0]  > 100 )
    & ( r_data['CMF'][0]     > 0.3 )
    #& ( r_data['resample_sma'] < data['resample_medium'])
    #& ( r_data['resample_medium'] < data['resample_short'])
    ):
    print ( "S4: exit long\n" )


########################################
##### S5: CMCWiner: CCI, MFI, CMO  #####
########################################
if ( ( r_data['CCI_20'][1] < -100) &
    (  r_data['MFI_14'][1] < 20) &
    (  r_data['CMO'][1]    < -50)):
    print ("S5: enter long\n" )

if ( ( r_data['CCI_20'][1] > 100 ) &
    ( r_data['MFI_14'][1]  > 80 ) &
    ( r_data['CMO'][1]     > 50 )):
    print ( "S5: Exit long\n" )


#############################
##### S6: CLUCMAY72018  #####
#############################
Vol_SMA_30 = data['Volume'].rolling(window=30).mean().shift(1) * 20

if  ( ( r_data['Close'][0]   < r_data['EMA_100'][0] ) &
    (   r_data['Close'][0]   < 0.985 * r_data['BB_lower'][0] ) &
    (   r_data['Volume'][0]  < Vol_SMA_30[-1] ) ):
    print ("S6: enter long")

if ( ( r_data['Close'][0] > r_data['BB_middle'][0] )):
    print ( "S6: Exit long\n" )


#############################
#####  S7: EMASkipPump  #####
#############################
EMA_SHORT_TERM = 5
EMA_MEDIUM_TERM = 12
EMA_LONG_TERM = 21

data = __EMA ( data, 5 )
data = __EMA ( data, 12 )
data = __EMA ( data, 21 )

Vol_SMA_30 = data['Volume'].rolling(window=30).mean().shift(1) * 20

r_data = data.tail(2)

if (( r_data['Volume'][0] < Vol_SMA_30[-1] ) &
    ( r_data['Close'][0]   < r_data['EMA_{}'.format(EMA_SHORT_TERM)][0] ) &
    ( r_data['Close'][0]   < r_data['EMA_{}'.format(EMA_MEDIUM_TERM)][0] ) &
    #( rdata['Close'][0]  == r_data['min'][0]) &
    ( r_data['Close'][0]  <= r_data['BB_lower'][0] ) ):
    print ( "S7: enter_long\n")

if (( r_data['Close'][0] > r_data['EMA_{}'.format(EMA_SHORT_TERM)][0] ) &
    ( r_data['Close'][0] > r_data['EMA_{}'.format(EMA_MEDIUM_TERM)][0] ) &
    #( r_data['Close'][0] >= r_data['max'][0] ) &
    ( r_data['Close'][0] >= r_data['BB_upper'][0] ) ):
    print ("S7  exit long\n")


########################
#####  S8: Low BB  #####
########################
if ( r_data['Close'][0] <= 0.98 * r_data['BB_lower'][0] ):
    print ("S8: enter long\n")

# EXIT ?!?


###########################
#####  S9: MACD + CCI #####
###########################
buy_cci = -48
sell_cci = 687

r_data = data.tail(2)

if ( ( r_data['MACD'][0] >  r_data['MACD_SIGNAL'][0] ) &
    (  r_data['CCI_20'][0]  <= buy_cci) &
    (  r_data['Volume'][0]  > 0) ):
    print ( "S9: enter_long\n")

if ( ( r_data['MACD'][0]  <  r_data['MACD_SIGNAL'][0] ) &
    (  r_data['CCI_20'][0] >= sell_cci ) &
    (  r_data['Volume'][0]  > 0) ):
    print ("S9  exit long\n")


#################################
#####  S10: MACD + CCI (2)  #####
#################################

if ( ( r_data["MACD"][0] > r_data["MACD_SIGNAL"][0] ) & ( r_data["MACD"][1] <= r_data["MACD_SIGNAL"][1]) &
    (  r_data['CCI_20'][0] <= -50.0) ):
    print ( "S10: enter_long\n")


if ( ( r_data["MACD"][0] < r_data["MACD_SIGNAL"][0] ) & ( r_data["MACD"][1] >= r_data["MACD_SIGNAL"][1] ) &
    (  r_data['CCI_20'][0] >= 100.0) ):
    print ("S10  exit long\n")


##########################
#####  S11: Quickie  #####
##########################
data = __TEMA ( data, 9 )
data = __SMA ( data, 50 )
data = __SMA ( data, 200 )

#data = __ADX ( data )

r_data = data.tail(2)
if ( (r_data['ADX_14'][0]     > 30) &
    ( r_data['TEMA_9'][0]  < r_data['BB_middle'][0] ) &
    ( r_data['TEMA_9'][0]  > r_data['TEMA_9'][1]) &
    ( r_data['SMA_200'][0] > r_data['Close'][0] ) ):
    print ( "S11: Quickie enter long\n" )

if (  (  r_data['ADX_14'][0]     > 70 )
    & (  r_data['TEMA_9'][0]  > r_data['BB_middle'][0] )
    & (  r_data['TEMA_9'][0]  < r_data['TEMA_9'][1] ) ):
    print ("S11  exit long\n")


############################################
#####  S12: ReinForcedAverageStrategy  #####
############################################
maShort = 8
maMedium = 21

data = __EMA ( data, maShort )
data = __EMA ( data, maMedium )


r_data = data.tail(2)

# EMA_8 crossover EMA_21
if ( ( ( r_data["EMA_8"][0] > r_data["EMA_21"][0] ) & ( r_data["EMA_8"][1] < r_data["EMA_21"][1] ) ) & 
    #( r_data['Close'][0] > dataframe[f'resample_{self.resample_interval}_sma']) &
    ( r_data['Volume'][0] > 0 ) ):
    print ( "S12: enter long\n" )

if ( ( ( r_data["EMA_8"][0] < r_data["EMA_21"][0] ) & ( r_data["EMA_8"][1] > r_data["EMA_21"][1] ) ) & 
    ( r_data['Volume'][0] > 0 ) ):
    print ("S12  exit long\n")


####################################
#####  S13: ReinforcedQuickie  #####
####################################
timeframe = '5m'

# resample factor to establish our general trend. Basically don't buy if a trend is not given
resample_factor = 12

EMA_SHORT_TERM = 5
EMA_MEDIUM_TERM = 12
EMA_LONG_TERM = 21

data = __EMA ( data, EMA_SHORT_TERM )
data = __EMA ( data, EMA_MEDIUM_TERM )
data = __EMA ( data, EMA_LONG_TERM )

r_data = data.tail(2)

# ?!?!???


########################
#####  S14: Simple #####
########################
if ( (  r_data['MACD'][0]     > 0)  # over 0
    & ( r_data['MACD'][0]     > r_data['MACD_SIGNAL'][0] )  # over signal
    & ( r_data['BB_upper'][0] > r_data['BB_upper'][1] )  # pointed up
    & ( r_data['RSI_14'][0]   > rsi_oversold )  # optional filter, need to investigate
    ):
    print ( "S14: enter long\n" )

if ( r_data['RSI_14'][0] > 80 ):
    print ( "S14: exit long\n" )


########################
#####  S15: Trend  #####
########################
data = __EMA ( data, 14 )
data = __EMA ( data, 28 )
data = __RSI ( data, 14 )
data = __WR ( data, 20 )

r_data = data.tail(1)

if ( (  r_data['Close'][0]  > r_data['EMA_14'][0] ) 
    & ( r_data['EMA_14'][0] > r_data['EMA_28'][0] ) 
    & ( r_data['RSI_14'][0] > rsi_oversold ) 
    & ( r_data['WR_20'][0]  < -98 )):
    print ("S15: BUY\n")

if ( ( r_data['Close'][0]  < r_data['EMA_14'][0] ) &
    (  r_data['EMA_14'][0] < r_data['EMA_28'][0] ) &
    (  r_data['RSI_14'][0] < rsi_overbought ) &
    (  r_data['WR_20'][0]  > -34 ) ):
    print ("S15: SELL\n")


####################################
#####  S16: InformativeSimple  #####
####################################

data = __EMA ( data, 20 )
data = __EMA ( data, 50 )
data = __EMA ( data, 100 )

r_data = data.tail(2)

# informative['sma20'] = informative['close'].rolling(20).mean()

#if (( r_data['EMA_20'][0]    >  r_data['EMA_50'][0] )
#    #& ( r_data['close_15m'][0] >  r_data['sma20_15m']) ):
#    print ("S16  enter long\n")

#if ( ( r_data['EMA_20'][0]  < r_dataframe['ema50'][0] ) &
#    & ( r_data['close_15m'][0] < r_data['sma20_15m'][0] ) ):
#    print ( "S16 Exit_long\n")



##############################
#####  S17: Strategy001  #####
##############################

data = __EMA ( data, 20 )
data = __EMA ( data, 50 )
data = __EMA ( data, 100 )

# grab last 2 dataframe rows as recent r_data
r_data = data.tail(2)

if ( ( ( r_data["EMA_20"][0] > r_data["EMA_50"][0] ) & ( r_data["EMA_20"][1] < r_data["EMA_50"][1] ) )
    & ( r_data['Close'][0] > r_data['EMA_20'][0] )
    & ( r_data['Open'][0]  < r_data['Close'][0]) ):
    print (" S17 001 enter long\n")

if ( ( ( r_data["EMA_50"][0] > r_data["EMA_100"][0] ) & ( r_data["EMA_50"][1] < r_data["EMA_100"][1] ) )
    & ( r_data['Close'][0]   < r_data['EMA_20'][0] )
    & ( r_data['Open'][0]    > r_data['Close'][0] ) ):
    print ("S17 001 exit long\n")


###############################
#####  S18: Strategy 002  #####
###############################
data = hammer ( data )
hammer = data["hammer"]

r_data = data.tail(2)
#print (data.tail(5))

#if ( is_hammer ( data ) & ( r_data["Close"][0] > r_data["Close"][1] ) ):
#    print ("Hammer\n")

if ( (  r_data['RSI_14'][0]   < 30) 
    & ( r_data['STO_K'][0]    < 20)
    & ( r_data['BB_lower'][0] > r_data['Close'][0] )):
    #& ( hammer ) ):
    print (" S18: enter long\n")

#if ( ( r_data['sar'][0]         > r_data['Close'][0] ) 
#    & ( r_data['fisher_rsi'][0] > 0.3)


###############################
#####  S19: Strategy 003  #####
###############################
data = __SMA ( data, 40 )

data = __EMA ( data, 50 )
data = __EMA ( data, 5 )
data = __EMA ( data, 10 )
data = __EMA ( data, 100 )

r_data = data.tail(2)

if ( (  r_data['RSI_14'][0]     < 28)
    & ( r_data['RSI_14'][0]     > 0)
    & ( r_data['Close'][0]      < r_data['SMA_40'][0] )
    & ( r_data['FRSI_14'][0]    < -0.94)
    & ( r_data['MFI_14'][0]     < 16.0) 
    & ( ( r_data['EMA_50'][0]   > r_data['EMA_100'][0] ) | ( ( r_data['EMA_5'][0] > r_data['EMA_10'][0] ) & ( r_data['EMA_5'][1] < r_data['EMA_10'][1]) ) )
    & ( r_data['STO_D'][0]      > r_data['STO_K'][0] )
    & ( r_data['STO_D'][0]      > 0) ):
    print ("S19 enter long\n")

"""
if ( ( r_data['sar'][0] > r_data['close'][0] ) &
    (  r_data['fisher_rsi'] > 0.3) ):
    print ("S19: exit long\n")
"""

##### S20 
data['mean-volume'] = data['Volume'].rolling(12).mean()
data = __ADX ( data , 35 )

"""
                (
                    (r_data['ADX'][0] > 50) |
                    (r_data['slowadx'] > 26)
                ) &
                (dataframe['cci'] < -100) &
                (
                    (dataframe['fastk-previous'] < 20) &
                    (dataframe['fastd-previous'] < 20)
                ) &
                (
                    (dataframe['slowfastk-previous'] < 30) &
                    (dataframe['slowfastd-previous'] < 30)
                ) &
                (dataframe['fastk-previous'] < dataframe['fastd-previous']) &
                (dataframe['fastk'] > dataframe['fastd']) &
                (dataframe['mean-volume'] > 0.75) &
                (dataframe['close'] > 0.00000100)
            ),
            'enter_long'] = 1


                        (
                (dataframe['slowadx'] < 25) &
                ((dataframe['fastk'] > 70) | (dataframe['fastd'] > 70)) &
                (dataframe['fastk-previous'] < dataframe['fastd-previous']) &
                (dataframe['close'] > dataframe['ema5'])
            ),
            'exit_long'] = 1
"""



###############################
#####  S20: Strategy 004  #####
###############################


###############################
#####  S21: Strategy 005  #####
###############################

"""
##### S22 hlhb
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=10, price='hl2')
            (
                (qtpylib.crossed_above(dataframe['rsi'], 50)) &
                (qtpylib.crossed_above(dataframe['ema5'], dataframe['ema10'])) &
                (dataframe['adx'] > 25) &
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'enter_long'] = 1

            (
                (qtpylib.crossed_below(dataframe['rsi'], 50)) &
                (qtpylib.crossed_below(dataframe['ema5'], dataframe['ema10'])) &
                (dataframe['adx'] > 25) &
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'exit_long'] = 1
"""

# //github.com/Nikhil-Adithyan/ADX-and-RSI-Trading-Strategy-with-Python
#        if adx[i] > 35 and plus_di[i] < minus_di[i] and rsi[i] < 50:
#        if adx[i] > 35 and plus_di[i] > minus_di[i] and rsi[i] > 50:
#
# //github.com/Nikhil-Adithyan/Algoithmic-Trading-with-Stochastic-Oscillator-in-Python 
#        if k[i] < 20 and d[i] < 20 and k[i] < d[i]:
#      if k[i] > 80 and d[i] > 80 and k[i] > d[i]:
#
#
#    lower_band = (-150)
#    upper_band = 150
#        if cci[i-1] > lower_band and cci[i] < lower_band:
# if cci[i-1] < upper_band and cci[i] > upper_band:

#        if wr[i-1] > -80 and wr[i] < -80:
#        elif wr[i-1] < -20 and wr[i] > -20:

#        if prices[i] < kc_lower[i] and prices[i+1] > prices[i]:
#        elif prices[i] > kc_upper[i] and prices[i+1] < prices[i]:

# ADXMomentum.py
# timeframe = "1h"
r_data = data.tail(2)

if (  ( r_data['ADX_14'][0]         > 25)
    & ( r_data['MOM_14'][0]         > 0)
    & ( r_data['ADX_14_plus_di'][0] > 25)
    & ( r_data['ADX_14_plus_di'][0] > r_data['ADX_14_minus_di'][0] ) ):
    print ( "ADXMomentum.py enter_long\n")

if (  ( r_data['ADX_14'][0]          > 25) 
    & ( r_data['MOM_14'][0]          < 0)
    & ( r_data['ADX_14_minus_di'][0] > 25)
    & ( r_data['ADX_14_plus_di'][0]  < r_data['ADX_14_minus_di'][0]) ):
    print ("ADXMom exit_long\n")


#################################
# https://github.com/alisalavati/freq
#AdxSmas.py: ADX 14, SMA 3, SMA 6
#timeframe = '1h'
data = __ADX ( data, 14 )
data = __SMA ( data, 3 )
data = __SMA ( data, 6 )

r_data = data.tail(2)

if ( (    r_data['ADX_14'][0] > 25)
    & ( ( r_data["SMA_3"][0]  > r_data["SMA_6"][0] ) & ( r_data["SMA_3"][1] < r_data["SMA_6"][1] ) ) ):
    print ("enter_long\n")

if ( (    r_data['ADX_14'][0] < 25 )
    & ( ( r_data["SMA_6"][0]  > r_data["SMA_3"][0] ) & ( r_data["SMA_6"][1] < r_data["SMA_3"][1] ) ) ):
    print ("ADX SMAs exit_long\n")


# AwesomeMacd.py
#timeframe = '1h'
r_data = data.tail(2)

if (  ( r_data["MACD"][0] > 0 )
    & ( r_data['AO'][0]   > 0 )
    & ( r_data['AO'][1]   < 0 ) ):
    print ("AWESOMEMACD Enter long\n")

if (  ( r_data["MACD"][0] < 0 )
    & ( r_data['AO'][0]   < 0 )
    & ( r_data['AO'][1]   > 0 ) ):
    print ("AWESOMEMACD Exit long\n")



# BBANDRSI.py
# Optimal timeframe for the strategy
#timeframe = '1h'

data = __RSI ( data, 14 )
r_data = data.tail(2)

if ( (  r_data["RSI_14"][0] < 30 )
    & ( r_data["Close"][0] < r_data["BB_lower"][0] ) ):
    print ("BBANDRSI.py enter long\n")

if ( r_data["RSI_14"][0] > 70 ):
    print ("BBANDRSI.py exit long\n")



# AO CROSSOVER https://github.com/Amar0628/MQL5-Python-Backtesting/tree/929e492930347ce660931a4998dfc991feceac49/trading_strategies 
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
    print ("AO cross: enter long\n") 

# SELL CRITERIA: awesome oscillator crosses from above to below the zero line, followed by 3 decreasing values
if data['AO'].iloc[-4]  >= 0 and data['AO'].iloc[-3] <= 0 and \
    data['AO'].iloc[-2] < data['AO'].iloc[-3] and \
    data['AO'].iloc[-1] < data['AO'].iloc[-2]:
    print ("AO cross Exit long\n")


# ADX RSI https://github.com/Amar0628/MQL5-Python-Backtesting/tree/929e492930347ce660931a4998dfc991feceac49/trading_strategies
'''
### Author:Vita ###
Strategy from:
https://forextester.com/blog/adx-14-ema-strategy
This strategy uses ADX and 14EMA for buy and sell signals
'''
data = __EMA ( data, 14 )
if (data["Close"].iloc[-1] > data["Open"].iloc[-1]) and ( data["Close"].iloc[-1] > data["EMA_14"].iloc[-1]) and ( data["ADX_14"].iloc[-2] < 25 and data["ADX_14"].iloc[-1] > 25):
    print (" ADX RSI enter long\n")

# SELL CRITERIA: if candlestick is bearish, close is less than 14 EMA and ADX indicator has crossed above 25:
if ( data["Open"].iloc[-1] > data["Close"].iloc[-1]) and ( data["Close"].iloc[-1] < data["EMA_14"].iloc[-1]) and ( data["ADX_14"].iloc[-2] < 25 and data["ADX_14"].iloc[-1] > 25):
    print ("ADX RSI exit long\n")



# awesome saucer
'''
The Awesome Oscillator Saucers strategy looks for a bullish or bearish saucer pattern in the Awesome Oscillator, where close price is greater than 200 EMA.
A bullish saucer pattern consists of 3 positive AO bars which form the curve of a saucer (i.e. the middle value is smallest).
A bearish saucer patter consists of 3 negative AO bars which form the curve of an upside down saucer (i.e. the middle value is greatest (least negative)).
Author: Cheryl
'''
data = __EMA ( data, 200 )
ema_dist = data['Close'].iloc[-1] - data['EMA_200'].iloc[-1]

bar_1 = data['AO'].iloc[-3]
bar_2 = data['AO'].iloc[-2]
bar_3 = data['AO'].iloc[-1]
curr_close = data['Close'].iloc[-1]
curr_200ema = data['EMA_200'].iloc[-1]

# BUY CRITERIA: CONSECUTIVELY: all 3 bars positive, 2 decreasing awesome oscillator values followed by an increase, and close is above the 200EMA
if bar_1 > 0 and bar_2 > 0 and bar_3 > 0 and \
    bar_1 > bar_2 and bar_2 < bar_3 and curr_close > curr_200ema:
    print ( "AO saucer enter long\n")

# SELL CRITERIA: CONSECUTIVELY: all 3 bars negative, 2 increasing awesome oscillator values followed by a decrease, and close is below the 200EMA
if bar_1 < 0 and bar_2 < 0 and bar_3 < 0 and\
    bar_1 < bar_2 and bar_2 > bar_3 and curr_close < curr_200ema:
    print (" AO saucer exit long\n")


'''
### Author: Wilson ###
Strategy from:
https://www.ig.com/au/trading-strategies/best-forex-trading-strategies-and-tips-190520#Bladerunner
The first candlestick that touches the EMA is called the ‘signal candle’,
The second candle that moves away from the EMA again is the ‘confirmatory candle’.
Traders would place their open orders at this price level to take advantage of the rebounding price.
'''

data = __EMA ( data, 20 )

# BUY if first candle stick touches ema and then next candle stick rebounds off it
if ( ( data['Low'].iloc[-2] <= data['EMA_20'].iloc[-2] and data['EMA_20'].iloc[-2] <= data['High'].iloc[-2]) & (data['Close'].iloc[-1] > data['Close'].iloc[-2])):
    print (" BladeRunner enter long\n")

# SELL if first candle stick touches ema and then next candle stick rebounds off it
if ( ( data['Low'].iloc[-2] <= data['EMA_20'].iloc[-2] and data['EMA_20'].iloc[-2] <= data['High'].iloc[-2]) & (data['Close'].iloc[-1] < data['Close'].iloc[-2])):
    print (" BladeRunner exit long\n")





# CCI MA
"""
@author: mingyu and caitlin
This strategy combines the CCI, the commodity channel index with a simple moving average for 100 periods.
The CCI is a trend indicator that shows oversold and overbought conditions. Combine with the sma100
to attempt to filter some false signals.
"""
data['average'] = (data['High'] + data['Low'] + data['Close']) / 3
data['period_100_average'] = data['average'].rolling(window=100).mean()

# A buy entry signal is when cci left oversold zone, i.e. just above -100, and price intersects the period 100 moving average from below
if data['CCI_20'].iloc[-1] > -100 and data['CCI_20'].iloc[-2] <= -100 and data['Close'].iloc[-1] > data['period_100_average'].iloc[-1] and data['Close'].iloc[-2] <= data['period_100_average'].iloc[-2]:
    print ("Enter LONG\n")

# A sell entry signal is when cci left overbought zone, i.e. just below 100, and price intersects the period 100 moving average from above
if data['CCI_20'].iloc[-1] < 100 and data['CCI_20'].iloc[-2] >= 100 and data['Close'].iloc[-1] < data['period_100_average'].iloc[-1] and data['Close'].iloc[-2] >= data['period_100_average'].iloc[-2]:
    print ("Exit LONG\n")




# CCI
# A buy entry signal is given when the cci leaves the oversold zone, i.e. just above -100
if data['CCI_20'].iloc[-1] > -100 and data['CCI_20'].iloc[-2] <= -100:
    print ("Enter LONG\n")

# A sell entry signal is given when the cci leaves the overbought zone, i.e. just above 100
if data['CCI_20'].iloc[-1] < 100 and data['CCI_20'].iloc[-2] >= 100:
    print ("Exit LONG\n")



# EMA 20, 50 cross
data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()

#buy if 20 ema crosses above 50 ema
if ( data["EMA_20"].iloc[-2] < data["EMA_50"].iloc[-2]) and ( data["EMA_20"].iloc[-1] > data["EMA_50"].iloc[-1]):
    print ("Enter LONG\n")

#sell if 20 ema crosses below 50 ema
if ( data["EMA_20"].iloc[-2] > data["EMA_50"].iloc[-2]) and ( data["EMA_20"].iloc[-1] < data["EMA_50"].iloc[-1]):
    print ("Exit LONG\n")



# EMA, MACD
"""
@author: vita
This strategy uses the crossover between 9EMA and 21EMA with MACD histogram as confirmation to avoid false signals
http://www.forexfunction.com/trading-strategy-of-ema-crossover-with-macd
"""
data = __EMA ( data, 9 )
data = __EMA ( data, 21 )

ema9 = data['EMA_9']
ema21 = data['EMA_21']
histogram = data['MACD_HIST']
close = data['Close']

# SELL CRITERIA: 9EMA crosses below 21EMA followed by a MACD histogram crossover into negatives
if (ema9.iloc[-2] < ema21.iloc[-2] and ema9.iloc[-3]>ema21.iloc[-3]) and ((histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0) or (histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0)):
    print ("Exit LONG\n")

# BUY CRITERIA: 9EMA crosses above 21EMA followed by a MACD histogram crossover ito positives
if (ema9.iloc[-2] > ema21.iloc[-2] and ema9.iloc[-3]<ema21.iloc[-3]) and ((histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0) or (histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0)):
    print ("Enter LONG\n")





# EMA, RSI
data = __EMA ( data, 6 )
data = __EMA ( data, 12 )
data = __RSI ( data, 14 )

ema6 = data['EMA_6']
ema12 = data['EMA_12']
rsi = data['RSI_14']
close = data['Close']

# SELL CRITERIA: when 6EMA crosses above 12EMA and RSI value has crossed below 50
if (ema6.iloc[-1] < ema12.iloc[-1] and ema6.iloc[-2] > ema12.iloc[-2]) and ( rsi.iloc[-1] < 50 and rsi.iloc[-2] > 50):
    print ("Exit LONG\n")

# BUY CRITERIA: when 6EMA crosses below 12EMA and RSI value has crossed above 50
if (ema6.iloc[-1] > ema12.iloc[-1] and ema6.iloc[-2] < ema12.iloc[-2]) and ( rsi.iloc[-1] > 50 and rsi.iloc[-2] < 50):
    print ("Enter LONG\n")





'''
This strategy combines ema_crossover_rsi_alternative and a modified ema_crossover_macd to determine buy and sell
signals. Ema_crossover_macd was modified such that 9EMA only needs to be below/above 21EMA to fulfill sell/buy
signals respectively rather than a crossover below or above.
'''
for i in [ 6, 9, 12, 21 ]:
    data = __EMA ( data, i )
data = __RSI ( data, 14 )
data = __MACD ( data )

close = data['Close']
ema6 = data['EMA_6']
ema9 = data['EMA_9']
ema12 = data['EMA_12']
ema21 = data['EMA_21']
histogram = data['MACD_HIST']
rsi = data['RSI_14']

# BUY CRITERIA: 9EMA crosses above 21EMA followed by a MACD histogram crossover ito positives
if ((ema9.iloc[-2] > ema21.iloc[-2]) and (
    (histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0) or (histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0))) \
    or ((ema6.iloc[-1] > ema12.iloc[-1]) and (rsi.iloc[-1] > 50)):
    print ("Enter LONG\n")

# SELL CRITERIA: 9EMA crosses below 21EMA followed by a MACD histogram crossover into negatives
if ((ema9.iloc[-2] < ema21.iloc[-2]) and (
    (histogram.iloc[-1] < 0 and histogram.iloc[-2] > 0) or (histogram.iloc[-1] > 0 and histogram.iloc[-2] < 0))) \
    or ((ema6.iloc[-1] < ema12.iloc[-1]) and (rsi.iloc[-1] < 50)):
    print ("Exit LONG\n")





# KeltnerStochasticAdx


#KeltnerAdx
'''
@author: Caitlin
This strategy combines Keltner Channels with ADX. Buy signals are given when at least 3 candles
are at or below the low band, and oversold conditions are confirmed by an adx reading of at least 25.
Sell signals are given when at least 3 candles are at or above the high band, and overbought conditions are
confirmed by an adx reading of at least 20.
'''
high = data['High']
low = data['Low']
close = data['Close']

data = __KC ( data )
data = __ADX ( data, 14 )

r_data = data.tail(3)

# BUY SIGNAL: adx is >= 25 and at least 3 candles are less than or touch the lower keltner band
if (  ( r_data['High'][0]   <= data['KC_lower'][0] )
    & ( r_data['High'][1]   <= data['KC_lower'][1] )
    & ( r_data['High'][2]   <= data['KC_lower'][2] ) 
    & ( r_data['ADX_14'][0] >= 20) ):
    print ("KeltnerAdx enter long\n")

if (  ( data['Low'][0]     >= data['KC_upper'][0] )
    & ( data['Low'][1]     >= data['KC_upper'][1] )
    & ( data['Low'][2]     >= data['KC_upper'][2] ) 
    & ( data['ADX_14'][0]  >= 20) ):
    print ("KeltnerAdx exit long\n")




# MACDCrossover
'''
@ Vita
https://www.dailyfx.com/forex/education/trading_tips/daily_trading_lesson/2020/01/09/macd-histogram.html
'''
data = __MACD ( data )

macd = data['MACD']
signal = data['MACD_SIGNAL']

# BUY CRITERIA: if MACD line has crossed signal line and are < 0
if (    macd.iloc[-1] < 0 and signal.iloc[-1] < 0 and macd.iloc[-2] < 0 and signal.iloc[-2] < 0 and
        macd.iloc[-3] < 0 and signal.iloc[-3] < 0) and \
    ( ( macd.iloc[-3] > signal.iloc[-3] and macd.iloc[-1] < signal.iloc[-1]) or ( macd.iloc[-3] < signal.iloc[-3] and macd.iloc[-1] > signal.iloc[-1])):
    print ("Enter LONG\n")

# SELL CRITERIA: if MACD line has crossed signal line and are > 0
if (    macd.iloc[-1] > 0 and signal.iloc[-1] > 0 and macd.iloc[-2] > 0 and signal.iloc[-2] > 0 and macd.iloc[-3]>0 and signal.iloc[-3]>0) and \
    ( ( macd.iloc[-3] < signal.iloc[-3] and macd.iloc[-1] > signal.iloc[-1]) or (macd.iloc[-3] > signal.iloc[-3] and macd.iloc[-1] < signal.iloc[-1])):
    print ("Exit LONG\n")



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

sma_5 = data['SMA_5']
macd_line = data['MACD']
macd_signal = data['MACD_SIGNAL']
rsi = data['RSI_14']
close = data['Close']

# buy if close price is higher than the moving average, rsi reads less than 30 and the macd line crosses up through macd signal line
if (  sma_5.iloc[-1] < close.iloc[-1]) and (macd_line.iloc[-2] < macd_signal.iloc[-2]) and \
    ( macd_line.iloc[-1] > macd_signal.iloc[-1]) and (macd_line.iloc[-1] < 0 and rsi.iloc[-1] < 30):
    print ("Enter LONG\n")

# sell if close price less than moving average, rsi reads over 70, and macd line crosses down through signal line
if (  close.iloc[-1] < sma_5.iloc[-1]) and (macd_line.iloc[-1] > 0 and rsi.iloc[-1] > 70) and \
    ( macd_line.iloc[-2] > macd_signal.iloc[-2]) and (macd_line.iloc[-1] < macd_signal.iloc[-1]):
    print ("Exit LONG\n")



# MACDStochasticCrossover
"""
@author: vita
This strategy uses the MACD crossovers and Stochastic crossovers. The stochastic crossover should occur just before the MACD crossover.
https://www.dailyfx.com/forex/education/trading_tips/daily_trading_lesson/2020/02/11/macd-vs-stochastic.html
"""

close = data['Close']
high = data['High']
low = data['Low']

data = __MACD ( data )
data = __STOCHASTIC ( data, 14, 3 )

m_line = data['MACD']
m_signal = data['MACD_SIGNAL']
k_line = data['STO_K']
d_signal = data['STO_D']

# BUY CRITERIA: stoch %k and %d lines crossover that are <20 shortly before MACD signal and line crossover that are <0
if (k_line.iloc[-3] < 20 and d_signal.iloc[-3] < 20 and k_line.iloc[-2] < 20 and d_signal.iloc[-2] < 20) and \
    ((k_line.iloc[-3] > d_signal.iloc[-3] and k_line.iloc[-2] < d_signal.iloc[-2])) and \
    (m_line.iloc[-2] < 0 and m_signal.iloc[-2] < 0 and m_line.iloc[-1] < 0 and m_signal.iloc[-1] < 0) and \
    (m_line.iloc[-2] < m_signal.iloc[-2] and m_line.iloc[-1] > m_signal.iloc[-1]):
    print ("Enter LONG\n")

# SELL CRITERIA: stoch %k and %d lines crossover that are >80 shortly before MACD signal and line crossover that are >0
if (k_line.iloc[-3] > 80 and d_signal.iloc[-3] > 80 and k_line.iloc[-2] > 80 and d_signal.iloc[-2] > 80) and \
    ((k_line.iloc[-3] < d_signal.iloc[-3] and k_line.iloc[-2] > d_signal.iloc[-2])) and \
    (m_line.iloc[-2] > 0 and m_signal.iloc[-2] > 0 and m_line.iloc[-1] > 0 and m_signal.iloc[-1] > 0) and \
    (m_line.iloc[-2] > m_signal.iloc[-2] and m_line.iloc[-1] < m_signal.iloc[-1]):
    print ("Exit LONG\n")




'''
Larry Connors' 2 period RSI strategy uses mean reversion to provide a short-term buy or sell signal.
When the price is above the 200 Moving Average, and 2-period RSI is below 10, this is a buy signal
When the price is below the 200 Moving Average, and 2-period RSI is above 90, this is a sell signal
'''
data = __SMA ( data, 5 )
data = __SMA ( data, 200 )
data = __RSI ( data, 14 )
data = __RSI ( data, 2 )

# Buy when RSI2 between 0 and 10, and price above 200sma but below 5sma
if data['RSI_2'].iloc[-1] < 10 and data['Close'].iloc[-1] > data['SMA_200'].iloc[-1] and data['Close'].iloc[-1] < data['SMA_5'].iloc[-1]:
    print ("Enter LONG\n")

# Sell when RSI2 between 90 and 100, and price below 200sma but above 5sma
if data['RSI_2'].iloc[-1] > 90 and data['Close'].iloc[-1] < data['SMA_200'].iloc[-1] and data['Close'].iloc[-1] > data['SMA_5'].iloc[-1]:
    print ("Exit LONG\n")



"""
@author: vita
https://www.investopedia.com/terms/t/tsi.asp
"""
data = __TSI ( data, 25, 13, 12)
line = data['TSI']
signal = data['TSI_SIGNAL']

# BUY CRITERIA: if TSI line and signal line is below 0 and tsi crosses signal line
if (line.iloc[-1] < 0 and signal.iloc[-1] < 0 and line.iloc[-2] < 0 and signal.iloc[-2] < 0) and \
    ((line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2]) or (line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2])):
    print ("TSI Enter LONG\n")

# SELL CRITERIA: if TSI line and signal line has crossed above 0 and TSI line crosses signal
if (line.iloc[-1] > 0 and signal.iloc[-1] > 0 and line.iloc[-2] > 0 and signal.iloc[-2] > 0) and \
    ((line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2]) or (line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2])):
    print ("Exit LONG\n")





# WilliamsRsi
"""
@author: caitlin
This strategy uses the Williams%R indicator. This momentum indicator oscillates between 0 and -100, and shows
how the current price compares to a 14 day look back period, where a reading near -100 indicates the market is
near the lowest low and a reading near 0 indicates the market is near the highest high. This strategy combines
an 8 period rsi.
"""
high = data['High']
low = data['Low']
close = data['Close']

data = __RSI ( data, 8 )
data = __WR ( data, 14 )

r_data = data.tail(5)

if ( ( ( r_data['WR_14'][2] < -70) | ( r_data['WR_14'][1] < -70) | ( r_data['WR_14'][0] < -70) | ( r_data['WR_14'][3] < -70))
    & ( ( r_data['RSI_8'][0] < 30) | ( r_data['RSI_8'][1] < 30)  | ( r_data['RSI_8'][2] < 30))):
    print ("Enter LONG\n")

if ( ( ( r_data['WR_14'][2] > -30) | ( r_data['WR_14'][1] > -30) | ( r_data['WR_14'][0] > -30) | ( r_data['WR_14'][3] > -30))
    & (( r_data['RSI_8'][0] > 70)  | ( r_data['RSI_8'][1] > 70) | ( r_data['RSI_8'][2] > 70))):
    print ("Exit LONG\n")



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

data['stoch_signal'] = data['STO_D']
data['williams_indicator'] = data["WR_14"]

# BUY SIGNAL: signal line is less than or equal to 35 and williams indicator is less than -65 within the last 5 candles
if ( ( ( data['stoch_signal'][-1] <= 35) | (data['stoch_signal'][-2] <= 35) | ( data['stoch_signal'][-3] <= 35)
    |  ( data['stoch_signal'][-4] <= 35) | (data['stoch_signal'][-5] <= 35) | (data['stoch_signal'][-6] <= 35))
    & ( ( data['williams_indicator'][-3] < -65) | (data['williams_indicator'][-2] < -65)
                       | (data['williams_indicator'][-1] < -65) | (data['williams_indicator'][-4] < -65)
                       | (data['williams_indicator'][-5] < -65) | (
                        data['williams_indicator'][-6] < -65))):
    print ( "WR STO enter long\n")

# SELL SIGNAL: signal line is greater than or equal to 65 and williams indicator is greater than -35 within the last 5 candles
if ( ( ( data['stoch_signal'][-1] >= 65) | (data['stoch_signal'][-2] >= 65) | ( data['stoch_signal'][-3] >= 65)
                     | (data['stoch_signal'][-4] >= 65) | (data['stoch_signal'][-5] >= 65) | (
                             data['stoch_signal'][-6] >= 65))
                    & ((data['williams_indicator'][-3] > -35) | (data['williams_indicator'][-2] > -35)
                       | (data['williams_indicator'][-1] > -35) | (data['williams_indicator'][-3] > -35) | (
                               data['williams_indicator'][-5] > -35)
                       | (data['williams_indicator'][-6] > -35))):
    print ("WR STO exit long\n")



"""
# PSAR
#Buy Criteria - current pSAR below close, previous pSAR above close
if pSAR.iloc[-1] < close.iloc[-1] and pSAR.iloc[-2] > close.iloc[-2]:
    print ("Enter LONG\n")

#Sell Criteria - current pSAR above close, previous pSAR below close
if pSAR.iloc[-1] > close.iloc[-1] and pSAR.iloc[-2] < close.iloc[-2]:
            print ("Exit LONG\n")
"""


