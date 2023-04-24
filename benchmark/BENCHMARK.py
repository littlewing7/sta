import yfinance as yf
import pandas as pd


def calculate_stochastic_rsi(data, n=14, k=3):
    """
    Function to calculate stochastic RSI
    """
    rsi = calculate_rsi(data, n)
    rsi_range = rsi.max() - rsi.min()
    data["stoch_rsi"] = (rsi - rsi.min()) / rsi_range
    data["stoch_rsi_K"] = data["stoch_rsi"].rolling(k).mean() * 100
    data["stoch_rsi_D"] = data["stoch_rsi_K"].rolling(k).mean()

    return data


def calculate_rsi(data, n=14):
    """
    Function to calculate RSI
    """
    delta = data["Adj Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(n).mean()
    avg_loss = loss.rolling(n).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def backtest_strategy(stock, start_date, end_date):
    """
    Function to backtest a strategy
    """
    # Download data
    data = yf.download(stock, start=start_date, end=end_date)

    # Calculate Stochastic RSI
    data = calculate_stochastic_rsi(data)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["stoch_rsi_K"][i] > 20 and data["stoch_rsi_D"][i] > 20 and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif data["stoch_rsi_K"][i] < 80 and data["stoch_rsi_D"][i] < 80 and position == 1:
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
    stock = "XLE"
    start_date = "2020-01-01"
    end_date = "2023-04-19"
    backtest_strategy(stock, start_date, end_date)
    backtest_strategy("SPY", start_date, end_date)


