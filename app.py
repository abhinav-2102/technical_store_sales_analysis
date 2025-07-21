import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="Sales Data Dashboard", layout="wide")
st.title("📊 Electronic Sales Analysis Dashboard")

# -----------------------------
# 1. Sample CSV Data Strings
# -----------------------------
sample_csv_1 = """
Order Date,Product,Quantity Ordered,Price Each,Purchase Address
04/19/19 08:46,iPhone,2,700,917 1st St, Dallas, TX 75001
04/07/19 22:30,Lightning Charging Cable,1,14.95,682 Chestnut St, Boston, MA 02215
04/12/19 14:38,Macbook Pro Laptop,1,1700,669 Spruce St, Los Angeles, CA 90001
"""

sample_csv_2 = """
Order Date,Product,Quantity Ordered,Price Each,Purchase Address
05/01/19 09:15,Google Phone,1,600,333 8th St, New York, NY 10001
05/03/19 11:20,Wired Headphones,2,11.99,222 Walnut St, San Francisco, CA 94016
05/03/19 17:45,AA Batteries (4-pack),3,3.84,111 Pine St, Austin, TX 73301
"""

sample_csv_3 = """
Order Date,Product,Quantity Ordered,Price Each,Purchase Address
06/15/19 13:55,Macbook Pro Laptop,2,1700,894 Birch St, Miami, FL 33101
06/16/19 10:32,27in 4K Gaming Monitor,1,399.99,1010 Cedar St, Seattle, WA 98101
06/17/19 18:47,USB-C Charging Cable,4,11.95,354 Elm St, Denver, CO 80201
"""

sample_csv_4 = """
Order Date,Product,Quantity Ordered,Price Each,Purchase Address
07/21/19 19:07,ThinkPad Laptop,1,1200,5057 Oak St, San Diego, CA 92101
07/22/19 16:20,Bose SoundSport Headphones,1,99.99,211 Prairie St, Dallas, TX 75001
07/23/19 08:49,Apple AirPods,2,150,299 Market St, Boston, MA 02215
"""

sample_csv_5 = """
Order Date,Product,Quantity Ordered,Price Each,Purchase Address
08/01/19 09:30,Google Home Mini,3,40,4244 West St, Las Vegas, NV 88901
08/02/19 12:45,Wired Headphones,2,11.99,988 Bridge St, St. Louis, MO 63101
08/02/19 21:12,iPhone,1,700,1441 East St, Chicago, IL 60601
"""

SAMPLE_FILES = {
    "Electronics Q1": sample_csv_1,
    "Electronics Q2": sample_csv_2,
    "Electronics Q3": sample_csv_3,
    "Electronics Q4": sample_csv_4,
    "Electronics Q5": sample_csv_5
}

# -----------------------------
# 2. Sidebar: Upload or Sample
# -----------------------------
st.sidebar.header("1. Upload CSV Files or Select a Sample")

uploaded_files = st.sidebar.file_uploader("Upload your CSV files", type="csv", accept_multiple_files=True)

use_sample = False
if not uploaded_files:
    sample_choice = st.sidebar.selectbox("📁 Or select sample data to try:", ["(None)"] + list(SAMPLE_FILES.keys()))
    if sample_choice != "(None)":
        use_sample = True

# -----------------------------
# 3. Read and Combine Data
# -----------------------------
if uploaded_files:
    combined_df = pd.concat([pd.read_csv(file) for file in uploaded_files], ignore_index=True)
    st.success("✅ Uploaded files loaded successfully.")
elif use_sample:
    combined_df = pd.read_csv(StringIO(SAMPLE_FILES[sample_choice]))
    st.success(f"✅ Sample data '{sample_choice}' loaded.")
else:
    st.info("Upload CSV files or select a sample dataset from the sidebar to begin.")
    st.stop()

st.subheader("🔍 Raw Sales Data Preview")
st.dataframe(combined_df.head())

# -----------------------------
# 4. Data Cleaning
# -----------------------------
st.subheader("🧹 Data Cleaning")
df = combined_df.copy()

df.dropna(subset=["Order Date"], inplace=True)
df = df[df["Order Date"].astype(str).str[0:2] != 'Or']


df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"], errors="coerce")
df["Price Each"] = pd.to_numeric(df["Price Each"], errors="coerce")
df.dropna(subset=["Quantity Ordered", "Price Each"], inplace=True)

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df.dropna(subset=["Order Date"], inplace=True)

df["Month"] = df["Order Date"].dt.month
df["Hour"] = df["Order Date"].dt.hour
df["Minute"] = df["Order Date"].dt.minute
df["Count"] = 1
df["Sales"] = df["Quantity Ordered"] * df["Price Each"]

# Extract city and state
def get_city(address): return address.split(",")[1].strip()
def get_state(address): return address.split(",")[2].split(" ")[1]

df["City"] = df["Purchase Address"].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
st.write("✅ Cleaned Data Preview:")
st.dataframe(df.head())

# -----------------------------
# 5. Visualizations
# -----------------------------
st.subheader("📈 Data Visualizations")

# 5.1 Sales by Month
st.markdown("### 📆 Monthly Sales")
fig1, ax1 = plt.subplots()
monthly_sales = df.groupby("Month")["Sales"].sum()
ax1.bar(monthly_sales.index, monthly_sales.values, color="teal")
ax1.set_xlabel("Month")
ax1.set_ylabel("Sales (USD)")
ax1.set_title("Sales Per Month")
ax1.set_xticks(monthly_sales.index)
st.pyplot(fig1)

# 5.2 Sales by City
st.markdown("### 🏙️ Sales by City")
fig2, ax2 = plt.subplots()
city_sales = df.groupby("City")["Sales"].sum()
ax2.bar(city_sales.index, city_sales.values, color="orange")
ax2.set_xticklabels(city_sales.index, rotation=45, ha='right')
ax2.set_title("Sales by City")
ax2.set_ylabel("Sales (USD)")
st.pyplot(fig2)

# 5.3 Orders by Hour
st.markdown("### ⏰ Orders by Hour")
fig3, ax3 = plt.subplots()
hourly_orders = df.groupby("Hour")["Count"].count()
ax3.plot(hourly_orders.index, hourly_orders.values, marker="o")
ax3.set_title("Orders by Hour")
ax3.set_xlabel("Hour of Day")
ax3.set_ylabel("Number of Orders")
ax3.grid(True)
st.pyplot(fig3)

# 5.4 Top Products by Quantity
st.markdown("### 📦 Units Sold by Product")
product_quantity = df.groupby("Product")["Quantity Ordered"].sum()
sorted_products = product_quantity.sort_values(ascending=False)
fig4, ax4 = plt.subplots(figsize=(10,5))
ax4.bar(sorted_products.index, sorted_products.values, color='purple')
ax4.set_xticklabels(sorted_products.index, rotation='vertical', size=9)
ax4.set_ylabel("Quantity Sold")
ax4.set_title("Top Selling Products")
st.pyplot(fig4)

# 5.5 Price vs Quantity
st.markdown("### 💰 Price vs Quantity Sold")
product_group = df.groupby("Product")
quantity = product_group["Quantity Ordered"].sum()
prices = product_group["Price Each"].mean()

fig5, ax5 = plt.subplots(figsize=(10,5))
ax6 = ax5.twinx()
ax5.bar(quantity.index, quantity.values, color='green', label='Quantity Sold')
ax6.plot(prices.index, prices.values, color='blue', marker='o', label='Average Price')

ax5.set_xticklabels(quantity.index, rotation='vertical', size=9)
ax5.set_ylabel("Quantity Sold", color='green')
ax6.set_ylabel("Avg. Price (USD)", color='blue')
ax5.set_title("Price vs Quantity Sold")
st.pyplot(fig5)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Demo Sales Dashboard for Electronics")
