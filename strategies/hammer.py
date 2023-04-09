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

class Hammer(Strategy):

    def initialize(self):
        risk = input('enter percentage willing to risk per trade:')


        signal = None
        start = "2021-01-01"

        self.signal = signal
        self.start = start
        self.sleeptime = "1s"

        def on_trading_iteration(self):

            #15 hammer
            fifteen_min_bars = self.get_historical_prices("GLD", 4, "15m")
            gld = fifteen_min_bars.df
            gld = fifteen_min_bars.df

            atr_bars = self.get_historical_prices("GLD", 14, "15m")
            atr_df = atr_bars.df

            # Calculate true range
            atr_df['high_low'] = atr_df['high'] - atr_df['low']
            atr_df['high_close'] = abs(atr_df['high'] - atr_df['close'].shift(1))
            atr_df['low_close'] = abs(atr_df['low'] - atr_df['close'].shift(1))
            atr_df['true_range'] = atr_df[['high_low', 'high_close', 'low_close']].max(axis=1)

            # Calculate 14-day ATR
            atr_df['atr'] = atr_df['true_range'].rolling(window=14).mean()

            # Get the most recent ATR value
            latest_atr = atr_df.iloc[-1]['atr']

            hammer = False
            last_candle = gld.iloc[-1]
            last_open_val = last_candle['open']
            last_high_val = last_candle['high']
            last_low_val = last_candle['low']
            close_values = gld['close'].values
            first_value_close = close_values[0]
            last_value_close = close_values[-1]

            absolute_movement = last_high_val - last_low_val
            fib = absolute_movement*.382
            lowerbound = last_high_val - fib

            # account
            trading_client = TradingClient('PK2XNKDSJH4PVPCYDK8E', 'f5cD1kbR3p5RRfgvNgDiQ09qRpi4LCYmPZprl3KM')
            account = trading_client.get_account()
            balance = account.equity


            not_hold = True

            symbol = "GLD"
            position = self.get_position(symbol)
            if position is None:
                not_hold = True


            if not_hold:
                if last_open_val > lowerbound and last_open_val-last_value_close > 0:
                    if last_value_close < first_value_close:
                        stop_loss_signal = first_value_close - latest_atr
                        take_profit_signal = first_value_close + latest_atr*1.71
                        buy_signal = first_value_close
                        not_hold = False

                        # calculating position size
                        max_risk = account.cash*risk/100
                        quantity = max_risk//latest_atr

                        buy_order = self.create_order("GLD", quantity, "buy", limit_price=buy_signal)
                        sell_order = self.create_order("GLD", quantity, "sell", take_profit_price=take_profit_signal,
                                                       stop_loss_price=stop_loss_signal)
                        self.submit_order(buy_order)
                        self.submit_order(sell_order)
            else:
                buy_signal = None
                stop_loss_signal = None
                take_profit_signal = None

