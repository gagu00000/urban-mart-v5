"""
UrbanMart Sales Dashboard
Streamlit Web Application
Author: MAIB Student
Date: 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="UrbanMart Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

@st.cache_data
def load_data():
    """Load and prepare the sales data"""
    try:
        df = pd.read_csv("urbanmart_sales.csv")
        df['date'] = pd.to_datetime(df['date'])
        df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
        df['day_of_week'] = df['date'].dt.day_name()
        return df
    except FileNotFoundError:
        st.error("❌ Error: urbanmart_sales.csv not found! Please ensure the file is in the same directory.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()


def filter_data(df, start_date, end_date, store_locations, channel, categories):
    """Apply filters to the dataframe"""
    filtered_df = df.copy()
    
    # Date filter
    filtered_df = filtered_df[
        (filtered_df['date'] >= pd.to_datetime(start_date)) & 
        (filtered_df['date'] <= pd.to_datetime(end_date))
    ]
    
    # Store location filter
    if store_locations:
        filtered_df = filtered_df[filtered_df['store_location'].isin(store_locations)]
    
    # Channel filter
    if channel != "All":
        filtered_df = filtered_df[filtered_df['channel'] == channel]
    
    # Category filter
    if categories:
        filtered_df = filtered_df[filtered_df['product_category'].isin(categories)]
    
    return filtered_df


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()

# ============================================================
# HEADER
# ============================================================

st.title("🛒 UrbanMart Sales Dashboard")
st.markdown("**Built by MAIB students using Python & Streamlit**")
st.markdown("---")

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("📊 Dashboard Filters")

# Date range filter
min_date = df['date'].min().date()
max_date = df['date'].max().date()

st.sidebar.subheader("Date Range")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handle date range selection
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

# Store location filter
st.sidebar.subheader("Store Location")
all_locations = df['store_location'].unique().tolist()
selected_locations = st.sidebar.multiselect(
    "Select Store Location(s)",
    options=all_locations,
    default=all_locations
)

# Channel filter
st.sidebar.subheader("Sales Channel")
channel_option = st.sidebar.selectbox(
    "Select Channel",
    options=["All", "In-store", "Online"]
)

# Product category filter
st.sidebar.subheader("Product Category")
all_categories = df['product_category'].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Select Category(ies)",
    options=all_categories,
    default=all_categories
)

# Apply filters
df_filtered = filter_data(df, start_date, end_date, selected_locations, channel_option, selected_categories)

# Display filter summary
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Filtered Records:** {len(df_filtered):,} / {len(df):,}")

# ============================================================
# KEY METRICS
# ============================================================

st.header("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = df_filtered['line_revenue'].sum()
    st.metric(
        label="💰 Total Revenue",
        value=f"${total_revenue:,.2f}"
    )

with col2:
    total_transactions = len(df_filtered)
    st.metric(
        label="📝 Total Transactions",
        value=f"{total_transactions:,}"
    )

with col3:
    avg_revenue = df_filtered['line_revenue'].mean()
    st.metric(
        label="📊 Avg Revenue/Transaction",
        value=f"${avg_revenue:,.2f}"
    )

with col4:
    unique_customers = df_filtered['customer_id'].nunique()
    st.metric(
        label="👥 Unique Customers",
        value=f"{unique_customers:,}"
    )

st.markdown("---")

# ============================================================
# REVENUE BY CATEGORY
# ============================================================

st.header("📦 Revenue by Product Category")

revenue_by_category = df_filtered.groupby('product_category')['line_revenue'].sum().sort_values(ascending=False).reset_index()

fig_category = px.bar(
    revenue_by_category,
    x='product_category',
    y='line_revenue',
    title="Revenue Distribution Across Product Categories",
    labels={'product_category': 'Product Category', 'line_revenue': 'Revenue ($)'},
    color='line_revenue',
    color_continuous_scale='Blues',
    text='line_revenue'
)

fig_category.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
fig_category.update_layout(
    xaxis_title="Product Category",
    yaxis_title="Revenue ($)",
    showlegend=False,
    height=500
)

st.plotly_chart(fig_category, use_container_width=True)

# ============================================================
# REVENUE BY STORE & CHANNEL
# ============================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏪 Revenue by Store Location")
    revenue_by_store = df_filtered.groupby('store_location')['line_revenue'].sum().sort_values(ascending=False).reset_index()
    
    fig_store = px.bar(
        revenue_by_store,
        x='store_location',
        y='line_revenue',
        title="Store Performance Comparison",
        labels={'store_location': 'Store Location', 'line_revenue': 'Revenue ($)'},
        color='line_revenue',
        color_continuous_scale='Greens',
        text='line_revenue'
    )
    
    fig_store.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_store.update_layout(showlegend=False, height=400)
    
    st.plotly_chart(fig_store, use_container_width=True)

with col2:
    st.subheader("🛍️ Revenue by Channel")
    revenue_by_channel = df_filtered.groupby('channel')['line_revenue'].sum().reset_index()
    
    fig_channel = px.pie(
        revenue_by_channel,
        values='line_revenue',
        names='channel',
        title="Sales Channel Distribution",
        color_discrete_sequence=['#636EFA', '#EF553B']
    )
    
    fig_channel.update_traces(textposition='inside', textinfo='percent+label+value')
    fig_channel.update_layout(height=400)
    
    st.plotly_chart(fig_channel, use_container_width=True)

st.markdown("---")

# ============================================================
# DAILY REVENUE TREND
# ============================================================

st.header("📅 Daily Revenue Trend")

daily_revenue = df_filtered.groupby('date')['line_revenue'].sum().reset_index()

fig_trend = px.line(
    daily_revenue,
    x='date',
    y='line_revenue',
    title="Revenue Trend Over Time",
    labels={'date': 'Date', 'line_revenue': 'Revenue ($)'},
    markers=True
)

fig_trend.update_traces(line_color='#FF6692', line_width=3)
fig_trend.update_layout(
    xaxis_title="Date",
    yaxis_title="Revenue ($)",
    height=400,
    hovermode='x unified'
)

st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# ============================================================
# TOP PRODUCTS AND CUSTOMERS
# ============================================================

st.header("🏆 Top Performers")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🥇 Top 5 Products by Revenue")
    top_products = df_filtered.groupby('product_name')['line_revenue'].sum().sort_values(ascending=False).head(5).reset_index()
    top_products['rank'] = range(1, len(top_products) + 1)
    top_products = top_products[['rank', 'product_name', 'line_revenue']]
    top_products.columns = ['Rank', 'Product Name', 'Revenue ($)']
    top_products['Revenue ($)'] = top_products['Revenue ($)'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(
        top_products,
        hide_index=True,
        use_container_width=True,
        height=250
    )

with col2:
    st.subheader("👑 Top 5 Customers by Revenue")
    top_customers = df_filtered.groupby('customer_id')['line_revenue'].sum().sort_values(ascending=False).head(5).reset_index()
    top_customers['rank'] = range(1, len(top_customers) + 1)
    
    # Add customer segment info
    customer_segments = df_filtered.groupby('customer_id')['customer_segment'].first().reset_index()
    top_customers = top_customers.merge(customer_segments, on='customer_id')
    
    top_customers = top_customers[['rank', 'customer_id', 'customer_segment', 'line_revenue']]
    top_customers.columns = ['Rank', 'Customer ID', 'Segment', 'Revenue ($)']
    top_customers['Revenue ($)'] = top_customers['Revenue ($)'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(
        top_customers,
        hide_index=True,
        use_container_width=True,
        height=250
    )

st.markdown("---")

# ============================================================
# ADDITIONAL INSIGHTS
# ============================================================

st.header("💡 Additional Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Payment Methods")
    payment_dist = df_filtered.groupby('payment_method')['line_revenue'].sum().reset_index()
    
    fig_payment = px.pie(
        payment_dist,
        values='line_revenue',
        names='payment_method',
        title="Revenue by Payment Method"
    )
    fig_payment.update_layout(height=300)
    st.plotly_chart(fig_payment, use_container_width=True)

with col2:
    st.subheader("👥 Customer Segments")
    segment_dist = df_filtered.groupby('customer_segment')['line_revenue'].sum().reset_index()
    
    fig_segment = px.pie(
        segment_dist,
        values='line_revenue',
        names='customer_segment',
        title="Revenue by Customer Segment",
        color_discrete_sequence=['#00CC96', '#AB63FA', '#FFA15A']
    )
    fig_segment.update_layout(height=300)
    st.plotly_chart(fig_segment, use_container_width=True)

with col3:
    st.subheader("📅 Day of Week Performance")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_revenue = df_filtered.groupby('day_of_week')['line_revenue'].sum().reset_index()
    day_revenue['day_of_week'] = pd.Categorical(day_revenue['day_of_week'], categories=day_order, ordered=True)
    day_revenue = day_revenue.sort_values('day_of_week')
    
    fig_day = px.bar(
        day_revenue,
        x='day_of_week',
        y='line_revenue',
        title="Revenue by Day of Week",
        color='line_revenue',
        color_continuous_scale='Purples'
    )
    fig_day.update_layout(height=300, showlegend=False, xaxis_title="", yaxis_title="Revenue ($)")
    st.plotly_chart(fig_day, use_container_width=True)

st.markdown("---")

# ============================================================
# RAW DATA PREVIEW
# ============================================================

st.header("📋 Raw Data Sample")
st.markdown(f"Showing first 20 records from {len(df_filtered):,} filtered transactions")

# Format the dataframe for display
display_df = df_filtered.head(20).copy()
display_df['line_revenue'] = display_df['line_revenue'].apply(lambda x: f"${x:.2f}")
display_df['unit_price'] = display_df['unit_price'].apply(lambda x: f"${x:.2f}")
display_df['discount_applied'] = display_df['discount_applied'].apply(lambda x: f"${x:.2f}")
display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=400
)

# Download button for filtered data
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=df_filtered.to_csv(index=False).encode('utf-8'),
    file_name=f"urbanmart_filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>UrbanMart Retail Insights Dashboard</strong></p>
        <p>Built with ❤️ by MAIB Students | Powered by Streamlit & Python</p>
        <p>© 2025 UrbanMart Analytics. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)
