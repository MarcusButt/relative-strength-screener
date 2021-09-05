import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

startyear=2018
startmonth=1
startday=1

start = dt.datetime(startyear,startmonth,startday)

now = now=dt.datetime.now()

stocks=list(map(str,input("Enter up to five stock ticker symbols: ").split()))

print(stocks) 

dataFrame=pdr.get_data_yahoo(stocks,start,now)

print(dataFrame)

newDf = pd.DataFrame()

SPYIndex = pdr.get_data_yahoo("SPY",start,now)

print(SPYIndex)

low_of_52week = min(dataFrame["Adj Close"][-260:]) #Finds minimum value of last 260 closing prices (260 trading days in 52 weeks)
high_of_52week = max(dataFrame["Adj Close"][-260:]) #Finds maximum value of last 260 closing prices (260 trading days in 52 weeks)

#Add for loop to check muptiple stocks

#for x in stocks:

dataFrame["RS"] = ((dataFrame["Adj Close"]/SPYIndex["Adj Close"])/(dataFrame["Adj Close"][-260]/SPYIndex["Adj Close"][-260]))*100

newDf[stocks] = dataFrame["RS"]

print(newDf[stocks])

currentClose = dataFrame["Adj Close"][-1] #Access most recent close price from Yahoo finance database

if currentClose >= (0.8*high_of_52week): 
    print("Near 52 Week High")
else:
    print("Out of Range")