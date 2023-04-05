from config import ALPACA_CONFIG
from datetime import datetime, timedelta
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader
import numpy as np
import pandas as pd
import yfinance as yf

class Hammer(Strategy):

    def initialize(self):
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

            hold = True
            if hold:
                if last_open_val > lowerbound and last_open_val-last_value_close > 0:
                    if last_value_close > first_value_close:
                        stop_loss_signal = first_value_close - latest_atr
                        take_profit_signal = first_value_close + latest_atr*1.71
                        buy_signal = first_value_close
                        hold = False
                        buy_order = self.create_order("GLD", 1, "buy", limit_price=buy_signal)
                        sell_order = self.create_order("GLD", 1, "sell", take_profit_price=take_profit_signal,
                                                       stop_loss_price=stop_loss_signal)
            else:
                buy_signal = None
                stop_loss_signal = None
                take_profit_signal = None





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




