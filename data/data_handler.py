import pandas as pd
import glob
import os
import numpy as np
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
    return item_data[['snapshot_order', 'unit_price', 'quantity']].to_dict(orient='records')

# Function to get the lowest price for a specific item
def get_lowest_price(item_name):
    item_prices = get_item_prices(item_name)
    
    if item_prices is None:
        return 0
    
    # Filter the results for 'snapshot_order' = 25
    filtered_prices = [price for price in item_prices if price['snapshot_order'] == 25]
    
    # Check if filtered_prices is not empty
    if filtered_prices:
        # Find the entry with the lowest 'unit_price'
        lowest_price_entry = min(filtered_prices, key=lambda x: x['unit_price'])
        return lowest_price_entry['unit_price']
    else:
        return 0

# Function to get item statistics for graphs
def get_item_statistics(item_name):
    item_data = merged_df[merged_df['item_name'].str.contains(item_name, case=False)]
    if item_data.empty:
        return None
    return item_data

    
def get_category_dict():
    # Extract unique categories and ensure they are strings, excluding integers
    unique_categories = [category for category in merged_df['category'].unique() if isinstance(category, str)]
    
    # Organize the categories and sub-categories, implicitly skipping non-string categories
    categories_dict = {}
    for category in sorted(unique_categories):
        categories_dict[category] = sorted(merged_df[merged_df['category'] == category]['subcategory'].unique().tolist())
    
    return categories_dict
def filter_items_by_category(item_dataframe, category, sub_category=None):
    # Filter by category only if sub_category is not provided
    if sub_category is None:
        filtered_df = item_dataframe.loc[item_dataframe['category'] == category]
    else:
        # Filter by both category and sub_category
        filtered_df = item_dataframe.loc[(item_dataframe['category'] == category) & (item_dataframe['subcategory'] == sub_category)]
    
    if filtered_df.empty:
        return None
    else:
        return filtered_df

# Function to get crafting dependencies
def get_crafting_dependencies():
    crafting_data = pd.read_excel('../api/wow_recipes.xlsx')

    # Create node labels
    nodes = list(crafting_data['recipe_name'].unique()) + list(crafting_data['reagent_name'].unique())
    
    # Create link data
    link_data = crafting_data.groupby(['recipe_name', 'reagent_name']).sum().reset_index()
    links = {
        'source': [nodes.index(row['reagent_name']) for _, row in link_data.iterrows()],
        'target': [nodes.index(row['recipe_name']) for _, row in link_data.iterrows()],
        'value': list(link_data['reagent_quantity'])
    }

    return {'nodes': nodes, 'links': links}

df = pd.read_excel('../api/data/wow_recipes.xlsx')
def get_es_mx_name(name):
    try:
        name_dict = eval(name)
        return name_dict.get('es_MX', 'Nombre no disponible')
    except:
        return 'Nombre no disponible'

# Apply the function to the columns
df['item_name_es'] = df['recipe_name'].apply(get_es_mx_name)
df['reagent_name_es'] = df['reagent_name'].apply(get_es_mx_name)

# Helper function to create nodes and edges for cytoscape
def create_elements(item_id):
    elements = []
    visited = set()

    def add_elements(item_id, is_parent=False):
        if item_id in visited:
            return
        visited.add(item_id)

        item_rows = df[df['item_id'] == item_id]
        if item_rows.empty:
            print(f"No item found for ID: {item_id}")
            return

        item_row = item_rows.iloc[0]
        item_name = item_row['item_name_es']
        print(f"Adding item: {item_name} (ID: {item_id})")

        # Assign a different color if it's the parent node
        if is_parent:
            elements.append({'data': {'id': str(item_id), 'label': item_name, 'color': '#FF0000'}})  # Red color for the parent node
        else:
            elements.append({'data': {'id': str(item_id), 'label': item_name}})

        reagents = df[df['recipe_id'] == item_row['recipe_id']]
        for _, reagent in reagents.iterrows():
            reagent_id = reagent['reagent_id']
            reagent_name = reagent['reagent_name_es']
            reagent_quantity = reagent['reagent_quantity']
            reagent_price = get_item_prices(reagent_name)
            unit_price = reagent_price[0]['unit_price']
            print(f"Adding reagent: {reagent_name} (ID: {reagent_id}, Quantity: {reagent_quantity}, Price: {unit_price})")
            elements.append({'data': {'id': str(reagent_id), 'label': f"{reagent_name} ({reagent_quantity}, Price: {unit_price})"}})
            elements.append({'data': {'source': str(item_id), 'target': str(reagent_id)}})
            add_elements(reagent_id)

    add_elements(item_id, is_parent=True)  # The initial call sets the root node as the parent
    return elements
# Function to get the initial search options for the search bar
def create_initial_search_options():
    items_df = get_item_summary()
    items = items_df['item_name_'].tolist()
    return [{'label': item, 'value': item} for item in items]
# Function to remove outliers from data

def remove_outliers(data, min_data_points=None, adjust_criteria=False, percentage_threshold=300):
    if len(data) == 0:
        return data  # Return empty list if input is empty
    
    if len(set(data)) == 1:
        return data  # Return data as is if all values are the same
    
    data = np.array(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    multiplier = 1.5
    
    # Dynamically adjust criteria if enabled
    if adjust_criteria and len(data) < 10:  
        multiplier = 2.0  # Loosen the criteria
    
    lower_bound = q1 - (multiplier * iqr)
    upper_bound = q3 + (multiplier * iqr)
    
    # Calculate median or mean and apply percentage threshold
    central_value = np.median(data)  # You can also use np.mean(data) if preferred
    percentage_upper_bound = central_value * (1 + percentage_threshold / 100.0)
    
    # Use the smaller of the IQR upper bound and the percentage threshold upper bound
    final_upper_bound = min(upper_bound, percentage_upper_bound)
    
    filtered_data = [x for x in data if lower_bound <= x <= final_upper_bound]
    
    # Ensure a minimum number of data points are retained
    if min_data_points is not None and len(filtered_data) < min_data_points:
        return data[:min_data_points]
    
    return filtered_data if filtered_data else data  # Return original data if all were outliers
