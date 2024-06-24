import dash_bootstrap_components as dbc
from dash import html, dcc
from components import create_search_bar, create_category_dropdown, create_sidebar_list_button
from data import get_category_dict
import dash_cytoscape as cyto



categories_dict = get_category_dict()

def create_layout(items):
    return dbc.Container([
        dbc.Row([
            dbc.Col([ 
                create_sidebar_list_button("precios", "ACTUALES", "/assets/icons/price-tag.png"), 
                create_sidebar_list_button("precios", "HISTORICOS", "/assets/icons/price-tag.png"), 
                
                *[create_category_dropdown(category, categories_dict[category]) for category in categories_dict],
            ], width=3, className="col1"),
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H2("WOW TRADE MANIAC", className="tm-h2"),
                        html.H2("Plataforma para tradear y craftear.", className="tm-h2-subtitle"),
                    ]), width=4),
                    create_search_bar(items),
                    dbc.Col(
                        [
                            html.Div([
                                html.Div(id='selected-category-name', className='selected-category'), 
                                dbc.Button("Reset Filter", id='clear-filter-button', n_clicks=0, className='clear-filter-button', style={'display': 'none'})
                            ], style={'display': 'flex', 'alignItems': 'center'}),  # This div wraps the filter and the button, applying flexbox
                        ],
                        width=4  # Adjust width as needed
                    )
                ], class_name="top-bar"),
                dbc.Card([
                    html.H2(id='item-title', style={'color': 'white'}),
                    
                    dbc.CardBody([
                        cyto.Cytoscape(
                            id='cytoscape',
                            layout={'name': 'breadthfirst'},
                            style={'width': '100%', 'height': '600px'},
                            elements=[],
                        ),
                        html.H4('Current Prices', style={'color': 'white'}),
                        html.P(id='current-prices', style={'color': 'white'}),
                        dcc.Graph(id='lowest-price-graph'),
                        dcc.Graph(id='price-distribution-graph'),
                        dcc.Graph(id='quantity-sold-graph'),
                        dcc.Graph(id='price-quantity-scatter'),
                    ])
                ], className="item_card")
            ], width=8, className="col2", style={"margin-left": "100px;"})
        ], className="column-style")
    ])
