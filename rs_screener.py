import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

startyear=2021
startmonth=1
startday=1

start = dt.datetime(startyear,startmonth,startday)

now = now=dt.datetime.now()

stock=input("Enter a stock ticker symbol: ")

dataFrame=pdr.get_data_yahoo(stock,start,now)

newDf = pd.DataFrame()

SPYIndex = pdr.get_data_yahoo("SPY",start,now)["Adj Close"]

low_of_52week = min(dataFrame["Adj Close"][-260:]) #Finds minimum value of last 260 closing prices (260 trading days in 52 weeks)
high_of_52week = max(dataFrame["Adj Close"][-260:]) #Finds maximum value of last 260 closing prices (260 trading days in 52 weeks)

#Add for loop to check muptiple stocks

dataFrame["RS"] = (dataFrame["Adj Close"]/SPYIndex)*100

newDf[stock] = dataFrame["RS"]

print(newDf[stock])