##############################
#####  S27: MACDStrategy #####
##############################
# _freq/user_data/strategies/berlinguyinca/MACDStrategy.py
buy_cci = -48
sell_cci = 687


if ( ( data['MACD'][-1]    >  data['MACD_SIGNAL'][-1] ) &
    (  data['CCI_20'][-1]  <= buy_cci) &
    (  data['Volume'][-1]  > 0) ):
    print ( f"{ticker} {interval} ---> LONG ::: S27_MACDStrategy\n")
    strategy_log[ticker].append
if ( ( data['MACD'][-1]    <  data['MACD_SIGNAL'][-1] ) &
    (  data['CCI_20'][-1]  >= sell_cci ) &
    (  data['Volume'][-1]  > 0) ):
    message = f"{ticker} {interval} ---> SHORT ::: S27_MACDStrategy"
    print ( f"{message}\n")
    logging.warning(message)

strategies[ticker].append('LONG_S27_MACDStrategy')


