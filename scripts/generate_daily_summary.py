import pandas as pd
import os
from utils import get_data_path

# --- Resolve paths ---
master_file = get_data_path("sales_master.csv")
summary_file = get_data_path("daily_summary.csv")

# --- Load master sales data ---
if not os.path.exists(master_file):
    print(" No master file found. Run combine_daily_sales.py first.")
    exit()

df = pd.read_csv(master_file)
df["Date"] = pd.to_datetime(df["Date"])

# --- Get latest date ---
latest_date = df["Date"].max()
latest_df = df[df["Date"] == latest_date]

# --- Compute KPIs ---
total_sales = latest_df["Total_Sale"].sum()
top_region = latest_df.groupby("Region")["Total_Sale"].sum().idxmax()
top_product = latest_df.groupby("Product")["Total_Sale"].sum().idxmax()
top_sales_rep = latest_df.groupby("Sales_Rep")["Total_Sale"].sum().idxmax()

summary_df = pd.DataFrame({
    "Date": [latest_date.date()],
    "Total_Sales": [round(total_sales, 2)],
    "Top_Region": [top_region],
    "Top_Product": [top_product],
    "Top_Sales_Rep": [top_sales_rep]
})

# --- Save summary (skip if Streamlit Cloud) ---
if os.environ.get("STREAMLIT_CLOUD") == "1":
    print("Streamlit Cloud detected — skipping summary CSV write.")
else:
    summary_df.to_csv(summary_file, index=False)
    print(f"Summary for {latest_date.date()} saved to {summary_file}")

print(summary_df)
