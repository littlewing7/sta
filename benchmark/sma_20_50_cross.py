import yfinance as yf
import pandas as pd

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Close'].rolling(window=n).mean()
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

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["SMA_20"][i] > data["SMA_50"][i] and data["SMA_20"][i - 1] < data["SMA_50"][i - 1] and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif data["SMA_20"][i] < data["SMA_50"][i] and data["SMA_20"][i - 1]  > data["SMA_50"][i - 1] and position == 1:
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

