"""
UrbanMart Sales Analysis Script
Part 1, 2, and 3 of the Mini Project
Author: MAIB Student
Date: 2025
"""

import pandas as pd
from datetime import datetime

# ============================================================
# PART 1: Basic Python & Data Loading (Console Work)
# ============================================================

def part1_data_loading():
    """Part 1: Load data and perform basic analysis"""
    
    # a. Print welcome message using variables and f-strings
    store_name = "UrbanMart"
    print("=" * 60)
    print(f"Welcome to {store_name} Sales Analysis")
    print("=" * 60)
    print()
    
    try:
        # b. Read the CSV file using pandas
        print("Loading data from urbanmart_sales.csv...")
        df = pd.read_csv("urbanmart_sales.csv")
        print("✓ Data loaded successfully!\n")
        
        # c. Basic sanity checks
        print("--- BASIC SANITY CHECKS ---")
        print(f"Total number of rows: {len(df)}")
        print(f"Total number of columns: {len(df.columns)}")
        
        unique_stores = df['store_id'].unique()
        print(f"Unique store IDs: {list(unique_stores)}")
        
        min_date = df['date'].min()
        max_date = df['date'].max()
        print(f"Date range: {min_date} to {max_date}")
        print()
        
        # 3. Use basic lists, tuples, and dictionaries
        print("--- BASIC DATA STRUCTURES ---")
        
        # Create a list of all product categories
        product_categories = df['product_category'].unique().tolist()
        print(f"Product Categories (List): {product_categories}")
        print()
        
        # Create a dictionary that maps store_id → store_location
        store_mapping = df[['store_id', 'store_location']].drop_duplicates().set_index('store_id')['store_location'].to_dict()
        print(f"Store ID to Location Mapping (Dictionary):")
        for store_id, location in store_mapping.items():
            print(f"  {store_id} → {location}")
        print()
        
        # Use a loop to count how many transactions are "Online" vs "In-store" manually
        print("Counting channel distribution manually (without pandas):")
        online_count = 0
        instore_count = 0
        
        for index, row in df.iterrows():
            if row['channel'] == 'Online':
                online_count += 1
            elif row['channel'] == 'In-store':
                instore_count += 1
        
        print(f"  Online transactions: {online_count}")
        print(f"  In-store transactions: {instore_count}")
        print()
        
        return df
        
    except FileNotFoundError:
        print("❌ Error: urbanmart_sales.csv file not found!")
        print("Please ensure the file is in the same directory as this script.")
        return None
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None


# ============================================================
# PART 2: Functions & Simple KPIs
# ============================================================

def compute_total_revenue(df):
    """
    Returns total revenue = sum((quantity * unit_price) - discount_applied)
    
    Parameters:
    df (DataFrame): Sales data
    
    Returns:
    float: Total revenue
    """
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    total_revenue = df['line_revenue'].sum()
    return total_revenue


def compute_revenue_by_store(df):
    """
    Returns a dictionary of store-wise revenue
    
    Parameters:
    df (DataFrame): Sales data
    
    Returns:
    dict: Dictionary with store_location as keys and revenue as values
    """
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    revenue_by_store = df.groupby('store_location')['line_revenue'].sum().to_dict()
    return revenue_by_store


def compute_top_n_products(df, n=5):
    """
    Returns top n products by revenue
    
    Parameters:
    df (DataFrame): Sales data
    n (int): Number of top products to return (default=5)
    
    Returns:
    DataFrame: Top n products with their revenue
    """
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    top_products = df.groupby('product_name')['line_revenue'].sum().sort_values(ascending=False).head(n)
    return top_products.reset_index()


# ============================================================
# PART 3: Prepare Data for Dashboard
# ============================================================

def prepare_data_for_dashboard(df):
    """
    Prepare data with additional columns and summary tables
    
    Parameters:
    df (DataFrame): Original sales data
    
    Returns:
    tuple: (enhanced_df, summary_dict)
    """
    # Create new columns
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()
    
    # Prepare summary tables
    revenue_by_category = df.groupby('product_category')['line_revenue'].sum().sort_values(ascending=False)
    revenue_by_store = df.groupby('store_location')['line_revenue'].sum().sort_values(ascending=False)
    revenue_by_channel = df.groupby('channel')['line_revenue'].sum().sort_values(ascending=False)
    top_customers = df.groupby('customer_id')['line_revenue'].sum().sort_values(ascending=False).head(10)
    
    summary_dict = {
        'revenue_by_category': revenue_by_category,
        'revenue_by_store': revenue_by_store,
        'revenue_by_channel': revenue_by_channel,
        'top_customers': top_customers
    }
    
    return df, summary_dict


def filter_data(df, start_date=None, end_date=None, store=None, channel=None):
    """
    Filter data for a date range, store, and channel
    
    Parameters:
    df (DataFrame): Sales data
    start_date (str): Start date in YYYY-MM-DD format
    end_date (str): End date in YYYY-MM-DD format
    store (str or list): Store location(s) to filter
    channel (str): Channel to filter ('Online', 'In-store', or None for all)
    
    Returns:
    DataFrame: Filtered data
    """
    filtered_df = df.copy()
    
    # Apply date filter
    if start_date is not None:
        filtered_df = filtered_df[filtered_df['date'] >= pd.to_datetime(start_date)]
    
    if end_date is not None:
        filtered_df = filtered_df[filtered_df['date'] <= pd.to_datetime(end_date)]
    
    # Apply store filter
    if store is not None:
        if isinstance(store, list):
            filtered_df = filtered_df[filtered_df['store_location'].isin(store)]
        else:
            filtered_df = filtered_df[filtered_df['store_location'] == store]
    
    # Apply channel filter
    if channel is not None and channel != 'All':
        filtered_df = filtered_df[filtered_df['channel'] == channel]
    
    return filtered_df


# ============================================================
# CLI MENU (Part 2 - Task 4 & 5)
# ============================================================

def display_menu():
    """Display CLI menu options"""
    print("\n" + "=" * 60)
    print("URBANMART SALES ANALYTICS MENU")
    print("=" * 60)
    print("1. Show Total Revenue")
    print("2. Show Revenue by Store")
    print("3. Show Top 5 Products by Revenue")
    print("4. Show Summary Statistics")
    print("5. Exit")
    print("=" * 60)


def run_cli_menu(df):
    """
    Run interactive CLI menu for sales analytics
    
    Parameters:
    df (DataFrame): Sales data
    """
    if df is None:
        print("Cannot run menu without valid data!")
        return
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                # Show total revenue
                print("\n--- TOTAL REVENUE ---")
                total_rev = compute_total_revenue(df)
                print(f"Total Revenue: ${total_rev:,.2f}")
                
            elif choice == '2':
                # Show revenue by store
                print("\n--- REVENUE BY STORE ---")
                store_revenue = compute_revenue_by_store(df)
                for store, revenue in sorted(store_revenue.items(), key=lambda x: x[1], reverse=True):
                    print(f"{store:15} : ${revenue:,.2f}")
                
            elif choice == '3':
                # Show top 5 products
                print("\n--- TOP 5 PRODUCTS BY REVENUE ---")
                top_products = compute_top_n_products(df, n=5)
                print(f"\n{'Rank':<6} {'Product Name':<30} {'Revenue':<15}")
                print("-" * 60)
                for idx, row in top_products.iterrows():
                    print(f"{idx+1:<6} {row['product_name']:<30} ${row['line_revenue']:,.2f}")
                
            elif choice == '4':
                # Show summary statistics
                print("\n--- SUMMARY STATISTICS ---")
                df_enhanced, summaries = prepare_data_for_dashboard(df)
                
                print(f"\nTotal Transactions: {len(df_enhanced)}")
                print(f"Total Revenue: ${df_enhanced['line_revenue'].sum():,.2f}")
                print(f"Average Transaction Value: ${df_enhanced['line_revenue'].mean():,.2f}")
                print(f"Unique Customers: {df_enhanced['customer_id'].nunique()}")
                print(f"Unique Products: {df_enhanced['product_id'].nunique()}")
                
                print("\n--- Revenue by Category ---")
                for category, revenue in summaries['revenue_by_category'].items():
                    print(f"{category:20} : ${revenue:,.2f}")
                
            elif choice == '5':
                # Exit
                print("\n✓ Thank you for using UrbanMart Sales Analytics!")
                print("Goodbye!\n")
                break
                
            else:
                print("\n⚠ Invalid choice! Please enter a number between 1 and 5.")
                
        except KeyboardInterrupt:
            print("\n\n✓ Program interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Main function to execute the analysis"""
    print("\n")
    print("█" * 60)
    print("█  URBANMART RETAIL INSIGHTS - CONSOLE APPLICATION       █")
    print("█  Data Analytics & Business Intelligence Project        █")
    print("█" * 60)
    print("\n")
    
    # Part 1: Load and explore data
    df = part1_data_loading()
    
    if df is not None:
        # Part 2 & 3: Run CLI menu
        run_cli_menu(df)


if __name__ == "__main__":
    main()
