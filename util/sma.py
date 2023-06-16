########################
#####  PANDAS SMA  #####
########################
#def SMA ( close, t ):
#    import talib
#    return talib.SMA( close, t)
# https://github.com/Priyanshu154/Backtest/blob/511e2e8525b23a14ecdf5a48c28399c7fd41eb14/Backtest/Backtest/Indicator.py

## Retrieve the data using yfinance
#data = yf.download(tickers, start=start_date, end=end_date, interval='1d')
#
## Calculate the SMA 5 and SMA 8
#data['SMA5'] = data['Close'].rolling(window=5).mean()
#data['SMA8'] = data['Close'].rolling(window=8).mean()

#def __SMA(close, t):
#    mas = []
#    for i in range(t - 1):
#        mas.append(-1)
#    for i in range(len(close) - t + 1):
#        summ = 0
#        for j in range(i, t + i):
#            summ = summ + close[j]
#        meann = summ / t
#        mas.append(meann)
#    return mas
##SMA Ends here

def __SMA ( data, n ):
    data['SMA_{}'.format(n)] = data['Adj Close'].rolling(window=n).mean()
    #data['Trend_{}'.format(n)]= data['Close'] / data['Close'].rolling(n).mean()
    return data

