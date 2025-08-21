import pandas as pd

def validate_prices(data: pd.DataFrame):
    errors = []
    for ticker in data.columns.levels[0]:
        df = data[ticker]
        if df.isnull().values.any():
            errors.append(f"{ticker}: Missing values detected")
        if (df["High"] < df["Low"]).any():
            errors.append(f"{ticker}: High < Low detected")
    return errors
