import pandas as pd
from openpyxl import load_workbook

def save_to_excel(data, errors, path):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for ticker in data.columns.levels[0]:
            data[ticker].to_excel(writer, sheet_name=ticker)
        pd.DataFrame(errors, columns=["Validation Errors"]).to_excel(writer, sheet_name="Errors", index=False)
