from config import ALPACA_CONFIG
from datetime import datetime, timedelta
from lumibot.backtesting import YahooDataBacktesting
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
from strategies.real_data_trading import Trader

if __name__ == "__main__":
    trade = False
    if trade:
        broker = Alpaca(ALPACA_CONFIG)
        strategy = Hammer(broker=broker)
        bot = Trader()
        bot.add_strategy(strategy)
        bot.run_all()
    else:
        start = datetime(2022, 1, 1)
        end = datetime(2022, 12, 31)
        Hammer.backtest(
            YahooDataBacktesting,
            start,
            end
        )
