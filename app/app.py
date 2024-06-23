import dash
import dash_bootstrap_components as dbc
import sys
import os

# Modify sys.path to include the project root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from layout import create_layout
from callbacks.callbacks import register_callbacks
from data import get_item_summary

# Get the list of items for the dropdown
items_df = get_item_summary()
items = items_df['item_name_'].tolist()



# Create a Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'])

# Set the layout of the app
app.layout = create_layout(items)

# Register callbacks
register_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
