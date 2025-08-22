import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import yaml

# --- Utility functions ---
def load_config(path="config/config.yaml"):
    import os
    with open(path, "r") as f:
        return yaml.safe_load(f)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

# --- Fetch stock prices dynamically ---
def fetch_prices(tickers, start_date=None, end_date=None):
    """
    Fetch historical prices for a list of tickers using yfinance.
    If start_date or end_date are None, defaults to last 30 days.
    Returns a nested DataFrame if multiple tickers.
    """
    end = end_date or datetime.today()
    start = start_date or (end - timedelta(days=30))
    data = yf.download(tickers, start=start, end=end, group_by="ticker", auto_adjust=True)
    return data

