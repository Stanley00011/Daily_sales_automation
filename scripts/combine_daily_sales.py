import pandas as pd
import os
from utils import get_data_path

# --- Resolve data directory ---
data_dir = os.path.dirname(get_data_path("dummy.txt"))  # safely get /data path
master_file = get_data_path("sales_master.csv")

# --- Collect all sales_YYYY-MM-DD.csv files ---
all_files = [
    f for f in os.listdir(data_dir)
    if f.startswith("sales_") and f.endswith(".csv")
]

if not all_files:
    print("No daily sales files found. Generate one first.")
    exit()

# --- Read and merge ---
df_list = [pd.read_csv(os.path.join(data_dir, f)) for f in all_files]
combined_df = pd.concat(df_list, ignore_index=True)

# --- Sort by Date ---
combined_df["Date"] = pd.to_datetime(combined_df["Date"])
combined_df = combined_df.sort_values("Date")

# --- Save master file (skip in Streamlit Cloud) ---
if os.environ.get("STREAMLIT_CLOUD") == "1":
    print("Streamlit Cloud detected — skipping master CSV write.")
else:
    combined_df.to_csv(master_file, index=False)
    print(f"Combined {len(all_files)} daily files into {master_file}")
    print(f"Total records: {len(combined_df)}")
