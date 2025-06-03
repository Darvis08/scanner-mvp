"""option_selector.py

Helpers to compute the at-the-money option symbol for NIFTY.
"""

from datetime import date


def get_atm_option_symbol(nifty_ltp: float, option_type: str, expiry: str | None = None) -> str:
    """Return the FYERS symbol for the ATM option.

    Args:
        nifty_ltp: Current NIFTY spot price.
        option_type: "CE" or "PE".
        expiry: Optional expiry string (YYYY-MM-DD). Defaults to current week.
    """
    nearest_50 = round(nifty_ltp / 50) * 50
    if expiry is None:
        today = date.today()
        expiry = today.strftime("%Y-%m-%d")
    return f"NSE:NIFTY{expiry}{nearest_50}{option_type}"
