import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_headlines(url="https://finance.yahoo.com", outdir="scraped"):
    os.makedirs(outdir, exist_ok=True)
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")

    headlines = [h.get_text() for h in soup.select("h3")[:10]]
    out_path = os.path.join(outdir, "news.json")
    with open(out_path, "w") as f:
        json.dump(headlines, f, indent=2)
    return headlines
