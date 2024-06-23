from dash import html
import dash_bootstrap_components as dbc

def create_category_dropdown(label, items):
    dropdown_items = [dbc.DropdownMenuItem(item, id={'type': 'category-dropdown-item', 'index': item}) for item in items]
    dropdown = dbc.DropdownMenu(
        label=label, 
        children=dropdown_items,  
        color="primary",  
        className="category_dropdown",
        id="category-dropdown-menu"
    )
    return dropdown