import pandas as pd
import numpy as np
from datetime import datetime
import os
from utils import get_data_path

# --- Config ---
NUM_RECORDS = 200
TODAY = datetime.now().date()

# --- Resolve correct data directory ---
data_file_path = get_data_path(f"sales_{TODAY}.csv")
data_dir = os.path.dirname(data_file_path)

# Create folder if local or CI
os.makedirs(data_dir, exist_ok=True)

# --- Simulate sales data ---
products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Printer", "Webcam"]
regions = ["North", "South", "East", "West"]
sales_reps = ["Alice", "Ben", "Chika", "David", "Ella"]

data = {
    "Date": [TODAY] * NUM_RECORDS,
    "Region": np.random.choice(regions, NUM_RECORDS),
    "Sales_Rep": np.random.choice(sales_reps, NUM_RECORDS),
    "Product": np.random.choice(products, NUM_RECORDS),
    "Quantity": np.random.randint(1, 10, NUM_RECORDS),
    "Unit_Price": np.random.randint(50, 1500, NUM_RECORDS),
}

df = pd.DataFrame(data)
df["Total_Sale"] = df["Quantity"] * df["Unit_Price"]

# --- Save output (only local + CI, not Streamlit Cloud) ---
if os.environ.get("STREAMLIT_CLOUD") == "1":
    print("Streamlit Cloud detected — skipping CSV write.")
else:
    df.to_csv(data_file_path, index=False)
    print(f"Sales data saved → {data_file_path}")
