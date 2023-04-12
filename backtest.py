from config import ALPACA_CONFIG
from datetime import datetime, timedelta
from lumibot.backtesting import YahooDataBacktesting, PandasDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

import numpy as np
import pandas as pd
import yfinance as yf

'''
Import strategies here
'''
from strategies.hammer import Hammer
from strategies.lumibot_buy_hold import BuyHold
from strategies.nine_cross_twenty import Trend

Str = Trend
Datasource = YahooDataBacktesting


def trade(start, end):
    trade = False
    if trade:
        broker = Alpaca(ALPACA_CONFIG)
        strategy = Str(broker=broker)
        bot = Trader()
        bot.add_strategy(strategy)
        bot.run_all()
    else:
        Str.backtest(
            Datasource,
            start,
            end
        )


trade(datetime(2022, 1, 1), datetime(2022, 2, 1))
