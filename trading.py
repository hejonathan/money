from alpaca.trading.client import TradingClient

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

API_KEY = "PK2XNKDSJH4PVPCYDK8E"
SECRET_KEY = "f5cD1kbR3p5RRfgvNgDiQ09qRpi4LCYmPZprl3KM"

print('Program Starting...')


def setup_account(api, secret):
    tc = TradingClient(api, secret, paper=True)  # setting up trading client
    print('Trading Client Established: ' + str(tc))

    account = tc.get_account()
    for name, val in account:
        print(f'{name}\t:\t{val}')

    return tc, account


client, account = setup_account(API_KEY, SECRET_KEY)


