
data = __PSAR ( data )

#Buy Criteria - current pSAR below close, previous pSAR above close
if data["PSAR"].iloc[-1] < data["Adj Close"].iloc[-1] and data["PSAR"].iloc[-2] > data["Adj Close"].iloc[-2]:
    print_log ( '32_PSAR', 'LONG', [ 'PSAR' ] )

#Sell Criteria - current pSAR above close, previous pSAR below close
if data["PSAR"].iloc[-1] > data["Adj Close"].iloc[-1] and data["PSAR"].iloc[-2] < data["Adj Close"].iloc[-2]:
    print_log ( '32_PSAR', 'SHORT', [ 'PSAR' ] )

