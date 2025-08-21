import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_prices(tickers, days=30):
    end = datetime.today()
    start = end - timedelta(days=days)
    data = yf.download(tickers, start=start, end=end, group_by="ticker", auto_adjust=True)
    return data
