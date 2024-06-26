from dash import html
import dash_bootstrap_components as dbc

def create_category_dropdown(unique_id, category_name, label, items):
    # Incorporate the category name into the ID for uniqueness
    dropdown_items = [
        dbc.DropdownMenuItem(item, id={'type': 'category-dropdown-item', 'index': f"{category_name}-{item}"})
        for item in items
    ]
    dropdown = dbc.DropdownMenu(
        label=label, 
        children=dropdown_items,  
        color="primary",  
        className="category_dropdown",
        id=f"category-dropdown-menu-{unique_id}"
    )
    return dropdown