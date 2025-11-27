import schedule
import time
import os
import sys

# --- Detect project root ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Paths to scripts ---
GENERATE_SCRIPT = os.path.join(BASE_DIR, "generate_sales_data.py")
COMBINE_SCRIPT = os.path.join(BASE_DIR, "combine_daily_sales.py")
SUMMARY_SCRIPT = os.path.join(BASE_DIR, "generate_daily_summary.py")
EMAIL_SCRIPT = os.path.join(BASE_DIR, "send_daily_email.py")

PYTHON = sys.executable  # ensures correct Python interpreter

# --- Tasks ---
def generate_daily_sales():
    print("Running daily sales generator...")
    os.system(f"{PYTHON} {GENERATE_SCRIPT}")

def run_morning_pipeline():
    print("Running morning pipeline...")
    os.system(f"{PYTHON} {COMBINE_SCRIPT}")
    os.system(f"{PYTHON} {SUMMARY_SCRIPT}")
    os.system(f"{PYTHON} {EMAIL_SCRIPT}")

# --- Schedule ---
# End of day sales data generation (11:59 PM)
schedule.every().day.at("23:59").do(generate_daily_sales)

# Morning report (7:00 AM)
schedule.every().day.at("07:00").do(run_morning_pipeline)

print("⏱ Scheduler started and running...")

while True:
    schedule.run_pending()
    time.sleep(60)
