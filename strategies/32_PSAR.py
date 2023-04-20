
data = __PSAR ( data )

#Buy Criteria - current pSAR below close, previous pSAR above close
if data["PSAR"].iloc[-1] < data["Close"].iloc[-1] and data["PSAR"].iloc[-2] > data["Close"].iloc[-2]:
    print ("LONG ::: 32_PSAR\n")

#Sell Criteria - current pSAR above close, previous pSAR below close
if data["PSAR"].iloc[-1] > data["Close"].iloc[-1] and data["PSAR"].iloc[-2] < data["Close"].iloc[-2]:
    print ("SHORT ::: 32_PSAR\n")

