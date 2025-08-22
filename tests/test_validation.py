import pandas as pd
from app.validation import validate_prices

def test_high_low():
    df = pd.DataFrame({"High":[100,90], "Low":[95,95]})
    data = pd.concat([df], axis=1, keys=["AAPL"])
    errors = validate_prices(data)
    assert any("High < Low" in e for e in errors)
