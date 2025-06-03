"""main_options.py

Example orchestration for NIFTY option scalping with FYERS API.
"""

from __future__ import annotations

import threading
import time

from fyers_apiv2 import fyersModel

from nifty_streamer import NiftyStreamer
from nifty_signal_monitor import NiftySignalMonitor
from option_selector import get_atm_option_symbol
from option_trade_engine import OptionTradeEngine


class ScalpingBot:
    def __init__(self, access_token: str, client_id: str, qty: int = 50):
        self.session = fyersModel.FyersModel(client_id=client_id, token=access_token)
        self.streamer = NiftyStreamer(access_token)
        self.monitor = NiftySignalMonitor()
        self.trade_engine = OptionTradeEngine(self.session)
        self.qty = qty

    def start(self):
        self.streamer.start()
        threading.Thread(target=self.run_signals, daemon=True).start()

    def run_signals(self):
        while True:
            signal = self.monitor.check_signal()
            if signal and not self.trade_engine.active_trade:
                ltp = self.session.quote(["NSE:NIFTY50-INDEX"])["d"][0]["v"][0]["last_traded_price"]
                symbol = get_atm_option_symbol(ltp, "CE" if signal == "BUY" else "PE")
                self.trade_engine.enter_trade(symbol, self.qty)
                threading.Thread(target=self.trade_engine.run_trailing, daemon=True).start()
            time.sleep(60)


if __name__ == "__main__":
    ACCESS_TOKEN = "YOUR_TOKEN_HERE"
    CLIENT_ID = "YOUR_CLIENT_ID"

    bot = ScalpingBot(ACCESS_TOKEN, CLIENT_ID)
    bot.start()
    while True:
        time.sleep(1)
