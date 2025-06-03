"""option_trade_engine.py

Execute option trades and handle trailing stop-loss using Fyers API.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

from fyers_apiv2 import fyersModel


@dataclass
class Trade:
    order_id: str
    sl_order_id: str
    symbol: str
    qty: int
    sl_price: float


class OptionTradeEngine:
    def __init__(self, fyers: fyersModel.FyersModel, sl_buffer: float = 5.0):
        self.fyers = fyers
        self.sl_buffer = sl_buffer
        self.active_trade: Optional[Trade] = None

    def enter_trade(self, symbol: str, qty: int) -> None:
        if self.active_trade:
            return
        order = {
            "symbol": symbol,
            "qty": qty,
            "type": 2,  # market order
            "side": 1,  # buy
            "productType": "INTRADAY",
        }
        result = self.fyers.place_order(order)
        order_id = result.get("id")
        ltp = self.fyers.quote([symbol])["d"][0]["v"][0]["last_traded_price"]
        sl_price = max(1.0, ltp - self.sl_buffer)
        sl_order = {
            "symbol": symbol,
            "qty": qty,
            "type": 3,  # sl-limit
            "side": -1,
            "productType": "INTRADAY",
            "limitPrice": sl_price,
            "stopPrice": sl_price,
            "parent_order_id": order_id,
        }
        sl_res = self.fyers.place_order(sl_order)
        sl_order_id = sl_res.get("id")
        self.active_trade = Trade(order_id, sl_order_id, symbol, qty, sl_price)

    def trail_stop(self) -> None:
        if not self.active_trade:
            return
        trade = self.active_trade
        ltp = self.fyers.quote([trade.symbol])["d"][0]["v"][0]["last_traded_price"]
        new_sl = ltp - self.sl_buffer
        if new_sl > trade.sl_price:
            modify = {
                "id": trade.sl_order_id,
                "limitPrice": new_sl,
                "stopPrice": new_sl,
            }
            self.fyers.modify_order(modify)
            trade.sl_price = new_sl

    def check_exit(self):
        if not self.active_trade:
            return
        status = self.fyers.get_orderbook()
        for order in status.get("orderBook", []):
            if order.get("id") == self.active_trade.sl_order_id and order.get("status") == "Exited":
                self.active_trade = None

    def run_trailing(self, interval: int = 5):
        while self.active_trade:
            self.trail_stop()
            self.check_exit()
            time.sleep(interval)
