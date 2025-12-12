# Updated app.py with requested changes
# (Professional color scheme, per-chart filters, and attribution text)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="UrbanMart Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    df = pd.read_csv("urbanmart_sales.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    df['day_of_week'] = df['date'].dt.day_name()
    return df

df = load_data()

# ----------------------------------------
# HEADER
# ----------------------------------------
st.title("🛒 UrbanMart Sales Dashboard")
st.markdown("**Built by MAIB students - Gagandeep Singh | Kartik Joshi | Karan Baid**")
st.markdown("---")

# ----------------------------------------
# GLOBAL FILTERS (for KPIs only)
# ----------------------------------------
st.sidebar.header("📊 Global Filters (KPI Only)")

min_date = df['date'].min().date()
max_date = df['date'].max().date()

global_date = st.sidebar.date_input(
    "Global Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(global_date) == 2:
    g_start, g_end = global_date
else:
    g_start = g_end = global_date[0]

global_df = df[(df['date'] >= pd.to_datetime(g_start)) & (df['date'] <= pd.to_datetime(g_end))]

# ----------------------------------------
# KPIs
# ----------------------------------------
st.header("📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Revenue", f"${global_df['line_revenue'].sum():,.2f}")
with col2:
    st.metric("📝 Total Transactions", f"{len(global_df):,}")
with col3:
    st.metric("📊 Avg Revenue/Transaction", f"${global_df['line_revenue'].mean():,.2f}")
with col4:
    st.metric("👥 Unique Customers", f"{global_df['customer_id'].nunique():,}")

st.markdown("---")

# ------------------------------------------------
# CHART 1 FILTERS: CATEGORY ANALYSIS
# ------------------------------------------------
st.subheader("📦 Revenue by Category – Custom Filters")

cat_cols = st.columns(3)
with cat_cols[0]:
    cat_date = st.date_input("Category Date Range", (min_date, max_date))
with cat_cols[1]:
    cat_locations = st.multiselect("Category Store Location", df['store_location'].unique())
with cat_cols[2]:
    cat_channels = st.multiselect("Category Channels", df['channel'].unique())

cat_df = df.copy()
# Apply filters
if len(cat_date) == 2:
    c_start, c_end = cat_date
else:
    c_start = c_end = cat_date[0]
cat_df = cat_df[(cat_df['date'] >= pd.to_datetime(c_start)) & (cat_df['date'] <= pd.to_datetime(c_end))]
if cat_locations:
    cat_df = cat_df[cat_df['store_location'].isin(cat_locations)]
if cat_channels:
    cat_df = cat_df[cat_df['channel'].isin(cat_channels)]

# Professional color scheme: Blues / Greys
cat_rev = cat_df.groupby('product_category')['line_revenue'].sum().reset_index()
fig_category = px.bar(
    cat_rev,
    x='product_category',
    y='line_revenue',
    color='line_revenue',
    color_continuous_scale='Blues',
    title="Revenue by Category",
)
st.plotly_chart(fig_category, use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# CHART 2 FILTERS: STORE LOCATION PERFORMANCE
# ------------------------------------------------
st.subheader("🏪 Store Revenue – Custom Filters")

store_cols = st.columns(2)
with store_cols[0]:
    store_date = st.date_input("Store Date Range", (min_date, max_date))
with store_cols[1]:
    store_channel = st.multiselect("Store Channels", df['channel'].unique())

store_df = df.copy()
if len(store_date) == 2:
    s_start, s_end = store_date
else:
    s_start = s_end = store_date[0]
store_df = store_df[(store_df['date'] >= pd.to_datetime(s_start)) & (store_df['date'] <= pd.to_datetime(s_end))]
if store_channel:
    store_df = store_df[store_df['channel'].isin(store_channel)]

store_rev = store_df.groupby('store_location')['line_revenue'].sum().reset_index()
fig_store = px.bar(
    store_rev,
    x='store_location',
    y='line_revenue',
    color='line_revenue',
    color_continuous_scale='Greys',
    title="Store Revenue",
)
st.plotly_chart(fig_store, use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# CHART 3: DAILY TREND WITH ITS OWN FILTER
# ------------------------------------------------
st.subheader("📅 Daily Revenue Trend – Custom Filters")

trend_cols = st.columns(2)
with trend_cols[0]:
    t_date = st.date_input("Trend Date Range", (min_date, max_date))
with trend_cols[1]:
    t_category = st.multiselect("Trend Categories", df['product_category'].unique())

trend_df = df.copy()
if len(t_date) == 2:
    t_start, t_end = t_date
else:
    t_start = t_end = t_date[0]
trend_df = trend_df[(trend_df['date'] >= pd.to_datetime(t_start)) & (trend_df['date'] <= pd.to_datetime(t_end))]
if t_category:
    trend_df = trend_df[trend_df['product_category'].isin(t_category)]

daily = trend_df.groupby('date')['line_revenue'].sum().reset_index()
fig_trend = px.line(
    daily,
    x='date',
    y='line_revenue',
    title="Revenue Trend",
    markers=True,
)
fig_trend.update_traces(line=dict(width=3))
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# RAW DATA OPTIONAL
# ------------------------------------------------
st.subheader("📋 Raw Data Preview")
st.dataframe(df.head(20), use_container_width=True)

st.download_button(
    "Download CSV",
    df.to_csv(index=False).encode('utf-8'),
    file_name="urbanmart_export.csv"
)

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#444;'>Built by MAIB students - Gagandeep Singh | Kartik Joshi | Karan Baid</p>",
    unsafe_allow_html=True
)
