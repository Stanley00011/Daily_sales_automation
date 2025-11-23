import pandas as pd
from datetime import datetime
import os

DATA_DIR = "../data"
MASTER_FILE = os.path.join(DATA_DIR, "sales_master.csv")
SUMMARY_FILE = os.path.join(DATA_DIR, "daily_summary.csv")

# --- Load master sales data ---
if not os.path.exists(MASTER_FILE):
    print(" No master file found. Run combine_daily_sales.py first.")
    exit()

df = pd.read_csv(MASTER_FILE)
df["Date"] = pd.to_datetime(df["Date"])

# --- Get latest date in data ---
latest_date = df["Date"].max()
latest_df = df[df["Date"] == latest_date]

# --- Compute key KPIs ---
total_sales = latest_df["Total_Sale"].sum()
top_region = latest_df.groupby("Region")["Total_Sale"].sum().idxmax()
top_product = latest_df.groupby("Product")["Total_Sale"].sum().idxmax()
top_sales_rep = latest_df.groupby("Sales_Rep")["Total_Sale"].sum().idxmax()

summary_dict = {
    "Date": [latest_date.date()],
    "Total_Sales": [round(total_sales, 2)],
    "Top_Region": [top_region],
    "Top_Product": [top_product],
    "Top_Sales_Rep": [top_sales_rep]
}

summary_df = pd.DataFrame(summary_dict)

# --- Save summary ---
summary_df.to_csv(SUMMARY_FILE, index=False)

print(f"Summary for {latest_date.date()} saved to {SUMMARY_FILE}")
print(summary_df)
