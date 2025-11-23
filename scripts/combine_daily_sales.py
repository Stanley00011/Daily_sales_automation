import pandas as pd
import os

DATA_DIR = "../data"
MASTER_FILE = os.path.join(DATA_DIR, "sales_master.csv")

# --- Collect all sales_YYYY-MM-DD.csv files --- scripts/combine_daily_sales.py
all_files = [
    f for f in os.listdir(DATA_DIR)
    if f.startswith("sales_") and f.endswith(".csv")
]

if not all_files:
    print("No daily sales files found. Generate one first.")
    exit()

# --- Read and merge ---
df_list = [pd.read_csv(os.path.join(DATA_DIR, f)) for f in all_files]
combined_df = pd.concat(df_list, ignore_index=True)

# --- Sort by Date ---
combined_df["Date"] = pd.to_datetime(combined_df["Date"])
combined_df = combined_df.sort_values("Date")

# --- Save master file ---
combined_df.to_csv(MASTER_FILE, index=False)
print(f"Combined {len(all_files)} daily files into {MASTER_FILE}")
print(f"Total records: {len(combined_df)}")
