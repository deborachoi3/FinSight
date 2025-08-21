from app.utils import load_config, ensure_dir
from app.logsetup import get_logger
from app.api import fetch_prices
from app.validation import validate_prices
from app.excel import save_to_excel
import os

logger = get_logger()

def run_pipeline():
    cfg = load_config()
    ensure_dir(cfg["output_dir"])

    logger.info("Fetching prices...")
    data = fetch_prices(cfg["tickers"], cfg["days"])

    logger.info("Validating data...")
    errors = validate_prices(data)

    out_path = os.path.join(cfg["output_dir"], "market_report.xlsx")
    logger.info(f"Saving report to {out_path}")
    save_to_excel(data, errors, out_path)

    logger.info("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()
