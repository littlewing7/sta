#!/usr/bin/env python3

import yfinance as yf
import pandas as pd

#  WMA and Double WMA
def __DWMA(df, window):
    weights = pd.Series(range(1,window+1))
    wma = df['Close'].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    #df_wma = pd.concat([df['Close'], wma], axis=1)
    #df_wma.columns = ['Close', 'WMA']
    #return df_wma
    df['WMA_{}'.format(window)] = wma
    df['DWMA_{}'.format(window)] = df['WMA_{}'.format(window)].rolling(window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    return df

def backtest_strategy(stock, start_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download(stock, start=start_date, progress=False)

    # Calculate Stochastic RSI
    data = __DWMA (data, 20)
    data = __DWMA (data, 50)
    #print ( data.tail(2) )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["DWMA_20"][i] > data["DWMA_50"][i] and data["DWMA_20"][i - 1] < data["DWMA_50"][i - 1] and position == 0:
            position = 1
            buy_price = data["Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["DWMA_20"][i] < data["DWMA_50"][i] and data["DWMA_20"][i - 1]  > data["DWMA_50"][i - 1] and position == 1:
            position = 0
            sell_price = data["Close"][i]
            today = data.index[i]
            #print(f"Selling {stock} at {sell_price} @ {today}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000

    import sys
    name = sys.argv[0]

    # Print results
    print(f"\n{name} ::: {stock} Backtest Results ({start_date} - today)")
    print(f"---------------------------------------------")
    print(f"{name} ::: {stock} - Total Returns: ${total_returns:,.2f}")
    print(f"{name} ::: {stock} - Profit/Loss: {((total_returns - 100000) / 100000) * 100:.2f}%")


if __name__ == '__main__':

    start_date = "2020-01-01"

    backtest_strategy("AAPL", start_date)
    print ("\n")
    backtest_strategy("SPY", start_date)

