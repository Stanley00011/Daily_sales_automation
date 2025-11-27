import streamlit as st
import time
import pandas as pd
import os

# --- Auto-refresh every 5 minutes ---

REFRESH_INTERVAL = 5 * 60  # seconds
last_refresh = st.session_state.get("last_refresh", time.time())

if time.time() - last_refresh > REFRESH_INTERVAL:
    st.session_state["last_refresh"] = time.time()
    st.experimental_rerun()

DATA_URL = "https://raw.githubusercontent.com/Stanley00011/Daily_sales_automation/main/data/sales_master.csv"
df = pd.read_csv(DATA_URL)

# --- Page Config ---
st.set_page_config(page_title="Daily Sales Dashboard", layout="wide")

st.title("Daily Sales Performance Dashboard")
st.markdown("This dashboard updates automatically when new sales data arrives.")

# --- Load Data ---
if not os.path.exists(DATA_URL):
    st.warning(" No sales data found. Run your data scripts first.")
else:
    df = pd.read_csv(DATA_URL)
    df["Date"] = pd.to_datetime(df["Date"])

    # --- Metrics ---
    latest_date = df["Date"].max()
    latest_df = df[df["Date"] == latest_date]

    total_sales = latest_df["Total_Sale"].sum()
    top_region = latest_df.groupby("Region")["Total_Sale"].sum().idxmax()
    top_product = latest_df.groupby("Product")["Total_Sale"].sum().idxmax()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Top Region", top_region)
    col3.metric("Top Product", top_product)

    st.markdown("---")

    # --- Charts ---
    st.subheader("Sales Trend Over Time")
    trend = df.groupby("Date")["Total_Sale"].sum().reset_index()
    st.line_chart(trend, x="Date", y="Total_Sale")

    st.subheader("Top Products by Revenue")
    product_sales = df.groupby("Product")["Total_Sale"].sum().sort_values(ascending=False)
    st.bar_chart(product_sales)

    st.subheader("Sales by Region")
    region_sales = df.groupby("Region")["Total_Sale"].sum().sort_values(ascending=False)
    st.bar_chart(region_sales)
