import pandas as pd
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

yf.pdr_override()

startyear=2020
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
fig = make_subplots(specs=[[{"secondary_y": True}],
                          [{"secondary_y": True}]],
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0,
                    )
fig.update_layout(title_text="Stock Price Performance vs. Relative Strength")
fig.update_yaxes(title_text="<b>Relative Strength</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>Stock Price</b>", secondary_y=True)

for stock in stocks:
    
    dataFrame=pdr.get_data_yahoo(stock,start,now)

    print(dataFrame)

    low_of_52week = min(dataFrame["Adj Close"][-260:]) #Finds minimum value of last 260 closing prices (260 trading days in 52 weeks)
    high_of_52week = max(dataFrame["Adj Close"][-260:]) #Finds maximum value of last 260 closing prices (260 trading days in 52 weeks)

    dataFrame["RS"] = (dataFrame["Adj Close"]/SPYIndex["Adj Close"])

    columnName = "RS_"+stock

    newDf[columnName] = dataFrame["RS"]

    closingPrice = stock+"_Price"

    newDf[closingPrice] = dataFrame["Adj Close"]

    print(newDf)

    if count == 0:
        newDf["Date"] = newDf.index

    count = count + 1

    currentClose = dataFrame["Adj Close"][-1] #Access most recent close price from Yahoo finance database

    if currentClose >= (0.8*high_of_52week): 
        stocksInRange.append(stock)
    else:
        stocksOutOfRange.append(stock)

    fig.add_trace(go.Scatter(x=newDf["Date"], y=newDf[columnName], mode="lines", name=columnName, line=dict(dash='dash')), row=2, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=newDf["Date"], y=newDf[closingPrice], mode="lines", name=closingPrice), row=1, col=1, secondary_y=True)

fig.add_trace(go.Scatter(x=newDf["Date"], y=SPYIndex["Adj Close"], mode="lines", name=SPY_Price), row=1, col=1, secondary_y=True)

fig.show()

print("Stocks within 20 percent of 52 week high: "+ listToString(stocksInRange))

if not stocksOutOfRange:
    print("Stocks out of desired range: none")
else:
    print("Stocks out of desired range: "+ listToString(stocksOutOfRange))