import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import os
from dotenv import load_dotenv
from utils import get_data_path

# --- Load environment variables (Gmail, etc.) ---
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

summary_file = get_data_path("daily_summary.csv")

# --- Load summary ---
if not os.path.exists(summary_file):
    print("No summary file found. Run generate_daily_summary.py first.")
    exit()

summary_df = pd.read_csv(summary_file)
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

# --- Don’t send email in Streamlit Cloud ---
if os.environ.get("STREAMLIT_CLOUD") == "1":
    print("⚠️ Streamlit Cloud — email sending skipped.")
    print(body)
    exit()

# --- Safe checks ---
if not all([SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL]):
    print("Missing email credentials in .env — email not sent.")
    exit()

# --- Send email ---
try:
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("Email sent successfully!")

except Exception as e:
    print(" Error sending email:", e)
