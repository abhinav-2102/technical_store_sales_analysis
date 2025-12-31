import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="Sales Data Dashboard", layout="wide")
st.title("📊 Electronic Sales Analysis Dashboard")

# -- 1. Demo Sample CSV Data --
sample_csv_1 = """Order Date,Product,Quantity Ordered,Price Each,Purchase Address
01/15/19 10:20,iPhone,1,700,"123 Main St, New York, NY 10001"
01/22/19 21:25,Lightning Charging Cable,2,14.95,"456 Park Ave, New York, NY 10001"
02/10/19 08:30,27in 4K Gaming Monitor,1,389.99,"789 1st St, Boston, MA 02215"
02/14/19 13:15,Apple AirPods,1,150,"321 2nd St, Boston, MA 02215"
03/05/19 16:45,AAA Batteries (4-pack),3,2.99,"654 3rd St, San Francisco, CA 94016"
03/18/19 11:10,Google Phone,1,600,"987 4th St, Los Angeles, CA 90001"
03/25/19 09:05,Wired Headphones,1,11.99,"159 5th St, Los Angeles, CA 90001"
01/05/19 12:00,USB-C Charging Cable,1,11.95,"753 6th St, Austin, TX 73301"
02/28/19 19:30,Macbook Pro Laptop,1,1700,"951 7th St, Portland, OR 97035"
03/12/19 14:20,Bose SoundSport Headphones,1,99.99,"357 8th St, Dallas, TX 75001"
"""

sample_csv_2 = """Order Date,Product,Quantity Ordered,Price Each,Purchase Address
04/02/19 07:15,ThinkPad Laptop,1,999.99,"246 9th St, Seattle, WA 98101"
04/15/19 18:40,AAA Batteries (4-pack),2,2.99,"135 10th St, Seattle, WA 98101"
05/10/19 12:30,iPhone,1,700,"864 11th St, Atlanta, GA 30301"
05/20/19 20:10,Lightning Charging Cable,1,14.95,"975 12th St, Atlanta, GA 30301"
06/05/19 15:55,Flatscreen TV,1,300,"202 13th St, New York, NY 10001"
06/18/19 09:45,Macbook Pro Laptop,1,1700,"303 14th St, New York, NY 10001"
04/25/19 11:05,Vareebadd Phone,1,400,"404 15th St, Portland, OR 97035"
05/05/19 16:20,USB-C Charging Cable,2,11.95,"505 16th St, San Francisco, CA 94016"
06/30/19 23:15,Wired Headphones,1,11.99,"606 17th St, Los Angeles, CA 90001"
04/11/19 14:00,AA Batteries (4-pack),4,3.84,"707 18th St, Dallas, TX 75001"
"""

sample_csv_3 = """Order Date,Product,Quantity Ordered,Price Each,Purchase Address
07/04/19 13:20,20in Monitor,1,109.99,"808 19th St, Boston, MA 02215"
07/15/19 08:50,Apple AirPods,1,150,"909 20th St, Boston, MA 02215"
08/08/19 17:35,34in Ultrawide Monitor,1,379.99,"121 21st St, Austin, TX 73301"
08/22/19 10:15,Google Phone,1,600,"232 22nd St, San Francisco, CA 94016"
09/01/19 19:40,Lightning Charging Cable,3,14.95,"343 23rd St, San Francisco, CA 94016"
09/10/19 14:25,iPhone,1,700,"454 24th St, Los Angeles, CA 90001"
07/20/19 22:10,Wired Headphones,1,11.99,"565 25th St, Seattle, WA 98101"
08/15/19 11:30,Bose SoundSport Headphones,1,99.99,"676 26th St, New York, NY 10001"
09/25/19 16:05,LG Washing Machine,1,600.00,"787 27th St, Atlanta, GA 30301"
09/30/19 09:00,AA Batteries (4-pack),2,3.84,"898 28th St, Portland, OR 97035"
"""

sample_csv_4 = """Order Date,Product,Quantity Ordered,Price Each,Purchase Address
10/05/19 18:10,Google Phone,1,600,"101 Pine St, Dallas, TX 75001"
10/12/19 12:45,USB-C Charging Cable,1,11.95,"202 Oak St, Dallas, TX 75001"
11/02/19 08:20,Macbook Pro Laptop,1,1700,"303 Cedar St, Austin, TX 73301"
11/25/19 20:30,ThinkPad Laptop,1,999.99,"404 Birch St, Boston, MA 02215"
12/10/19 15:15,iPhone,1,700,"505 Walnut St, New York, NY 10001"
12/15/19 10:50,Apple AirPods,3,150,"606 Maple St, New York, NY 10001"
12/24/19 17:00,27in 4K Gaming Monitor,1,389.99,"707 Elm St, San Francisco, CA 94016"
10/31/19 23:45,Lightning Charging Cable,1,14.95,"808 Spruce St, Seattle, WA 98101"
11/15/19 14:10,Wired Headphones,2,11.99,"909 Ash St, Los Angeles, CA 90001"
12/05/19 09:25,AA Batteries (4-pack),5,3.84,"111 Fir St, Atlanta, GA 30301"
"""

# Combine all previous samples into a "Full Year" dataset
sample_csv_5 = sample_csv_1 + "\n" + "\n".join(sample_csv_2.split("\n")[1:]) + "\n" + "\n".join(sample_csv_3.split("\n")[1:]) + "\n" + "\n".join(sample_csv_4.split("\n")[1:])

SAMPLE_FILES = {
    "Q1 Data (Jan-Mar)": sample_csv_1,
    "Q2 Data (Apr-Jun)": sample_csv_2,
    "Q3 Data (Jul-Sep)": sample_csv_3,
    "Q4 Data (Oct-Dec)": sample_csv_4,
    "Full Year Data (All)": sample_csv_5
}

# -- 2. Sidebar for Upload or Sample Data --
st.sidebar.header("1. Upload CSV Files or Select a Sample")
uploaded_files = st.sidebar.file_uploader(
    "Upload your CSV files", type="csv", accept_multiple_files=True
)

use_sample = False
if not uploaded_files:
    sample_choice = st.sidebar.selectbox(
        "📁 Or select sample data to try:", ["(None)"] + list(SAMPLE_FILES.keys())
    )
    if sample_choice != "(None)":
        use_sample = True

# -- 3. Read and Combine Data --
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

# -- 4. Robust Data Cleaning --
st.subheader("🧹 Data Cleaning")
df = combined_df.copy()

# Defensive cleaning for 'Order Date'
df = df[df['Order Date'].notna()]
df['Order Date'] = df['Order Date'].astype(str)
df = df[~df['Order Date'].str.startswith('Or')]
df['Order Date'] = pd.to_datetime(df['Order Date'], errors="coerce")
df.dropna(subset=["Order Date"], inplace=True)

# Convert numeric columns
df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"], errors="coerce")
df["Price Each"] = pd.to_numeric(df["Price Each"], errors="coerce")
df.dropna(subset=["Quantity Ordered", "Price Each"], inplace=True)

df["Month"] = df["Order Date"].dt.month
df["Hour"] = df["Order Date"].dt.hour
df["Minute"] = df["Order Date"].dt.minute
df["Count"] = 1
df["Sales"] = df["Quantity Ordered"] * df["Price Each"]

def get_city(address):
    try:
        return address.split(",")[1].strip()
    except Exception:
        return ""
def get_state(address):
    try:
        return address.split(",")[2].split(" ")[1]
    except Exception:
        return ""

if "Purchase Address" in df.columns:
    df["City"] = df["Purchase Address"].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
else:
    df["City"] = ""

st.write(f"✅ Cleaned Data Preview: {len(df)} rows remain.")
st.dataframe(df.head())

if df.empty:
    st.warning("No data remains after cleaning. Please check your dataset or sample selection.")
    st.stop()

# -- 5. Visualizations with Safeguards --

st.subheader("📈 Data Visualizations")

# 5.1 Sales by Month
st.markdown("### 📆 Monthly Sales")
monthly_sales = df.groupby("Month")["Sales"].sum()
if not monthly_sales.empty:
    fig1, ax1 = plt.subplots()
    ax1.bar(monthly_sales.index.astype(str), monthly_sales.values, color="teal")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Sales (USD)")
    ax1.set_title("Sales Per Month")
    st.pyplot(fig1)
else:
    st.warning("No data available for monthly sales.")

# 5.2 Sales by City
st.markdown("### 🏙️ Sales by City")
city_sales = df.groupby("City")["Sales"].sum()
if not city_sales.empty:
    fig2, ax2 = plt.subplots()
    ax2.bar(city_sales.index, city_sales.values, color="orange")
    ax2.set_xticks(range(len(city_sales.index)))
    ax2.set_xticklabels(city_sales.index, rotation=45, ha='right')
    ax2.set_title("Sales by City")
    ax2.set_ylabel("Sales (USD)")
    st.pyplot(fig2)
else:
    st.warning("No data available for city sales.")

# 5.3 Orders by Hour
st.markdown("### ⏰ Orders by Hour")
hourly_orders = df.groupby("Hour")["Count"].count()
if not hourly_orders.empty:
    fig3, ax3 = plt.subplots()
    ax3.plot(hourly_orders.index, hourly_orders.values, marker="o")
    ax3.set_title("Orders by Hour")
    ax3.set_xlabel("Hour of Day")
    ax3.set_ylabel("Number of Orders")
    ax3.grid(True)
    st.pyplot(fig3)
else:
    st.warning("No data available for hourly orders.")

# 5.4 Top Products by Quantity
st.markdown("### 📦 Units Sold by Product")
product_quantity = df.groupby("Product")["Quantity Ordered"].sum().sort_values(ascending=False)
if not product_quantity.empty:
    fig4, ax4 = plt.subplots(figsize=(10,5))
    ax4.bar(product_quantity.index, product_quantity.values, color='purple')
    ax4.set_xticks(range(len(product_quantity.index)))
    ax4.set_xticklabels(product_quantity.index, rotation='vertical', size=9)
    ax4.set_ylabel("Quantity Sold")
    ax4.set_title("Top Selling Products")
    st.pyplot(fig4)
else:
    st.warning("No data available for product sales.")

# 5.5 Price vs Quantity
st.markdown("### 💰 Price vs Quantity Sold")
product_group = df.groupby("Product")
quantity = product_group["Quantity Ordered"].sum()
prices = product_group["Price Each"].mean()
if not quantity.empty and not prices.empty:
    fig5, ax5 = plt.subplots(figsize=(10,5))
    ax6 = ax5.twinx()
    ax5.bar(quantity.index, quantity.values, color='green', label='Quantity Sold')
    ax6.plot(prices.index, prices.values, color='blue', marker='o', label='Average Price')
    ax5.set_xticks(range(len(quantity.index)))
    ax5.set_xticklabels(quantity.index, rotation='vertical', size=9)
    ax5.set_ylabel("Quantity Sold", color='green')
    ax6.set_ylabel("Avg. Price (USD)", color='blue')
    ax5.set_title("Price vs Quantity Sold")
    st.pyplot(fig5)
else:
    st.warning("No data available for price vs quantity charts.")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Demo Sales Dashboard for Electronics")

