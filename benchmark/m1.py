import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Set initial investment amount
initial_investment = 100000

# Download historical data
ticker = "AAPL"  # replace with your desired ticker
start_date = "2019-01-01"  # replace with your desired start date
end_date = "2022-04-23"  # replace with your desired end date
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate MACD
short_period = 12
long_period = 26
signal_period = 9
data["ema_short"] = data["Close"].ewm(span=short_period, adjust=False).mean()
data["ema_long"] = data["Close"].ewm(span=long_period, adjust=False).mean()
data["macd"] = data["ema_short"] - data["ema_long"]
data["signal"] = data["macd"].ewm(span=signal_period, adjust=False).mean()

# Generate trading signals based on MACD cross above/below signal line
data["positions"] = 0
data["positions"][short_period:] = \
    [1 if data["macd"][i] > data["signal"][i] else -1 if data["macd"][i] < data["signal"][i] else 0 for i in range(short_period, len(data))]
data["signals"] = data["positions"].diff()

# Calculate returns based on trading signals
data["shares"] = (initial_investment * data["signals"]) // data["Close"]
data["positions"] += data["shares"]
data["positions"] = data["positions"].clip(lower=-1, upper=1)  # limit to no more than 1 share per trade
data["strategy_returns"] = data["positions"].shift(1) * data["Close"].pct_change()

# Calculate cumulative returns and ending amount
data["cumulative_returns"] = (data["strategy_returns"] + 1).cumprod()
ending_amount = initial_investment * data["cumulative_returns"][-1]

# Calculate percentage gains or losses
total_return = (ending_amount / initial_investment - 1) * 100

# Plot cumulative returns
plt.plot(data["cumulative_returns"])
plt.title(f"Cumulative Returns for {ticker}")
plt.xlabel("Date")
plt.ylabel("Returns")
plt.show()

# Print ending amount and percentage gains or losses
print(f"Ending amount: ${ending_amount:.2f}")
print(f"Total return: {total_return:.2f}%")

