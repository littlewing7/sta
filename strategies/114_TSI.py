#TSI

data = __TSI ( data, 25, 13, 12 )

line = data['TSI']
signal = data['TSI_SIGNAL']


def backtest_strategy1 (stock, start_date):
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

    # Calculate Stochastic RSI
    data = __TSI ( data, 25, 13, 12 )

    line = data['TSI']
    signal = data['TSI_SIGNAL']


# BUY CRITERIA: if TSI line and signal line is below 0 and tsi crosses signal line

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if (position == 0) and  (  line.iloc[i] < 0 and signal.iloc[i] < 0 and line.iloc[i-1] < 0 and signal.iloc[i-1] < 0) and \
            ((line.iloc[i] > signal.iloc[i] and line.iloc[i-1] < signal.iloc[i-1]) or (
              line.iloc[i] < signal.iloc[i] and line.iloc[i-1] > signal.iloc[i-1])):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( position == 1 ) and (line.iloc[i] > 0 and signal.iloc[i] > 0 and line.iloc[i-1] > 0 and signal.iloc[i-1] > 0) and \
            ((line.iloc[i] < signal.iloc[i] and line.iloc[i-1] > signal.iloc[i-1]) or (
              line.iloc[i] > signal.iloc[i] and line.iloc[i-1] < signal.iloc[i-1])):
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000
    percentage = ( ( (total_returns - 100000) / 100000) * 100)
    percentage = "{:.0f}".format ( percentage )

    return percentage + '%'


# BUY CRITERIA 1: if TSI line and signal line is below 0 and tsi crosses signal line
if (line.iloc[-1] < 0 and signal.iloc[-1] < 0 and line.iloc[-2] < 0 and signal.iloc[-2] < 0) and \
    ((line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2]) or (
    line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2])):
    print_log ( '114_TSI', 'LONG', [ 'TSI' ], backtest_strategy1 ( ticker , '2020-01-01' ) )

# SELL CRITERIA1: if TSI line and signal line has crossed above 0 and TSI line crosses signal
if (line.iloc[-1] > 0 and signal.iloc[-1] > 0 and line.iloc[-2] > 0 and signal.iloc[-2] > 0) and \
    ((line.iloc[-1] < signal.iloc[-1] and line.iloc[-2] > signal.iloc[-2]) or (
    line.iloc[-1] > signal.iloc[-1] and line.iloc[-2] < signal.iloc[-2])):
    print_log ( '114_TSI', 'SHORT', [ 'TSI' ] , backtest_strategy1 ( ticker , '2020-01-01' ) )





def backtest_strategy2 (stock, start_date):
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

    # Calculate Stochastic RSI
    data = __TSI ( data, 25, 13, 12 )

    # Set initial conditions
    position = 0
    buy_price = 0
    sell_price = 0
    returns = []

    # Loop through data
    for i in range(len(data)):

        # Buy signal
        if ( data["TSI"][i-1] < data["TSI_SIGNAL"][i-1] ) and ( data["TSI"][i] > data["TSI_SIGNAL"][i] ) and ( position == 0 ):
            position = 1
            buy_price = data["Adj Close"][i]
            #print(f"Buying {stock} at {buy_price}")

        # Sell signal
        elif ( data["TSI"][i-1] > data["TSI_SIGNAL"][i-1] ) and ( data["TSI"][i] < data["TSI_SIGNAL"][i] ) and ( position == 1 ):
            position = 0
            sell_price = data["Adj Close"][i]
            #print(f"Selling {stock} at {sell_price}")

            # Calculate returns
            returns.append((sell_price - buy_price) / buy_price)

    # Calculate total returns
    total_returns = (1 + sum(returns)) * 100000
    percentage = ( ( (total_returns - 100000) / 100000) * 100)
    percentage = "{:.0f}".format ( percentage )

    return percentage + '%'


# BUY CRITERIA 2:
if data["TSI"][-2] < data["TSI_SIGNAL"][-2] and data["TSI"][-1] > data["TSI_SIGNAL"][-1]:
    print_log ( '114_TSI_2', 'LONG', [ 'TSI' ], backtest_strategy2 ( ticker , '2020-01-01' ) )

# SELL CRITERIA 2:
if data["TSI"][-2] > data["TSI_SIGNAL"][-2] and data["TSI"][-1] < data["TSI_SIGNAL"][-1]:
    print_log ( '114_TSI_2', 'SHORT', [ 'TSI' ] , backtest_strategy2 ( ticker , '2020-01-01' ) )

