# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---

# DWMA 14
data = WMA  ( data, 14 )

# Price crossover DWMA 14
if ( ( data["Close"][-1] > data["DWMA_14"][-1] ) and ( data["Close"][-2] < data["DWMA_14"][-2] ) ):
    print_log ( '118_DWMA_14_Close', 'LONG', [ 'DWMA_14', 'Close' ] )

# Price crossunder DWMA 14
if ( ( data["Close"][-1] < data["DWMA_14"][-1] ) and ( data["Close"][-2] > data["DWMA_14"][-2] ) ):
    print_log ( '118_DWMA_14_Close', 'SHORT', [ 'DWMA_14', 'Close' ] )




