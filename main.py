#!/usr/bin/env python3
# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# pylint: disable=C0122
# isort: skip_file

import os,sys
import argparse
import time
import datetime

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
from util.atr        import calculate_ATR


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

# def __TSI ( data, long, short, signal)
from util.tsi import __TSI

# def __ROC (data, n=12, m=6)
from util.roc  import __ROC


# def __PSAR (data, iaf = 0.02, maxaf = 0.2)
from util.psar  import __PSAR



from util.candles import hammer



logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
#logging.warning('Admin logged out')

#            Period           Interval              Sleep before refresh data
TIMEFRAMES = {
    "1m":  { "Period": "7d",   "Interval": "1m",    "Refresh": "60"   },
    "5m":  { "Period": "60d",  "Interval": "5m",    "Refresh": "120"  },
    "15m": { "Period": "60d",  "Interval": "15m",   "Refresh": "300"  },
    "30m": { "Period": "60d",  "Interval": "30m",   "Refresh": "600"  },
    "90m": { "Period": "60d",  "Interval": "90m",   "Refresh": "900"  },
    "1h":  { "Period": "730d", "Interval": "1h",    "Refresh": "1200" },
    "1d":  { "Period": "5y",   "Interval": "1d",    "Refresh": "1800" },
    "5d":  { "Period": "5y",   "Interval": "5d",    "Refresh": "14000"},
    "1wk": { "Period": "5y",   "Interval": "1wk",   "Refresh": "86400"},
    "1mo": { "Period": "5y",   "Interval": "1mo",   "Refresh": "86400"},
    "3mo": { "Period": "5y",   "Interval": "3mo",   "Refresh": "86400"}

}

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Script that monitors a number of tickers')

# Add a positional argument for the time interval
parser.add_argument('-i', '--interval', type=str, required=True, help='time interval i.e. one of 1m 5m 15m 30m 90m 1h 1d 5d 1wk 1mo 3mo')

# Add a positional argument for a list of stocks
parser.add_argument('-t', '--tickers', type=str, nargs='+', required=True, help='list of stock tickers')

# Add a positional argument for a strategy
parser.add_argument('-s', '--strategy', type=str, required=False, help='load a strategy from file')


# Parse the command-line arguments
args = parser.parse_args()

while True:


    # Use the list of stocks and integer value in the script
    for ticker in args.tickers:
        now = datetime.datetime.now()

        print("=====  " + ticker + "  =====  " + now.strftime("%Y-%m-%d %H:%M:%S") + "  =====" )

        period   = TIMEFRAMES[args.interval]['Period']
        interval = TIMEFRAMES[args.interval]['Interval']
        refresh  = TIMEFRAMES[args.interval]['Refresh']
    
        # Get stock data from Yahoo Finance
        #data = yf.download(ticker, period="5y")
        data = yf.download(ticker, period=period, interval = interval, progress=False )

        data['Fibonacci_0.236'] = data['Close'].shift(0) * 0.236
        data['Fibonacci_0.382'] = data['Close'].shift(0) * 0.382
        data['Fibonacci_0.50']  = data['Close'].shift(0) * 0.50
        data['Fibonacci_0.618'] = data['Close'].shift(0) * 0.618
        data['Fibonacci_1.00']  = data['Close'].shift(0) * 1.00
        data['Fibonacci_1.27']  = data['Close'].shift(0) * 1.27
        data['Fibonacci_1.618'] = data['Close'].shift(0) * 1.618

        data['candle_size'] = ( data['Close'] - data['Open'] ) * ( data['Close'] - data['Open'] ) / 2

        data = hammer ( data )

    #########  SMA 5, 8  #####
        for i in [ 5, 8, 9, 20, 21, 50, 100, 200]:
            data = __SMA ( data, i )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['SMA_5_8_Signal'] = np.select(
            [ ( data['SMA_5'] > data['SMA_8'] ) & ( data['SMA_5'].shift(1) < data['SMA_8'].shift(1) ),
            (   data['SMA_5'] < data['SMA_8'] ) & ( data['SMA_5'].shift(1) > data['SMA_8'].shift(1) )],
            [2, -2])


        # Trend indicator
        #data['Trend_20'] = data['Close'] / data['Close'].rolling(20).mean()
        data['Trend_20']  = data['Close'] / data['SMA_20']
        data['Trend_50']  = data['Close'] / data['SMA_50']
        data['Trend_100'] = data['Close'] / data['SMA_100']
        data['Trend_200'] = data['Close'] / data['SMA_200']


    #########  EMA 9, 21  #####
        # Calculate the EMAs
        for i in [ 5, 8, 9, 20, 21, 50, 100, 200]:
           data = __EMA ( data, i )

        # CROSS_over / CROSS_under ::: 2 = LONG, -2 = SHORT
        data['EMA_20_50_Signal'] = np.select(
            [ ( data['EMA_20'] > data['EMA_50'] ) & ( data['EMA_20'].shift(1) < data['EMA_50'].shift(1) ) ,
              ( data['EMA_20'] < data['EMA_50'] ) & ( data['EMA_20'].shift(1) > data['EMA_50'].shift(1) ) ],
            [2, -2])

        data['EMA_9_21_Signal'] = np.select(
            [ ( data['EMA_9'] > data['EMA_21'] ) & ( data['EMA_9'].shift(1) < data['EMA_21'].shift(1) ) ,
              ( data['EMA_9'] < data['EMA_21'] ) & ( data['EMA_9'].shift(1) > data['EMA_21'].shift(1) ) ],
            [2, -2])


    #########  RSI 14 #####
        rsi_window      = 14

        rsi_overbought  = 70
        rsi_oversold    = 30

        data            = __RSI ( data, window=rsi_window )

        data['Trend_20']   = data['Close'] / data['Close'].rolling(20).mean()

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['RSI_Signal'] = np.select(
            [ ( data['Trend_20'] > 1 ) & ( data['RSI_{}'.format(rsi_window)] > 40 ) & ( data['RSI_{}'.format(rsi_window)].shift(1) < 40),
            (   data['Trend_20'] < 1 ) & ( data['RSI_{}'.format(rsi_window)] < 60)  & ( data['RSI_{}'.format(rsi_window)].shift(1) > 60)],
            [2, -2])


    #########  W%R 20  #####
        wr_window      = 20

        wr_upper_level = -20
        wr_lower_level = -80

        data           = __WR ( data, wr_window )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['WR_Signal'] = np.select(
            [ ( data['WR_{}'.format(wr_window)] > -80 ) & ( data['WR_{}'.format(wr_window)].shift(1) < -80),
            (   data['WR_{}'.format(wr_window)] < -20 ) & ( data['WR_{}'.format(wr_window)].shift(1) > -20)],
            [2, -2])


    #########  TEMA 30 & 9  #####
        tema_window     = 30

        data            = __TEMA ( data, tema_window )
        data            = __TEMA ( data, 9 )


    #########  STOCH  #####
        sto_k                = 14
        sto_d                = 3
        sto_slow             = 3

        sto_overbought       = 80
        sto_oversold         = 20

        data                 = __STOCHASTIC (data, sto_k, 3)


        data['Trend_20'] = data['Close'] / data['Close'].rolling(20).mean()

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['STO_Signal'] = np.select(
            [ ( data['Trend_20'] > 1) & ( ( data['STO_D'] > sto_oversold )   & ( data['STO_D'].shift(1) < sto_oversold ) ),
            (   data['Trend_20'] < 1) & ( ( data['STO_D'] < sto_overbought ) & ( data['STO_D'].shift(1) > sto_overbought ) )],
            [2, -2])


    #########  STOCHASTIC RSI  #####
        srsi_overbought  = 80
        srsi_oversold    = 20

        data             = __STOCHASTIC_RSI ( data, period=14, SmoothD=3, SmoothK=3 )

        data['SRSI_Signal'] = np.select(
            [ ( ( data['STO_K'] > srsi_oversold )   & ( data['STO_K'].shift(1) < srsi_oversold ) ),
              ( ( data['STO_K'] < srsi_overbought ) & ( data['STO_K'].shift(1) > srsi_overbought ) )],
            [2, -2])


    #########  CCI 20  #####
        cci_window = 20
        data = __CCI (data, cci_window)

        data = __CCI ( data, 170 )
        data = __CCI ( data, 34 )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['CCI_Signal'] = np.select(
           [ ( data['CCI_{}'.format(cci_window)] > -100) & ( data['CCI_{}'.format(cci_window)].shift(1) < -100),
            (   data['CCI_{}'.format(cci_window)] <  100) & ( data['CCI_{}'.format(cci_window)].shift(1) >  100)],
            [2, -2])


    #####  Bolinger Bands  #####
        bb_window = 20
        # Calculate the Bollinger Bands for the stock data
        data = __BB ( data, bb_window )

        data['BB_percent'] = ( data['Close']    - data['BB_lower'] ) / ( data['BB_upper'] - data['BB_lower'] ) * 100
        data['BB_sharp']   = ( data['BB_upper'] - data['BB_lower'] ) / ( data['BB_middle'] )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['BB_Signal'] = np.select(
            [ ( data['Close'] < data['BB_lower'] ) & ( data['Close'].shift(1) > data['BB_lower'].shift(1)),
            (   data['Close'] > data['BB_upper'] ) & ( data['Close'].shift(1) < data['BB_upper'].shift(1))],
            [2, -2])


    #########  MACD  #####
        data = __MACD (data)

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['MACD_Signal'] = np.select(
            [ ( data['Trend_20'] > 1) & ((data['MACD_HIST'] > 0 ) & ( data['MACD_HIST'].shift(1)<0)) ,
            (   data['Trend_20'] < 1) & ((data['MACD_HIST'] < 0 ) & ( data['MACD_HIST'].shift(1)>0))],
            [2, -2])


    #########  KDJ  #####
        data = __KDJ (data)


    #########  ATR BANDS  #####
        data = __ATR_BANDS ( data, 14 )

        atr_bands_upper = data['ATR_BANDS_UPPER'][-1]
        atr_bands_lower = data['ATR_BANDS_LOWER'][-1]

    #########  KC  #####
        data = __KC (data)

    #########  CMO  #####
        data = __CMO (data)

    #########  CMF  #####
        data = __CMF (data)

    #########  AO  #####
        data = __AO ( data, 5, 34 )

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['AO_Signal'] = np.select(
            [ ( data['AO'] > 0 ) & ( data['AO'].shift(1) < 0 ),
            (   data['AO'] < 0 ) & ( data['AO'].shift(1) > 0 )],
            [2, -2])

    #########  MFI  #####
        mfi_window = 14
        data       = __MFI ( data, mfi_window )

        # Define the overbought and oversold levels
        mfi_overbought = 80
        mfi_oversold   = 20

        # 2 = Long ( Buy Now ), 1 = Oversold ( Buy Soon ), 0 = Neutral, -1 = Overbought ( Sell Soon ), -2 = Short ( Sell Now )
        data['MFI_Signal'] = np.select(
            [ ( data['MFI_{}'.format(mfi_window)] > mfi_oversold )   & ( data['MFI_{}'.format(mfi_window)].shift(1) < mfi_oversold ),
            (   data['MFI_{}'.format(mfi_window)] < mfi_overbought)  & ( data['MFI_{}'.format(mfi_window)].shift(1) > mfi_overbought)],
            [2, -2])

    #########  ADX  #####
        data       = __ADX ( data , 14 )

    #########  MOM  #####
        data       = __MOM ( data, 14 )

    #########  TSI  #####
        data = __TSI ( data, 25, 13, 12)

    #########  ROC  #####
        data = __ROC ( data, 12, 6 )

    #########  PSAR  #####
        data = __PSAR ( data )



        ########################
        #####  STRATEGIES  #####
        ########################

        # A list of  messages for a ticker
        advice = []


        #####  1_BB_RSI_TEMA  #####
        with open('strategies/1_BB_RSI_TEMA.py') as f: exec(f.read())

        #####  2_EMA_TEMA  #####
        with open('strategies/2_EMA_TEMA.py') as f: exec(f.read())

        #####  3_SMA_5,8  #####
        with open('strategies/3_SMA.py') as f: exec(f.read())

        #####  4_CCI 20 crossover/crossunder  #####
        with open('strategies/4_CCI.py') as f: exec(f.read())

        #####  5_ATR_WR  #####
        with open('strategies/5_ATR_WR.py') as f: exec(f.read())

        #####  S6: KDJ  #####
        with open('strategies/6_KDJ.py') as f: exec(f.read())

        #####  S7: MACD  #####
        with open('strategies/7_MACD.py') as f: exec(f.read())

        #####  S8: EMA  #####
        with open('strategies/8_EMA.py') as f: exec(f.read())

        #####  20: AO_SAUCER  #####
        with open('strategies/20_AO_SAUCER.py') as f: exec(f.read())

        #####  21_TSI  #####
        with open('strategies/21_TSI.py') as f: exec(f.read())

        #####  22_BB_RSI  #####
        with open('strategies/22_BB_RSI.py') as f: exec(f.read())

        #####  23_CCI_MFI_RSI  #####
        with open('strategies/23_CCI_MFI_RSI.py') as f: exec(f.read())

        #####  24_CMCWinner: CCI_MFI_RSI  #####
        with open('strategies/24_CMCWinner.py') as f: exec(f.read())

        #####  25_ClucMay72018  #####
        with open('strategies/25_ClucMay72018.py') as f: exec(f.read())

        #####  26_EMASkipPump.py  #####
        with open('strategies/26_EMASkipPump.py') as f: exec(f.read())

        #####  27_MACDStrategy.py  #####
        with open('strategies/27_MACDStrategy.py') as f: exec(f.read())

        #####  S28: MACDStrategy_crossed  # _freq/user_data/strategies/berlinguyinca/MACDStrategy_crossed.py
        with open('strategies/28_MACDStrategy_crossed.py') as f: exec(f.read())

        #####  S29: Quickie  # _freq/user_data/strategies/berlinguyinca/Quickie.py
        with open('strategies/29_Quickie.py') as f: exec(f.read())

        #####  S30: Simple  #####
        with open('strategies/30_Simple.py') as f: exec(f.read())

        #####  S31: Trend  #####
        with open('strategies/31_Trend.py') as f: exec(f.read())

        #####  S32: PSAR  #####
        with open('strategies/32_PSAR.py') as f: exec(f.read())

        #####  S33: EMA CROSS 20, 50  Strategy001  #####
        with open('strategies/33_EMA_CROSS.py') as f: exec(f.read())


        #####  S34: BB_RSI_STO   Strategy 002  #####
        with open('strategies/34_BB_RSI_STO.py') as f: exec(f.read())

        #####  S35: EMA_MFI_RSI_STO   Strategy 003  #####
        with open('strategies/35_EMA_MFI_RSI_STO.py') as f: exec(f.read())

        #####  S36: Strategy 005  #####
        with open('strategies/36_005.py') as f: exec(f.read())

        #################
        #####  MQL5 #####
        #################

        #####  S40: MQL5_adx_crossover                      # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/adx_crossover.py
        with open('strategies/40_MQL5_adx_crossover.py') as f: exec(f.read())

        #####  S41: MQL5_awesome_zero_crossover             # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/awesome_zero_crossover.py
        with open('strategies/41_MQL5_awesome_zero_crossover.py') as f: exec(f.read())

        #####  S42: 42_MQL5_ADX_RSI                         # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/adx_rsi.py
        with open('strategies/42_MQL5_ADX_RSI.py') as f: exec(f.read())

        #####  S43: 43_MQL5_BladeRunner                     # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/BladeRunner.py
        with open('strategies/43_MQL5_BladeRunner.py') as f: exec(f.read())

        #####  S44: 44_MQL5_cci_macd_psar                   # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/cci_macd_psar.py
        with open('strategies/44_MQL5_cci_macd_psar.py') as f: exec(f.read())

        #####  S45: 45_MQL5_cci_moving_average              # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/cci_moving_average.py
        with open('strategies/45_MQL5_cci_moving_average.py') as f: exec(f.read())

        #####  S46: 46_MQL5_elder_ray                       # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/elder_ray.py
        with open('strategies/46_MQL5_elder_ray.py') as f: exec(f.read())
                                
        #####  S46: 46_MQL5_elder_ray 2                     # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/elder_ray_alternative.py
        with open('strategies/46_MQL5_elder_ray2.py') as f: exec(f.read())
                              
        #####  S47: 47_MQL5_ema_crossover_macd              # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/ema_crossover_macd.py
        with open('strategies/47_MQL5_ema_crossover_macd.py') as f: exec(f.read())

        #####  S48: 48_MQL5_ema_crossover_rsi               # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/ema_crossover_rsi.py
        with open('strategies/48_MQL5_ema_crossover_rsi.py') as f: exec(f.read())

        #####  S49: 49_MQL5_k_stoch_adx                     # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/k_stoch_adx.py
        with open('strategies/49_MQL5_k_stoch_adx.py') as f: exec(f.read())

        #####  S50: 50_MQL5_keltner_adx                     # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/keltner_adx.py
        with open('strategies/50_MQL5_keltner_adx.py') as f: exec(f.read())

        #####  S51: 51_MQL5_keltner_stochastic              # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/keltner_stochastic.py
        with open('strategies/51_MQL5_keltner_stochastic.py') as f: exec(f.read())
 

        #####  S52: 52_MQL5_macd_crossover                  # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/macd_crossover.py
        with open('strategies/52_MQL5_macd_crossover.py') as f: exec(f.read())

        #####  S53: 53_MQL5_macd_rsi_sma                    # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/macd_rsi_sma.py
        with open('strategies/53_MQL5_macd_rsi_sma.py') as f: exec(f.read())

        #####  S54: 54_MQL5_macd_stochastic_crossover       # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/macd_stochastic_crossover.py
        with open('strategies/54_MQL5_macd_stochastic_crossover.py') as f: exec(f.read())

        #####  S55: 55_MQL5_mfi_stochastic                  # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/mfi_stochastic.py
        with open('strategies/55_MQL5_mfi_stochastic.py') as f: exec(f.read())

        #####  S56: 56_MQL5_Rsi_2                           # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/rsi_2.py
        with open('strategies/56_MQL5_Rsi_2.py') as f: exec(f.read())

        #####  S57: 57_MQL5_tsi_crossover                   # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/57_MQL5_tsi_crossover.py
        with open('strategies/57_MQL5_tsi_crossover.py') as f: exec(f.read())

        #####  S58: 58_MQL5_williams_rsi                    # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/williams_rsi.py
        with open('strategies/58_MQL5_williams_rsi.py') as f: exec(f.read())

        #####  S59: 59_MQL5_williams_stochastic # https://github.com/Amar0628/MQL5-Python-Backtesting trading_strategies/williams_stochastic.py
        #with open('strategies/59_MQL5_williams_stochastic.py') as f: exec(f.read())

        # ------------------------------------------------------------ #

        #####  S50: S50_ADXMomemtum                         # https://github.com/alisalavati/freq user_data/strategies/berlinguyinca/ADXMomentum.py
        with open('strategies/50_ADXMomentum.py') as f: exec(f.read())

        #####  S51: AdxSmas                                 # https://github.com/alisalavati/freq user_data/strategies/berlinguyinca/AdxSmas.py
        with open('strategies/51_AdxSmas.py') as f: exec(f.read())


        #####  S52: AwesomeMacd                             # https://github.com/alisalavati/freq user_data/strategies/berlinguyinca/AwesomeMacd.py
        with open('strategies/52_AwesomeMacd.py') as f: exec(f.read())

        #####  S53: BBandsRsi                               # https://github.com/alisalavati/freq user_data/strategies/berlinguyinca/BBandRsi.py
        with open('strategies/53_BBandRsi.py') as f: exec(f.read())

        #####  S70: 70_3EMA_RSI_ATR                         # https://github.com/WaveyTechLtd/Stock_market_trader_EMA_RSI_ATR/blob/443b2e74d203f12c61f4e174789518c9ca8a5736/3EMA_RSI_ATR_youtube_v3.py
        with open('strategies/70_3EMA_RSI_ATR.py') as f: exec(f.read())

        print ("\n")
        
    time.sleep ( int ( refresh ) )

        ##### S20 
        #data['mean-volume'] = data['Volume'].rolling(12).mean()
        #data = __ADX ( data , 35 )

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
