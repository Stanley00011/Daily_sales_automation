import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

DATA_DIR = "../data"
SUMMARY_FILE = os.path.join(DATA_DIR, "daily_summary.csv")

# --- Load summary ---
if not os.path.exists(SUMMARY_FILE):
    print("No summary file found. Run generate_daily_summary.py first.")
    exit()

summary_df = pd.read_csv(SUMMARY_FILE)
summary = summary_df.iloc[0]

# --- Build email ---
subject = f"Daily Sales Summary - {summary['Date']}"
body = f"""
Hello Team,

Here’s your automated sales summary for {summary['Date']}:

• Total Sales: ${summary['Total_Sales']:,.2f}
• Top Region: {summary['Top_Region']}
• Top Product: {summary['Top_Product']}
• Top Sales Rep: {summary['Top_Sales_Rep']}

Best,
Your Automation Bot 🤖
"""

msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# --- Send email ---
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(" Error sending email:", e)
