import requests
import json
import pandas as pd
from datetime import datetime

# Get current timestamp for filenames
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# API request
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=70H117QUS6AVTGV5'
r = requests.get(url)
data = r.json()

# Save the raw JSON data first
json_filename = f"IBM_stock_data_{timestamp}.json"
with open(json_filename, 'w') as json_file:
    json.dump(data, json_file, indent=4)
print(f"Raw JSON data saved to {json_filename}")

# Check if we have valid data
if 'Time Series (Daily)' not in data:
    print("Error: Could not find time series data in the response")
    print("Response content:", data)
    exit(1)

# Extract the time series data
time_series = data['Time Series (Daily)']

# ========== METHOD 1: MANUAL LOOP APPROACH ==========
print("\n=== Using Manual Loop Method ===")

# Loop through each date and create a row dictionary for each
rows = []
for date, values in time_series.items():
    row = {
        'date': date,
        'open': values['1. open'],
        'high': values['2. high'],
        'low': values['3. low'],
        'close': values['4. close'],
        'volume': values['5. volume']
    }
    rows.append(row)

# Create DataFrame from the list of dictionaries
df_manual = pd.DataFrame(rows)

# Sort by date
df_manual['date'] = pd.to_datetime(df_manual['date'])
df_manual = df_manual.sort_values('date', ascending=False)

# Convert numeric columns
for col in ['open', 'high', 'low', 'close', 'volume']:
    df_manual[col] = pd.to_numeric(df_manual[col])

# Save to CSV
manual_csv = f"IBM_stock_manual_{timestamp}.csv"
df_manual.to_csv(manual_csv, index=False)
print(f"Manual method CSV saved to {manual_csv}")
print(df_manual.head(3))

# ========== METHOD 2: PANDAS FROM_DICT APPROACH ==========
print("\n=== Using Pandas from_dict Method ===")

# Convert directly to DataFrame, with dates as index
df_auto = pd.DataFrame.from_dict(time_series, orient='index')

# Clean up column names
df_auto.columns = [col.split('. ')[1] for col in df_auto.columns]

# Add date as a column (it's currently the index)
df_auto.reset_index(inplace=True)
df_auto.rename(columns={'index': 'date'}, inplace=True)

# Sort by date
df_auto['date'] = pd.to_datetime(df_auto['date'])
df_auto = df_auto.sort_values('date', ascending=False)

# Convert numeric columns
for col in ['open', 'high', 'low', 'close', 'volume']:
    df_auto[col] = pd.to_numeric(df_auto[col])

# Save to CSV
auto_csv = f"IBM_stock_auto_{timestamp}.csv"
df_auto.to_csv(auto_csv, index=False)
print(f"Automatic method CSV saved to {auto_csv}")
print(df_auto.head(3))

# ========== VERIFY BOTH METHODS PRODUCE THE SAME RESULT ==========
print("\n=== Comparing Both Methods ===")
are_equal = df_manual.equals(df_auto)
print(f"Do both methods produce identical DataFrames? {are_equal}")