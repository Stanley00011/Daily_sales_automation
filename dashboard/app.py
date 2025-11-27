import streamlit as st
import pandas as pd
import time
import altair as alt
from utils import get_data_path

st.set_page_config(page_title="Daily Sales Dashboard", layout="wide")

# Auto-refresh every 5 minutes
REFRESH_SEC = 300
last_refresh = st.session_state.get("last_refresh", time.time())
if time.time() - last_refresh > REFRESH_SEC:
    st.session_state["last_refresh"] = time.time()
    st.experimental_rerun()

st.title("Daily Sales Performance Dashboard")

# Dynamic path
DATA_PATH = get_data_path("sales_master.csv")
st.caption(f"Data Source → {DATA_PATH}")

# Load CSV
try:
    df = pd.read_csv(DATA_PATH)
except Exception:
    st.warning("No data found yet. Run GitHub Actions or wait for the 6 PM refresh.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])

# Metrics
latest = df["Date"].max()
latest_df = df[df["Date"] == latest]

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales For Today", f"${latest_df['Total_Sale'].sum():,.0f}")
col2.metric("Top Region", latest_df.groupby("Region")["Total_Sale"].sum().idxmax())
col3.metric("Top Product", latest_df.groupby("Product")["Total_Sale"].sum().idxmax())

st.divider()

st.subheader("Sales Trend Over Time")
trend = df.groupby("Date")["Total_Sale"].sum().reset_index()
st.line_chart(trend, x="Date", y="Total_Sale")


st.subheader("Top Products by Revenue")
product_sales = df.groupby("Product")["Total_Sale"].sum().sort_values(ascending=False)
st.bar_chart(product_sales)

st.subheader("Sales by Region")
region_sales = df.groupby("Region")["Total_Sale"].sum().sort_values(ascending=False)
st.bar_chart(region_sales)                                  


import altair as alt # Ensure this import is at the top of your file!

st.subheader("Product Revenue Mix")

# 1. Group by Product and calculate percentage contribution
product_mix = df.groupby("Product")["Total_Sale"].sum().reset_index()
total_sales = product_mix['Total_Sale'].sum()
product_mix['Percentage'] = (product_mix['Total_Sale'] / total_sales)

# 2. Create the Altair Pie/Donut Chart
# Make the chart bigger by setting explicit height/width
base = alt.Chart(product_mix).encode(
    theta=alt.Theta("Total_Sale", stack=True)
).properties(
    title='Product Revenue Contribution',
    height=350, # Set a fixed height
    width=350  # Set a fixed width
)

# Increase radius for a bigger chart (e.g., 120 -> 160, 80 -> 100)
pie = base.mark_arc(outerRadius=160, innerRadius=100).encode(
    color=alt.Color("Product"),
    order=alt.Order("Total_Sale", sort="descending"),
    # Tooltip Total_Sale format changed to remove cents ($.0f)
    tooltip=["Product", alt.Tooltip("Total_Sale", format="$,.0f"), alt.Tooltip("Percentage", format=".0%")] 
)

# Outer text labels (Percentage)
text_outer = base.mark_text(radius=180).encode( # Adjusted radius for new arc size
    text=alt.Text("Percentage", format=".0%"),  # FORMAT CHANGED TO REMOVE DECIMAL POINT
    order=alt.Order("Total_Sale", sort="descending"),
    color=alt.value("black")
)

# New center text detail layer (Total Sales)
# We need a small, separate DataFrame just for the center text
center_df = pd.DataFrame([{'Total_Sale': total_sales}])

center_text = alt.Chart(center_df).mark_text(
    align='center',
    baseline='middle',
    fontSize=20, # Makes the number bigger
    fontWeight='bold',
    text=f"Total: ${total_sales:,.0f}" # Display the formatted Total Sales string
)

# Combine all three layers: pie ring, outer percentage labels, and center total
st.altair_chart(pie + text_outer + center_text, use_container_width=True)


st.subheader("Top Sales Representatives by Revenue")
# Use the nlargest() function for a cleaner top N list
rep_performance = df.groupby("Sales_Rep")["Total_Sale"].sum().nlargest(10).reset_index()
st.bar_chart(rep_performance, x="Sales_Rep", y="Total_Sale")


st.subheader("Volume and Price Analysis by Product")

# Aggregate key metrics per product
volume_price_analysis = df.groupby('Product').agg(
    Total_Quantity=('Quantity', 'sum'),
    Average_Unit_Price=('Unit_Price', 'mean'),
    Total_Revenue=('Total_Sale', 'sum')
).reset_index()

# 1. Create the base chart
base = alt.Chart(volume_price_analysis).encode(
    x=alt.X('Total_Quantity', title='Total Units Sold'),
    y=alt.Y('Average_Unit_Price', title='Avg. Unit Price'),
    tooltip=[
        'Product', 
        alt.Tooltip('Total_Quantity', title='Units Sold'),
        alt.Tooltip('Average_Unit_Price', title='Avg. Price', format='$,.2f'),
        alt.Tooltip('Total_Revenue', title='Revenue', format='$,.0f')
    ]
)

# 2. Create the scatter plot layer (dots, sized by revenue)
scatter = base.mark_circle().encode(
    size=alt.Size('Total_Revenue', legend=alt.Legend(title='Total Revenue')),
    color=alt.value('#87CEEB') # Set a fixed color
)

# 3. Create the text label layer
text = base.mark_text(
    align='left',
    baseline='middle',
    dx=7 # Nudges the text slightly to the right of the dot
).encode(
    text='Product', # Use the 'Product' column for the text label
    size=alt.value(10) # Set a fixed size for the text
)

# 4. Combine the layers and display
st.altair_chart(scatter + text, use_container_width=True)