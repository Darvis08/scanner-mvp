"""nifty_streamer.py

Stream NIFTY50 index ticks using the Fyers WebSocket API.
Ticks are appended to a CSV file for use by the signal monitor.

This module keeps the interface lightweight so it can be
integrated into other scripts without major dependencies.
"""

from datetime import datetime
import csv
import threading
from fyers_apiv2.Websocket import ws


class NiftyStreamer:
    """Streams NIFTY50 index LTP and saves ticks to CSV."""

    def __init__(self, fyers_access_token: str, data_file: str = "nifty_tick_data.csv"):
        self.token = fyers_access_token
        self.data_file = data_file
        self._socket = None
        self.running = False

    def on_message(self, message):
        ltp = message.get("ltp")
        if ltp is None:
            return
        timestamp = datetime.utcnow().isoformat()
        with open(self.data_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, ltp])

    def start(self):
        """Start streaming ticks in a background thread."""
        self.running = True
        self._socket = ws.FyersSocket(access_token=self.token, run_background=False, log_path="logs/")
        self._socket.websocket_data = self.on_message
        self._socket.subscribe(["NSE:NIFTY50-INDEX"])
        thread = threading.Thread(target=self._socket.keep_running)
        thread.daemon = True
        thread.start()

    def stop(self):
        if self._socket:
            self._socket.close()
        self.running = False
