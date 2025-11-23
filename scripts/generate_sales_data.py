import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# --- Config ---
DATA_DIR = "../data"
NUM_RECORDS = 200  # number of daily transactions
TODAY = datetime.now().date()

# --- Make sure data folder exists ---
os.makedirs(DATA_DIR, exist_ok=True)

# --- Simulate sales data ---
#np.random.seed(42)
products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Printer", "Webcam"]
regions = ["North", "South", "East", "West"]
sales_reps = ["Alice", "Ben", "Chika", "David", "Ella"]

data = {
    "Date": [TODAY for _ in range(NUM_RECORDS)],
    "Region": np.random.choice(regions, NUM_RECORDS),
    "Sales_Rep": np.random.choice(sales_reps, NUM_RECORDS),
    "Product": np.random.choice(products, NUM_RECORDS),
    "Quantity": np.random.randint(1, 10, NUM_RECORDS),
    "Unit_Price": np.random.randint(50, 1500, NUM_RECORDS),
}

df = pd.DataFrame(data)
df["Total_Sale"] = df["Quantity"] * df["Unit_Price"]

# --- Save to CSV (new daily data) -- scripts/
file_name = f"sales_{TODAY}.csv"
output_path = os.path.join(DATA_DIR, file_name)
df.to_csv(output_path, index=False)

print(f"Sales data for {TODAY} generated and saved to {output_path}")
