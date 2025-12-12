# 🛒 UrbanMart Retail Insights Dashboard

A comprehensive Python & Streamlit mini-project for retail sales analytics, built as part of the MAIB (Master of AI in Business) curriculum.

---

## 📊 Project Overview

**UrbanMart** is a mid-sized retail chain operating in a metropolitan city. This project provides management with an interactive web-based dashboard to understand:

- Which product categories are performing well
- How sales vary across stores and days
- Which customers are most valuable
- Revenue trends and patterns

---

## 🎯 Learning Objectives

This project demonstrates practical skills in:

- ✅ Basic Python: variables, data types, operators
- ✅ Data structures: lists, tuples, dictionaries
- ✅ Control flow: loops (for, while) and conditionals (if/elif/else)
- ✅ Functions with parameters and return values
- ✅ File handling (reading CSV files)
- ✅ Error handling (try/except)
- ✅ External libraries: pandas, plotly, streamlit
- ✅ Building interactive dashboards with filters and visualizations

---

## 📁 Project Structure

```
urbanmart-dashboard/
│
├── urbanmart_sales.csv          # Sales transaction data
├── urbanmart_analysis.py        # Console-based analytics (Parts 1-3)
├── app.py                       # Streamlit dashboard (Part 4)
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 🗃️ Dataset Description

**File:** `urbanmart_sales.csv`

**Size:** 200 transaction records

**Date Range:** January 10, 2025 - March 16, 2025

### Columns (15 total)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| transaction_id | string | Unique ID for each transaction line | TXN-2025-0001 |
| bill_id | string | Bill number (one bill can have multiple products) | BILL-1001 |
| date | string | Date of transaction (YYYY-MM-DD) | 2025-01-15 |
| store_id | string | Unique store identifier | S1, S2, S3 |
| store_location | string | Store area/region | Downtown, Uptown, Suburban |
| customer_id | string | Unique customer identifier | C001, C002 |
| customer_segment | string | Customer segment | Regular, New, Loyal |
| product_id | string | Unique product identifier | P101, P205 |
| product_category | string | Product category | Beverages, Snacks, Personal Care |
| product_name | string | Name of the product | Orange Juice 1L, Potato Chips |
| quantity | integer | Units purchased | 2, 5 |
| unit_price | float | Price per unit | 3.5, 1.25 |
| payment_method | string | Payment method used | Cash, Credit Card, UPI |
| discount_applied | float | Discount amount in currency | 0.0, 2.5 |
| channel | string | Sales channel | In-store, Online |

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/urbanmart-dashboard.git
cd urbanmart-dashboard
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Console Application

```bash
python urbanmart_analysis.py
```

This will run the CLI menu with options to:
1. Show total revenue
2. Show revenue by store
3. Show top 5 products
4. Show summary statistics
5. Exit

### Step 4: Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

---

## 🌐 Deployment on Streamlit Cloud

### Option 1: Deploy via GitHub

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: UrbanMart Dashboard"
   git push origin main
   ```

2. **Visit [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Sign in with GitHub**

4. **Click "New app"**

5. **Configure deployment:**
   - Repository: `yourusername/urbanmart-dashboard`
   - Branch: `main`
   - Main file path: `app.py`

6. **Click "Deploy"**

Your dashboard will be live at: `https://yourusername-urbanmart-dashboard.streamlit.app`

### Option 2: Deploy via Streamlit CLI

```bash
streamlit deploy
```

---

## 📦 Dependencies

Create a `requirements.txt` file with:

```
streamlit==1.31.0
pandas==2.2.0
plotly==5.18.0
```

---

## 🎨 Dashboard Features

### 📊 Interactive Filters (Sidebar)
- **Date Range Selector**: Filter transactions by custom date range
- **Store Location**: Multi-select filter for specific store locations
- **Sales Channel**: Choose between All, Online, or In-store
- **Product Category**: Multi-select filter for product categories

### 📈 Key Performance Indicators
- 💰 **Total Revenue**: Sum of all filtered transactions
- 📝 **Total Transactions**: Count of transaction records
- 📊 **Average Revenue per Transaction**: Mean transaction value
- 👥 **Unique Customers**: Count of distinct customers

### 📉 Visualizations

1. **Revenue by Product Category** - Bar chart showing category performance
2. **Revenue by Store Location** - Bar chart comparing store performance
3. **Revenue by Channel** - Pie chart showing online vs in-store split
4. **Daily Revenue Trend** - Line chart tracking revenue over time
5. **Top 5 Products** - Table of best-performing products
6. **Top 5 Customers** - Table of highest-value customers
7. **Payment Method Distribution** - Pie chart of payment preferences
8. **Customer Segment Analysis** - Pie chart of segment revenue
9. **Day of Week Performance** - Bar chart showing weekly patterns

### 📋 Raw Data Preview
- Display first 20 filtered records
- Download filtered data as CSV

---

## 🤔 Part 5: Reflection Questions & Answers

### 1. Which store location generates the highest revenue overall?

**Answer:** Based on the data analysis, **[Store Location]** generates the highest revenue overall with approximately **$[Amount]**. This can be attributed to:
- Higher foot traffic in the area
- Larger product selection
- Strategic location in a commercial hub

*Note: Run the dashboard to see the actual figures for your dataset.*

---

### 2. Does online or in-store channel generate more revenue in your filtered view?

**Answer:** The **[Channel]** channel generates more revenue. Key observations:
- In-store transactions typically have higher average order values
- Online transactions show growing trend over time
- Product categories perform differently across channels (e.g., Electronics do better online)

*Use the dashboard filters to compare different time periods and see channel trends.*

---

### 3. Which 3 product categories contribute the most revenue?

**Answer:** The top 3 revenue-generating categories are:

1. **[Category 1]** - $[Amount] ([Percentage]%)
2. **[Category 2]** - $[Amount] ([Percentage]%)
3. **[Category 3]** - $[Amount] ([Percentage]%)

**Insights:**
- These three categories account for approximately [X]% of total revenue
- Focus marketing efforts on these high-performing categories
- Consider expanding inventory in these categories

*Check the "Revenue by Product Category" chart in the dashboard for exact figures.*

---

### 4. What additional filter/feature would you add to make this dashboard more useful for management?

**Suggested Enhancements:**

1. **Time Comparison Features**
   - Year-over-Year (YoY) comparison
   - Month-over-Month (MoM) growth rates
   - Same period last year comparison

2. **Customer Analytics**
   - Customer lifetime value (CLV) calculation
   - Churn analysis
   - Customer acquisition cost vs. revenue
   - Repeat purchase rate

3. **Product Performance Metrics**
   - Inventory turnover rate
   - Profit margin by product/category
   - Product bundling analysis
   - Seasonal trends identification

4. **Advanced Filters**
   - Filter by payment method
   - Filter by customer segment
   - Filter by discount ranges
   - Filter by price ranges

5. **Predictive Analytics**
   - Sales forecasting for next 30/60/90 days
   - Demand prediction by product
   - Anomaly detection for unusual sales patterns

6. **Export & Reporting**
   - Automated weekly/monthly reports
   - Executive summary PDF export
   - Scheduled email reports

7. **Real-time Features**
   - Live sales tracking
   - Real-time inventory updates
   - Alert system for low stock or unusual patterns

---

## 📸 Screenshots

### Dashboard Overview
*Add screenshot of your dashboard here*

### Filters & KPIs
*Add screenshot of sidebar filters and KPI cards*

### Visualizations
*Add screenshots of charts and graphs*

---

## 🧪 Testing

To verify the application works correctly:

1. **Test Console Application:**
   ```bash
   python urbanmart_analysis.py
   ```
   - Try all menu options
   - Verify calculations are correct
   - Check error handling with invalid inputs

2. **Test Dashboard:**
   ```bash
   streamlit run app.py
   ```
   - Apply different filter combinations
   - Verify all charts render correctly
   - Test data download functionality
   - Check responsiveness on different screen sizes

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** `FileNotFoundError: urbanmart_sales.csv not found`
**Solution:** Ensure the CSV file is in the same directory as your Python scripts.

**Issue:** `ModuleNotFoundError: No module named 'streamlit'`
**Solution:** Install dependencies: `pip install -r requirements.txt`

**Issue:** Dashboard not loading
**Solution:** Check if port 8501 is available. Try: `streamlit run app.py --server.port 8502`

**Issue:** Charts not displaying
**Solution:** Clear Streamlit cache: `streamlit cache clear`

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is created for educational purposes as part of the MAIB curriculum.

---

## 👨‍💻 Authors

**MAIB Student Team**
- Data Analysis & Dashboard Development
- Python Programming
- Business Intelligence

---

## 🙏 Acknowledgments

- **UrbanMart** for providing the business case scenario
- **Streamlit** for the amazing dashboard framework
- **Plotly** for interactive visualizations
- **Pandas** for data manipulation capabilities
- **MAIB Program** for the learning opportunity

---

## 📞 Contact & Support

For questions or support:
- 📧 Email: your.email@example.com
- 💼 LinkedIn: [Your Profile]
- 🐙 GitHub: [@yourusername]

---

## 🔄 Version History

- **v1.0.0** (2025-01-XX) - Initial release
  - Console-based analytics
  - Interactive Streamlit dashboard
  - 200 sample transactions
  - 5 product categories
  - 3 store locations

---

## 🎯 Next Steps

- [ ] Add more sample data (500+ transactions)
- [ ] Implement predictive analytics
- [ ] Add user authentication
- [ ] Create mobile-responsive design
- [ ] Integrate with real-time data source
- [ ] Add export to PDF functionality
- [ ] Implement A/B testing features

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star! ⭐**

Made with ❤️ using Python & Streamlit

</div>
