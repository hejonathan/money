from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime

import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import cufflinks as cf
cf.go_offline()


API_KEY = "PK2XNKDSJH4PVPCYDK8E"
SECRET_KEY = "f5cD1kbR3p5RRfgvNgDiQ09qRpi4LCYmPZprl3KM"

print('Program Starting...')

client = StockHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)


def search_historical_data(stock_client,
                           symbol: str,
                           start: str,
                           end: str,
                           interval: int,
                           timeframe: str) -> pd.DataFrame:
    print(f'receiving data from {symbol} in range ({start}, {end})...')
    d = {'min': TimeFrameUnit.Minute,
         'hour': TimeFrameUnit.Hour,
         'day': TimeFrameUnit.Day,
         'week': TimeFrameUnit.Week,
         'mon': TimeFrameUnit.Month}
    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame(amount=interval, unit=d[timeframe]),
        start=datetime.strptime(start, '%Y-%m-%d'),
        end=datetime.strptime(end, '%Y-%m-%d'),
    )
    data = stock_client.get_stock_bars(request_params)
    data = data.df
    print(f'stock data from {symbol} in range ({start}, {end}) received')
    return data


def graph_historical_data(dataframe):
    print('plotting data...')
    plt.figure(figsize=(24, 16))
    fig = go.Figure(data=[go.Candlestick(x=dataframe.index,
                                         open=dataframe['open'],
                                         high=dataframe['high'],
                                         low=dataframe['low'],
                                         close=dataframe['close'])])
    fig.update_layout(xaxis_rangeslider_visible=True)
    fig.show()


usr_input = False
if usr_input:
    df = search_historical_data(client,
                                symbol=input('enter company code: '),
                                start=input('enter start date YYYY-MM-DD: '),
                                end=input('enter start date YYYY-MM-DD: '),
                                interval=int(input('enter candle duration: ')),
                                timeframe=input('enter unit (min/hour/day/week/mon): '))
else:
    df = search_historical_data(client,
                                symbol='AAPL',
                                start='2021-9-10',
                                end='2021-10-20',
                                interval=15,
                                timeframe='min'
                                )
df = df.reset_index(level=[0], drop=True)
graph_historical_data(df)

