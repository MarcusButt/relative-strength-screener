import pandas as pd
import yfinance as yf
import datetime as dt
from datetime import date
from pandas_datareader import data as pdr
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

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

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Lato&display=swap']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Relative Strength Screener', className="header-text"),

    html.Div([
        "Enter a Stock Ticker: ",
        dcc.Input(id='my-input', value='AAPL', type='text')
    ]),
    
    html.Br(),

    html.Div(id='stocksInRange', className='body-text'),

    html.Div(id='stocksOutOfRange', className='body-text'),

    html.Br(),

    html.Div(
        children=[
            html.Div(
                children="Date Range",
                className="menu-title"
                ),
            dcc.DatePickerRange(
                id="date-range",
                min_date_allowed=dt.datetime(1950,1,1),
                max_date_allowed=now,
                start_date=start,
                end_date=now,
            ),
        ]
    ),

    html.Button(id='submit-button', n_clicks=0, children='Submit'),

    html.Div(id='temporaryDate'),  

    dcc.Graph(id='my-graph'),  
])

@app.callback(
    Output('my-graph', 'figure'),
    Output('stocksInRange', 'children'),
    Output('stocksOutOfRange', 'children'),
    Output('temporaryDate', 'children'),
    Input('submit-button', 'n_clicks'),
    State('date-range','start_date'),
    State("date-range", "end_date"),
    State(component_id='my-input', component_property='value')
)
def update_output_div(n_clicks, start_date, end_date, input_value):

    startDateObj = dt.strptime(start_date, '%y-%m-%dT%H:%M:%S')
    endDateObj = dt.strptime(end_date, '%y-%m-%dT%H:%M:%S')

    stocks=list(map(str,input_value.split()))

    newDf = pd.DataFrame()

    SPYIndex = pdr.get_data_yahoo("SPY",start,now)

    stocksInRange = []
    stocksOutOfRange = []

    count = 0

    fig = go.Figure()
    fig = make_subplots(rows=2, cols=1,
                        specs=[[{"secondary_y": True}],[{}]],
                        shared_xaxes=True,
                        vertical_spacing=0.1,
                        subplot_titles=("Relative Strength", "Stock Price"),
                        x_title="Date",
                        y_title="Price",
                        )
    fig.update_layout(title_text="Stock Price Performance vs. Relative Strength")

    fig.update_layout(
    autosize=False,
    width=1500,
    height=500,
    margin=dict(
        l=100,
        r=100,
        b=100,
        t=100,
        pad=4),
    paper_bgcolor="#b3b3b3",)

    for stock in stocks:
        
        dataFrame=pdr.get_data_yahoo(stock,start,now)

        low_of_52week = min(dataFrame["Adj Close"][-260:]) #Finds minimum value of last 260 closing prices (260 trading days in 52 weeks)
        high_of_52week = max(dataFrame["Adj Close"][-260:]) #Finds maximum value of last 260 closing prices (260 trading days in 52 weeks)

        dataFrame["RS"] = (dataFrame["Adj Close"]/SPYIndex["Adj Close"])

        columnName = "RS_"+stock

        newDf[columnName] = dataFrame["RS"]

        closingPrice = stock+"_Price"

        newDf[closingPrice] = dataFrame["Adj Close"]

        if count == 0:
            newDf["Date"] = newDf.index

        count = count + 1

        currentClose = dataFrame["Adj Close"][-1] #Access most recent close price from Yahoo finance database

        if currentClose >= (0.8*high_of_52week): 
            stocksInRange.append(stock)
        else:
            stocksOutOfRange.append(stock)

        fig.add_trace(go.Scatter(x=newDf["Date"], y=newDf[columnName], mode="lines", name=columnName, line=dict(dash='dash')), row=1, col=1, secondary_y=True)
        fig.add_trace(go.Scatter(x=newDf["Date"], y=newDf[closingPrice], mode="lines", name=closingPrice), row=2, col=1)

    fig.add_trace(go.Scatter(x=newDf["Date"], y=SPYIndex["Adj Close"], mode="lines", name="SPY_Price", line_color="#e86100"), row=1, col=1, secondary_y=False)

    stocksInRangeOutput = "Stocks within 20 percent of 52 week high: "+ listToString(stocksInRange)

    stocksOutOfRangeOutput = "Stocks out of desired range: none"

    if stocksOutOfRange:
        stocksOutOfRangeOutput = "Stocks out of desired range: "+ listToString(stocksOutOfRange)

    date_output = 'test'

    string_prefix = 'You have selected: '

    if start_date is not None:
        string_prefix = string_prefix + 'Start Date: ' + start_date + ' | '
    if end_date is not None:
        string_prefix = string_prefix + 'End Date: ' + end_date
    if len(string_prefix) == len('You have selected: '):
        date_output = 'Select a date to see it displayed here'
    else:
        date_output = string_prefix

    return fig, stocksInRangeOutput, stocksOutOfRangeOutput, date_output

if __name__ == '__main__':
    app.run_server(debug=True)