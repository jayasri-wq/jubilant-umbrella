# preprocess.py

import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load CSV files
commodity_df = pd.read_csv("data/commodity_prices.csv")
weather_df = pd.read_csv("data/weather_data.csv")

# Step 2: Check for missing values
print("Commodity Data Nulls:\n", commodity_df.isnull().sum())
print("Weather Data Nulls:\n", weather_df.isnull().sum())

# Step 3: Convert 'Date' to datetime
commodity_df['Date'] = pd.to_datetime(commodity_df['Date'])
weather_df['Date'] = pd.to_datetime(weather_df['Date'])

# Step 4: Merge both dataframes on Date
merged_df = pd.merge(commodity_df, weather_df, on='Date')

# Step 5: Plotting Tomato and Onion prices over time
plt.figure(figsize=(10, 5))
plt.plot(merged_df['Date'], merged_df['Tomato'], label='Tomato Price (₹)', color='tomato')
plt.plot(merged_df['Date'], merged_df['Onion'], label='Onion Price (₹)', color='purple')
plt.title('Tomato & Onion Price Trend')
plt.xlabel('Date')
plt.ylabel('Price (₹)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 6: Save cleaned merged data for model training
merged_df.to_csv("data/merged_data.csv", index=False)
