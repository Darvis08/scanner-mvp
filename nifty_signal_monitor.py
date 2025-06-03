"""nifty_signal_monitor.py

Calculate EMA based buy/sell signals from NIFTY tick data.
"""

from __future__ import annotations

import pandas as pd
from pandas import DataFrame


class NiftySignalMonitor:
    """Reads tick data, constructs candles and generates trade signals."""

    def __init__(self, data_file: str = "nifty_tick_data.csv"):
        self.data_file = data_file
        self.last_signal: str | None = None

    def _load_candles(self) -> DataFrame:
        df = pd.read_csv(self.data_file, names=["timestamp", "ltp"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        candles = df["ltp"].resample("3min").last().dropna()
        return candles.to_frame("close")

    def check_signal(self) -> str | None:
        candles = self._load_candles()
        if len(candles) < 26:
            return None
        candles["ema9"] = candles["close"].ewm(span=9).mean()
        candles["ema26"] = candles["close"].ewm(span=26).mean()
        last = candles.iloc[-1]
        if last["ema9"] > last["ema26"] and self.last_signal != "BUY":
            self.last_signal = "BUY"
            return "BUY"
        if last["ema9"] < last["ema26"] and self.last_signal != "SELL":
            self.last_signal = "SELL"
            return "SELL"
        return None
