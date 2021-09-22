import pandas as pd
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import plotly.express as px
import plotly.graph_objects as go

yf.pdr_override()

startyear=2019
startmonth=1
startday=1

start = dt.datetime(startyear,startmonth,startday)

now = now=dt.datetime.now()

def listToString(list):   
    # initialize an empty string
    str1 = " " 
    # return string  
    return (str1.join(list))

stocks=list(map(str,input("Enter up to five stock ticker symbols: ").split()))

print(stocks) 

newDf = pd.DataFrame()

SPYIndex = pdr.get_data_yahoo("SPY",start,now)

print(SPYIndex)

stocksInRange = []
stocksOutOfRange = []

count = 0

fig = go.Figure()

for stock in stocks:
    
    dataFrame=pdr.get_data_yahoo(stock,start,now)

    print(dataFrame)

    low_of_52week = min(dataFrame["Adj Close"][-260:]) #Finds minimum value of last 260 closing prices (260 trading days in 52 weeks)
    high_of_52week = max(dataFrame["Adj Close"][-260:]) #Finds maximum value of last 260 closing prices (260 trading days in 52 weeks)

    dataFrame["RS"] = (dataFrame["Adj Close"]/SPYIndex["Adj Close"])

    columnName = "RS_"+stock

    newDf[columnName] = dataFrame["RS"]

    print(newDf)

    if count == 0:
        newDf["date"] = newDf.index

    count = count + 1

    currentClose = dataFrame["Adj Close"][-1] #Access most recent close price from Yahoo finance database

    if currentClose >= (0.8*high_of_52week): 
        stocksInRange.append(stock)
    else:
        stocksOutOfRange.append(stock)

    fig.add_trace(go.Scatter(x=newDf["date"], y=newDf[columnName], mode="lines", name=columnName))

print(newDf)

fig.show()

print("Stocks within 20 percent of 52 week high: "+ listToString(stocksInRange))

if not stocksOutOfRange:
    print("Stocks out of desired range: none")
else:
    print("Stocks out of desired range: "+ listToString(stocksOutOfRange))