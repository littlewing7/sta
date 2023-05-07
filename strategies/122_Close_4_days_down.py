# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---


if ( ( data["Close"][-1] > data["Close"][-2] > data["Close"][-3] < data["Close"][-4] ) ):
    print_log ( '122_Close_4_days_down', 'LONG', [ 'Close' ] )

if ( ( data["Close"][-1] > data["Close"][-2] > data["Close"][-3] ) ):
    print_log ( '122_Close_4_days_down', 'SHORT', [ 'Close' ] )




