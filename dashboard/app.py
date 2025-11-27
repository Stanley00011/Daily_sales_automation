import streamlit as st
import pandas as pd
import time
from utils import get_data_path

st.set_page_config(page_title="Daily Sales Dashboard", layout="wide")

# Auto-refresh every 5 minutes
REFRESH_SEC = 300
last_refresh = st.session_state.get("last_refresh", time.time())
if time.time() - last_refresh > REFRESH_SEC:
    st.session_state["last_refresh"] = time.time()
    st.experimental_rerun()

st.title("Daily Sales Performance Dashboard")

# Dynamic path
DATA_PATH = get_data_path("sales_master.csv")
st.caption(f"Data Source → {DATA_PATH}")

# Load CSV
try:
    df = pd.read_csv(DATA_PATH)
except Exception:
    st.warning("No data found yet. Run GitHub Actions or wait for the 6 PM refresh.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])

# Metrics
latest = df["Date"].max()
latest_df = df[df["Date"] == latest]

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${latest_df['Total_Sale'].sum():,.0f}")
col2.metric("Top Region", latest_df.groupby("Region")["Total_Sale"].sum().idxmax())
col3.metric("Top Product", latest_df.groupby("Product")["Total_Sale"].sum().idxmax())

st.divider()

st.subheader("Sales Trend Over Time")
trend = df.groupby("Date")["Total_Sale"].sum().reset_index()
st.line_chart(trend, x="Date", y="Total_Sale")
