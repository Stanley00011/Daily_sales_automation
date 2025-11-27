# Daily Sales Automation Pipeline

An end-to-end **automated data pipeline** that simulates daily sales, consolidates data, generates insights, sends automated email reports, and powers a live auto-refreshing dashboard.

This project shows how a Data Analyst can merge **automation + analytics + lightweight engineering** to deliver consistent value—hands-free.

---

## Why I Built This

To demonstrate how a modern Data Analyst can:

* Automate recurring reporting work
* Deliver insights without manual effort
* Build pipeline-style systems with Python
* Combine analytics with automation tools

This project works **fully offline**, uses simulated data, and can run **locally** or be extended to the cloud.

---

## Pipeline Flow

```
[Generate Daily Data] → [Combine Dataset] → [Generate Summary] → [Send Email]
                             ↓
                   Streamlit Dashboard
                  (auto-refresh + updates)
```

---

## older Structure

```
daily_sales_automation/
│
├── data/          # stores daily CSV files + master dataset
├── scripts/       # Python automation scripts
├── dashboard/     # Streamlit dashboard
└── README.md
```

---

## How the Pipeline Works

### **1. Daily Data Generation** (`generate_sales_data.py`)

Simulates 200+ transactions daily with:

* region
* sales rep
* product
* quantity
* unit price
* total sale

Each day produces a file like:

```
sales_2025-11-27.csv
```

---

### **2. Data Consolidation** (`consolidate_data.py`)

Merges each new daily file into a long-term `sales_master.csv`.

Ensures no duplicates and maintains full history.

---

### **3. Daily Insight Extraction** (`generate_daily_summary.py`)

Creates key KPIs:

* Total revenue
* Units sold
* Top product
* Best performing sales rep
* Region with highest revenue

Exports a daily summary table.

---

### **4. Automated Email Report** (`send_email_report.py`)

Sends a formatted email containing:

* KPI summary
* Trends
* Attached CSV

Uses Gmail SMTP + App Passwords.
Secrets stored in `.env`:

```
SENDER_EMAIL=
APP_PASSWORD=
RECEIVER_EMAIL=
```

---

## Dashboard – Streamlit (`dashboard/app.py`)

Features:

* Auto-refresh (every 5 mins)
* Dynamically loads the latest dataset
* KPI cards
* Daily trend charts
* Top products vs regions

Run it with:

```
cd dashboard
streamlit run app.py
```

---

## How to Run the Entire System

1. Clone the repo
2. Create a virtual env
3. Install dependencies
4. Set `.env` values
5. Run the automation scripts
6. Start the Streamlit dashboard
