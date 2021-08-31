import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

startyear=2021
startmonth=1
startday=1

start=dt.datetime(startyear,startmonth,startday)

now = now=dt.datetime.now()

RS = stockPrice/SPYIndex

