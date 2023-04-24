# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---

# SMA 5, SMA 8
data = __SMA  ( data, 20 )

# Price crossover SMA 20
if ( ( data["Close"][-1] > data["SMA_20"][-1] ) and ( data["Close"][-2] < data["SMA_20"][-2] ) ):
    print_log ( '111_SMA_20_Close', 'LONG', [ 'SMA_20', 'Close' ] )

# Price crossunder SMA 20
if ( ( data["Close"][-1] < data["SMA_20"][-1] ) and ( data["Close"][-2] > data["SMA_20"][-2] ) ):
    print_log ( '111_SMA_20_Close', 'SHORT', [ 'SMA_20', 'Close' ] )




