import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from io import StringIO

st.set_page_config(layout="wide")
st.title("📊 Sales Data Dashboard")

# --- Upload Section ---
st.sidebar.header("1. Upload Sales CSV Files")
uploaded_files = st.sidebar.file_uploader("Upload multiple CSV files", type="csv", accept_multiple_files=True)

if uploaded_files:
    # Combine all uploaded CSVs
    combined_df = pd.concat([pd.read_csv(file) for file in uploaded_files], ignore_index=True)
    combined_df.to_csv("combined_file.csv", index=False)
    
    st.success("✅ Files combined successfully!")
    
    # Data Cleaning
    all_data = combined_df.copy()
    st.subheader("Raw Data Sample")
    st.dataframe(all_data.head())

    st.subheader("2. Data Cleaning")
    
    # Drop all-NaN rows
    all_data = all_data.dropna(how='all')

    # Remove invalid rows in 'Order Date'
    all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
    
    # Convert columns
    all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'], errors='coerce')
    all_data['Price Each'] = pd.to_numeric(all_data['Price Each'], errors='coerce')

    # Drop any rows with remaining NaNs
    all_data.dropna(inplace=True)

    # Add Month Column
    all_data['Month'] = all_data['Order Date'].str[0:2].astype('int32')

    # Add City Column
    def get_city(address):
        return address.split(",")[1].strip()

    def get_state(address):
        return address.split(",")[2].split(" ")[1]

    all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

    # Add Sales Column
    all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

    # Add Hour/Minute Columns
    all_data['Order Date'] = pd.to_datetime(all_data['Order Date'], errors='coerce')
    all_data.dropna(subset=['Order Date'], inplace=True)
    all_data['Hour'] = all_data['Order Date'].dt.hour
    all_data['Minute'] = all_data['Order Date'].dt.minute
    all_data['Count'] = 1

    # Show cleaned data
    st.write("✅ Cleaned Data Preview:")
    st.dataframe(all_data.head())

    # --- Visualizations ---
    st.subheader("3. Visualizations")

    # Sales per Month
    st.markdown("### 📆 Sales Per Month")
    fig1, ax1 = plt.subplots()
    monthly_sales = all_data.groupby('Month').sum(numeric_only=True)['Sales']
    ax1.bar(monthly_sales.index, monthly_sales.values)
    ax1.set_xticks(range(1,13))
    ax1.set_title("Sales Per Month")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Sales (USD)")
    st.pyplot(fig1)

    # Sales by City
    st.markdown("### 🏙️ Sales Per City")
    fig2, ax2 = plt.subplots()
    city_sales = all_data.groupby('City').sum(numeric_only=True)['Sales']
    ax2.bar(city_sales.index, city_sales.values)
    ax2.set_title("Sales by City")
    ax2.set_ylabel("Sales (USD)")
    ax2.set_xlabel("City")
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

    # Orders by Hour
    st.markdown("### ⏰ Orders by Hour")
    fig3, ax3 = plt.subplots()
    hourly_orders = all_data.groupby('Hour').count()['Count']
    ax3.plot(hourly_orders.index, hourly_orders.values)
    ax3.set_title("Orders by Hour")
    ax3.set_xlabel("Hour")
    ax3.set_ylabel("Total Orders")
    ax3.grid()
    st.pyplot(fig3)

    # Products Sold
    st.markdown("### 📦 Products Sold")
    fig4, ax4 = plt.subplots()
    product_group = all_data.groupby('Product')
    quantity_ordered = product_group.sum(numeric_only=True)['Quantity Ordered']
    keys = [product for product, _ in product_group]
    ax4.bar(keys, quantity_ordered)
    ax4.set_xticklabels(keys, rotation='vertical', size=8)
    ax4.set_title("Quantity Sold per Product")
    ax4.set_ylabel("Quantity Ordered")
    st.pyplot(fig4)

    # Product Price vs Quantity
    st.markdown("### 💰 Price vs Quantity Sold")
    prices = product_group.mean(numeric_only=True)['Price Each']

    fig5, ax5 = plt.subplots()
    ax6 = ax5.twinx()
    ax5.bar(keys, quantity_ordered, color='green')
    ax6.plot(keys, prices, color='blue')

    ax5.set_xticklabels(keys, rotation='vertical', size=8)
    ax5.set_ylabel("Quantity Ordered", color='green')
    ax6.set_ylabel("Price (USD)", color='blue')
    ax5.set_title("Price vs Quantity Ordered")
    st.pyplot(fig5)

else:
    st.info("Upload CSV files to begin analysis.")

