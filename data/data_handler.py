import pandas as pd

# Load data from Excel files
commodities_snapshot = pd.read_excel('../api/data/commodities_snapshot-2024-06-03.xlsx')
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
    return item_data[['unit_price', 'quantity']].to_dict(orient='records')
