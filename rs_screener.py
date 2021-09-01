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

newDf = pd.DataFrame()

SPYIndex = pdr.get_data_yahoo("SPY",start,now)["Adj Close"]

#Add for loop to check muptiple stocks

stock=input("Enter a stock ticker symbol: ")

dataFrame=pdr.get_data_yahoo(stock,start,now)

dataFrame["RS"] = (dataFrame["Adj Close"]/SPYIndex)*100

newDf[stock] = dataFrame["RS"]

print(newDf[stock])