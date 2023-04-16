#import yfinance as yf
import pandas as pd

########################
#####  PANDAS MOM  #####
########################

#def __MOM (data, window=14):
#
#    # Calculate the Momentum (MOM) indicator
#    mom = pd.Series(data["Close"]).diff(window)
#
#    # Add the MOM indicator to the DataFrame
#    data["MOM_14"] = mom
#
#    return data

#Momentum
def __MOM(data, window=14):
    M = pd.Series(data['Close'].diff(window), name = 'MOM_' + str(window))
    data = data.join(M)
    return data

