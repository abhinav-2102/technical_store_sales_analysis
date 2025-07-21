import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import glob

# Get a list of all CSV files in the directory
csv_files = glob.glob('*.csv')

# Create an empty DataFrame to store the combined data
combined_df = pd.DataFrame()

# Loop through each CSV file and append it to the combined DataFrame
for file in csv_files:
    df = pd.read_csv(file)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# Write the combined DataFrame to a new CSV file
combined_df.to_csv('combined_file.csv', index=False)

all_data = pd.read_csv("combined_file.csv")
all_data.head()

# Finding and dropping rows with NaN

nan_df = all_data[all_data.isna().any(axis=1)]
display(nan_df.head())

all_data = all_data.dropna(how='all')
all_data.head()

# Checking if the NaN were succesffully dropped

nan_df = all_data[all_data.isna().any(axis=1)]
display(nan_df.head())
# Removing text in order date column

all_data = all_data[all_data['Order Date'].str[0:2]!='Or']
# Converting columns to the correct type

all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

# Adding month column

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')

all_data.head()
# Adding city column

def get_city(address):
    return address.split(",")[1].strip(" ")

def get_state(address):
    return address.split(",")[2].split(" ")[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)}  ({get_state(x)})")
all_data.head()
# Adding sales column

all_data['Sales'] = all_data['Quantity Ordered'].astype('int') * all_data['Price Each'].astype('float')

all_data.head()
all_data.groupby(['Month']).sum()


# Visualizing the data for Sales per Month

months = range(1,13)
print(months)

plt.bar(months,all_data.groupby(['Month']).sum()['Sales'])
plt.xticks(months)
plt.title('Sales per Month')
plt.ylabel('Sales (USD$)')
plt.xlabel('Month')
plt.show()

all_data.groupby(['City']).sum()

# Visualizing the data for Sales per city
keys = [city for city, df in all_data.groupby(['City'])]
keys = [k[0] for k in keys]  # Extract city name as a string

plt.bar(keys, all_data.groupby(['City']).sum()['Sales'])
plt.title('Sales by City')
plt.ylabel('Sales (USD$)')
plt.xlabel('City')
plt.xticks(keys, rotation='vertical', size=8)
plt.show()
# Adding time columns

all_data['Hour'] = pd.to_datetime(all_data['Order Date']).dt.hour
all_data['Minute'] = pd.to_datetime(all_data['Order Date']).dt.minute
all_data['Count'] = 1
all_data.head()

# Using the order time from customers' orders to plot a graph

keys = [pair for pair, df in all_data.groupby(['Hour'])]
# Extract the hour values from the tuples in keys
keys = [k[0] for k in keys]  # Extract the hour value from the tuple

plt.plot(keys, all_data.groupby(['Hour']).count()['Count'])
plt.xticks(keys)
plt.title('Total Orders vs Time of Order')
plt.ylabel('Total Number of Orders')
plt.xlabel('Order Time (Hour)')
plt.grid()
plt.show()

product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

keys = [pair for pair, df in product_group]
plt.bar(keys, quantity_ordered)
plt.xticks(keys, rotation='vertical', size=10)
plt.title('Total Number of Products Sold')
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.show()

# Comparing cost of items to the quantity sold.

# Convert 'Price Each' to numeric, handling errors
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'], errors='coerce')

# Calculate prices after ensuring numeric type
prices = all_data.groupby('Product')['Price Each'].mean() # Changes in this line

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(keys, quantity_ordered, color='g')
ax2.plot(keys, prices, color='b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price (USD$)', color='b')
ax1.set_xticklabels(keys, rotation='vertical', size=8)

fig.show()
