import streamlit as st
import pandas as pd

st.title("📊 Market Report Dashboard")

uploaded_file = st.file_uploader("Upload Market Report (Excel)", type="xlsx")

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    tickers = [s for s in xls.sheet_names if s not in ["Errors"]]
    for t in tickers:
        st.subheader(f"Stock: {t}")
        df = pd.read_excel(uploaded_file, sheet_name=t, index_col=0)
        st.line_chart(df["Close"])
    
    st.subheader("Validation Errors")
    errors = pd.read_excel(uploaded_file, sheet_name="Errors")
    st.write(errors)
