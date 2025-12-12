# app.py updated to KEEP your original filters and add multipage navigation

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="UrbanMart Sales Dashboard", page_icon="🛒", layout="wide")

# --------------------
# LOAD DATA
# --------------------
# --------------------
# OPTIONAL HELPER FILTER FUNCTION (added as requested)
# --------------------
def filter_data(df, start_date=None, end_date=None, store=None, channel=None):
    filtered_df = df.copy()

    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['date'] >= pd.to_datetime(start_date)) & (filtered_df['date'] <= pd.to_datetime(end_date))]
    if store:
        filtered_df = filtered_df[filtered_df['store_location'].isin(store)]
    if channel and channel != "All":
        filtered_df = filtered_df[filtered_df['channel'] == channel]

    return filtered_df

@st.cache_data
def filter_data(df, start_date=None, end_date=None, store=None, channel=None):
    filtered_df = df.copy()

    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['date'] >= pd.to_datetime(start_date)) &
            (filtered_df['date'] <= pd.to_datetime(end_date))
        ]

    if store:
        filtered_df = filtered_df[filtered_df['store_location'].isin(store)]

    if channel and channel != "All":
        filtered_df = filtered_df[filtered_df['channel'] == channel]

    return filtered_df


def load_data():
    df = pd.read_csv("urbanmart_sales.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    df['day_of_week'] = df['date'].dt.day_name()
    return df

df = load_data()

# --------------------
# MULTIPAGE NAVIGATION
# --------------------
st.sidebar.title("📑 Navigation")
page = st.sidebar.radio("Go to:", ["Dashboard", "Category Insights", "Store Insights", "Trends", "Top Performers", "Raw Data"])

# --------------------
# ORIGINAL GLOBAL FILTERS (unchanged)
# --------------------
st.sidebar.header("📊 Filters")
min_date = df['date'].min().date()
max_date = df['date'].max().date()

# Date filter
date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

# Store filter
all_locations = df['store_location'].unique().tolist()
selected_locations = st.sidebar.multiselect("Store Location", all_locations, default=all_locations)

# Channel filter
channel_option = st.sidebar.selectbox("Sales Channel", ["All", "In-store", "Online"])

# Category filter
all_categories = df['product_category'].unique().tolist()
selected_categories = st.sidebar.multiselect("Category", all_categories, default=all_categories)

# APPLY FILTERS – SAME LOGIC AS ORIGINAL
filtered_df = df.copy()
filtered_df = filtered_df[(filtered_df['date'] >= pd.to_datetime(start_date)) & (filtered_df['date'] <= pd.to_datetime(end_date))]
if selected_locations:
    filtered_df = filtered_df[filtered_df['store_location'].isin(selected_locations)]
if channel_option != "All":
    filtered_df = filtered_df[filtered_df['channel'] == channel_option]
if selected_categories:
    filtered_df = filtered_df[filtered_df['product_category'].isin(selected_categories)]

# --------------------
# PAGE 1 – MAIN DASHBOARD
# --------------------
if page == "Dashboard":
    st.title("🛒 UrbanMart Sales Dashboard")
    st.markdown("**Built by MAIB students - Gagandeep Singh | Kartik Joshi | Karan Baid**")
    st.markdown("---")

    # KPIs
    st.header("📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"${filtered_df['line_revenue'].sum():,.2f}")
    col2.metric("📝 Transactions", f"{len(filtered_df):,}")
    col3.metric("📊 Avg Revenue", f"${filtered_df['line_revenue'].mean():,.2f}")
    col4.metric("👥 Unique Customers", f"{filtered_df['customer_id'].nunique():,}")
    st.markdown("---")

    st.header("📦 Revenue by Product Category")
    revenue_by_category = filtered_df.groupby('product_category')['line_revenue'].sum().reset_index()
    fig = px.bar(revenue_by_category, x='product_category', y='line_revenue', color='line_revenue', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

# --------------------
# PAGE 2 – CATEGORY INSIGHTS
# --------------------
elif page == "Category Insights":
    st.title("📦 Category Insights")
    rev = filtered_df.groupby('product_category')['line_revenue'].sum().reset_index()
    fig = px.pie(rev, values='line_revenue', names='product_category')
    st.plotly_chart(fig, use_container_width=True)

# --------------------
# PAGE 3 – STORE INSIGHTS
# --------------------
elif page == "Store Insights":
    st.title("🏪 Store Insights")
    store_rev = filtered_df.groupby('store_location')['line_revenue'].sum().reset_index()

fig = px.bar(
    store_rev,
    x='store_location',
    y='line_revenue',
    color='store_location',   # categorical colors (fix applied)
    title="Store Revenue"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------
# PAGE 4 – DAILY REVENUE TRENDS
# --------------------
elif page == "Trends":
    st.title("📅 Revenue Trends")
    daily = filtered_df.groupby('date')['line_revenue'].sum().reset_index()
    fig = px.line(
        daily,
        x='date',
        y='line_revenue',
        markers=True,
        title="Daily Revenue Trend"
        x='date', y='line_revenue', markers=True)
    st.plotly_chart(fig, use_container_width=True)

# --------------------
# PAGE 5 – TOP PERFORMERS
# --------------------
elif page == "Top Performers":
    st.title("🏆 Top Performers")

    st.subheader("Top 5 Products")
    top_products = filtered_df.groupby('product_name')['line_revenue'].sum().sort_values(ascending=False).head(5).reset_index()
    st.dataframe(top_products, use_container_width=True)

    st.subheader("Top 5 Customers")
    top_customers = filtered_df.groupby('customer_id')['line_revenue'].sum().sort_values(ascending=False).head(5).reset_index()
    st.dataframe(top_customers, use_container_width=True)

# --------------------
# PAGE 6 – RAW DATA
# --------------------
elif page == "Raw Data":
    st.title("📋 Raw Data Preview")
    st.dataframe(filtered_df.head(50), use_container_width=True)
    st.download_button("Download CSV", filtered_df.to_csv(index=False), "urbanmart_filtered.csv")

# FOOTER
st.markdown("---")
st.markdown("<p style='text-align:center;color:#555;'>Built by MAIB students - Gagandeep Singh | Kartik Joshi | Karan Baid</p>", unsafe_allow_html=True)
