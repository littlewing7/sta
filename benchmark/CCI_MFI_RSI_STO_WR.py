import yfinance as yf
import pandas as pd
import numpy as np

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
    return data

def __CCI(df, ndays = 20):
    df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['sma'] = df['TP'].rolling(ndays).mean()
    df['mad'] = df['TP'].rolling(ndays).apply(lambda x: pd.Series(x).mad())

    df['CCI_20'] = (df['TP'] - df['sma']) / (0.015 * df['mad'])

    df = df.drop('TP', axis=1)
    df = df.drop('sma', axis=1)
    df = df.drop('mad', axis=1)

    df['CCI_Signal'] = np.select(
           [ ( df['CCI_{}'.format(ndays)] > -100) & ( df['CCI_{}'.format(ndays)].shift(1) < -100),
            (  df['CCI_{}'.format(ndays)] <  100) & ( df['CCI_{}'.format(ndays)].shift(1) >  100)],
        [2, -2])

    return df

def __WR (data, t):
    highh = data["High"].rolling(t).max()
    lowl  = data["Low"].rolling(t).min()
    close = data["Close"]

    data['WR_{}'.format(t)] = -100 * ((highh - close) / (highh - lowl))

    data['WR_Signal'] = np.select(
            [ ( data['WR_{}'.format(t)] > -80 ) & ( data['WR_{}'.format(t)].shift(1) < -80),
            (   data['WR_{}'.format(t)] < -20 ) & ( data['WR_{}'.format(t)].shift(1) > -20)],
            [2, -2])

    return data

def __STOCHASTIC (df, k, d):
     temp_df = df.copy()
     # Set minimum low and maximum high of the k stoch
     low_min = temp_df["Low"].rolling(window=k).min()
     high_max = temp_df["High"].rolling(window=k).max()

     # Fast Stochastic
     temp_df['k_fast'] = 100 * (temp_df["Close"] - low_min)/(high_max - low_min)
     temp_df['d_fast'] = temp_df['k_fast'].rolling(window=d).mean()

     # Slow Stochastic
     temp_df['STO_K'] = temp_df["d_fast"]
     temp_df['STO_D'] = temp_df['STO_K'].rolling(window=d).mean()

     temp_df = temp_df.drop(['k_fast'], axis=1)
     temp_df = temp_df.drop(['d_fast'], axis=1)

     sto_overbought       = 80
     sto_oversold         = 20

     temp_df['STO_Signal'] = np.select(
            [ ( ( temp_df['STO_K'] > sto_oversold )   & ( temp_df['STO_K'].shift(1) < sto_oversold ) ),
              ( ( temp_df['STO_K'] < sto_overbought ) & ( temp_df['STO_K'].shift(1) > sto_overbought ) )],
            [2, -2])
     return temp_df

def __RSI ( data: pd.DataFrame, window: int = 14, round_rsi: bool = True):

    delta = data["Close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm ( up, alpha =1 / window ).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha = 1 / window ).mean()

    rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

    if ( round_rsi ):
        data['RSI_{}'.format ( window )] = np.round (rsi, 2)
    else:
        data['RSI_{}'.format( window )] = rsi

    data['RSI_Signal'] = np.select(
            [ ( data['RSI_{}'.format(window)] > 40 ) & ( data['RSI_{}'.format(window)].shift(1) < 40),
              ( data['RSI_{}'.format(window)] < 60)  & ( data['RSI_{}'.format(window)].shift(1) > 60)],
            [2, -2])

    return data


def __MFI ( data, window=14):
    # Calculate the Money Flow Index (MFI)
    typical_price = ( data['High'] + data['Low'] + data['Close']) / 3
    money_flow = typical_price * data['Volume']
    positive_money_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_money_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    money_ratio = positive_money_flow.rolling(window=window).sum() / negative_money_flow.rolling(window=window).sum()
    mfi = 100 - (100 / (1 + money_ratio))

    data['MFI_{}'.format(window)] = mfi

    mfi_overbought = 80
    mfi_oversold = 20
    data['MFI_Signal'] = np.select(
            [ ( data['MFI_{}'.format(window)] > mfi_oversold )   & ( data['MFI_{}'.format(window)].shift(1) < mfi_oversold ),
            (   data['MFI_{}'.format(window)] < mfi_overbought)  & ( data['MFI_{}'.format(window)].shift(1) > mfi_overbought)],
            [2, -2])

    return data



def backtest_strategy(stock, start_date, end_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download(stock, start=start_date, end=end_date)

    # Calculate Stochastic RSI
    data = __SMA (data, 20)
    data = __SMA (data, 50)
    data = __CCI ( data, 20 )
    data = __MFI ( data, 14 )
    data = __RSI ( data, 20 )
    data = __STOCHASTIC ( data, 14, 3 )
    data = __WR ( data, 20 )

    #print ( data.tail(60))

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []


    # Loop through data
    for i in range(len(data)):
        go_long  = 0
        go_short = 0

        if ( data['CCI_Signal'][i] == 2 ):
            go_long += 1
        if ( data['MFI_Signal'][i] == 2 ):
            go_long += 1
        if ( data['RSI_Signal'][i] == 2 ):
            go_long += 1
        if ( data['STO_Signal'][i] == 2 ):
            go_long += 1
        if ( data['WR_Signal'][i] == 2 ):
            go_long += 1

        if ( data['CCI_Signal'][i] == -2 ):
            go_short += 1
        if ( data['MFI_Signal'][i] == -2 ):
            go_short += 1
        if ( data['RSI_Signal'][i] == -2 ):
            go_short += 1
        if ( data['STO_Signal'][i] == -2 ):
            go_short += 1
        if ( data['WR_Signal'][i] == -2 ):
            go_short += 1

        # Buy signal
        #if ( data['MFI_Signal'][i] == 2 and  (position == 0 )):
        if ( go_long >= 3 and  (position == 0 )):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        #elif ( data['MFI_Signal'][i] == -2 and  (position == 1 )):
        elif ( go_short >= 3 and ( position == 1 )):
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000

    # Print results
    print(f"\n{stock} Backtest Results ({start_date} - {end_date})")
    print(f"---------------------------------------------")
    print(f"Total Returns: ${total_returns:,.2f}")
    print(f"Profit/Loss: {((total_returns - 100000) / 100000) * 100:.2f}%")


if __name__ == '__main__':

    stock = "AAPL"
    start_date = "2020-01-01"
    end_date = "2023-04-19"

    backtest_strategy(stock, start_date, end_date)
    backtest_strategy("SPY", start_date, end_date)

