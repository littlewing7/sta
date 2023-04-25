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

#            Period           Interval              Sleep before refresh data
TIMEFRAMES = {
    "1m":  { "Period": "7d",   "Interval": "1m",    "Refresh": "60"   },
    "5m":  { "Period": "30d",  "Interval": "5m",    "Refresh": "60"  },
    "15m": { "Period": "30d",  "Interval": "15m",   "Refresh": "60"  },
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

# log file
parser.add_argument('-l', '--logfile', type=str, required=False, help='log file i.e. app.log')

# Add a positional argument for a list of stocks
parser.add_argument('-t', '--tickers', type=str, nargs='+', required=True, help='list of stock tickers')

# Add a positional argument for a strategy
parser.add_argument('-s', '--strategies', type=str, nargs='+', required=False, help='load named strategies from strategie/ folder')

# Add a positional argument for a strategy
parser.add_argument('-r', '--refresh', type=str, required=False, help='override default refresh settings, in seconds')


# Parse the command-line arguments
args = parser.parse_args()

strategies = {}
indicators = {}
counter = 0

period   = TIMEFRAMES[args.interval]['Period']
interval = TIMEFRAMES[args.interval]['Interval']
refresh  = TIMEFRAMES[args.interval]['Refresh']

if ( args.logfile ):
    append_to = args.logfile
else:
    append_to = "app.log"
logging.basicConfig(filename=append_to, filemode='a', format='%(name)s - %(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')



for ticker in args.tickers:
    strategies[ticker] = []
    indicators[ticker] = []


while True:

    def print_log ( strategy_name, long_short='LONG', *ind):
        my_list = sorted ( set ( strategies[ticker] ) )
        #print ( my_list )
        if strategy_name not in my_list:
            message = f"{ticker} {interval} ---> {long_short} ::: {strategy_name} ::: {ind}"
            logging.warning(message)
            strategies[ticker].append(strategy_name)
            #indicators[ticker].extend ( ind )
            print ( f"{message}")

    counter += 1
    print ("-------------------------  %d  -------------------------" % counter) 

    # Use the list of stocks and integer value in the script
    for ticker in args.tickers:
        
        #my_list = list ( set ( strategies[ticker] ))
        
        now = datetime.datetime.now()

        print("=====  " + ticker + "  =====  " + now.strftime("%Y-%m-%d %H:%M:%S") + "  =====" )
    
        # Get stock data from Yahoo Finance
        #data = yf.download(ticker, period="5y")
        data = yf.download(ticker, period=period, interval = interval, progress=False, threads=True )
     
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

        #data['Trend_20']   = data['Close'] / data['Close'].rolling(20).mean()

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

        #data['Trend_20'] = data['Close'] / data['Close'].rolling(20).mean()

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
        mfi_overbought = 80
        mfi_oversold   = 20
        data       = __MFI ( data, mfi_window )

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

        # Load strategy files from command line
        if args.strategies:
            for strategy_file in args.strategies:
                  with open ( 'strategies/' + strategy_file ) as f: exec(f.read())
                  

        # Load all strategy files from strategies/ folder
        else:
            path = 'strategies' 
            files = os.listdir(path)
            files_py = [i for i in files if i.endswith('.py')]
            files_py = sorted ( files_py )

            for strategy_file in files_py:
                #print ("Loading file: strategies/" + strategy_file)
                with open ( 'strategies/' + strategy_file ) as f: exec(f.read())
   
        #print ("\n")

    #print ( strategies )
    #print ( indicators )        

    if ( args.refresh ):
        time.sleep ( int ( args.refresh ) )
    else:
        time.sleep ( int ( refresh ) )
