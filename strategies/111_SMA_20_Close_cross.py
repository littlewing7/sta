# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---

# SMA 5, SMA 8
data = __SMA  ( data, 20 )


def backtest_strategy(stock, start_date ):
    """
    Function to backtest a strategy
    """

    csv_file = "./data/{}_1d.csv".format( stock )

    # Get today's date
    today = datetime.datetime.now().date()

    # if the file was downloaded today, read from it
    if  ( ( os.path.exists ( csv_file ) ) and ( datetime.datetime.fromtimestamp ( os.path.getmtime ( csv_file ) ).date() == today ) ):
        data = pd.read_csv ( csv_file, index_col='Date' )
    else:
        # Download data
        data = yf.download(stock, start=start_date, progress=False)
        data.to_csv ( csv_file )

    # Calculate indicator
    data = __SMA (data, 20)

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):
        # Buy signal
        if data["Adj Close"][i] > data["SMA_20"][i] and data["Adj Close"][i - 1] < data["SMA_20"][i - 1] and position == 0:
            position = 1
            buy_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Buying {stock} at {buy_price} @ {today}")

        # Sell signal
        elif data["Adj Close"][i] < data["SMA_20"][i] and data["Adj Close"][i - 1]  > data["SMA_20"][i - 1] and position == 1:
            position = 0
            sell_price = data["Adj Close"][i]
            today = data.index[i]
            #print(f"Selling {stock} at {sell_price} @ {today}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000
    percentage = ( ( (total_returns - 100000) / 100000) * 100)
    percentage = "{:.0f}".format ( percentage )

    return percentage + '%'


# Price crossover SMA 20
if ( ( data["Adj Close"][-1] > data["SMA_20"][-1] ) and ( data["Adj Close"][-2] < data["SMA_20"][-2] ) ):
    print_log ( '111_SMA_20_Close_cross', 'LONG', [ 'SMA_20', 'Close' ] , backtest_strategy ( ticker , '2020-01-01' ) )

# Price crossunder SMA 20
if ( ( data["Adj Close"][-1] < data["SMA_20"][-1] ) and ( data["Adj Close"][-2] > data["SMA_20"][-2] ) ):
    print_log ( '111_SMA_20_Close_cross', 'SHORT', [ 'SMA_20', 'Close' ] , backtest_strategy ( ticker , '2020-01-01' ) )




