import streamlit as st
import pandas as pd
import json
import os
import subprocess
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from app.api import fetch_prices

st.set_page_config(page_title="FinSight Dashboard", layout="wide")
st.title("FinSight Dashboard")

# --- Sidebar Controls ---
st.sidebar.header("Controls")

# Dynamic ticker input
tickers_input = st.sidebar.text_area(
    "Enter tickers separated by commas",
    value="AAPL,MSFT,GOOG,AMZN,TSLA,NFLX"
)
tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

# Date range picker
start_date = st.sidebar.date_input("Start Date", datetime.today() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.today())

# Fetch Prices Button
if st.sidebar.button("Fetch Prices"):
    data = fetch_prices(tickers_list, start_date=start_date, end_date=end_date)
    
    st.header("Fetched Stock Prices")
    
    # Handle single vs multiple tickers
    if len(tickers_list) == 1:
        df = data.reset_index()
        st.dataframe(df)
        st.line_chart(df.set_index("Date")["Close"])
    else:
        for ticker in tickers_list:
            if ticker not in data:
                st.warning(f"No data for {ticker}")
                continue
            df = data[ticker].reset_index()
            st.subheader(ticker)
            st.dataframe(df)
            st.line_chart(df.set_index("Date")["Close"])

# --- Upload Excel Report (Optional) ---
report_path = "reports/market_report.xlsx" if os.path.exists("reports/market_report.xlsx") else None
uploaded_file = st.file_uploader("Upload Day 1 Excel report", type=["xlsx"])
if uploaded_file:
    report_path = uploaded_file

if report_path:
    df_dict = pd.read_excel(report_path, sheet_name=None)
    # Option 1 — use all sidebar tickers
    selected_tickers = tickers_list

    # OR Option 2 — intersection with Excel sheets
    excel_tickers = [sheet for sheet in df_dict.keys() if sheet.lower() != "errors"]
    selected_tickers = [t for t in tickers_list if t in excel_tickers]

    st.header("Excel Stock Data")
    for sheet_name in selected_tickers:
        df = df_dict[sheet_name]
        st.subheader(sheet_name)
        st.dataframe(df)

        if "Date" in df.columns and "Close" in df.columns:
            fig = px.line(df, x="Date", y="Close", title=f"{sheet_name} Closing Prices")
            st.plotly_chart(fig, use_container_width=True)

    if "Errors" in df_dict:
        st.header("Validation Errors")
        st.dataframe(df_dict["Errors"])
        st.metric("Number of Validation Errors", len(df_dict["Errors"]))

# --- Headlines Section ---
st.header("Latest Headlines")
news_file = os.path.join("scraped", "news.json")
headlines = []
if os.path.exists(news_file):
    with open(news_file, "r") as f:
        headlines = json.load(f)

    # Keyword search
    query = st.text_input("Filter Headlines by Keyword")
    filtered_headlines = [h for h in headlines if query.lower() in h.lower()] if query else headlines
    for h in filtered_headlines:
        st.markdown(f"- {h}")

    # Word cloud visualization
    st.subheader("Word Cloud of Headlines")
    combined_text = " ".join(filtered_headlines)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

else:
    st.warning("No news.json found. Run the scraper first.")

# --- Scraper Control ---
st.header("Scraper Control")
if st.button("Refresh Headlines"):
    st.info("Running scraper...")
    result = subprocess.run(["python", "-m", "app.scraper"], capture_output=True, text=True)
    if result.returncode == 0:
        st.success("Headlines refreshed!")
    else:
        st.error(f"Scraper failed:\n{result.stderr}")

# --- Download Validation Errors ---
if report_path and "Errors" in df_dict:
    st.header("Download Validation Errors")
    csv_data = df_dict["Errors"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="validation_errors.csv",
        mime="text/csv"
    )
