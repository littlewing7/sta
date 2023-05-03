# Load the necessary packages and modules
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


# In[19]:


# Ease of Movement 
def EMV(data, ndays): 
    dm = ((data['High'] + data['Low'])/2) - ((data['High'].shift(1) + data['Low'].shift(1))/2)
    br = (data['Volume'] / 100000000) / ((data['High'] - data['Low']))
    EMV = dm / br 
    EMV_MA = pd.Series(EMV.rolling(ndays).mean(), name = 'EMV') 
    data = data.join(EMV_MA) 
    return data 


# In[20]:


# Retrieve the AAPL data from Yahoo finance
data = yf.download("AAPL", start="2020-01-01", end="2022-04-30")  

# Compute the 14-day Ease of Movement for AAPL
n = 14
AAPL_EMV = EMV(data, n)
EMV = AAPL_EMV['EMV']

# Plotting the Price Series chart and the Ease Of Movement below
fig = plt.figure(figsize=(10, 7))

# Define position of 1st subplot
ax = fig.add_subplot(2, 1, 1)

# Set the title and axis labels
plt.title('AAPL Price Chart')
plt.xlabel('Date')
plt.ylabel('Close Price')

# Plot the close price of the Apple
plt.plot(data['Close'], label='Close price')

# Add a legend to the axis
plt.legend()

# Define position of 2nd subplot
bx = fig.add_subplot(2, 1, 2)

# Set the title and axis labels
plt.title('Ease Of Movement Chart')
plt.xlabel('Date')
plt.ylabel('EMV values')

# Plot the ease of movement
plt.plot(EMV, 'm', label='EMV(14)')

# Add a legend to the axis
plt.legend()

plt.tight_layout()
plt.show()

