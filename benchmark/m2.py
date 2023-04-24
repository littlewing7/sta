import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    # Calculate MACD
    data["ema_short"] = data["Close"].ewm(span=short_period, adjust=False).mean()
    data["ema_long"] = data["Close"].ewm(span=long_period, adjust=False).mean()
    data["macd"] = data["ema_short"] - data["ema_long"]
    data["signal"] = data["macd"].ewm(span=signal_period, adjust=False).mean()

    # Generate trading signals based on MACD cross above/below signal line
    data["positions"] = 0
    data["positions"][short_period:] = \
        [1 if data["macd"][i] > data["signal"][i] else -1 if data["macd"][i] < data["signal"][i] else 0 for i in range(short_period, len(data))]
    data["signals"] = data["positions"].diff()

    return data[["Close", "macd", "signal", "positions", "signals"]]

# Download historical data for Apple stock (AAPL)
ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2023-01-01"
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate MACD and trading signals
macd_data = calculate_macd(data)

# Calculate returns based on trading signals
initial_investment = 100000
macd_data["shares"] = (initial_investment * macd_data["signals"]) // macd_data["Close"]
macd_data["positions"] = macd_data["shares"].cumsum().clip(lower=-1, upper=1)
macd_data["strategy_returns"] = macd_data["positions"].shift(1) * macd_data["Close"].pct_change()
macd_data["cumulative_returns"] = (macd_data["strategy_returns"] + 1).cumprod()

# Plot cumulative returns
plt.plot(macd_data["cumulative_returns"])
plt.title(f"Cumulative Returns for {ticker}")
plt.xlabel("Date")
plt.ylabel("Returns")
plt.show()

