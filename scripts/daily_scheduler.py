import schedule
import time
import os

# --- Paths to scripts ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATE_SCRIPT = os.path.join(BASE_DIR, "generate_sales_data.py")
COMBINE_SCRIPT = os.path.join(BASE_DIR, "combine_daily_sales.py")
SUMMARY_SCRIPT = os.path.join(BASE_DIR, "generate_daily_summary.py")
EMAIL_SCRIPT = os.path.join(BASE_DIR, "send_daily_email.py")

# --- Tasks ---
def generate_daily_sales():
    os.system(f"python3 {GENERATE_SCRIPT}")

def run_morning_pipeline():
    os.system(f"python3 {COMBINE_SCRIPT}")
    os.system(f"python3 {SUMMARY_SCRIPT}")
    os.system(f"python3 {EMAIL_SCRIPT}")

# --- Schedule ---
# End of day sales data generation (e.g., 11:59 PM)
schedule.every().day.at("23:59").do(generate_daily_sales)

# Morning report (e.g., 7:00 AM)
schedule.every().day.at("07:00").do(run_morning_pipeline)

print("Daily scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(60)
