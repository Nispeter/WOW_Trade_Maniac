import pandas as pd
import glob
import os

# Define the path to the folder containing the Excel files
data_folder = '../api/data'

# Get a list of all Excel files in the data folder
excel_files = glob.glob(os.path.join(data_folder, '*.xlsx'))

# Initialize an empty list to hold the DataFrames
df_list = []

# Iterate over the files and read each into a DataFrame
for idx, file in enumerate(sorted(excel_files)):
    df = pd.read_excel(file)
    df['snapshot_order'] = idx + 1  # Add a column for the snapshot order
    df_list.append(df)

# Concatenate all DataFrames into one
commodities_snapshot = pd.concat(df_list, ignore_index=True)

# Load item cache
item_cache = pd.read_excel('../api/item_cache.xlsx')

# Merge the dataframes on item_id
merged_df = pd.merge(commodities_snapshot, item_cache, on='item_id')

# Function to get summary of all items
def get_item_summary():
    summary_df = merged_df.groupby('item_name').agg({
        'unit_price': ['mean', 'max', 'min', 'std'],
        'quantity': 'sum'
    }).reset_index()
    summary_df.columns = ['_'.join(col).strip() for col in summary_df.columns.values]
    return summary_df

# Function to get historical prices for a specific item
def get_item_prices(item_name):
    item_data = merged_df[merged_df['item_name'].str.contains(item_name, case=False)]
    if item_data.empty:
        return None
    print("Item data columns:", item_data.columns)
    return item_data[['snapshot_order', 'unit_price', 'quantity']].to_dict(orient='records')

# Function to get item statistics for graphs
def get_item_statistics(item_name):
    item_data = merged_df[merged_df['item_name'].str.contains(item_name, case=False)]
    if item_data.empty:
        return None
    return item_data
