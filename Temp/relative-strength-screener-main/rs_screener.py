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

server = app.server

app.layout = html.Div(className="body", children=[
    html.P(children='Relative Strength Stock Screener', className="header-text"),

    html.Div(className="input_div", children=[
        "Enter a Stock Ticker: ",
        dcc.Input(id='my-input', value='AAPL', type='text', className="ticker-input"),
    
        html.Div(className="statement_div", children=[
            html.Div(id='stocksInRange', className='statement-text'),

            html.Br(),

            html.Div(id='stocksOutOfRange', className='statement-text'),])
    ]),

    html.Br(),
    html.Br(),

    html.Div(className="selections_div", children=[

        html.Div(children=[
                html.Div(
                    children="Select Date Range:",
                    className="datePicker-text"
                    ),
                dcc.DatePickerRange(
                    id="date-range",
                    className="datePicker",
                    min_date_allowed=dt.datetime(1950,1,1),
                    max_date_allowed=now,
                    start_date=start,
                    end_date=now,
                    ),
                html.Button(id='submit-button', n_clicks=0, children='Submit', className='submit-button'),
            ]
        ),

        html.Br(),

        html.Div(
            [dcc.Checklist(
            id="ema-checklist",
            options= [  {"label": "10 Day EMA", "value": "10"},
                        {"label": "20 Day EMA", "value": "20"},
                        {"label": "50 Day EMA", "value": "50"}],
            value=[],
            labelStyle={"display": "inline-block"},),
            dcc.Checklist(
            id="sma-checklist",
            options= [  {"label": "50 Day SMA", "value": "50"},
                        {"label": "100 Day SMA", "value": "100"},
                        {"label": "200 Day SMA", "value": "200"},],
            value=[],
            labelStyle={"display": "inline-block"},),
            ]
        )
    ]),

    html.Br(),

    html.Div(id='graph-div', className='graph-div', children=[
        dcc.Graph(id='my-graph', className='graph-plot')
    ]),  
])

@app.callback(
    Output('my-graph', 'figure'),
    Output('stocksInRange', 'children'),
    Output('stocksOutOfRange', 'children'),
    Input('submit-button', 'n_clicks'),
    State('date-range','start_date'),
    State('date-range', 'end_date'),
    State(component_id='my-input', component_property='value'),
    Input('ema-checklist', 'value'),
    Input('sma-checklist', 'value')
)
def update_output_div(n_clicks, start_date, end_date, input_value, ema_list, sma_list):
    startDateObj = dt.datetime.fromisoformat(start_date)
    endDateObj = dt.datetime.fromisoformat(end_date)

    stocks=list(map(str,input_value.split()))

    newDf = pd.DataFrame()

    SPYIndex = pdr.get_data_yahoo("SPY",startDateObj,endDateObj)

    stocksInRange = []
    stocksOutOfRange = []

    count = 0

    fig = go.Figure()
    fig = make_subplots(rows=2, cols=1,
                        specs=[[{"secondary_y": True}],[{}]],
                        shared_xaxes=True,
                        vertical_spacing=0.1,
                        subplot_titles=["Relative Strength vs. SPY", "Stock Price"],
                        x_title="Date",
                        y_title="Price",
                        )
    fig.update_layout(title={
        "text": "Stock Price Performance vs. Relative Strength", 
        "font": dict(size=24),
        "x": 0.45,
        })

    fig.update_yaxes(
        ticks="outside",
        tickprefix="$",
        tickcolor="whitesmoke",
        tickwidth=2,
        ticklen=5)

    fig.update_layout(
        autosize=False,
        width=1200,
        height=700,
        margin=dict(
            l=100,
            r=100,
            b=100,
            t=100,
            pad=4),
        paper_bgcolor="#1f1f1f",
        font_color="whitesmoke",
        yaxis2=dict(
            title="Relative Strength",
            side="right",
            tickprefix="")
        )

    fig.layout.annotations[0].update(y=1.01)
    fig.layout.annotations[1].update(y=0.46)

    for stock in stocks:
        
        dataFrame=pdr.get_data_yahoo(stock,startDateObj,endDateObj)

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

        for x in ema_list:
            ema=int(x)
            emaName= "EMA_" + x
            newDf[emaName]=round(newDf[closingPrice].ewm(span=ema, adjust=False).mean(),2)
            fig.add_trace(go.Scatter(x=newDf["Date"], y=newDf[emaName], mode="lines", name=emaName), row=2, col=1)

        for x in sma_list:
            sma=int(x)
            smaName= "SMA_" + x
            newDf[smaName]=newDf[closingPrice].rolling(window=sma, min_periods=1).mean()
            fig.add_trace(go.Scatter(x=newDf["Date"], y=newDf[smaName], mode="lines", name=smaName), row=2, col=1)

    print(newDf)
    
    fig.add_trace(go.Scatter(x=newDf["Date"], y=SPYIndex["Adj Close"], mode="lines", name="SPY_Price", line_color="#e86100"), row=1, col=1, secondary_y=False)

    stocksInRangeOutput = "Stocks within 20 percent of 52 week high: "+ listToString(stocksInRange)

    stocksOutOfRangeOutput = "Stocks out of desired range: None"

    if stocksOutOfRange:
        stocksOutOfRangeOutput = "Stocks out of desired range: "+ listToString(stocksOutOfRange)

    return fig, stocksInRangeOutput, stocksOutOfRangeOutput

if __name__ == '__main__':
    app.run_server(debug=True)